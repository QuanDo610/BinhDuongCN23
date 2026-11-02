# -*- coding: utf-8 -*-
import json, re

# =========================================================================
# 1. UPDATE A_THANG/google_apps_script.js
# =========================================================================
with open("A_THANG/google_apps_script.js", "r", encoding="utf-8") as f:
    gas_code = f.read()

# Update handleLogin to prioritize CCCD matching
new_handle_login = '''/**
 * Hàm xác thực Đăng nhập bằng CCCD và Mật khẩu trực tiếp từ Google Sheet
 * Hỗ trợ tạo user mới bên Sheet hoặc đổi mật khẩu bên Sheet sẽ có hiệu lực ngay lập tức
 */
function handleLogin(identifier, password, ss) {
  try {
    ss = ss || SpreadsheetApp.getActiveSpreadsheet();
    identifier = (identifier || "").toString().trim().replace(/[\\s\\.\\-]+/g, "").replace(/^'+/, "");
    password = (password || "").toString().trim();

    if (!identifier || !password) {
      return { success: false, message: "Vui lòng nhập đầy đủ Số CCCD và Mật khẩu!" };
    }

    // Chuẩn hóa CCCD (nếu bị mất số 0 ở đầu còn 11 số -> bù số 0)
    if (identifier.length === 11 && !identifier.startsWith("0")) identifier = "0" + identifier;

    const sheetUsers = getUsersSheet(ss);
    const data = sheetUsers.getDataRange().getDisplayValues();
    let matchedUser = null;
    let identifierFound = false;

    for (let i = 1; i < data.length; i++) {
      // Cột F (index 5) là Số CCCD
      let rowCccd = (data[i][5] || "").toString().trim().replace(/[\\s\\.\\-]+/g, "").replace(/^'+/, "");
      if (rowCccd.length === 11 && !rowCccd.startsWith("0")) rowCccd = "0" + rowCccd;

      // Cột A (index 0) là Số ĐT / Tên đăng nhập (dự phòng nếu người dùng nhập CCCD ở Cột A)
      let rowA = (data[i][0] || "").toString().trim().replace(/[\\s\\.\\-]+/g, "").replace(/^'+/, "");
      if (rowA.length === 11 && !rowA.startsWith("0")) rowA = "0" + rowA;

      const rowPass = (data[i][1] || "").toString().trim();

      // So khớp CCCD (Cột F) ưu tiên cao nhất, hoặc Cột A nếu điền CCCD ở Cột A
      const isMatch = (rowCccd && rowCccd.toLowerCase() === identifier.toLowerCase()) ||
                      (rowA && rowA.toLowerCase() === identifier.toLowerCase()) ||
                      (identifier.length >= 9 && rowCccd.replace(/^0+/, "") === identifier.replace(/^0+/, "")) ||
                      (identifier.length >= 9 && rowA.replace(/^0+/, "") === identifier.replace(/^0+/, ""));

      if (isMatch) {
        identifierFound = true;
        if (rowPass === password) {
          const cccdVal = rowCccd || identifier;
          const phoneVal = (rowA && rowA.length === 10 && rowA.startsWith("0")) ? rowA : (data[i][0] || "");
          const fullname = (data[i][2] || "").trim() || ("Cán bộ " + cccdVal);
          const position = (data[i][3] || "").trim() || "Cán bộ";
          const department = (data[i][4] || "").trim() || "Chi nhánh số 23";
          const status = (data[i][6] || "").trim() || "Đang làm việc";
          const role = (data[i][7] && data[i][7].toLowerCase().includes("admin")) ? "admin" : "user";

          matchedUser = {
            cccd: cccdVal,
            phone: phoneVal,
            fullname: fullname,
            position: position,
            department: department,
            status: status,
            role: role
          };
          break;
        }
      }
    }

    if (!identifierFound) {
      return {
        success: false,
        message: "Số CCCD này chưa được đăng ký trong danh sách trên Google Sheet!"
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
}'''

# Replace old handleLogin
old_hl_pattern = re.compile(r'/\*\*[\s\S]*?function handleLogin\(phone, password, ss\) \{[\s\S]*?return \{\s+success: true,\s+message: "Đăng nhập thành công!",\s+user: matchedUser\s+\};\s+\}\s+catch \(err\) \{[\s\S]*?\}\s+\}', re.MULTILINE)

gas_code = old_hl_pattern.sub(new_handle_login, gas_code)

# Update doGet and doPost parameter reading
gas_code = gas_code.replace(
    'const phone = (params.phone || params.username || params.email || "").toString();\n      const password = (params.password || "").toString();\n      return jsonResponse(handleLogin(phone, password, ss));',
    'const identifier = (params.cccd || params.username || params.phone || params.email || "").toString();\n      const password = (params.password || "").toString();\n      return jsonResponse(handleLogin(identifier, password, ss));'
)

gas_code = gas_code.replace(
    'const phone = (body.phone || body.username || body.email || "").toString();\n      const password = (body.password || "").toString();\n      return jsonResponse(handleLogin(phone, password, ss));',
    'const identifier = (body.cccd || body.username || body.phone || body.email || "").toString();\n      const password = (body.password || "").toString();\n      return jsonResponse(handleLogin(identifier, password, ss));'
)

