# -*- coding: utf-8 -*-
import json, re

# 1. BUILD A_THANG/lich_tuan.html
with open("/tmp/orig_lich_tuan.html", "r", encoding="utf-8") as f:
    orig_html = f.read()

# Replace Header buttons and title
header_target = '''      <div class="header-action-box" id="headerUserArea" style="display: none;">
        <div class="user-badge">
          <span class="user-icon-svg-box">
            <svg class="user-avatar-svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </span>
          <div class="user-info-text">
            <strong id="displayUserName">Người dùng</strong>
            <small id="displayUserEmail">email@gmail.com</small>
          </div>
        </div>
        <button id="btnAdminServerConfig" class="btn btn-admin-config btn-sm" style="display: none;" title="Cài đặt Server API (Chỉ Quản trị viên)">⚙️ Cài đặt Server</button>
        <button id="btnLogout" class="btn btn-header-logout btn-sm">Đăng xuất</button>
      </div>'''

header_replacement = '''      <div class="header-action-box" id="headerUserArea" style="display: none;">
        <a href="index.html" class="nav-tab-btn" style="text-decoration: none;" title="Quay lại Cổng Dịch Vụ Hub">
          <i class="fa-solid fa-house"></i> <span>Cổng Dịch Vụ</span>
        </a>
        <a href="it_helpdesk.html" class="nav-tab-btn" style="text-decoration: none; background-color: #2563eb; border-color: #3b82f6;" title="Chuyển sang IT Helpdesk">
          <i class="fa-solid fa-headset"></i> <span>IT Helpdesk</span>
        </a>
        <div class="user-badge">
          <span class="user-icon-svg-box">
            <svg class="user-avatar-svg" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </span>
          <div class="user-info-text">
            <strong id="displayUserName">Người dùng</strong>
            <small id="displayUserEmail">email@gmail.com</small>
          </div>
        </div>
        <button id="btnAdminServerConfig" class="btn btn-admin-config btn-sm" style="display: none;" title="Cài đặt Server API (Chỉ Quản trị viên)">⚙️ Cài đặt Server</button>
        <button id="btnLogout" class="btn btn-header-logout btn-sm">
          <i class="fa-solid fa-arrow-right-to-bracket mr-1"></i> Đăng xuất
        </button>
      </div>'''

lich_tuan_html = orig_html.replace(header_target, header_replacement)

# Add FontAwesome in head
if "cdnjs.cloudflare.com/ajax/libs/font-awesome" not in lich_tuan_html:
    lich_tuan_html = lich_tuan_html.replace(
        '<link rel="stylesheet" href="style.css">',
        '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">\n  <link rel="stylesheet" href="style.css">'
    )

# Hide loginSection by default in lich_tuan.html
lich_tuan_html = lich_tuan_html.replace(
    '<section id="loginSection" class="card login-card">',
    '<section id="loginSection" class="card login-card" style="display: none;">'
)

with open("A_THANG/lich_tuan.html", "w", encoding="utf-8") as f:
    f.write(lich_tuan_html)
print("Created A_THANG/lich_tuan.html successfully!")


# 2. BUILD A_THANG/app.js
with open("/tmp/orig_app.js", "r", encoding="utf-8") as f:
    orig_app = f.read()

# Load 70 accounts to inject into KNOWN_USERS_MAP
with open("A_THANG/danh_sach_tai_khoan_cn23.json", "r", encoding="utf-8") as f:
    accounts = json.load(f)

users_map_injection = "const KNOWN_USERS_MAP = {\n"
for acc in accounts:
    p = (acc.get("so_dien_thoai") or "").strip().lstrip("'")
    if len(p) == 9 and not p.startswith("0"):
        p = "0" + p
    name = acc.get("ho_ten", "").strip()
    if p and name:
        users_map_injection += f'  "{p}": "{name}",\n'
users_map_injection += '''  "quan.vpdk@gmail.com": "Đỗ Trọng Minh Quân",
  "tuyen.vpdk@gmail.com": "Nguyễn Thị Bích Tuyền",
  "trangntt.vpdk@gmail.com": "Nguyễn Thị Thùy Trang",
  "thangnc.vpdk@gmail.com": "Nguyễn Chiến Thắng",
  "thang.vpdk@gmail.com": "Nguyễn Chiến Thắng",
  "nhanvien@gmail.com": "Nguyễn Văn An"
};'''

orig_map_target = '''const KNOWN_USERS_MAP = {
  "quan.vpdk@gmail.com": "Đỗ Trọng Minh Quân",
  "tuyen.vpdk@gmail.com": "Nguyễn Thị Bích Tuyền",
  "trangntt.vpdk@gmail.com": "Nguyễn Thị Thùy Trang",
  "thangnc.vpdk@gmail.com": "Nguyễn Chiến Thắng",
  "thang.vpdk@gmail.com": "Nguyễn Chiến Thắng",
  "nhanvien@gmail.com": "Nguyễn Văn An"
};'''

