import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "session_state.json"
PAGES_DIR = BASE_DIR / "reports" / "pages_audit"
PAGES_DIR.mkdir(parents=True, exist_ok=True)

ROUTES = [
    {"name": "TrangChu", "path": "/vptdm/trangchu"},
    {"name": "TiepNhanHoSo", "path": "/vptdm/tiepnhanhoso"},
    {"name": "XuLyHoSo", "path": "/vptdm/xulyhoso"},
    {"name": "SuaHoSo", "path": "/vptdm/suahoso"},
    {"name": "TraHoSo", "path": "/vptdm/trahoso"},
    {"name": "TraCuuHoSo", "path": "/vptdm/tracuuhoso"},
    {"name": "QuanLyTrangThai", "path": "/vptdm/quanlytrangthaihoso"},
    {"name": "DashboardTrichDo", "path": "/vptdm/dashboard-trichdo"},
    {"name": "ThongKeTongHop", "path": "/vptdm/thongketonghop"},
]

async def explore_all_pages():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1440, "height": 900}
        )
        page = await context.new_page()

        results = []

        for r in ROUTES:
            full_url = f"https://vpdkddtdm.vn{r['path']}"
            print(f"👉 Đang kiểm tra: {r['name']} ({full_url})")
            try:
                await page.goto(full_url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)
                title = await page.title()

                # Chụp ảnh
                shot_path = PAGES_DIR / f"{r['name']}.png"
                await page.screenshot(path=str(shot_path))

                # Lấy text tiêu đề / nội dung chính
                page_info = await page.evaluate('''() => {
                    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, .title, .card-header, .header-title'))
                        .map(h => h.innerText.trim()).filter(Boolean);
                    const buttons = Array.from(document.querySelectorAll('button, a.btn, input[type="button"], input[type="submit"]'))
                        .map(b => b.innerText ? b.innerText.trim() : b.value).filter(Boolean);
                    const tables = document.querySelectorAll('table').length;
                    const inputs = Array.from(document.querySelectorAll('input, select, textarea'))
                        .map(i => i.placeholder || i.name || i.getAttribute('aria-label') || '').filter(Boolean);

                    return { headings, buttons: buttons.slice(0, 15), tables, inputs: inputs.slice(0, 15) };
                }''')

                results.append({
                    "name": r["name"],
                    "path": r["path"],
                    "url": full_url,
                    "title": title,
                    "headings": page_info["headings"][:5],
                    "buttons": page_info["buttons"],
                    "tables_count": page_info["tables"],
                    "inputs_sample": page_info["inputs"],
                    "screenshot": str(shot_path.name)
                })
                print(f"   ✅ Đã quét {r['name']}: {len(page_info['buttons'])} buttons, {page_info['tables']} tables")
            except Exception as e:
                print(f"   ⚠️ Lỗi khi quét {r['name']}: {e}")
                results.append({
                    "name": r["name"],
                    "path": r["path"],
                    "error": str(e)
                })

        with open(PAGES_DIR / "pages_summary.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

        print("\n🎉 Hoàn thành quét toàn bộ các trang chức năng!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(explore_all_pages())
