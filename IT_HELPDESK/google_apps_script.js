/**
 * =========================================================================
 * GOOGLE APPS SCRIPT: HỆ THỐNG IT HELPDESK & TIẾP NHẬN SỰ CỐ MÁY TÍNH
 * =========================================================================
 * Tính năng chính:
 * 1. Tiếp nhận Ticket từ Website gửi về (Họ tên, SĐT, Phòng ban, Tên máy tự động,
 *    Loại sự cố, Câu thông báo lỗi tiếng Anh, Mô tả chi tiết, IP & Thiết bị).
 * 2. Tự động tải ảnh chụp màn hình / ảnh lỗi lên Google Drive (Thư mục IT_Helpdesk_Uploads)
 *    và lưu đường dẫn xem ảnh vào Google Sheet.
 * 3. Tự động đánh mã Ticket (#TK-YYMMDD-XXX) và lưu thời gian chuẩn xác.
 * 4. Cung cấp API GET để Website hiển thị Bảng Monitoring thời gian thực cạnh bên Form.
 * 5. Cho phép IT trực tiếp sửa cột "Trạng thái" ("Chờ xử lý", "Đang xử lý", "Đã hoàn thành")
 *    và "Ghi chú IT" trên Google Sheet -> Website tự động cập nhật ngay!
 * =========================================================================
 */

const SHEET_NAME = "Tickets";
const DRIVE_FOLDER_NAME = "IT_Helpdesk_Uploads";

/**
 * Tự động tạo Sheet và định dạng cột chuẩn nếu chưa có
 */
function initSheet() {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  let sheet = ss.getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    // Xoá bớt sheet mặc định Sheet1 nếu trống
    const defaultSheet = ss.getSheetByName("Sheet1") || ss.getSheetByName("Trang tính1");
    if (defaultSheet && ss.getSheets().length > 1) {
      try { ss.deleteSheet(defaultSheet); } catch(e){}
    }

    const headers = [
      "Mã Ticket",              // 1
      "Thời gian gửi",          // 2
      "Họ và tên",              // 3
      "Số ĐT / Zalo",           // 4
      "Phòng ban",              // 5
      "Tên máy / Thiết bị",     // 6 (Tự động nhận diện)
      "Loại sự cố",             // 7
      "Thông báo lỗi (Tiếng Anh)", // 8 (Error message)
      "Mô tả hiện tượng",       // 9
      "Ảnh chụp lỗi (Link)",    // 10 (Google Drive link)
      "Trạng thái",             // 11 ("Chờ xử lý", "Đang xử lý", "Đã hoàn thành")
      "Ghi chú IT",             // 12
      "IP & Cấu hình máy"       // 13 (IP LAN/WAN, OS, RAM, CPU...)
    ];

    sheet.appendRow(headers);
    
    // Định dạng dòng tiêu đề
    const headerRange = sheet.getRange(1, 1, 1, headers.length);
    headerRange.setFontWeight("bold");
    headerRange.setBackground("#1e3a8a"); // Xanh than chuẩn VPĐK
    headerRange.setFontColor("#ffffff");
    headerRange.setHorizontalAlignment("center");
    headerRange.setVerticalAlignment("middle");
    sheet.setRowHeight(1, 38);
    sheet.setFrozenRows(1);

    // Căn chỉnh độ rộng các cột
    sheet.setColumnWidth(1, 130); // Mã Ticket
    sheet.setColumnWidth(2, 150); // Thời gian gửi
    sheet.setColumnWidth(3, 160); // Họ và tên
    sheet.setColumnWidth(4, 120); // Số ĐT
    sheet.setColumnWidth(5, 160); // Phòng ban
    sheet.setColumnWidth(6, 170); // Tên máy
    sheet.setColumnWidth(7, 140); // Loại sự cố
    sheet.setColumnWidth(8, 200); // Thông báo lỗi
    sheet.setColumnWidth(9, 280); // Mô tả
    sheet.setColumnWidth(10, 200); // Ảnh đính kèm
    sheet.setColumnWidth(11, 140); // Trạng thái
    sheet.setColumnWidth(12, 220); // Ghi chú IT
    sheet.setColumnWidth(13, 220); // IP & Cấu hình

    // Định dạng cột Số ĐT (Cột D) là Text thuần để không bao giờ bị mất số 0
    sheet.getRange("D:D").setNumberFormat("@");
  }
  return sheet;
}

/**
 * Xử lý lưu ảnh Base64 lên Google Drive
 */