app_js = orig_app.replace(orig_map_target, users_map_injection)

# Update checkAutoLogin to check binhduong_user and redirect if not found
orig_check_auto_login = '''function checkAutoLogin() {
  const savedUser = localStorage.getItem(STORAGE_KEYS.CURRENT_USER) || sessionStorage.getItem(STORAGE_KEYS.CURRENT_USER);
  if (savedUser) {
    try {
      currentUser = JSON.parse(savedUser);
      showWorkspaceUI();
      loadScheduleList();
    } catch (e) {
      localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
    }
  }
}'''

new_check_auto_login = '''function checkAutoLogin() {
  const savedUser = localStorage.getItem(STORAGE_KEYS.CURRENT_USER) || sessionStorage.getItem(STORAGE_KEYS.CURRENT_USER) || localStorage.getItem("binhduong_user") || sessionStorage.getItem("binhduong_user");
  if (savedUser) {
    try {
      const u = JSON.parse(savedUser);
      currentUser = {
        email: u.email || u.phone || u.so_dien_thoai || "user",
        name: u.name || u.fullname || u.ho_ten || "Cán bộ",
        phone: u.phone || u.so_dien_thoai || "",
        department: u.department || u.don_vi || "Chi nhánh số 23",
        role: u.role || "user"
      };
      showWorkspaceUI();
      loadScheduleList();
      return;
    } catch (e) {
      localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
      localStorage.removeItem("binhduong_user");
    }
  }
  // Nếu chưa đăng nhập, tự động chuyển về Cổng Dịch Vụ
  window.location.href = "index.html";
}'''

app_js = app_js.replace(orig_check_auto_login, new_check_auto_login)

# Update handleLogout to redirect to index.html
orig_handle_logout = '''function handleLogout() {
  currentUser = null;
  localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
  sessionStorage.removeItem(STORAGE_KEYS.CURRENT_USER);

  document.getElementById("loginSection").style.display = "block";
  document.getElementById("appWorkspace").style.display = "none";
  document.getElementById("headerUserArea").style.display = "none";

  const btnAdminConfig = document.getElementById("btnAdminServerConfig");
  if (btnAdminConfig) btnAdminConfig.style.display = "none";

  showToast("Bạn đã đăng xuất khỏi hệ thống.", "info");
}'''

new_handle_logout = '''function handleLogout() {
  currentUser = null;
  localStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
  sessionStorage.removeItem(STORAGE_KEYS.CURRENT_USER);
  localStorage.removeItem("binhduong_user");
  sessionStorage.removeItem("binhduong_user");

  window.location.href = "index.html";
}'''

app_js = app_js.replace(orig_handle_logout, new_handle_logout)

with open("A_THANG/app.js", "w", encoding="utf-8") as f:
    f.write(app_js)
print("Updated A_THANG/app.js successfully!")


# 3. BUILD A_THANG/it_helpdesk.html
with open("IT_HELPDESK/index.html", "r", encoding="utf-8") as f:
    orig_it = f.read()

# Replace Header in IT_HELPDESK to add Navigation
it_header_target = '''      <!-- Quick Action: Kho Phần Mềm & Status Badge -->
      <div class="flex items-center space-x-2 shrink-0">
        <!-- Nút Kho Phần Mềm Cài Đặt -->
        <a href="https://drive.google.com/drive/folders/1T2LVJKymM-52KBLNeabYxtAT4zfXneND" target="_blank" rel="noopener noreferrer"
          class="flex items-center space-x-1.5 text-[11px] sm:text-xs bg-amber-400 hover:bg-amber-300 text-blue-950 font-bold px-2.5 sm:px-3 py-1.5 rounded-xl border border-amber-300 shadow-sm transition group">
          <i class="fa-solid fa-cloud-arrow-down text-xs sm:text-sm"></i>
          <span class="hidden sm:inline">Kho Phần Mềm Cài Đặt</span>
          <span class="inline sm:hidden">Kho Cài Đặt</span>
          <i class="fa-solid fa-arrow-up-right-from-square text-[9px] opacity-70 group-hover:translate-x-0.5 transition-transform"></i>
        </a>

        <div class="hidden md:flex items-center space-x-2 text-xs bg-white/10 px-3 py-1.5 rounded-xl border border-white/15">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span>Hệ thống: <strong class="text-white">Sẵn sàng</strong></span>
        </div>
      </div>'''

