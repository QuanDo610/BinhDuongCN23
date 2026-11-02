import os
import base64
import zipfile

# 1. Read the ico file and convert to certutil base64 format
with open("A_THANG/vpdk23.ico", "rb") as f:
    ico_bytes = f.read()

b64_str = base64.b64encode(ico_bytes).decode("ascii")
b64_lines = [b64_str[i:i+64] for i in range(0, len(b64_str), 64)]
cert_content = "-----BEGIN CERTIFICATE-----\r\n" + "\r\n".join(b64_lines) + "\r\n-----END CERTIFICATE-----\r\n"

# 2. Build the bat file
bat_template = """@echo off
:: ===============================================================================
:: CÔNG CỤ TỰ ĐỘNG CÀI ĐẶT PHÍM TẮT CỔNG DỊCH VỤ NỘI BỘ - CHI NHÁNH SỐ 23
:: - Mở trực tiếp bằng Google Chrome hoặc Microsoft Edge
:: - Biểu tượng (Icon/Thumbnail) huy hiệu Chi Nhánh 23 Hoàng gia Vàng & Xanh nổi bật
:: ===============================================================================
chcp 65001 >nul
title Cài đặt Phím tắt Cổng Dịch Vụ - Chi Nhánh 23
color 0B

echo.
echo ===============================================================================
echo       CỔNG DỊCH VỤ NỘI BỘ - VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI CHI NHÁNH SỐ 23
echo               (Hệ thống Lịch Tuần & Tiếp nhận IT Helpdesk)
echo ===============================================================================
echo.
echo [*] BƯỚC 1: Đang thiết lập Biểu tượng (Icon) Chi Nhánh 23 độc quyền...

:: Tạo thư mục lưu Icon ứng dụng trong LocalAppData của cán bộ
set "APP_DIR=%LOCALAPPDATA%\\VPDK23"
if not exist "%APP_DIR%" mkdir "%APP_DIR%" 2>nul
set "ICON_FILE=%APP_DIR%\\vpdk23.ico"

:: Ưu tiên 1: Lấy icon có sẵn trong cùng thư mục (khi giải nén từ file zip)
if exist "%~dp0vpdk23.ico" (
    copy /y "%~dp0vpdk23.ico" "%ICON_FILE%" >nul 2>&1
)

:: Ưu tiên 2: Nếu chưa có, tải tự động từ máy chủ GitHub
if not exist "%ICON_FILE%" (
    curl -s -L "https://raw.githubusercontent.com/QuanDo610/vpdk-cn23/main/vpdk23.ico" -o "%ICON_FILE%" 2>nul
)

:: Ưu tiên 3: Nếu không có mạng ngoài, giải mã từ dữ liệu nhúng sẵn bên trong file BAT
if not exist "%ICON_FILE%" (
    set "TEMP_B64=%TEMP%\\vpdk23_ico.b64"
    > "!TEMP_B64!" (
        echo [BASE64_PLACEHOLDER]
    )
    certutil -decode "!TEMP_B64!" "%ICON_FILE%" >nul 2>&1
    del /f /q "!TEMP_B64!" 2>nul
)

:: Ưu tiên 4: Dự phòng icon bảo mật hệ thống Windows nếu tất cả đều không có
if not exist "%ICON_FILE%" (
    set "ICON_FILE=%SystemRoot%\\System32\\shell32.dll,220"
    echo   [!] Sử dụng biểu tượng bảo vệ hệ thống Windows.
) else (
    echo   [OK] Đã thiết lập thành công Icon Huy hiệu Chi Nhánh 23 sắc nét.
)

echo.
echo [*] BƯỚC 2: Đang tự động dò tìm trình duyệt Google Chrome hoặc Microsoft Edge...

:: Dò tìm Google Chrome
set "BROWSER_EXE="
set "BROWSER_NAME="

if exist "%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
)

:: Nếu không có Chrome, dùng Microsoft Edge (mặc định có sẵn 100%% trên Windows 10/11)
if not defined BROWSER_EXE (
    if exist "%ProgramFiles(x86)%\\Microsoft\\Edge\\Application\\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles(x86)%\\Microsoft\\Edge\\Application\\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    ) else if exist "%ProgramFiles%\\Microsoft\\Edge\\Application\\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles%\\Microsoft\\Edge\\Application\\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    )
)

:: Dò tìm bằng lệnh where nếu cài ở ổ đĩa khác
if not defined BROWSER_EXE (
    for /f "delims=" %%i in ('where chrome.exe 2^>nul') do (
        set "BROWSER_EXE=%%i"
        set "BROWSER_NAME=Google Chrome"
    )
)
if not defined BROWSER_EXE (
    for /f "delims=" %%i in ('where msedge.exe 2^>nul') do (
        set "BROWSER_EXE=%%i"
        set "BROWSER_NAME=Microsoft Edge"
    )
)

:: Dự phòng cuối cùng
if not defined BROWSER_EXE (
    set "BROWSER_EXE=%SystemRoot%\\explorer.exe"
    set "BROWSER_NAME=Trình duyệt hệ thống"
)

echo   [OK] Trình duyệt được chọn để mở hệ thống: %BROWSER_NAME%

echo.
echo [*] BƯỚC 3: Đang khởi tạo Lối tắt (Shortcut .lnk) nổi bật ngoài Desktop...

set "TARGET_URL=https://quando610.github.io/vpdk-cn23/index.html"

:: Gọi PowerShell để tạo Shortcut chuẩn Windows LNK có Icon đẹp
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $desktop = [Environment]::GetFolderPath('Desktop'); ^
   $name = 'Cổng Dịch Vụ - Chi Nhánh 23.lnk'; ^
   $p1 = Join-Path $desktop $name; ^
   function MakeLnk($dest) { ^
       $s = $ws.CreateShortcut($dest); ^
       $s.TargetPath = '%BROWSER_EXE%'; ^
       $s.Arguments = '%TARGET_URL%'; ^
       $s.IconLocation = '%ICON_FILE%'; ^
       $s.Description = 'Cổng Dịch Vụ Nội Bộ - Văn Phòng Đăng Ký Đất Đai Chi Nhánh 23'; ^
       $s.WorkingDirectory = [System.IO.Path]::GetDirectoryName('%BROWSER_EXE%'); ^
       $s.Save(); ^
   }; ^
   MakeLnk($p1); ^
   Write-Host '   -> Da tao Shortcut chinh tai:' $p1 -ForegroundColor Green; ^
   if (Test-Path \"$env:USERPROFILE\\Desktop\") { ^
       $p2 = Join-Path \"$env:USERPROFILE\\Desktop\" $name; ^
       if ($p2 -ne $p1) { MakeLnk($p2); } ^
   }; ^
   if (Test-Path \"$env:USERPROFILE\\OneDrive\\Desktop\") { ^
       $p3 = Join-Path \"$env:USERPROFILE\\OneDrive\\Desktop\" $name; ^
       if ($p3 -ne $p1) { MakeLnk($p3); } ^
   }; ^
   Remove-Item \"$desktop\\Cổng Dịch Vụ - Chi Nhánh 23.url\" -ErrorAction SilentlyContinue; ^
   Remove-Item \"$desktop\\Cong Dich Vu - Chi Nhanh 23.url\" -ErrorAction SilentlyContinue;"

echo.
echo ===============================================================================
echo  [V] HOÀN TẤT THÀNH CÔNG!
echo      - Đã tạo biểu tượng Huy Hiệu Chi Nhánh 23 cực đẹp ngoài Màn hình Desktop.
echo      - Mặc định khởi chạy qua: %BROWSER_NAME%.
echo ===============================================================================
echo.
echo [*] Đang tự động mở Cổng dịch vụ lần đầu bằng %BROWSER_NAME%...
start "" "%BROWSER_EXE%" "%TARGET_URL%"

echo.
echo -------------------------------------------------------------------------------
echo  HƯỚNG DẪN DÀNH CHO CÁN BỘ:
echo  1. Hằng ngày vào làm việc, chỉ cần bấm đúp vào biểu tượng "Cổng Dịch Vụ - Chi Nhánh 23"
echo     (hình khiên vàng xanh) ngay trên màn hình Desktop.
echo  2. Đăng nhập bằng Số CCCD (12 số) và Mật khẩu được cấp.
echo -------------------------------------------------------------------------------
echo.
echo Nhấn phím bất kỳ để đóng cửa sổ này...
pause >nul
exit /b
"""