function saveImageToDrive(base64Data, filename) {
  if (!base64Data || base64Data.trim() === "") return "";
  
  try {
    // 1. Tìm hoặc tạo thư mục trên Google Drive
    const folders = DriveApp.getFoldersByName(DRIVE_FOLDER_NAME);
    let folder;
    if (folders.hasNext()) {
      folder = folders.next();
    } else {
      folder = DriveApp.createFolder(DRIVE_FOLDER_NAME);
      folder.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    }

    // 2. Tách định dạng file và dữ liệu Base64
    let contentType = "image/jpeg";
    let base64String = base64Data;
    if (base64Data.indexOf("data:") === 0) {
      const parts = base64Data.split(",");
      const mimeMatch = parts[0].match(/:(.*?);/);
      if (mimeMatch) contentType = mimeMatch[1];
      base64String = parts[1];
    }

    const decodedBlob = Utilities.newBlob(
      Utilities.base64Decode(base64String),
      contentType,
      filename || ("ticket_img_" + new Date().getTime() + ".jpg")
    );

    // 3. Tạo file trên Drive và cấp quyền xem
    const file = folder.createFile(decodedBlob);
    try {
      file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    } catch (e) {}

    const fileId = file.getId();
    return `https://drive.google.com/file/d/${fileId}/view`;
  } catch (err) {
    return "Lỗi upload ảnh: " + err.toString();
  }
}

/**
 * Xử lý yêu cầu GET: Lấy danh sách Ticket hiển thị lên Web Monitoring
 */
function doGet(e) {
  try {
    const sheet = initSheet();
    const params = (e && e.parameter) ? e.parameter : {};
    const action = params.action || "getTickets";

    // Phục vụ fallback gửi GET nếu cần
    if (action === "createTicket" && params.data) {
      const ticketData = JSON.parse(decodeURIComponent(params.data));
      const result = createTicketRow(sheet, ticketData);
      return jsonResponse(result);
    }

    // Mặc định: Trả về danh sách Ticket (Lấy cả giá trị hiển thị và công thức để bóc tách URL)
    const dataRange = sheet.getDataRange();
    const values = dataRange.getDisplayValues();
    const formulas = dataRange.getFormulas();

    if (values.length <= 1) {
      return jsonResponse({ success: true, tickets: [] });
    }

    const tickets = [];
    for (let i = 1; i < values.length; i++) {
      const row = values[i];
      if (!row[0] && !row[2]) continue;

      // Xử lý link ảnh: Nếu là công thức HYPERLINK thì bóc tách URL thật ra
      let imgLink = row[9] || "";
      if (formulas[i] && formulas[i][9]) {
        const match = formulas[i][9].match(/=HYPERLINK\("([^"]+)"/i);
        if (match && match[1]) {
          imgLink = match[1];
        }
      }

      tickets.push({
        id: row[0],
        timestamp: row[1],
        fullname: row[2],
        phone: (row[3] || "").toString().replace(/^'+/, ""),
        department: row[4],
        machineName: row[5],
        category: row[6],
        errorMessage: row[7] || "",
        description: row[8] || "",
        imageUrl: imgLink,
        status: row[10] || "Chờ xử lý",
        itNote: row[11] || "",
        clientSpecs: row[12] || ""
      });
    }

    // Sắp xếp thứ tự ưu tiên: "Đang xử lý" (1) > "Chờ xử lý" (2) > "Đã hoàn thành" (3 - dưới cùng)
    // Trong mỗi nhóm: tự sort từ mới nhất tới cũ nhất
    function getStatusRank(status) {
      const s = (status || "").trim().toLowerCase();
      if (s.indexOf("đang") !== -1 || s.indexOf("progress") !== -1) return 1;
      if (s.indexOf("hoàn thành") !== -1 || s.indexOf("xong") !== -1 || s.indexOf("done") !== -1) return 3;
      return 2;
    }

    function parseTimeStr(ts) {
      if (!ts) return 0;
      const m = ts.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?/);
      if (m) {
        return new Date(m[3], m[2] - 1, m[1], m[4], m[5], m[6] || 0).getTime();
      }
      return 0;
    }

    tickets.sort(function(a, b) {
      const rankA = getStatusRank(a.status);
      const rankB = getStatusRank(b.status);
      if (rankA !== rankB) return rankA - rankB;
      return parseTimeStr(b.timestamp) - parseTimeStr(a.timestamp);
    });

    return jsonResponse({
      success: true,
      total: tickets.length,
      tickets: tickets
    });

  } catch (err) {
    return jsonResponse({ success: false, error: err.toString() });
  }
}

