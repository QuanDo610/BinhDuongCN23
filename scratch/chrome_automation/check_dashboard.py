import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "session_state.json"

async def check_dashboard():
    if not SESSION_FILE.exists():
        print("❌ Không tìm thấy file session_state.json.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Sử dụng lại phiên làm việc đã lưu
        context = await browser.new_context(
            storage_state=str(SESSION_FILE),
            viewport={"width": 1400, "height": 900}
        )
        page = await context.new_page()

        print("🔄 Đang kiểm tra phiên làm việc với session đã lưu...")
        await page.goto("https://vpdkddtdm.vn/vptdm/trangchu", wait_until="networkidle")

        title = await page.title()
        print(f"📄 Tiêu đề trang: {title}")

        # Lấy danh sách các menu hoặc chức năng chính trên trang chủ
        menu_items = await page.evaluate('''() => {
            const items = [];
            document.querySelectorAll('a, button, .nav-item, .menu-item').forEach(el => {
                const text = el.innerText ? el.innerText.trim() : '';
                if (text && text.length < 50 && !items.includes(text)) {
                    items.push(text);
                }
            });
            return items.slice(0, 20);
        }''')

        print(f"🎯 Các tính năng / menu tìm thấy trên giao diện ({len(menu_items)} mục):")
        for item in menu_items:
            print(f"  - {item}")

        screenshot_path = BASE_DIR / "reports" / "dashboard_logged_in.png"
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(screenshot_path))
        print(f"\n📸 Đã chụp ảnh màn hình trang quản trị: {screenshot_path}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_dashboard())
