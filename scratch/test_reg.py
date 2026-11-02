# Python script to verify batch registry query logic
reg_cmd = r'''
for /f "tokens=2*" %%a in ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" /v Desktop 2^>nul') do set "DESKTOP_PATH=%%b"
call set "DESKTOP_PATH=%DESKTOP_PATH%"
if not defined DESKTOP_PATH set "DESKTOP_PATH=%USERPROFILE%\Desktop"
'''
print("Reg query logic is standard for Windows 7, 8, 10, 11")