with open("A_THANG/google_apps_script.js", "w", encoding="utf-8") as f:
    f.write(gas_code)
print("Updated A_THANG/google_apps_script.js for CCCD login!")


# =========================================================================
# 2. UPDATE A_THANG/index.html (CCCD Form & Logic)
# =========================================================================
with open("A_THANG/index.html", "r", encoding="utf-8") as f:
    idx_code = f.read()

# Replace Phone label and input with CCCD
old_phone_field = '''          <div class="form-group">
            <label for="loginPhone">Số điện thoại (Tên đăng nhập): <span class="required">*</span></label>
            <div class="password-input-group">
              <input type="tel" id="loginPhone" class="form-control" placeholder="Nhập số điện thoại cán bộ" required autocomplete="username">
            </div>
            <small class="field-hint">Nhập đúng số điện thoại đã được nạp trên Google Sheet</small>
          </div>'''

new_cccd_field = '''          <div class="form-group">
            <label for="loginCccd">Số CCCD (Căn cước công dân): <span class="required">*</span></label>
            <div class="password-input-group">
              <input type="text" id="loginCccd" class="form-control" placeholder="Nhập 12 số Căn cước công dân" required autocomplete="username" inputmode="numeric">
            </div>
            <small class="field-hint">Nhập đúng 12 chữ số CCCD (hoặc CMND) đã đăng ký trên Google Sheet</small>
          </div>'''

idx_code = idx_code.replace(old_phone_field, new_cccd_field)

# Replace Hub meta Phone with CCCD
old_hub_phone = '''            <div class="hub-hero-meta-item">
              <i class="fa-solid fa-phone"></i>
              <span id="hubUserPhone">SĐT: <strong>090xxxxxxx</strong></span>
            </div>'''

new_hub_cccd = '''            <div class="hub-hero-meta-item">
              <i class="fa-solid fa-id-card"></i>
              <span id="hubUserCccd">CCCD: <strong>074xxxxxxxxx</strong></span>
            </div>'''

idx_code = idx_code.replace(old_hub_phone, new_hub_cccd)

# Update showHub in JS
old_show_hub = '''      const name = user.fullname || user.ho_ten || user.name || "Cán bộ";
      const phone = user.phone || user.so_dien_thoai || "";
      const role = user.position || user.chuc_vu || "Cán bộ";

      document.getElementById("displayUserName").textContent = name;
      document.getElementById("displayUserRole").textContent = role;
      document.getElementById("hubGreetingName").textContent = name;
      document.getElementById("hubUserRole").innerHTML = `Chức vụ: <strong>${role}</strong>`;
      document.getElementById("hubUserPhone").innerHTML = `SĐT: <strong>${phone}</strong>`;'''

new_show_hub = '''      const name = user.fullname || user.ho_ten || user.name || "Cán bộ";
      const cccd = user.cccd || "";
      const role = user.position || user.chuc_vu || "Cán bộ";

      document.getElementById("displayUserName").textContent = name;
      document.getElementById("displayUserRole").textContent = cccd ? ("CCCD: " + cccd) : role;
      document.getElementById("hubGreetingName").textContent = name;
      document.getElementById("hubUserRole").innerHTML = `Chức vụ: <strong>${role}</strong>`;
      document.getElementById("hubUserCccd").innerHTML = `CCCD: <strong>${cccd || "---"}</strong>`;'''

idx_code = idx_code.replace(old_show_hub, new_show_hub)

