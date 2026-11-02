# -*- coding: utf-8 -*-
import json, re

# =========================================================================
# 1. UPDATE A_THANG/google_apps_script.js
# =========================================================================
with open("A_THANG/google_apps_script.js", "r", encoding="utf-8") as f:
    gas_code = f.read()

# 1.1 Add handleLogin function
handle_login_func = '''/**
 * Hàm xác thực Đăng nhập trực tiếp từ Google Sheet
 * Hỗ trợ tạo user mới bên Sheet hoặc đổi mật khẩu bên Sheet sẽ có hiệu lực ngay lập tức
 */
function handleLogin(phone, password, ss) {
  try {
    ss = ss || SpreadsheetApp.getActiveSpreadsheet();
    phone = (phone || "").toString().trim().replace(/[\\s\\.\\-]+/g, "").replace(/^'+/, "");
    password = (password || "").toString().trim();

    if (!phone || !password) {
      return { success: false, message: "Vui lòng nhập đầy đủ Số điện thoại và Mật khẩu!" };
    }

    if (phone.length === 9 && !phone.startsWith("0")) phone = "0" + phone;

    const sheetUsers = getUsersSheet(ss);
    const data = sheetUsers.getDataRange().getDisplayValues();
    let matchedUser = null;
    let phoneFound = false;

    for (let i = 1; i < data.length; i++) {
      let rowIdentifier = (data[i][0] || "").toString().trim().replace(/[\\s\\.\\-]+/g, "").replace(/^'+/, "");
      if (rowIdentifier.length === 9 && !rowIdentifier.startsWith("0")) rowIdentifier = "0" + rowIdentifier;
      const rowPass = (data[i][1] || "").toString().trim();

      if (rowIdentifier.toLowerCase() === phone.toLowerCase()) {
        phoneFound = true;
        if (rowPass === password) {
          const fullname = (data[i][2] || "").trim() || ("Cán bộ " + rowIdentifier);
          const position = (data[i][3] || "").trim() || "Cán bộ";
          const department = (data[i][4] || "").trim() || "Chi nhánh số 23";
          const cccd = (data[i][5] || "").replace(/^'+/, "").trim();
          const status = (data[i][6] || "").trim() || "Đang làm việc";
          const role = (data[i][7] && data[i][7].toLowerCase().includes("admin")) ? "admin" : "user";

          matchedUser = {
            phone: rowIdentifier,
            fullname: fullname,
            position: position,
            department: department,
            cccd: cccd,
            status: status,
            role: role
          };
          break;
        }
      }
    }

    if (!phoneFound) {
      return {
        success: false,
        message: "Số điện thoại này chưa được đăng ký trong danh sách trên Google Sheet!"
      };
    }

    if (!matchedUser) {
      return {
        success: false,
        message: "Mật khẩu không chính xác! Vui lòng kiểm tra lại."
      };
    }

    if (matchedUser.status === "Đã nghỉ") {
      return {
        success: false,
        isRetired: true,
        message: "Tài khoản cán bộ (" + matchedUser.fullname + ") đã được ghi nhận trạng thái ĐÃ NGHỈ LÀM VIỆC trên Google Sheet. Không thể đăng nhập!"
      };
    }

    return {
      success: true,
      message: "Đăng nhập thành công!",
      user: matchedUser
    };
  } catch (err) {
    return { success: false, message: "Lỗi kiểm tra tài khoản: " + err.toString() };
  }
}

'''

# Insert handleLogin before handleAddSchedule
if "function handleLogin(" not in gas_code:
    gas_code = gas_code.replace("function handleAddSchedule(data, ss) {", handle_login_func + "function handleAddSchedule(data, ss) {")

# 1.2 Update doGet to handle action === "login"
doget_login_target = '''    // 0. ĐỒNG BỘ 1-CLICK TỪ XA QUA API (SYNC ALL DATA)
    if (action === "syncAllData" || action === "seedSystem") {
      seedAccountsOnly();
      seedTicketsOnly();
      return jsonResponse({
        success: true,
        message: "Đã đồng bộ thành công 70 tài khoản CN23 và 4 tickets sự cố sang Google Sheet!",
        totalAccounts: 70,
        totalTickets: 4
      });
    }'''

doget_login_replacement = '''    // 0. ĐỒNG BỘ 1-CLICK TỪ XA QUA API (SYNC ALL DATA)
    if (action === "syncAllData" || action === "seedSystem") {
      seedAccountsOnly();
      seedTicketsOnly();
      return jsonResponse({
        success: true,
        message: "Đã đồng bộ thành công 70 tài khoản CN23 và 4 tickets sự cố sang Google Sheet!",
        totalAccounts: 70,
        totalTickets: 4
      });
    }

    // 0.1 XÁC THỰC ĐĂNG NHẬP TRỰC TIẾP TỪ GOOGLE SHEET (HỖ TRỢ GET)
    if (action === "login") {
      const phone = (params.phone || params.username || params.email || "").toString();
      const password = (params.password || "").toString();
      return jsonResponse(handleLogin(phone, password, ss));
    }'''

