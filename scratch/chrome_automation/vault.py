import os
import json
import stat
import getpass
from pathlib import Path
from cryptography.fernet import Fernet

VAULT_DIR = Path(__file__).resolve().parent
KEY_FILE = VAULT_DIR / ".secret_key"
VAULT_FILE = VAULT_DIR / "credentials.vault"

def _ensure_strict_permissions(path: Path):
    """Đảm bảo chỉ có chủ sở hữu máy tính (user hiện tại) mới có quyền đọc/ghi file (chmod 600)"""
    if path.exists():
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)

def get_or_create_key() -> bytes:
    """Lấy hoặc tạo mới master key mã hóa AES-256"""
    if KEY_FILE.exists():
        with open(KEY_FILE, "rb") as f:
            return f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        _ensure_strict_permissions(KEY_FILE)
        return key

def save_credentials(data: dict):
    """Mã hóa toàn bộ data và lưu vào credentials.vault"""
    key = get_or_create_key()
    cipher = Fernet(key)
    json_bytes = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    encrypted_data = cipher.encrypt(json_bytes)

    with open(VAULT_FILE, "wb") as f:
        f.write(encrypted_data)
    _ensure_strict_permissions(VAULT_FILE)

def load_credentials() -> dict:
    """Giải mã credentials từ file vault"""
    if not VAULT_FILE.exists():
        return {}
    key = get_or_create_key()
    cipher = Fernet(key)
    with open(VAULT_FILE, "rb") as f:
        encrypted_data = f.read()
    decrypted_bytes = cipher.decrypt(encrypted_data)
    return json.loads(decrypted_bytes.decode("utf-8"))

def init_default_account():
    """Khởi tạo tài khoản ban đầu theo thông tin người dùng cung cấp"""
    default_data = {
        "site_url": "https://vpdkddtdm.vn/vptdm/trangchu",
        "username": "tdm_nguyetbtm",
        "password": None,  # Mật khẩu để trống cho đến khi người dùng quyết định nhập
        "note": "Tài khoản OERP Văn phòng Đăng ký đất đai Thủ Dầu Một",
        "has_password": False
    }
    save_credentials(default_data)
    print("🔒 Đã khởi tạo và mã hóa Vault thành công (AES-256)!")
    print(f"📁 Tệp mã hóa: {VAULT_FILE}")
    print(f"🔑 Tệp khóa: {KEY_FILE} (đã phân quyền chmod 600 nghiêm ngặt)")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "set-password":
        # Cho phép người dùng tự gõ password bí mật trên terminal mà không hiện ký tự
        pwd = getpass.getpass("Nhập mật khẩu của bạn (ký tự sẽ được ẩn hoàn toàn): ")
        creds = load_credentials()
        creds["password"] = pwd
        creds["has_password"] = True
        save_credentials(creds)
        print("✅ Mật khẩu đã được mã hóa và lưu an toàn vào Vault!")
    elif len(sys.argv) > 1 and sys.argv[1] == "show":
        creds = load_credentials()
        # Ẩn password khi hiển thị
        display_data = creds.copy()
        if display_data.get("password"):
            display_data["password"] = "********"
        print("\n--- THÔNG TIN TRONG VAULT (ĐÃ GIẢI MÃ BẢO MẬT) ---")
        print(json.dumps(display_data, ensure_ascii=False, indent=2))
    else:
        init_default_account()
