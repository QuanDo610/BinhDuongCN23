import os
import zipfile
import base64

def generate_family_cn23_installer():
    # 1. Read base64 of pikachu_badge.ico to embed in the bat file for 100% offline self-healing
    with open("A_THANG/pikachu_badge.ico", "rb") as f:
        ico_bytes = f.read()
    b64_str = base64.b64encode(ico_bytes).decode("ascii")
    b64_lines = [b64_str[i:i+64] for i in range(0, len(b64_str), 64)]
    b64_cert = "-----BEGIN CERTIFICATE-----\r\n" + "\r\n".join(b64_lines) + "\r\n-----END CERTIFICATE-----\r\n"

    bat_script = r"""@echo off
:: ===============================================================================
:: CÔNG CỤ TỰ ĐỘNG CÀI ĐẶT PHÍM TẮT "FAMILY CN23" (PIKACHU KÍNH VUÔNG)
:: - Văn phòng Đăng ký đất đai - Chi nhánh số 23
:: - Chạy được từ mọi vị trí: Downloads, Desktop, ổ C, D, E, USB...
:: - Tự động định vị Desktop chính xác (hỗ trợ cả Windows thường & OneDrive)
:: - Biểu tượng Pikachu Đeo Kính Vuông rực rỡ, không bao giờ mất icon
:: ===============================================================================
chcp 65001 >nul
title Cài đặt Phím tắt "Family CN23" Pikachu Kính Vuông
color 0E

:: Chuyển thư mục làm việc về đúng nơi chứa file BAT (hỗ trợ mọi ổ đĩa C, D, E, mạng)
pushd "%~dp0"

echo.
echo ===============================================================================
echo            FAMILY CN23 - VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI CHI NHÁNH SỐ 23
echo                 (Hệ thống Lịch Tuần & Tiếp nhận IT Helpdesk)
echo ===============================================================================
echo.
echo [*] BƯỚC 1: Đang thiết lập Biểu tượng Pikachu Kính Vuông vào hệ thống...

:: Tạo thư mục lưu Icon cố định trong LocalAppData của cán bộ (tránh mất icon khi xóa mục Downloads)
set "APP_DIR=%LOCALAPPDATA%\VPDK23"
if not exist "%APP_DIR%" mkdir "%APP_DIR%" 2>nul
set "ICON_FILE=%APP_DIR%\pikachu_badge.ico"

:: Ưu tiên 1: Copy icon có sẵn trong cùng thư mục giải nén
if exist "%~dp0pikachu_badge.ico" (
    copy /y "%~dp0pikachu_badge.ico" "%ICON_FILE%" >nul 2>&1
)

:: Ưu tiên 2: Copy icon pikachu.ico nếu có
if not exist "%ICON_FILE%" (
    if exist "%~dp0pikachu.ico" (
        copy /y "%~dp0pikachu.ico" "%ICON_FILE%" >nul 2>&1
    )
)

:: Ưu tiên 3: Tải từ máy chủ GitHub
if not exist "%ICON_FILE%" (
    curl -s -L "https://raw.githubusercontent.com/QuanDo610/vpdk-cn23/main/pikachu_badge.ico" -o "%ICON_FILE%" 2>nul
)

:: Ưu tiên 4: Giải mã từ dữ liệu nhúng sẵn bên trong file BAT (tự phục hồi 100% offline)
if not exist "%ICON_FILE%" (
    set "TEMP_B64=%TEMP%\pika_badge_%RANDOM%.b64"
    call :ExtractEmbeddedIcon "!TEMP_B64!"
    if exist "!TEMP_B64!" (
        certutil -decode "!TEMP_B64!" "%ICON_FILE%" >nul 2>&1
        del /f /q "!TEMP_B64!" 2>nul
    )
)

:: Kiểm tra kết quả thiết lập icon
if exist "%ICON_FILE%" (
    echo   [OK] Biểu tượng Pikachu Kính Vuông đã sẵn sàng tại:
    echo        %ICON_FILE%
) else (
    set "ICON_FILE=%SystemRoot%\System32\shell32.dll,220"
    echo   [!] Tạm thời dùng biểu tượng hệ thống Windows.
)

echo.
echo [*] BƯỚC 2: Đang tự động dò tìm trình duyệt web trên máy tính...

set "BROWSER_EXE="
set "BROWSER_NAME="

:: 1. Dò tìm Google Chrome
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles%\Google\Chrome\Application\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
) else if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
    set "BROWSER_EXE=%LocalAppData%\Google\Chrome\Application\chrome.exe"
    set "BROWSER_NAME=Google Chrome"
)

:: 2. Dò tìm Microsoft Edge (mặc định có sẵn 100% trên Win 10/11)
if not defined BROWSER_EXE (
    if exist "%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    ) else if exist "%ProgramFiles%\Microsoft\Edge\Application\msedge.exe" (
        set "BROWSER_EXE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    ) else if exist "%LocalAppData%\Microsoft\Edge\Application\msedge.exe" (
        set "BROWSER_EXE=%LocalAppData%\Microsoft\Edge\Application\msedge.exe"
        set "BROWSER_NAME=Microsoft Edge"
    )
)

:: 3. Dò tìm Cốc Cốc (rất phổ biến tại cơ quan)
if not defined BROWSER_EXE (
    if exist "%LocalAppData%\CocCoc\Browser\Application\browser.exe" (
        set "BROWSER_EXE=%LocalAppData%\CocCoc\Browser\Application\browser.exe"
        set "BROWSER_NAME=Cốc Cốc"
    ) else if exist "%ProgramFiles%\CocCoc\Browser\Application\browser.exe" (
        set "BROWSER_EXE=%ProgramFiles%\CocCoc\Browser\Application\browser.exe"
        set "BROWSER_NAME=Cốc Cốc"
    )
)

:: 4. Dò tìm bằng lệnh where nếu cài ở ổ đĩa khác (D:\, E:\)
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
    for /f "delims=" %%i in ('where browser.exe 2^>nul') do (
        set "BROWSER_EXE=%%i"
        set "BROWSER_NAME=Cốc Cốc"
    )
)

:: Dự phòng trình duyệt mặc định
if not defined BROWSER_EXE (
    set "BROWSER_EXE=%SystemRoot%\explorer.exe"
    set "BROWSER_NAME=Trình duyệt mặc định hệ thống"
)

echo   [OK] Đã chọn trình duyệt chuyên dụng: %BROWSER_NAME%

echo.
echo [*] BƯỚC 3: Đang cài đặt Lối tắt "Family CN23" ra Màn hình Desktop...

set "TARGET_URL=https://quando610.github.io/vpdk-cn23/index.html"

:: Tạo script VBScript trung gian để tạo Shortcut (chuẩn 100%, không phụ thuộc PowerShell)
set "VBS_SCRIPT=%TEMP%\make_family23_%RANDOM%.vbs"

> "%VBS_SCRIPT%" echo Set ws = CreateObject("WScript.Shell")
>> "%VBS_SCRIPT%" echo Set fso = CreateObject("Scripting.FileSystemObject")
>> "%VBS_SCRIPT%" echo targetExe = "%BROWSER_EXE%"
>> "%VBS_SCRIPT%" echo targetUrl = "%TARGET_URL%"
>> "%VBS_SCRIPT%" echo iconFile  = "%ICON_FILE%"
>> "%VBS_SCRIPT%" echo createdCount = 0
>> "%VBS_SCRIPT%" echo Sub MakeLnk(fPath)
>> "%VBS_SCRIPT%" echo   On Error Resume Next
>> "%VBS_SCRIPT%" echo   If fso.FolderExists(fPath) Then
>> "%VBS_SCRIPT%" echo     lnkPath = fso.BuildPath(fPath, "Family CN23.lnk")
>> "%VBS_SCRIPT%" echo     Set s = ws.CreateShortcut(lnkPath)
>> "%VBS_SCRIPT%" echo     s.TargetPath = targetExe
>> "%VBS_SCRIPT%" echo     s.Arguments = targetUrl
>> "%VBS_SCRIPT%" echo     s.IconLocation = iconFile
>> "%VBS_SCRIPT%" echo     s.Description = "Family CN23 - Cổng Dịch Vụ Nội Bộ Chi Nhánh 23"
>> "%VBS_SCRIPT%" echo     s.WorkingDirectory = fso.GetParentFolderName(targetExe)
>> "%VBS_SCRIPT%" echo     s.Save
>> "%VBS_SCRIPT%" echo     If fso.FileExists(lnkPath) Then
>> "%VBS_SCRIPT%" echo       WScript.Echo "   -> Da tao tai: " ^& lnkPath
>> "%VBS_SCRIPT%" echo       createdCount = createdCount + 1
>> "%VBS_SCRIPT%" echo     End If
>> "%VBS_SCRIPT%" echo     ' Xoa loi tat cu tranh trung lap
>> "%VBS_SCRIPT%" echo     old1 = fso.BuildPath(fPath, "Cổng Dịch Vụ - Chi Nhánh 23.lnk")
>> "%VBS_SCRIPT%" echo     old2 = fso.BuildPath(fPath, "Cổng Dịch Vụ - Chi Nhánh 23.url")
>> "%VBS_SCRIPT%" echo     old3 = fso.BuildPath(fPath, "Cong Dich Vu - Chi Nhanh 23.url")
>> "%VBS_SCRIPT%" echo     old4 = fso.BuildPath(fPath, "Family CN23.url")
>> "%VBS_SCRIPT%" echo     If fso.FileExists(old1) Then fso.DeleteFile old1, True
>> "%VBS_SCRIPT%" echo     If fso.FileExists(old2) Then fso.DeleteFile old2, True
>> "%VBS_SCRIPT%" echo     If fso.FileExists(old3) Then fso.DeleteFile old3, True
>> "%VBS_SCRIPT%" echo     If fso.FileExists(old4) Then fso.DeleteFile old4, True
>> "%VBS_SCRIPT%" echo   End If
>> "%VBS_SCRIPT%" echo End Sub
>> "%VBS_SCRIPT%" echo ' 1. Desktop theo Windows SpecialFolders
>> "%VBS_SCRIPT%" echo MakeLnk ws.SpecialFolders("Desktop")
>> "%VBS_SCRIPT%" echo ' 2. Desktop theo UserProfile
>> "%VBS_SCRIPT%" echo MakeLnk ws.ExpandEnvironmentStrings("%USERPROFILE%\Desktop")
>> "%VBS_SCRIPT%" echo ' 3. Desktop theo OneDrive Backup (neu co)
>> "%VBS_SCRIPT%" echo MakeLnk ws.ExpandEnvironmentStrings("%USERPROFILE%\OneDrive\Desktop")

:: Thực thi VBScript
cscript //nologo "%VBS_SCRIPT%"
del /f /q "%VBS_SCRIPT%" 2>nul

:: Cập nhật ngay bộ nhớ đệm Icon của Windows Explorer để hiển thị hình Pikachu ngay lập tức
ie4uinit.exe -show 2>nul

echo.
echo ===============================================================================
echo  [V] HOÀN TẤT THÀNH CÔNG!
echo      - Biểu tượng Pikachu Kính Vuông "Family CN23" đã xuất hiện trên Desktop.
echo      - Cố định mở chuyên dụng qua: %BROWSER_NAME%.
echo ===============================================================================
echo.
echo [*] Đang tự động mở Family CN23 lần đầu bằng %BROWSER_NAME%...
start "" "%BROWSER_EXE%" "%TARGET_URL%"

echo.
echo -------------------------------------------------------------------------------
echo  HƯỚNG DẪN DÀNH CHO CÁN BỘ:
echo  1. Hằng ngày vào làm việc, chỉ cần bấm đúp vào biểu tượng Pikachu
echo     mang tên "Family CN23" ngay trên màn hình Desktop.
echo  2. Đăng nhập bằng Số CCCD (12 số) và Mật khẩu được cấp.
echo -------------------------------------------------------------------------------
echo.
echo Nhấn phím bất kỳ để đóng cửa sổ này...
popd
pause >nul
exit /b

:: ===============================================================================
:: SUBROUTINE: GIẢI MÃ DỮ LIỆU ICON PIKACHU NHÚNG SẴN (OFFLINE RECOVERY)
:: ===============================================================================
:ExtractEmbeddedIcon
set "OUT_B64=%~1"
(
echo [EMBEDDED_B64_PLACEHOLDER]
) > "%OUT_B64%"
exit /b
"""

    # Replace placeholder with actual cert base64 lines
    # For neat bat syntax, echo each line
    echo_lines = []
    echo_lines.append("echo -----BEGIN CERTIFICATE-----")
    for line in b64_lines:
        echo_lines.append(f"echo {line}")
    echo_lines.append("echo -----END CERTIFICATE-----")
    embedded_block = "\r\n".join(echo_lines)

    full_bat = bat_script.replace("echo [EMBEDDED_B64_PLACEHOLDER]", embedded_block)

    # Save bat file with UTF-8 BOM for cmd.exe
    bat_path = "A_THANG/Cai_Dat_Family_CN23.bat"
    with open(bat_path, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(full_bat)
    print("1. Wrote A_THANG/Cai_Dat_Family_CN23.bat successfully!")

    # Also keep Tao_Icon_Desktop_VPDK23.bat identical
    with open("A_THANG/Tao_Icon_Desktop_VPDK23.bat", "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(full_bat)
    print("2. Wrote A_THANG/Tao_Icon_Desktop_VPDK23.bat successfully!")

    # 3. Create HUONG_DAN.txt
    guide_text = """================================================================================
HƯỚNG DẪN CÀI ĐẶT PHÍM TẮT "FAMILY CN23" (PIKACHU KÍNH VUÔNG)
================================================================================

Bước 1: Bấm đúp chuột (Double-click) vào file:
        👉 Cai_Dat_Family_CN23.bat

Bước 2: Chờ 2 giây để chương trình tự động tạo biểu tượng ngoài màn hình Desktop.

Bước 3: Xong! Màn hình Desktop của bạn sẽ xuất hiện biểu tượng Pikachu mang tên:
        ⭐ Family CN23

* Ghi chú quan trọng:
- Bạn có thể tải và chạy file này ở bất kỳ đâu (Downloads, ổ C, D, E, USB...).
- Chương trình tự động nhận diện màn hình Desktop và trình duyệt Chrome/Edge của bạn.
- Sau khi cài đặt xong, bạn có thể xóa hoặc di chuyển thư mục này đi nơi khác mà không bao giờ bị mất icon ngoài Desktop!
================================================================================
"""
    with open("A_THANG/HUONG_DAN.txt", "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(guide_text)

    # 4. PACKAGE ZIP ARCHIVE WITH ENCLOSING FOLDER "Family_CN23"
    # User's explicit rule: "lúc giải nén nên giải nén ra folder chứ đừng ra hết cái ruột nhé"
    folder_prefix = "Family_CN23"
    files_to_pack = [
        ("A_THANG/Cai_Dat_Family_CN23.bat", f"{folder_prefix}/Cai_Dat_Family_CN23.bat"),
        ("A_THANG/HUONG_DAN.txt", f"{folder_prefix}/HUONG_DAN.txt"),
        ("A_THANG/pikachu_badge.ico", f"{folder_prefix}/pikachu_badge.ico"),
        ("A_THANG/pikachu_badge_preview.png", f"{folder_prefix}/pikachu_badge_preview.png"),
        ("A_THANG/pikachu.ico", f"{folder_prefix}/pikachu.ico"),
        ("A_THANG/pikachu_preview.png", f"{folder_prefix}/pikachu_preview.png"),
        ("A_THANG/vpdk23.ico", f"{folder_prefix}/vpdk23.ico"),
        ("A_THANG/Tao_Icon_Desktop_VPDK23.bat", f"{folder_prefix}/Tao_Icon_Desktop_VPDK23.bat"),
    ]

    for zname in ["Family_CN23_Desktop.zip", "Tao_Icon_Desktop_VPDK23.zip"]:
        zip_path = os.path.join("A_THANG", zname)
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for src, arc in files_to_pack:
                z.write(src, arcname=arc)
        print(f"3. Packaged {zip_path} with enclosing folder '{folder_prefix}/' ({os.path.getsize(zip_path):,} bytes)")

if __name__ == "__main__":
    generate_family_cn23_installer()
