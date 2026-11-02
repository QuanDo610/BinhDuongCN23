# Verify bat script structure and contents
script = """@echo off
:: ======================================================================
:: CÔNG CỤ TẠO PHÍM TẮT TRUY CẬP CỔNG DỊCH VỤ - CHI NHÁNH SỐ 23
:: ======================================================================
chcp 65001 >nul
title Cài đặt Phím tắt Cổng Dịch Vụ - Chi Nhánh 23
color 0B

echo.
echo ===============================================================================
echo       CỔNG DỊCH VỤ NỘI BỘ - VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI CHI NHÁNH SỐ 23
echo               (Hệ thống Lịch Tuần & Đăng ký IT Helpdesk)
echo ===============================================================================
echo.
echo [*] Dang tao bieu tuong truy cap tren Man hinh Desktop...
echo.

:: 1. Tạo shortcut qua PowerShell để hỗ trợ chuẩn Unicode tiếng Việt và tự nhận diện Desktop / OneDrive Desktop
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ws = New-Object -ComObject WScript.Shell; ^
   $desktop = [Environment]::GetFolderPath('Desktop'); ^
   $name = 'Cổng Dịch Vụ - Chi Nhánh 23.url'; ^
   $path = Join-Path $desktop $name; ^
   $content = \"[InternetShortcut]`r`nURL=https://quando610.github.io/vpdk-cn23/index.html`r`nIconFile=$env:SystemRoot\System32\shell32.dll`r`nIconIndex=14`r`n\"; ^
   [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8); ^
   Write-Host '   -> Da tao bieu tuong: ' $path -ForegroundColor Green; ^
   if (Test-Path \"$env:USERPROFILE\Desktop\") { ^
       $p2 = Join-Path \"$env:USERPROFILE\Desktop\" $name; ^
       if ($p2 -ne $path) { [System.IO.File]::WriteAllText($p2, $content, [System.Text.Encoding]::UTF8); } ^
   } ^
   if (Test-Path \"$env:USERPROFILE\OneDrive\Desktop\") { ^
       $p3 = Join-Path \"$env:USERPROFILE\OneDrive\Desktop\" $name; ^
       if ($p3 -ne $path) { [System.IO.File]::WriteAllText($p3, $content, [System.Text.Encoding]::UTF8); } ^
   }"

:: 2. Dự phòng bằng lệnh Batch thuần (nếu máy tính chặn PowerShell)
if not exist "%USERPROFILE%\Desktop\Cổng Dịch Vụ - Chi Nhánh 23.url" (
    (
        echo [InternetShortcut]
        echo URL=https://quando610.github.io/vpdk-cn23/index.html
        echo IconFile=%SystemRoot%\System32\shell32.dll
        echo IconIndex=14
    ) > "%USERPROFILE%\Desktop\Cong Dich Vu - Chi Nhanh 23.url"
)
if exist "%USERPROFILE%\OneDrive\Desktop" (
    if not exist "%USERPROFILE%\OneDrive\Desktop\Cổng Dịch Vụ - Chi Nhánh 23.url" (
        (
            echo [InternetShortcut]
            echo URL=https://quando610.github.io/vpdk-cn23/index.html
            echo IconFile=%SystemRoot%\System32\shell32.dll
            echo IconIndex=14
        ) > "%USERPROFILE%\OneDrive\Desktop\Cong Dich Vu - Chi Nhanh 23.url"
    )
)

echo.
echo [V] HOÀN TẤT! Đã tạo thành công biểu tượng ngoài màn hình Desktop.
echo.
echo [*] Đang tự động mở Cổng dịch vụ lần đầu trên trình duyệt...
start https://quando610.github.io/vpdk-cn23/index.html
echo.
echo ===============================================================================
echo  Mỗi lần sử dụng, cán bộ chỉ cần bấm đúp vào biểu tượng trên Desktop là xong.
echo ===============================================================================
echo.
pause
"""
print("Length of script:", len(script))