if 'if (action === "login") {' not in gas_code[:gas_code.find("function doPost")]:
    gas_code = gas_code.replace(doget_login_target, doget_login_replacement)

# 1.3 Update doPost to use handleLogin
dopost_login_pattern = re.compile(r'    // 1\. XÁC THỰC ĐĂNG NHẬP\s+if \(action === "login"\) \{[\s\S]*?return jsonResponse\(\{\s+success: true,\s+message: "Đăng nhập thành công!",\s+user: matchedUser\s+\}\);\s+\}', re.MULTILINE)

dopost_login_replacement = '''    // 1. XÁC THỰC ĐĂNG NHẬP TRỰC TIẾP TỪ GOOGLE SHEET (HỖ TRỢ POST)
    if (action === "login") {
      const phone = (body.phone || body.username || body.email || "").toString();
      const password = (body.password || "").toString();
      return jsonResponse(handleLogin(phone, password, ss));
    }'''

gas_code = dopost_login_pattern.sub(dopost_login_replacement, gas_code)

with open("A_THANG/google_apps_script.js", "w", encoding="utf-8") as f:
    f.write(gas_code)
print("Updated A_THANG/google_apps_script.js successfully!")


# =========================================================================
# 2. UPDATE A_THANG/style.css FOR VERTICAL (TRÊN DƯỚI) LOGIN HEADER
# =========================================================================
with open("A_THANG/style.css", "r", encoding="utf-8") as f:
    css_code = f.read()

login_css_target = '''/* ================= LOGIN VIEW ================= */
.login-card {
  max-width: 480px;
  margin: 50px auto;
  box-shadow: var(--shadow-lg);
}'''

login_css_replacement = '''/* ================= LOGIN VIEW ================= */
.login-card {
  max-width: 480px;
  margin: 50px auto;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
}

/* Đảm bảo Tiêu đề và Mô tả luôn xếp DỌC (TRÊN DƯỚI), tuyệt đối không bị chia 2 cột */
.login-card-header,
.login-card .card-header {
  padding: 28px 24px 20px 24px !important;
  background-color: #f8fafc !important;
  border-bottom: 1px solid #e2e8f0 !important;
  display: flex !important;
  flex-direction: column !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  gap: 8px !important;
  width: 100% !important;
}

.login-icon-box {
  font-size: 2.5rem;
  color: #1e40af;
  margin-bottom: 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.login-title,
.login-card .card-header h2 {
  margin: 0 !important;
  padding: 0 !important;
  font-size: 1.25rem !important;
  font-weight: 800 !important;
  color: #1e3a8a !important;
  letter-spacing: -0.01em !important;
  text-align: center !important;
  width: 100% !important;
  display: block !important;
  line-height: 1.4 !important;
}

.login-subtitle,
.login-card .card-header p {
  margin: 0 !important;
  padding: 0 !important;
  font-size: 0.9rem !important;
  color: #64748b !important;
  text-align: center !important;
  width: 100% !important;
  display: block !important;
  line-height: 1.4 !important;
}'''

css_code = css_code.replace(login_css_target, login_css_replacement)

with open("A_THANG/style.css", "w", encoding="utf-8") as f:
    f.write(css_code)
print("Updated A_THANG/style.css successfully!")


# =========================================================================
# 3. UPDATE A_THANG/index.html (HTML + LIVE SHEET LOGIN)
# =========================================================================
with open("A_THANG/index.html", "r", encoding="utf-8") as f:
    idx_code = f.read()

# 3.1 Replace login header HTML structure to use dedicated classes
header_old_html = '''    <section id="loginSection" class="card login-card">
      <div class="card-header text-center">
        <div style="font-size: 2.2rem; color: #1e40af; margin-bottom: 6px;">
          <i class="fa-solid fa-shield-halved"></i>
        </div>
        <h2>ĐĂNG NHẬP HỆ THỐNG NỘI BỘ</h2>
        <p class="text-muted">Cổng dịch vụ cán bộ - Chi nhánh số 23</p>
      </div>'''

header_new_html = '''    <section id="loginSection" class="card login-card">
      <div class="login-card-header">
        <div class="login-icon-box">
          <i class="fa-solid fa-shield-halved"></i>
        </div>
        <h2 class="login-title">ĐĂNG NHẬP HỆ THỐNG NỘI BỘ</h2>
        <p class="login-subtitle">Cổng dịch vụ cán bộ - Chi nhánh số 23</p>
      </div>'''