it_header_replacement = '''      <!-- Quick Action: Navigation & Kho Phần Mềm -->
      <div class="flex items-center space-x-2 shrink-0">
        <a href="index.html" class="flex items-center space-x-1.5 text-xs bg-white/10 hover:bg-white/20 text-white font-semibold px-2.5 sm:px-3 py-1.5 rounded-xl border border-white/20 transition shadow-sm">
          <i class="fa-solid fa-house"></i>
          <span class="hidden sm:inline">Cổng Dịch Vụ</span>
        </a>
        <a href="lich_tuan.html" class="flex items-center space-x-1.5 text-xs bg-blue-700 hover:bg-blue-600 text-white font-semibold px-2.5 sm:px-3 py-1.5 rounded-xl border border-blue-500 shadow-sm transition">
          <i class="fa-solid fa-calendar-week"></i>
          <span class="hidden sm:inline">Lịch Tuần</span>
        </a>
        <a href="https://drive.google.com/drive/folders/1T2LVJKymM-52KBLNeabYxtAT4zfXneND" target="_blank" rel="noopener noreferrer"
          class="flex items-center space-x-1.5 text-[11px] sm:text-xs bg-amber-400 hover:bg-amber-300 text-blue-950 font-bold px-2.5 sm:px-3 py-1.5 rounded-xl border border-amber-300 shadow-sm transition group">
          <i class="fa-solid fa-cloud-arrow-down text-xs sm:text-sm"></i>
          <span class="hidden sm:inline">Kho Phần Mềm</span>
          <i class="fa-solid fa-arrow-up-right-from-square text-[9px] opacity-70 group-hover:translate-x-0.5 transition-transform"></i>
        </a>
        <div id="itUserBadge" class="hidden sm:flex items-center space-x-1.5 bg-white/15 px-2.5 py-1.5 rounded-xl text-xs text-white border border-white/20">
          <i class="fa-solid fa-circle-user text-amber-300"></i>
          <span id="itUserName">Cán bộ</span>
        </div>
        <button onclick="handleLogout()" class="text-xs bg-red-600/80 hover:bg-red-500 text-white font-semibold px-2.5 sm:px-3 py-1.5 rounded-xl border border-red-400 transition" title="Đăng xuất">
          <i class="fa-solid fa-arrow-right-from-bracket mr-0.5"></i>
          <span class="hidden sm:inline">Đăng xuất</span>
        </button>
      </div>'''

it_html = orig_it.replace(it_header_target, it_header_replacement)

# Replace SCRIPT_URL with unified URL
old_script_url_line = 'const SCRIPT_URL = atob("aHR0cHM6Ly9zY3JpcHQuZ29vZ2xlLmNvbS9tYWNyb3Mvcy9BS2Z5Y2J6c2ZfOHJVSXFLUllwOU5Fcl9CQ3pYeTRXZTNoSldtekhzMGhQN2wxVWgyOFl2RS1JRHhXSmRtMWVtajZkVzRna0cvZXhlYw==");'
new_script_url_line = '''const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxLjARkYWp2TegCCdMcfVc3W6qQm6PmhFz71-y8zB_xFXxXbRXpsUhk6aPbJtqVqUHE/exec";

    // Kiểm tra xác thực cán bộ từ phiên đăng nhập
    function checkAuth() {
      const raw = localStorage.getItem("binhduong_user") || sessionStorage.getItem("binhduong_user") || localStorage.getItem("vpdk_current_user");
      if (!raw) {
        window.location.href = "index.html";
        return;
      }
      try {
        const user = JSON.parse(raw);
        const nameEl = document.getElementById("itUserName");
        if (nameEl) nameEl.textContent = user.fullname || user.name || "Cán bộ";
        const badgeEl = document.getElementById("itUserBadge");
        if (badgeEl) badgeEl.classList.remove("hidden");
        
        // Tự động điền Họ tên và SĐT vào form
        const fnInput = document.getElementById("fullname");
        if (fnInput && !fnInput.value) fnInput.value = user.fullname || user.name || "";
        const phInput = document.getElementById("phone");
        if (phInput && !phInput.value) phInput.value = user.phone || "";
        const deptSelect = document.getElementById("department");
        if (deptSelect && user.department) {
          for (let opt of deptSelect.options) {
            if (opt.value && (user.department.toLowerCase().includes(opt.value.toLowerCase()) || opt.value.toLowerCase().includes(user.department.toLowerCase()))) {
              deptSelect.value = opt.value;
              break;
            }
          }
        }
      } catch (e) {
        window.location.href = "index.html";
      }
    }

    function handleLogout() {
      localStorage.removeItem("binhduong_user");
      sessionStorage.removeItem("binhduong_user");
      localStorage.removeItem("vpdk_current_user");
      sessionStorage.removeItem("vpdk_current_user");
      window.location.href = "index.html";
    }'''

it_html = it_html.replace(old_script_url_line, new_script_url_line)

# Trigger checkAuth on init
it_html = it_html.replace(
    'document.addEventListener("DOMContentLoaded", () => {',
    'document.addEventListener("DOMContentLoaded", () => {\n      checkAuth();'
)

with open("A_THANG/it_helpdesk.html", "w", encoding="utf-8") as f:
    f.write(it_html)
print("Created A_THANG/it_helpdesk.html successfully!")
