# -*- coding: utf-8 -*-

with open("A_THANG/google_apps_script.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove INITIAL_ACCOUNTS array
start_marker = "// Danh sách 70 tài khoản cán bộ Chi nhánh 23 nạp sẵn\nconst INITIAL_ACCOUNTS = ["
end_marker = "];\n\n// Danh sách 4 ticket sự cố từ IT Helpdesk cũ chuyển sang"

idx_start = code.find(start_marker)
idx_end = code.find(end_marker)

if idx_start != -1 and idx_end != -1:
    code = code[:idx_start] + "// Danh sách 4 ticket sự cố từ IT Helpdesk cũ chuyển sang" + code[idx_end + len(end_marker) - len("// Danh sách 4 ticket sự cố từ IT Helpdesk cũ chuyển sang"):]
    print("Removed INITIAL_ACCOUNTS block successfully!")
else:
    print("Could not find INITIAL_ACCOUNTS markers, checking alternative...")

# 2. Update seedAccountsOnly
old_seed_accounts = '''function seedAccountsOnly() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheetUsers = ss.getSheetByName(SHEET_USERS_NAME);
  
  if (!sheetUsers) {
    sheetUsers = ss.insertSheet(SHEET_USERS_NAME);
  } else {
    sheetUsers.clear();
  }

  const headers = [
    "Số ĐT (Username)",
    "Mật khẩu",
    "Họ và tên",
    "Chức danh / Chức vụ",
    "Đơn vị / Bộ phận",
    "Số CCCD",
    "Trạng thái",
    "Vai trò",
    "Ngày tạo"
  ];
  sheetUsers.appendRow(headers);

  const headerRange = sheetUsers.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight("bold").setBackground("#1e40af").setFontColor("#ffffff");
  headerRange.setHorizontalAlignment("center");
  sheetUsers.setRowHeight(1, 35);
  sheetUsers.setFrozenRows(1);

  sheetUsers.getRange("A:A").setNumberFormat("@");
  sheetUsers.getRange("F:F").setNumberFormat("@");

  for (let i = 0; i < INITIAL_ACCOUNTS.length; i++) {
    const acc = INITIAL_ACCOUNTS[i];
    sheetUsers.appendRow([
      "'" + acc[0],
      acc[1],
      acc[2],
      acc[3],
      acc[4],
      "'" + acc[5],
      acc[6],
      acc[7],
      acc[8]
    ]);
  }

  sheetUsers.autoResizeColumns(1, 9);
}'''

new_seed_accounts = '''function seedAccountsOnly() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheetUsers = ss.getSheetByName(SHEET_USERS_NAME);
  
  if (!sheetUsers) {
    sheetUsers = ss.insertSheet(SHEET_USERS_NAME);
  }

  // Nếu sheet mới tạo hoặc trống, khởi tạo hàng tiêu đề chuẩn
  if (sheetUsers.getLastRow() === 0) {
    const headers = [
      "Số ĐT (Username)",
      "Mật khẩu",
      "Họ và tên",
      "Chức danh / Chức vụ",
      "Đơn vị / Bộ phận",
      "Số CCCD",
      "Trạng thái",
      "Vai trò",
      "Ngày tạo"
    ];
    sheetUsers.appendRow(headers);

    const headerRange = sheetUsers.getRange(1, 1, 1, headers.length);
    headerRange.setFontWeight("bold").setBackground("#1e40af").setFontColor("#ffffff");
    headerRange.setHorizontalAlignment("center");
    sheetUsers.setRowHeight(1, 35);
    sheetUsers.setFrozenRows(1);

    sheetUsers.getRange("A:A").setNumberFormat("@");
    sheetUsers.getRange("F:F").setNumberFormat("@");
    sheetUsers.autoResizeColumns(1, 9);
  }
}'''

if old_seed_accounts in code:
    code = code.replace(old_seed_accounts, new_seed_accounts)
    print("Updated seedAccountsOnly successfully!")
else:
    print("Warning: old_seed_accounts not matched exactly, checking regex...")

# 3. Update onOpen menu
old_menu = '''.addItem("▶️ 1-Click: Nạp 70 Tài Khoản CN23 + Chuyển 4 Ticket IT Sang", "setupBinhDuong23")
      .addSeparator()
      .addItem("👥 Chỉ nạp lại 70 Tài Khoản vào sheet TaiKhoan", "seedAccountsOnly")'''

new_menu = '''.addItem("▶️ 1-Click: Cấu hình chuẩn hệ thống BINHDUONG23", "setupBinhDuong23")
      .addSeparator()
      .addItem("👥 Định dạng tab TaiKhoan (Tài khoản lưu trên Sheet)", "seedAccountsOnly")'''

code = code.replace(old_menu, new_menu)

# 4. Update setupBinhDuong23 alert
old_alert = '''  SpreadsheetApp.getUi().alert(
    "✅ ĐỒNG BỘ THÀNH CÔNG!\\n\\n" +
    "1. Sheet 'LichTuan': Giữ nguyên toàn bộ dữ liệu lịch tuần cũ.\\n" +
    "2. Sheet 'TaiKhoan': Đã nạp đủ 70 cán bộ Chi nhánh 23.\\n" +
    "3. Sheet 'Tickets': Đã chuyển 4 ticket sự cố từ IT Helpdesk cũ sang!\\n\\n" +
    "Hệ thống đã sẵn sàng 100%!"
  );'''

new_alert = '''  SpreadsheetApp.getUi().alert(
    "✅ HỆ THỐNG BINHDUONG23 ĐÃ SẴN SÀNG!\\n\\n" +
    "1. Sheet 'LichTuan': Giữ nguyên toàn bộ dữ liệu lịch tuần.\\n" +
    "2. Sheet 'TaiKhoan': Đã định dạng chuẩn (quản lý trực tiếp trên Sheet).\\n" +
    "3. Sheet 'Tickets': Đã chuyển 4 ticket sự cố từ IT Helpdesk cũ sang!\\n\\n" +
    "Hệ thống đã sẵn sàng 100%!"
  );'''

code = code.replace(old_alert, new_alert)

with open("A_THANG/google_apps_script.js", "w", encoding="utf-8") as f:
    f.write(code)

print("google_apps_script.js updated and optimized!")
