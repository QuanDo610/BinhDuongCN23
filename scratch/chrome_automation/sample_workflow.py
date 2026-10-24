import asyncio
import os
from playwright.async_api import async_playwright

"""
Kịch bản tự động hóa tác vụ mẫu:
- Mở Chrome (có thể hiển thị giao diện hoặc chạy ngầm)
- Đăng nhập hoặc điều hướng tới trang cần thao tác
- Điền dữ liệu tự động, bấm nút, xử lý popup
- Lưu phiên làm việc (cookies / storage state) để không cần đăng nhập lại lần sau
"""

AUTH_STATE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "storage_state.json")

async def run_automation_example():
    async with async_playwright() as p:
        # headless=False để người dùng nhìn thấy Chrome đang thao tác thật
        browser = await p.chromium.launch(headless=False, slow_mo=500)

        # Sử dụng storage_state nếu đã lưu phiên đăng nhập trước đó
        context_args = {
            "viewport": {"width": 1280, "height": 800}
        }
        if os.path.exists(AUTH_STATE_FILE):
            print("🔑 Tìm thấy phiên đăng nhập cũ, đang tải cookies...")
            context_args["storage_state"] = AUTH_STATE_FILE

        context = await browser.new_context(**context_args)
        page = await context.new_page()

        print("🌐 Đang mở trang web ví dụ...")
        await page.goto("https://quotes.toscrape.com/")

        # Ví dụ tương tác: Bấm nút Login
        print("🖱️ Tìm và bấm nút Login...")
        login_btn = page.locator("a[href='/login']")
        if await login_btn.count() > 0:
            await login_btn.click()
            await page.wait_for_load_state("networkidle")

            # Điền form
            print("✍️ Tự động điền tài khoản mẫu...")
            await page.fill("#username", "my_automation_user")
            await page.fill("#password", "super_secret_password")

            # Nhấn submit
            await page.click("input[type='submit']")
            await page.wait_for_timeout(2000)

            # Lưu lại trạng thái cookies/session cho lần chạy sau
            await context.storage_state(path=AUTH_STATE_FILE)
            print(f"💾 Đã lưu session vào {AUTH_STATE_FILE}")

        print("🎉 Hoàn tất kịch bản tự động hóa mẫu!")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automation_example())
