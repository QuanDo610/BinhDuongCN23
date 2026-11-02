# -*- coding: utf-8 -*-

with open("A_THANG/google_apps_script.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Remove INITIAL_TICKETS block
start_marker = "// Danh sách 4 ticket sự cố từ IT Helpdesk cũ chuyển sang\nconst INITIAL_TICKETS = ["
end_marker = "];\n\n/**\n * Tự động tạo menu tiện ích"

idx_start = code.find(start_marker)
idx_end = code.find(end_marker)

if idx_start != -1 and idx_end != -1:
    code = code[:idx_start] + "/**\n * Tự động tạo menu tiện ích" + code[idx_end + len(end_marker) - len("/**\n * Tự động tạo menu tiện ích"):]
    print("Removed INITIAL_TICKETS block successfully!")
else:
    print("Marker not found, check indices:", idx_start, idx_end)

# 2. Update seedTicketsOnly to purely format headers without hardcoded tickets
old_seed_tickets = '''function seedTicketsOnly() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheetSupport = ss.getSheetByName(SHEET_SUPPORT_NAME) || ss.getSheetByName("DangKySupport");
  
  if (!sheetSupport) {
    sheetSupport = ss.insertSheet(SHEET_SUPPORT_NAME);
  } else {
    sheetSupport.clear();
  }

  const headers = [
    "Mã Ticket",
    "Thời gian gửi",
    "Họ và tên",
    "Số ĐT / Zalo",
    "Phòng ban",
    "Tên máy / Thiết bị",
    "Loại sự cố",
    "Thông báo lỗi (Tiếng Anh)",
    "Mô tả hiện tượng",
    "Ảnh chụp lỗi (Link)",
    "Trạng thái",
    "Ghi chú IT",
    "IP & Cấu hình máy"
  ];
  sheetSupport.appendRow(headers);
  const headerRange = sheetSupport.getRange(1, 1, 1, headers.length);
  headerRange.setFontWeight("bold").setBackground("#b45309").setFontColor("#ffffff");
  headerRange.setHorizontalAlignment("center");
  sheetSupport.setRowHeight(1, 35);
  sheetSupport.setFrozenRows(1);
  sheetSupport.getRange("D:D").setNumberFormat("@");

  // Nạp 4 tickets cũ
  for (let i = 0; i < INITIAL_TICKETS.length; i++) {
    const t = INITIAL_TICKETS[i];
    sheetSupport.appendRow([
      t[0],
      t[1],
      t[2],
      "'" + t[3],
      t[4],
      t[5],
      t[6],
      t[7],
      t[8],
      t[9],
      t[10],
      t[11],
      t[12]
    ]);

    const rIdx = sheetSupport.getLastRow();
    sheetSupport.getRange(rIdx, 1).setHorizontalAlignment("center").setFontWeight("bold");
    sheetSupport.getRange(rIdx, 2).setHorizontalAlignment("center");
    sheetSupport.getRange(rIdx, 4).setNumberFormat("@").setHorizontalAlignment("center");
  }

  sheetSupport.autoResizeColumns(1, 13);
}'''

new_seed_tickets = '''function seedTicketsOnly() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheetSupport = ss.getSheetByName(SHEET_SUPPORT_NAME) || ss.getSheetByName("DangKySupport");
  
  if (!sheetSupport) {
    sheetSupport = ss.insertSheet(SHEET_SUPPORT_NAME);
  }

  // Nếu sheet mới tạo hoặc trống, khởi tạo hàng tiêu đề chuẩn
  if (sheetSupport.getLastRow() === 0) {
    const headers = [
      "Mã Ticket",
      "Thời gian gửi",
      "Họ và tên",
      "Số ĐT / Zalo",
      "Phòng ban",
      "Tên máy / Thiết bị",
      "Loại sự cố",
      "Thông báo lỗi (Tiếng Anh)",
      "Mô tả hiện tượng",
      "Ảnh chụp lỗi (Link)",
      "Trạng thái",
      "Ghi chú IT",
      "IP & Cấu hình máy"
    ];
    sheetSupport.appendRow(headers);
    const headerRange = sheetSupport.getRange(1, 1, 1, headers.length);
    headerRange.setFontWeight("bold").setBackground("#b45309").setFontColor("#ffffff");
    headerRange.setHorizontalAlignment("center");
    sheetSupport.setRowHeight(1, 35);
    sheetSupport.setFrozenRows(1);
    sheetSupport.getRange("D:D").setNumberFormat("@");
    sheetSupport.autoResizeColumns(1, 13);
  }
}'''

if old_seed_tickets in code:
    code = code.replace(old_seed_tickets, new_seed_tickets)
    print("Updated seedTicketsOnly successfully!")
else:
    print("Warning: old_seed_tickets not matched exactly!")

# 3. Update menu in onOpen
code = code.replace(
    '.addItem("🎫 Chỉ chuyển các Ticket IT vào sheet Tickets", "seedTicketsOnly")',
    '.addItem("🎫 Định dạng tab Tickets (Sự cố IT lưu trên Sheet)", "seedTicketsOnly")'
)

# 4. Update setupBinhDuong23 alert
code = code.replace(
    '"3. Sheet \'Tickets\': Đã chuyển 4 ticket sự cố từ IT Helpdesk cũ sang!\\n\\n"',
    '"3. Sheet \'Tickets\': Đã định dạng chuẩn (quản lý trực tiếp trên Sheet).\\n\\n"'
)

with open("A_THANG/google_apps_script.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Finished remove_initial_tickets.py!")