idx_code = idx_code.replace(header_old_html, header_new_html)

# 3.2 Update submit handler in index.html to ALWAYS verify live against Google Sheet
script_submit_pattern = re.compile(
    r'    // Xử lý Đăng nhập\s+const loginForm = document\.getElementById\("loginForm"\);[\s\S]*?btnLogin\.innerHTML = \'<i class="fa-solid fa-arrow-right-to-bracket mr-1"></i> <span class="btn-text">Đăng Nhập Vào Hệ Thống</span>\';\s+\}\s+\}\);\s+\}',
    re.MULTILINE
)

new_script_submit = '''    // Xử lý Đăng nhập: Luôn kiểm tra trực tiếp từ Google Sheet trong thời gian thực
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        let phone = (document.getElementById("loginPhone").value || "").trim().replace(/[\\s\\.\\-]+/g, "").replace(/^'+/, "");
        const password = (document.getElementById("loginPassword").value || "").trim();
        const remember = document.getElementById("rememberMe").checked;

        if (!phone || !password) {
          showToast("Vui lòng nhập đầy đủ Số điện thoại và Mật khẩu!", "error");
          return;
        }

        if (phone.length === 9 && !phone.startsWith("0")) phone = "0" + phone;

        const btnLogin = document.getElementById("btnLogin");
        btnLogin.disabled = true;
        btnLogin.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Đang xác thực từ Google Sheet...';

        let result = null;

        // 1. Gửi trực tiếp lên Google Sheet qua POST (CORS text/plain)
        try {
          const res = await fetch(DEFAULT_SCRIPT_URL, {
            method: "POST",
            headers: { "Content-Type": "text/plain;charset=utf-8" },
            body: JSON.stringify({ action: "login", phone: phone, password: password })
          });
          result = await res.json();
        } catch (postErr) {
          console.warn("POST error, fallback to GET:", postErr);
        }

        // 2. Dự phòng qua GET nếu POST bị mạng chặn
        if (!result) {
          try {
            const getUrl = `${DEFAULT_SCRIPT_URL}?action=login&phone=${encodeURIComponent(phone)}&password=${encodeURIComponent(password)}&t=${Date.now()}`;
            const resGet = await fetch(getUrl);
            result = await resGet.json();
          } catch (getErr) {
            console.warn("GET error:", getErr);
          }
        }

        btnLogin.disabled = false;
        btnLogin.innerHTML = '<i class="fa-solid fa-arrow-right-to-bracket mr-1"></i> <span class="btn-text">Đăng Nhập Vào Hệ Thống</span>';

        if (result) {
          if (result.success && result.user) {
            const u = result.user;
            if (u.status === "Đã nghỉ") {
              alert(`❌ CẢNH BÁO TRUY CẬP:\\n\\nCán bộ ${u.fullname} đã được ghi nhận trạng thái ĐÃ NGHỈ LÀM VIỆC trên Google Sheet.\\nTài khoản đã bị vô hiệu hóa.`);
              return;
            }

            const userObj = {
              fullname: u.fullname || ("Cán bộ " + phone),
              name: u.fullname || ("Cán bộ " + phone),
              phone: u.phone || phone,
              email: u.phone || phone,
              position: u.position || "Cán bộ",
              department: u.department || "Chi nhánh số 23",
              role: u.role || "user",
              status: u.status || "Đang làm việc"
            };

            if (remember) {
              localStorage.setItem("binhduong_user", JSON.stringify(userObj));
              localStorage.setItem("vpdk_current_user", JSON.stringify(userObj));
            } else {
              sessionStorage.setItem("binhduong_user", JSON.stringify(userObj));
              sessionStorage.setItem("vpdk_current_user", JSON.stringify(userObj));
            }

            showToast(`Xin chào ${userObj.fullname}! Đăng nhập thành công.`, "success");
            showHub(userObj);
            return;
          } else {
            if (result.isRetired) {
              alert(`❌ CẢNH BÁO TRUY CẬP:\\n\\n${result.message}`);
            } else {
              showToast(result.message || "Số điện thoại hoặc Mật khẩu không chính xác!", "error");
            }
            return;
          }
        } else {
          // Lỗi mất kết nối Internet hoàn toàn
          showToast("Không thể kết nối đến máy chủ Google Sheet! Vui lòng kiểm tra lại đường truyền mạng.", "error");
        }
      });
    }'''

idx_code = script_submit_pattern.sub(new_script_submit, idx_code)

with open("A_THANG/index.html", "w", encoding="utf-8") as f:
    f.write(idx_code)
print("Updated A_THANG/index.html successfully!")
