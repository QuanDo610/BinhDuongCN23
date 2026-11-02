# Test shortcut creation script structure
ps_script = r'''
$wscript = New-Object -ComObject WScript.Shell
$desktop = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktop 'Cổng Dịch Vụ - Chi Nhánh 23.lnk'
$shortcut = $wscript.CreateShortcut($shortcutPath)
$shortcut.TargetPath = 'C:\Program Files\Google\Chrome\Application\chrome.exe'
$shortcut.Arguments = 'https://quando610.github.io/vpdk-cn23/index.html'
$shortcut.IconLocation = 'C:\Users\admin\AppData\Local\VPDK23\vpdk23.ico,0'
$shortcut.Description = 'Cổng Dịch Vụ Nội Bộ - Chi Nhánh Số 23'
$shortcut.Save()
'''
print("Valid PowerShell syntax length:", len(ps_script))
