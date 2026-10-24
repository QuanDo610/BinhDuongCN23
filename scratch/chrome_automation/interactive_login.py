import os
import asyncio
import stat
from pathlib import Path
from playwright.async_api import async_playwright
from vault import load_credentials

BASE_DIR = Path(__file__).resolve().parent
SESSION_FILE = BASE_DIR / "session_state.json"

async def login_interactive():
    # 1. Đọc thông tin từ Vault bảo mật
    creds = load_credentials()
    site_url = creds.get("site_url", "https://vpdkddtdm.vn/vptdm/trangchu")
    username = creds.get("username", "tdm_nguyetbtm")

    print("\n" + "="*60)
    print("🔐 CHẾ ĐỘ ĐĂNG NHẬP BẢO MẬT (ZERO-KNOWLEDGE)")
    print("="*60)
    print(f"🌐 Trang web: {site_url}")
    print(f"👤 Tài khoản: {username}")
    print("🛡️ Bạn sẽ tự gõ mật khẩu trực tiếp trên Chrome. AI không nhìn thấy mật khẩu của bạn.")
    print("="*60 + "\n")

    async with async_playwright() as p:
        # Mở Chrome có giao diện thật trên màn hình macOS
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context(
            viewport={"width": 1400, "height": 900}
        )
        page = await context.new_page()

        print("🚀 Đang mở trình duyệt Chrome...")
        await page.goto(site_url, wait_until="networkidle")

        # Điền tự động tài khoản
        try:
            user_input = page.locator('input[name="taikhoan"], input[placeholder*="Tài khoản"]').first
            await user_input.wait_for(timeout=10000)
            await user_input.fill(username)
            print(f"✅ Đã tự động điền tài khoản: {username}")
        except Exception:
            print("ℹ️ Bạn vui lòng bấm vào ô tài khoản nếu chưa được điền.")

        # Focus vào ô mật khẩu để người dùng chỉ việc gõ
        try:
            pwd_input = page.locator('input[name="matkhau"], input[type="password"]').first
            await pwd_input.focus()
        except Exception:
            pass

        print("\n👉 HÃY CHUYỂN SANG CỬA SỔ CHROME VỪA MỞ:")
        print("   1. Gõ mật khẩu của bạn vào ô 'Mật khẩu'")
        print("   2. Bấm nút [Đăng nhập]")
        print("   3. Script đang chờ bạn đăng nhập thành công...\n")

        # Theo dõi sự kiện đăng nhập thành công
        login_success = False
        start_time = asyncio.get_event_loop().time()
        initial_check_done = False

        # Đợi 2 giây đầu tiên để trang tải hoàn toàn form
        await asyncio.sleep(2)

        while not login_success:
            await asyncio.sleep(1)

            # Kiểm tra xem ô password có còn trên màn hình không
            has_password_box = await page.locator('input[type="password"]').count() > 0

            # Kiểm tra xem có dấu hiệu đăng nhập thành công không (nút đăng xuất, menu, tên người dùng)
            logout_btn = await page.locator('text=Đăng xuất, a:has-text("Đăng xuất"), .fa-sign-out, .logout').count()
            user_text = await page.locator('text=tdm_nguyetbtm, .user-name, .header-user').count()

            # Nếu ban đầu có ô password, sau khi user login thì ô password biến mất hoặc xuất hiện nút đăng xuất
            if logout_btn > 0 or user_text > 0 or not has_password_box:
                # Đợi thêm 2 giây để đảm bảo token và cookies đã được lưu đầy đủ
                await asyncio.sleep(2)
                login_success = True
                break

            # Timeout sau 5 phút nếu người dùng chưa thao tác
            if asyncio.get_event_loop().time() - start_time > 300:
                print("⏱️ Đã hết thời gian chờ (5 phút).")
                break

        if login_success:
            print("\n🎉 ĐĂNG NHẬP THÀNH CÔNG!")
            # Lưu lại trạng thái phiên làm việc (cookies + local storage)
            await context.storage_state(path=str(SESSION_FILE))
            # Phân quyền file bảo mật chmod 600
            if SESSION_FILE.exists():
                os.chmod(SESSION_FILE, stat.S_IRUSR | stat.S_IWUSR)
            print(f"💾 Đã lưu phiên làm việc an toàn vào: {SESSION_FILE}")
            print("🔒 Lần chạy automation tiếp theo bạn sẽ không cần phải đăng nhập lại nữa!")
            await asyncio.sleep(2)
        else:
            print("⚠️ Chưa phát hiện phiên đăng nhập.")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(login_interactive())