# Update login submit logic to use CCCD
old_login_submit = '''    // XỬ LÝ ĐĂNG NHẬP: LUÔN KIỂM TRA TRỰC TIẾP TỪ GOOGLE SHEET THEO THỜI GIAN THỰC
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

        // 1. Gửi trực tiếp lên Google Sheet qua POST (text/plain để không bị CORS preflight)
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

new_login_submit = '''    // XỬ LÝ ĐĂNG NHẬP: BẰNG SỐ CCCD & MẬT KHẨU (KIỂM TRA TRỰC TIẾP TỪ GOOGLE SHEET)
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        let cccd = (document.getElementById("loginCccd").value || "").trim().replace(/[\\s\\.\\-]+/g, "").replace(/^'+/, "");
        const password = (document.getElementById("loginPassword").value || "").trim();
        const remember = document.getElementById("rememberMe").checked;

        if (!cccd || !password) {
          showToast("Vui lòng nhập đầy đủ Số CCCD và Mật khẩu!", "error");
          return;
        }

        if (cccd.length === 11 && !cccd.startsWith("0")) cccd = "0" + cccd;

        const btnLogin = document.getElementById("btnLogin");
        btnLogin.disabled = true;
        btnLogin.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Đang xác thực từ Google Sheet...';

        let result = null;

        // 1. Gửi trực tiếp lên Google Sheet qua POST (text/plain để không bị CORS preflight)
        try {
          const res = await fetch(DEFAULT_SCRIPT_URL, {
            method: "POST",
            headers: { "Content-Type": "text/plain;charset=utf-8" },
            body: JSON.stringify({ action: "login", cccd: cccd, username: cccd, password: password })
          });
          result = await res.json();
        } catch (postErr) {
          console.warn("POST error, fallback to GET:", postErr);
        }

        // 2. Dự phòng qua GET nếu POST bị mạng chặn
        if (!result) {
          try {
            const getUrl = `${DEFAULT_SCRIPT_URL}?action=login&cccd=${encodeURIComponent(cccd)}&username=${encodeURIComponent(cccd)}&password=${encodeURIComponent(password)}&t=${Date.now()}`;
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
              cccd: u.cccd || cccd,
              fullname: u.fullname || ("Cán bộ " + cccd),
              name: u.fullname || ("Cán bộ " + cccd),
              phone: u.phone || "",
              email: u.cccd || cccd,
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
              showToast(result.message || "Số CCCD hoặc Mật khẩu không chính xác!", "error");
            }
            return;
          }
        } else {
          // Lỗi mất kết nối Internet hoàn toàn
          showToast("Không thể kết nối đến máy chủ Google Sheet! Vui lòng kiểm tra lại đường truyền mạng.", "error");
        }
      });
    }'''

idx_code = idx_code.replace(old_login_submit, new_login_submit)

with open("A_THANG/index.html", "w", encoding="utf-8") as f:
    f.write(idx_code)
print("Updated A_THANG/index.html for CCCD login!")


# =========================================================================
# 3. UPDATE A_THANG/it_helpdesk.html
# =========================================================================
with open("A_THANG/it_helpdesk.html", "r", encoding="utf-8") as f:
    it_code = f.read()

# Update checkAuth in it_helpdesk.html to display CCCD
old_it_checkauth = '''        // Tự động gán Họ tên và SĐT vào form và hiển thị badge
        const fnVal = user.fullname || user.name || "Cán bộ";
        const phVal = user.phone || "";
        const fnInput = document.getElementById("fullname");
        if (fnInput) fnInput.value = fnVal;
        const phInput = document.getElementById("phone");
        if (phInput) phInput.value = phVal;

        const reqName = document.getElementById("requesterDisplayName");
        if (reqName) reqName.textContent = fnVal;
        const reqPhone = document.getElementById("requesterDisplayPhone");
        if (reqPhone) reqPhone.textContent = phVal;'''

new_it_checkauth = '''        // Tự động gán Họ tên, CCCD và SĐT vào form và hiển thị badge
        const fnVal = user.fullname || user.name || "Cán bộ";
        const cccdVal = user.cccd || "";
        const phVal = user.phone || "";
        const fnInput = document.getElementById("fullname");
        if (fnInput) fnInput.value = fnVal;
        const phInput = document.getElementById("phone");
        if (phInput) phInput.value = phVal || cccdVal;

        const reqName = document.getElementById("requesterDisplayName");
        if (reqName) reqName.textContent = fnVal;
        const reqPhone = document.getElementById("requesterDisplayPhone");
        if (reqPhone) reqPhone.textContent = cccdVal ? ("CCCD: " + cccdVal) : (phVal ? ("SĐT: " + phVal) : "");'''

it_code = it_code.replace(old_it_checkauth, new_it_checkauth)

with open("A_THANG/it_helpdesk.html", "w", encoding="utf-8") as f:
    f.write(it_code)
print("Updated A_THANG/it_helpdesk.html for CCCD display!")


# =========================================================================
# 4. UPDATE A_THANG/app.js (Lịch tuần)
# =========================================================================
with open("A_THANG/app.js", "r", encoding="utf-8") as f:
    app_code = f.read()

old_app_autologin = '''      currentUser = {
        email: u.email || u.phone || u.so_dien_thoai || "user",
        name: u.name || u.fullname || u.ho_ten || "Cán bộ",
        phone: u.phone || u.so_dien_thoai || "",
        department: u.department || u.don_vi || "Chi nhánh số 23",
        role: u.role || "user"
      };'''

new_app_autologin = '''      currentUser = {
        email: u.cccd || u.email || u.phone || u.so_dien_thoai || "user",
        name: u.name || u.fullname || u.ho_ten || "Cán bộ",
        cccd: u.cccd || "",
        phone: u.phone || u.so_dien_thoai || "",
        department: u.department || u.don_vi || "Chi nhánh số 23",
        role: u.role || "user"
      };'''

app_code = app_code.replace(old_app_autologin, new_app_autologin)

old_workspace_ui = '''  const displayName = getSenderDisplayName(currentUser);
  document.getElementById("displayUserName").textContent = displayName;
  document.getElementById("displayUserEmail").textContent = currentUser.email;'''

new_workspace_ui = '''  const displayName = getSenderDisplayName(currentUser);
  document.getElementById("displayUserName").textContent = displayName;
  document.getElementById("displayUserEmail").textContent = currentUser.cccd ? ("CCCD: " + currentUser.cccd) : currentUser.email;'''

app_code = app_code.replace(old_workspace_ui, new_workspace_ui)

with open("A_THANG/app.js", "w", encoding="utf-8") as f:
    f.write(app_code)
print("Updated A_THANG/app.js for CCCD display!")