# Replace placeholder with certutil block in a neat subroutine
# To avoid command line length limits in echo, we can output the base64 via a subroutine or certutil file
certutil_script = """@echo off
:: ===============================================================================
:: CÔNG CỤ TỰ ĐỘNG CÀI ĐẶT PHÍM TẮT CỔNG DỊCH VỤ NỘI BỘ - CHI NHÁNH SỐ 23
:: - Mở trực tiếp bằng Google Chrome hoặc Microsoft Edge
:: - Biểu tượng (Icon/Thumbnail) huy hiệu Chi Nhánh 23 Hoàng gia Vàng & Xanh nổi bật
:: ===============================================================================
chcp 65001 >nul
title Cài đặt Phím tắt Cổng Dịch Vụ - Chi Nhánh 23
color 0B

echo.
echo ===============================================================================
echo       CỔNG DỊCH VỤ NỘI BỘ - VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI CHI NHÁNH SỐ 23
echo               (Hệ thống Lịch Tuần & Tiếp nhận IT Helpdesk)
echo ===============================================================================
echo.
echo [*] BƯỚC 1: Đang thiết lập Biểu tượng (Icon) Chi Nhánh 23 độc quyền...

:: Tạo thư mục lưu Icon ứng dụng trong LocalAppData của cán bộ
set "APP_DIR=%LOCALAPPDATA%\\VPDK23"
if not exist "%APP_DIR%" mkdir "%APP_DIR%" 2>nul
set "ICON_FILE=%APP_DIR%\\vpdk23.ico"

:: Ưu tiên 1: Lấy icon có sẵn trong cùng thư mục (khi giải nén từ file zip)
if exist "%~dp0vpdk23.ico" (
    copy /y "%~dp0vpdk23.ico" "%ICON_FILE%" >nul 2>&1
)

:: Ưu tiên 2: Nếu chưa có, tải tự động từ máy chủ GitHub
if not exist "%ICON_FILE%" (
    curl -s -L "https://raw.githubusercontent.com/QuanDo610/vpdk-cn23/main/vpdk23.ico" -o "%ICON_FILE%" 2>nul
)

:: Ưu tiên 3: Dự phòng icon bảo mật hệ thống Windows nếu mạng chặn tải
if not exist "%ICON_FILE%" (
    set "ICON_FILE=%SystemRoot%\\System32\\shell32.dll,220"
    echo   [!] Tạm thời dùng biểu tượng bảo vệ hệ thống Windows.
) else (
    echo   [OK] Đã thiết lập thành công Icon Huy hiệu Chi Nhánh 23 sắc nét.
)

echo.
echo [*] BƯỚC 2: Đang tự động dò tìm trình duyệt Google Chrome hoặc Microsoft Edge...

set "BROWSER_EXE="
set "BROWSER_NAME="

:: Dò tìm Google Chrome
if exist "%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe" (
    set "BROWSER_EXE=%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
)

:: Nếu không có Chrome, tự động chuyển sang Microsoft Edge (sẵn 100% trên Win 10/11)
if not defined BROWSER_EXE (
    if exist "%ProgramFiles(x86)%\\Microsoft\\Edge\\Application\\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles(x86)%\\Microsoft\\Edge\\Application\\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    ) else if exist "%ProgramFiles%\\Microsoft\\Edge\\Application\\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles%\\Microsoft\\Edge\\Application\\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    )
)

:: Dò tìm bằng lệnh where nếu cài ở phân vùng khác
if not defined BROWSER_EXE (
    for /f "delims=" %%i in ('where chrome.exe 2^>nul') do (
        set "BROWSER_EXE=%%i"
        set "BROWSER_NAME=Google Chrome"
    )
)
if not defined BROWSER_EXE (
    for /f "delims=" %%i in ('where msedge.exe 2^>nul') do (
        set "BROWSER_EXE=%%i"
        set "BROWSER_NAME=Microsoft Edge"
    )
)

if not defined BROWSER_EXE (
    set "BROWSER_EXE=%SystemRoot%\\explorer.exe"
    set "BROWSER_NAME=Trình duyệt hệ thống"
)

echo   [OK] Trình duyệt chuyên dụng: %BROWSER_NAME%

echo.
echo [*] BƯỚC 3: Đang khởi tạo Lối tắt (Shortcut .lnk) nổi bật ngoài Desktop...

set "TARGET_URL=https://quando610.github.io/vpdk-cn23/index.html"

:: Gọi PowerShell để tạo Shortcut chuẩn Windows LNK có Icon đẹp
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $desktop = [Environment]::GetFolderPath('Desktop'); ^
   $name = 'Cổng Dịch Vụ - Chi Nhánh 23.lnk'; ^
   $p1 = Join-Path $desktop $name; ^
   function MakeLnk($dest) { ^
       $s = $ws.CreateShortcut($dest); ^
       $s.TargetPath = '%BROWSER_EXE%'; ^
       $s.Arguments = '%TARGET_URL%'; ^
       $s.IconLocation = '%ICON_FILE%'; ^
       $s.Description = 'Cổng Dịch Vụ Nội Bộ - Văn Phòng Đăng Ký Đất Đai Chi Nhánh 23'; ^
       $s.WorkingDirectory = [System.IO.Path]::GetDirectoryName('%BROWSER_EXE%'); ^
       $s.Save(); ^
   }; ^
   MakeLnk($p1); ^
   Write-Host '   -> Da tao Shortcut chinh tai:' $p1 -ForegroundColor Green; ^
   if (Test-Path \"$env:USERPROFILE\\Desktop\") { ^
       $p2 = Join-Path \"$env:USERPROFILE\\Desktop\" $name; ^
       if ($p2 -ne $p1) { MakeLnk($p2); } ^
   }; ^
   if (Test-Path \"$env:USERPROFILE\\OneDrive\\Desktop\") { ^
       $p3 = Join-Path \"$env:USERPROFILE\\OneDrive\\Desktop\" $name; ^
       if ($p3 -ne $p1) { MakeLnk($p3); } ^
   }; ^
   Remove-Item \"$desktop\\Cổng Dịch Vụ - Chi Nhánh 23.url\" -ErrorAction SilentlyContinue; ^
   Remove-Item \"$desktop\\Cong Dich Vu - Chi Nhanh 23.url\" -ErrorAction SilentlyContinue;"

echo.
echo ===============================================================================
echo  [V] HOÀN TẤT THÀNH CÔNG!
echo      - Biểu tượng Huy Hiệu Chi Nhánh 23 đã được cài đặt ngoài Desktop.
echo      - Đã cố định mở trực tiếp bằng: %BROWSER_NAME%.
echo ===============================================================================
echo.
echo [*] Đang tự động mở Cổng dịch vụ lần đầu bằng %BROWSER_NAME%...
start "" "%BROWSER_EXE%" "%TARGET_URL%"

echo.
echo -------------------------------------------------------------------------------
echo  HƯỚNG DẪN DÀNH CHO CÁN BỘ:
echo  1. Hằng ngày, cán bộ chỉ cần bấm đúp vào biểu tượng "Cổng Dịch Vụ - Chi Nhánh 23"
echo     (hình Huy Hiệu vàng - xanh có số 23) trên màn hình Desktop.
echo  2. Đăng nhập bằng Số CCCD (12 số) và Mật khẩu đã được cấp.
echo -------------------------------------------------------------------------------
echo.
echo Nhấn phím bất kỳ để đóng cửa sổ này...
pause >nul
exit /b
"""

bat_path = "A_THANG/Tao_Icon_Desktop_VPDK23.bat"
with open(bat_path, "w", encoding="utf-8-sig", newline="\r\n") as f:
    f.write(certutil_script)

print("Updated A_THANG/Tao_Icon_Desktop_VPDK23.bat successfully!")

# Recreate the zip with BOTH Tao_Icon_Desktop_VPDK23.bat AND vpdk23.ico
zip_path = "A_THANG/Tao_Icon_Desktop_VPDK23.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(bat_path, arcname="Tao_Icon_Desktop_VPDK23.bat")
    zipf.write("A_THANG/vpdk23.ico", arcname="vpdk23.ico")

print(f"Updated {zip_path} containing both .bat and .ico successfully ({os.path.getsize(zip_path)} bytes)")
