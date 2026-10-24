import argparse
import asyncio
import json
import os
import re
from datetime import datetime
from urllib.parse import urlparse
from playwright.async_api import async_playwright

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")

async def analyze_website(url: str, headless: bool = True, wait_seconds: int = 4):
    """
    Nghiên cứu toàn diện một website:
    - Chụp màn hình (screenshot)
    - Nhận diện Tech Stack (Frontend/Backend/Analytics)
    - Bắt toàn bộ API XHR/Fetch mà trang web gọi
    - Phân tích Form & input tương tác
    - Xuất báo cáo dạng Markdown và JSON
    """
    domain = urlparse(url).netloc.replace(":", "_")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_folder = os.path.join(OUTPUT_DIR, f"{domain}_{timestamp}")
    screenshot_dir = os.path.join(report_folder, "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)

    print(f"\n🚀 Đang khởi động phân tích website: {url}")
    print(f"📁 Thư mục lưu kết quả: {report_folder}\n")

    network_requests = []
    api_endpoints = []

    async with async_playwright() as p:
        # Khởi chạy Chromium / Google Chrome
        browser = await p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Bắt các network request để phát hiện API Backend
        def handle_response(response):
            try:
                req_url = response.url
                resource_type = response.request.resource_type
                status = response.status
                content_type = response.headers.get("content-type", "")

                if resource_type in ["fetch", "xhr"] or "application/json" in content_type:
                    api_endpoints.append({
                        "method": response.request.method,
                        "url": req_url,
                        "status": status,
                        "type": resource_type,
                        "content_type": content_type
                    })
            except Exception:
                pass

        page.on("response", handle_response)

        # Truy cập URL
        try:
            response = await page.goto(url, wait_until="networkidle", timeout=45000)
            status_code = response.status if response else "Unknown"
        except Exception as e:
            print(f"⚠️ Networkidle timeout hoặc cảnh báo: {e}. Vẫn tiếp tục thu thập dữ liệu...")
            status_code = "Loaded with timeout"

        # Chờ thêm cho dynamic scripts chạy
        await asyncio.sleep(wait_seconds)

        # Chụp ảnh màn hình toàn trang
        screenshot_path = os.path.join(screenshot_dir, "fullpage.png")
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"📸 Đã chụp ảnh màn hình: {screenshot_path}")

        # Trích xuất thông tin cơ bản
        title = await page.title()
        meta_desc = await page.evaluate('''() => {
            const meta = document.querySelector('meta[name="description"]') || document.querySelector('meta[property="og:description"]');
            return meta ? meta.getAttribute('content') : '';
        }''')

        # Phát hiện Framework và thư viện JS
        tech_stack = await page.evaluate('''() => {
            const techs = [];
            // Check Frontend Frameworks
            if (window.React || document.querySelector('[data-reactroot], [data-reactid]')) techs.push("React");
            if (window.Vue || document.querySelector('[data-v-]')) techs.push("Vue.js");
            if (window.angular || document.querySelector('[ng-app], [ng-version]')) techs.push("Angular");
            if (window.__NEXT_DATA__) techs.push("Next.js");
            if (window.__NUXT__) techs.push("Nuxt.js");
            if (window.jQuery || window.$) techs.push("jQuery " + (window.jQuery ? window.jQuery.fn.jquery : ""));
            if (document.querySelector('meta[name="generator"][content*="WordPress"]')) techs.push("WordPress");
            if (window.Shopify) techs.push("Shopify");
            if (window.bootstrap) techs.push("Bootstrap");
            if (document.querySelector('[class*="tw-"], [class*="tailwind"]') || Array.from(document.styleSheets).some(s => {
                try { return Array.from(s.cssRules || []).some(r => r.selectorText && r.selectorText.includes('-tw-')); } catch(e) { return false; }
            })) techs.push("Tailwind CSS");

            // Analytics & Tracking
            if (window.ga || window.GoogleAnalyticsObject || window.gtag) techs.push("Google Analytics / GTM");
            if (window.fbq) techs.push("Facebook Pixel");
            if (window.mixpanel) techs.push("Mixpanel");
            if (window.clarity) techs.push("Microsoft Clarity");
            if (window.Intercom) techs.push("Intercom Chat");

            return techs;
        }''')

        # Phân tích các Form và Input
        forms = await page.evaluate('''() => {
            const formElements = document.querySelectorAll('form');
            const result = [];
            formElements.forEach((f, idx) => {
                const inputs = Array.from(f.querySelectorAll('input, select, textarea, button')).map(el => ({
                    tag: el.tagName.toLowerCase(),
                    type: el.getAttribute('type') || '',
                    name: el.getAttribute('name') || '',
                    placeholder: el.getAttribute('placeholder') || '',
                    id: el.id || '',
                    text: el.innerText ? el.innerText.trim().slice(0, 30) : ''
                }));
                result.push({
                    index: idx + 1,
                    action: f.getAttribute('action') || '',
                    method: f.getAttribute('method') || 'GET',
                    inputs: inputs
                });
            });
            return result;
        }''')

        # Thống kê liên kết (Internal vs External links)
        links = await page.evaluate('''() => {
            const aTags = Array.from(document.querySelectorAll('a[href]'));
            const currentHost = window.location.hostname;
            let internal = 0;
            let external = 0;
            const samples = [];
            aTags.forEach(a => {
                const href = a.href;
                try {
                    const u = new URL(href);
                    if (u.hostname === currentHost) {
                        internal++;
                    } else if (u.protocol.startsWith('http')) {
                        external++;
                    }
                    if (samples.length < 15 && href.startsWith('http')) {
                        samples.push({ text: a.innerText.trim().slice(0, 40), url: href });
                    }
                } catch(e) {}
            });
            return { total: aTags.length, internal, external, samples };
        }''')

        await browser.close()

    # Lưu dữ liệu thô JSON
    raw_data = {
        "target_url": url,
        "analyzed_at": datetime.now().isoformat(),
        "title": title,
        "description": meta_desc,
        "status_code": status_code,
        "tech_stack": tech_stack,
        "api_endpoints": api_endpoints,
        "forms_count": len(forms),
        "forms": forms,
        "links": links,
        "screenshot": screenshot_path
    }

    json_file = os.path.join(report_folder, "analysis_data.json")
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, ensure_ascii=False, indent=2)

    # Xuất báo cáo Markdown trực quan
    md_file = os.path.join(report_folder, "RESEARCH_REPORT.md")
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# 📊 Báo Cáo Nghiên Cứu Hệ Thống Website\n\n")
        f.write(f"- **URL Phân Tích**: `{url}`\n")
        f.write(f"- **Thời Gian**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write(f"- **Tiêu Đề Trang**: {title}\n")
        f.write(f"- **Mô Tả (Meta Description)**: {meta_desc or 'Không có'}\n")
        f.write(f"- **Ảnh Chụp Màn Hình**: `screenshots/fullpage.png`\n\n")

        f.write("## 1. 🛠️ Công Nghệ Phát Hiện Được (Tech Stack)\n")
        if tech_stack:
            for tech in tech_stack:
                f.write(f"- ✅ **{tech}**\n")
        else:
            f.write("- *Chưa phát hiện framework phổ biến hoặc trang web dùng server-side rendering truyền thống.*\n")
        f.write("\n")

        f.write("## 2. 🌐 Các API Backend / Endpoint (XHR & Fetch)\n")
        f.write(f"Trang web đã thực hiện **{len(api_endpoints)}** request API khi tải:\n\n")
        if api_endpoints:
            f.write("| Phương thức | Trạng thái | Loại | URL |\n")
            f.write("|-------------|------------|------|-----|\n")
            for ep in api_endpoints[:30]:  # Top 30
                f.write(f"| `{ep['method']}` | `{ep['status']}` | `{ep['type']}` | `{ep['url'][:80]}` |\n")
            if len(api_endpoints) > 30:
                f.write(f"\n*(Còn {len(api_endpoints) - 30} API endpoints khác xem trong file analysis_data.json)*\n")
        else:
            f.write("- *Không bắt được API Fetch/XHR nào trong quá trình tải ban đầu.*\n")
        f.write("\n")

        f.write("## 3. 📝 Các Biểu Mẫu (Forms & Tương Tác)\n")
        f.write(f"Tìm thấy **{len(forms)}** biểu mẫu tương tác trên giao diện:\n\n")
        for form in forms:
            f.write(f"### Form #{form['index']} (Method: `{form['method']}`, Action: `{form['action']}`)\n")
            f.write("| Thẻ | Type | Tên/ID | Placeholder / Nhãn |\n")
            f.write("|-----|------|--------|---------------------|\n")
            for inp in form["inputs"]:
                name_or_id = inp["name"] or inp["id"] or "-"
                label = inp["placeholder"] or inp["text"] or "-"
                f.write(f"| `{inp['tag']}` | `{inp['type']}` | `{name_or_id}` | {label} |\n")
            f.write("\n")

        f.write("## 4. 🔗 Thống Kê Liên Kết (Links)\n")
        f.write(f"- **Tổng số liên kết**: {links['total']}\n")
        f.write(f"- **Liên kết nội bộ (Internal)**: {links['internal']}\n")
        f.write(f"- **Liên kết ngoài (External)**: {links['external']}\n\n")

    print(f"\n✅ ĐÃ HOÀN TẤT PHÂN TÍCH!")
    print(f"📄 Báo cáo chi tiết: {md_file}")
    print(f"📦 Dữ liệu JSON: {json_file}")
    return md_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Công cụ nghiên cứu và phân tích website bằng Chrome Playwright")
    parser.add_argument("url", help="URL website cần phân tích (VD: https://google.com)")
    parser.add_argument("--headed", action="store_true", help="Chạy Chrome hiển thị giao diện thay vì headless")
    parser.add_argument("--wait", type=int, default=4, help="Thời gian chờ thêm sau khi tải xong (giây)")

    args = parser.parse_args()
    target_url = args.url if args.url.startswith("http") else f"https://{args.url}"
    asyncio.run(analyze_website(target_url, headless=not args.headed, wait_seconds=args.wait))