/**
 * Xử lý yêu cầu POST: Tiếp nhận Ticket mới (hỗ trợ upload ảnh Base64)
 */
function doPost(e) {
  try {
    const sheet = initSheet();
    let body = {};

    if (e.postData && e.postData.contents) {
      try {
        body = JSON.parse(e.postData.contents);
      } catch (parseErr) {
        body = e.parameter || {};
      }
    } else if (e.parameter) {
      body = e.parameter;
    }

    const result = createTicketRow(sheet, body);
    return jsonResponse(result);

  } catch (err) {
    return jsonResponse({ success: false, error: err.toString() });
  }
}

/**
 * Hàm thêm 1 dòng Ticket vào Sheet, sinh mã Ticket và xử lý lưu ảnh
 */
function createTicketRow(sheet, data) {
  const now = new Date();
  
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, '0');
  const dd = String(now.getDate()).padStart(2, '0');
  const hh = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  const sec = String(now.getSeconds()).padStart(2, '0');
  
  const timeStr = `${dd}/${mm}/${yyyy} ${hh}:${min}:${sec}`;
  const dateCode = `${String(yyyy).slice(2)}${mm}${dd}`;

  const lastRow = sheet.getLastRow();
  const nextSeq = lastRow > 1 ? lastRow : 1;
  const ticketId = `TK-${dateCode}-${String(nextSeq).padStart(3, '0')}`;

  // Xử lý upload ảnh nếu có
  let imageUrl = "";
  if (data.imageBase64) {
    const imgName = `${ticketId}_${dd}${mm}${yyyy}.jpg`;
    imageUrl = saveImageToDrive(data.imageBase64, imgName);
  }

  // Xử lý số điện thoại để luôn lưu dưới dạng VĂN BẢN (Text), không bao giờ bị mất số 0 trong Excel/Sheets
  let phoneStr = String(data.phone || "").trim();
  if (phoneStr) {
    phoneStr = phoneStr.replace(/^'+/, "");
    phoneStr = "'" + phoneStr;
  }

  const rowData = [
    ticketId,                                      // 1. Mã Ticket
    timeStr,                                       // 2. Thời gian gửi
    data.fullname || "Không tên",                  // 3. Họ và tên
    phoneStr,                                      // 4. Số ĐT / Zalo (dạng Text giữ nguyên số 0)
    data.department || "Khác",                     // 5. Phòng ban
    data.machineName || "Tự động (Chưa rõ)",       // 6. Tên máy / Mã thiết bị
    data.category || "Sự cố chung",                // 7. Loại sự cố
    data.errorMessage || "",                       // 8. Thông báo lỗi tiếng Anh
    data.description || "Không có mô tả",          // 9. Mô tả hiện tượng
    imageUrl,                                      // 10. Link ảnh Drive
    "Chờ xử lý",                                   // 11. Trạng thái mặc định
    "",                                            // 12. Ghi chú IT (để IT gõ trong Sheet)
    data.clientSpecs || (data.ip ? ("IP: " + data.ip) : "") // 13. IP & Cấu hình máy
  ];

  sheet.appendRow(rowData);
  
  const newRowIndex = sheet.getLastRow();
  // Căn giữa các cột Mã, Ngày, SĐT, Trạng thái & Định dạng SĐT là Plain Text
  sheet.getRange(newRowIndex, 1).setHorizontalAlignment("center").setFontWeight("bold");
  sheet.getRange(newRowIndex, 2).setHorizontalAlignment("center");
  sheet.getRange(newRowIndex, 4).setNumberFormat("@").setHorizontalAlignment("center");
  
  // Format ô Trạng thái ban đầu: Màu vàng cam (Chờ xử lý)
  const statusCell = sheet.getRange(newRowIndex, 11);
  statusCell.setValue("Chờ xử lý");
  statusCell.setHorizontalAlignment("center");
  statusCell.setFontWeight("bold");
  statusCell.setBackground("#fef3c7").setFontColor("#b45309");

  // Lưu link ảnh trực tiếp vào ô, Google Sheets sẽ tự hiển thị link bấm được
  if (imageUrl && imageUrl.indexOf("http") === 0) {
    const imgCell = sheet.getRange(newRowIndex, 10);
    imgCell.setValue(imageUrl);
    imgCell.setFontColor("#2563eb").setFontUnderline(true);
  }

  return {
    success: true,
    message: "Tạo ticket thành công",
    ticketId: ticketId,
    timestamp: timeStr,
    imageUrl: imageUrl
  };
}

/**
 * Trả về JSON Response chuẩn CORS
 */
function jsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
