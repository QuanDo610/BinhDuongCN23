import asyncio
import json
import re
from pathlib import Path
from urllib.parse import urlparse
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "session_state.json"
REPORT_DIR = BASE_DIR / "reports" / "deep_audit"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

async def deep_audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            storage_state=str(SESSION_FILE) if SESSION_FILE.exists() else None,
            viewport={"width": 1440, "height": 900}
        )
        page = await context.new_page()

        requests_log = []
        api_calls = []

        def on_request(req):
            if any(ext in req.url for ext in ['.png', '.jpg', '.jpeg', '.svg', '.woff', '.css']):
                return
            requests_log.append({
                "method": req.method,
                "url": req.url,
                "resource_type": req.resource_type,
                "headers": dict(req.headers)
            })

        def on_response(res):
            content_type = res.headers.get("content-type", "")
            if "json" in content_type or res.request.resource_type in ["xhr", "fetch"]:
                api_calls.append({
                    "method": res.request.method,
                    "url": res.url,
                    "status": res.status,
                    "content_type": content_type
                })

        page.on("request", on_request)
        page.on("response", on_response)

        print("🔍 1. Truy cập trang chủ OERP...")
        await page.goto("https://vpdkddtdm.vn/vptdm/trangchu", wait_until="networkidle")
        await asyncio.sleep(3)

        # Trích xuất tất cả script tags để tìm Angular bundles
        scripts = await page.evaluate('''() => {
            return Array.from(document.querySelectorAll('script[src]')).map(s => s.src);
        }''')

        # Trích xuất tất cả menu và liên kết trên giao diện
        menu_tree = await page.evaluate('''() => {
            const result = [];
            // Tìm tất cả các thẻ a hoặc phần tử có sự kiện click/routerLink
            const elements = document.querySelectorAll('a, [routerlink], .nav-link, .dropdown-item, .menu-item');
            elements.forEach(el => {
                const text = el.innerText ? el.innerText.trim().replace(/\\s+/g, ' ') : '';
                const href = el.getAttribute('href') || el.getAttribute('routerlink') || '';
                if (text && text.length < 80) {
                    result.push({
                        text: text,
                        href: href,
                        tag: el.tagName.toLowerCase(),
                        classes: el.className
                    })
                }
            });
            return result;
        }''')

        # Thử click vào các menu chính để xem các submenu và chụp ảnh màn hình từng chức năng
        print("🔍 2. Khám phá các menu chính...")
        nav_items = ["TIẾP NHẬN", "TRA CỨU", "QUẢN LÝ HỒ SƠ", "THỐNG KÊ"]
        captured_submenus = {}

        for nav in nav_items:
            try:
                locator = page.locator(f"text='{nav}'").first
                if await locator.count() > 0:
                    await locator.hover()
                    await asyncio.sleep(1)
                    # Lấy text các item đang hiển thị
                    sub_texts = await page.evaluate('''() => {
                        return Array.from(document.querySelectorAll('.dropdown-menu.show a, .show a, .nav-item.show a'))
                            .map(a => ({ text: a.innerText.trim(), href: a.getAttribute('href') || a.getAttribute('routerlink') }));
                    }''')
                    captured_submenus[nav] = sub_texts
            except Exception as e:
                captured_submenus[nav] = str(e)

        # Chụp ảnh tổng quan trang chủ
        dashboard_screenshot = REPORT_DIR / "audit_dashboard.png"
        await page.screenshot(path=str(dashboard_screenshot), full_page=True)

        # Trích xuất nội dung LocalStorage và SessionStorage
        storages = await page.evaluate('''() => {
            const ls = {};
            for (let i = 0; i < localStorage.length; i++) {
                const k = localStorage.key(i);
                ls[k] = localStorage.getItem(k);
            }
            const ss = {};
            for (let i = 0; i < sessionStorage.length; i++) {
                const k = sessionStorage.key(i);
                ss[k] = sessionStorage.getItem(k);
            }
            return { localStorage: ls, sessionStorage: ss };
        }''')

        # Thử lấy danh sách route từ bundle Angular runtime/main nếu có
        # Lưu dữ liệu thô
        audit_data = {
            "title": await page.title(),
            "url": page.url,
            "scripts": scripts,
            "menu_tree": menu_tree,
            "captured_submenus": captured_submenus,
            "api_calls": api_calls,
            "storages_keys": list(storages["localStorage"].keys()) + list(storages["sessionStorage"].keys()),
            "storages": storages
        }

        with open(REPORT_DIR / "audit_data.json", "w", encoding="utf-8") as f:
            json.dump(audit_data, f, ensure_ascii=False, indent=2)

        print("✅ Hoàn tất thu thập dữ liệu Audit cơ bản!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(deep_audit())
