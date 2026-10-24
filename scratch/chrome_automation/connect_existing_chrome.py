import asyncio
from playwright.async_api import async_playwright

"""
KẾT NỐI VÀO CỬA SỔ GOOGLE CHROME BẠN ĐANG MỞ TRÊN MÁY:
1. Đóng Chrome đang mở (nếu cần).
2. Mở Chrome từ Terminal với cổng debug:
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
3. Đăng nhập vào trang web bạn muốn.
4. Chạy script này, Antigravity sẽ tự động kết nối vào đúng cửa sổ Chrome đó và thao tác trực tiếp!
"""

CDP_URL = "http://localhost:9222"

async def connect_to_existing_chrome():
    print(f"🔗 Đang kết nối vào Chrome có sẵn tại {CDP_URL}...")
    try:
        async with async_playwright() as p:
            browser = await p.chromium.connect_over_cdp(CDP_URL)
            default_context = browser.contexts[0]
            pages = default_context.pages

            print(f"✅ Đã kết nối thành công! Tìm thấy {len(pages)} tab đang mở.")
            for i, pg in enumerate(pages):
                title = await pg.title()
                print(f"  Tab {i+1}: {title} ({pg.url})")

            # Tìm tab OERP hoặc trang web mong muốn
            target_page = None
            for pg in pages:
                if "vpdkddtdm.vn" in pg.url:
                    target_page = pg
                    break

            if target_page:
                print(f"\n🎯 Đã tìm thấy tab mục tiêu: {target_page.url}")
                # Ví dụ thao tác trực tiếp trên tab này
            else:
                print("\nℹ️ Không tìm thấy tab vpdkddtdm.vn. Bạn có thể mở một tab mới hoặc chuyển tab.")

            await browser.close()
    except Exception as e:
        print(f"❌ Không thể kết nối tới Chrome qua cổng 9222.")
        print(f"Chi tiết lỗi: {e}")
        print("\n👉 Cách mở Chrome hỗ trợ kết nối:")
        print('/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222')

if __name__ == "__main__":
    asyncio.run(connect_to_existing_chrome())
