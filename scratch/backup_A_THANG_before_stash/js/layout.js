/**
 * =========================================================================
 * LAYOUT.JS: QUẢN LÝ BỐ CỤC TOÀN HỆ THỐNG (FULL-WIDTH TOPBAR + COLLAPSIBLE SIDEBAR)
 * Hệ Thống Web Portal - Văn Phòng Đăng Ký Đất Đai Chi Nhánh Số 23
 * =========================================================================
 */

(function () {
  "use strict";

  // Danh mục 5 phân hệ cốt lõi + 1 Kho cài đặt
  const MENU_ITEMS = [
    { id: "hub", label: "Trang chủ", href: "index.html", icon: "fa-solid fa-house" },
    { id: "lich", label: "Đăng ký lịch tuần", href: "lich_tuan.html", icon: "fa-solid fa-calendar-week" },
    { id: "it", label: "IT Helpdesk", href: "it_helpdesk.html", icon: "fa-solid fa-headset" },
    { id: "giao-viec", label: "Giao việc", href: "giao_viec.html", icon: "fa-solid fa-list-check" },
    { id: "bao-cao", label: "Báo cáo số liệu", href: "bao_cao_to.html", icon: "fa-solid fa-chart-pie" }
  ];

  const UTILITY_ITEMS = [
    {
      id: "kho",
      label: "Kho cài đặt",
      href: "https://drive.google.com/drive/folders/1T2LVJKymM-52KBLNeabYxtAT4zfXneND",
      icon: "fa-solid fa-cloud-arrow-down",
      target: "_blank"
    }
  ];

  function initAppLayout() {
    if (document.getElementById("appTopbar") || document.getElementById("appSidebar")) return;

    // Đọc thông tin cán bộ đăng nhập
    let userName = "Cán bộ";
    let userRole = "Chi nhánh số 23";
    let hasSession = false;

    try {
      const storedUser = sessionStorage.getItem("currentUser") || 
                         sessionStorage.getItem("binhduong_user") || 
                         sessionStorage.getItem("vpdk_current_user") || 
                         sessionStorage.getItem("currentStaff");
      if (storedUser) {
        hasSession = true;
        const parsed = JSON.parse(storedUser);
        userName = parsed.fullname || parsed.name || parsed.ho_ten || parsed.username || "Cán bộ";
        userRole = parsed.position || parsed.department || parsed.role || "Chi nhánh 23";
        if (!sessionStorage.getItem("currentUser")) {
          sessionStorage.setItem("currentUser", JSON.stringify(parsed));
        }
      } else {
        const storedName = sessionStorage.getItem("userName") || localStorage.getItem("lastLoginFullName");
        if (storedName) {
          hasSession = true;
          userName = storedName;
        }
      }
    } catch (e) {
      console.warn("Lỗi đọc thông tin đăng nhập:", e);
    }

    const currentPath = window.location.pathname.split("/").pop() || "index.html";
    const isHubLogin = (currentPath === "index.html" || currentPath === "" || currentPath.endsWith("index.html")) && !hasSession;

    // Kích hoạt App Shell (nếu không phải màn hình đăng nhập ban đầu của Hub)
    if (!isHubLogin) {
      document.body.classList.add("has-app-shell");
      // Khôi phục trạng thái thu gọn từ localStorage
      const isCollapsedSaved = localStorage.getItem("sidebar_collapsed") === "true";
      const isDesktop = window.innerWidth >= 1024;
      if (isCollapsedSaved && isDesktop) {
        document.body.classList.add("sidebar-collapsed");
      }
    }

    // 1. TẠO THANH HEADER CỐ ĐỊNH CHẠY DÀI TRÊN CÙNG (FULL-WIDTH TOPBAR)
    const topbarElement = document.createElement("header");
    topbarElement.id = "appTopbar";
    topbarElement.className = "app-topbar";
    topbarElement.innerHTML = `
      <div class="topbar-left">
        <button type="button" id="btnToggleSidebar" class="topbar-toggle-btn" title="Thu gọn / Mở rộng menu" style="${isHubLogin ? 'display: none;' : ''}">
          <i class="fa-solid fa-bars"></i>
        </button>
        <a href="index.html" class="topbar-brand" title="Trang chủ Cổng Dịch Vụ - VPĐK Chi Nhánh 23">
          <div class="topbar-logo-box">
            <i class="fa-solid fa-landmark"></i>
          </div>
          <div class="topbar-titles">
            <span class="topbar-agency-name">VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI THÀNH PHỐ HỒ CHÍ MINH</span>
            <span class="topbar-sub-agency">CHI NHÁNH SỐ 23 &bull; CỔNG DỊCH VỤ CÔNG NỘI BỘ</span>
          </div>
        </a>
      </div>

      <div class="topbar-right" id="headerUserArea" style="${isHubLogin ? 'display: none;' : 'display: flex;'}">
        <div class="topbar-user-badge" id="topbarUserBadge" title="${userName} - ${userRole}">
          <div class="topbar-user-avatar">
            <i class="fa-solid fa-user-tie"></i>
          </div>
          <div class="topbar-user-text">
            <span class="topbar-user-name" id="displayUserName">${userName}</span>
            <span class="topbar-user-role" id="displayUserRole">${userRole}</span>
            <span id="displayUserEmail" style="display: none;"></span>
            <span id="headerUserName" style="display: none;">${userName}</span>
            <span id="headerUserRole" style="display: none;">${userRole}</span>
            <span id="itUserName" style="display: none;">${userName}</span>
          </div>
        </div>

        <button type="button" id="btnTopbarLogout" class="topbar-logout-btn" title="Đăng xuất khỏi hệ thống">
          <i class="fa-solid fa-arrow-right-from-bracket"></i>
          <span class="hidden sm:inline">Đăng xuất</span>
        </button>
      </div>
    `;

    // 2. TẠO THANH SIDEBAR NẰM DƯỚI HEADER
    const menuHtml = MENU_ITEMS.map((item) => {
      const isActive = currentPath === item.href || (item.id === "hub" && (currentPath === "" || currentPath === "index.html"));
      return `
        <li>
          <a href="${item.href}" class="sidebar-nav-item ${isActive ? 'active' : ''}" data-id="${item.id}" title="${item.label}">
            <div class="sidebar-nav-icon"><i class="${item.icon}"></i></div>
            <span class="sidebar-nav-label">${item.label}</span>
          </a>
        </li>
      `;
    }).join("");

    const utilityHtml = UTILITY_ITEMS.map((item) => {
      return `
        <li>
          <a href="${item.href}" target="${item.target || '_self'}" rel="noopener noreferrer" class="sidebar-nav-item" data-id="${item.id}" title="${item.label} (Google Drive)">
            <div class="sidebar-nav-icon"><i class="${item.icon}"></i></div>
            <span class="sidebar-nav-label">${item.label}</span>
          </a>
        </li>
      `;
    }).join("");

    const isCollapsedSaved = localStorage.getItem("sidebar_collapsed") === "true";
    const isDesktop = window.innerWidth >= 1024;

    const sidebarElement = document.createElement("aside");
    sidebarElement.id = "appSidebar";
    sidebarElement.className = `app-sidebar ${isCollapsedSaved && isDesktop ? 'collapsed' : ''}`;
    if (isHubLogin) {
      sidebarElement.style.display = "none";
    }
    sidebarElement.innerHTML = `
      <div class="sidebar-menu-wrapper">
        <div class="sidebar-group-title">Phân Hệ Làm Việc</div>
        <ul class="sidebar-nav-list">
          ${menuHtml}
        </ul>

        <div class="sidebar-group-title" style="margin-top: 14px;">Tiện Ích</div>
        <ul class="sidebar-nav-list">
          ${utilityHtml}
        </ul>
      </div>

      <div class="sidebar-footer">
        <span>Phiên bản v3.6</span>
        <span>Chi nhánh 23</span>
      </div>
    `;

    // Backdrop cho Mobile
    const backdropElement = document.createElement("div");
    backdropElement.id = "sidebarBackdrop";
    backdropElement.className = "sidebar-backdrop";

    // Chèn vào đầu body
    document.body.prepend(backdropElement);
    document.body.prepend(sidebarElement);
    document.body.prepend(topbarElement);

    // Xử lý nút 3 gạch `☰` Toggle
    const btnToggle = document.getElementById("btnToggleSidebar");
    if (btnToggle) {
      btnToggle.addEventListener("click", function (e) {
        e.preventDefault();
        if (window.innerWidth >= 1024) {
          // Desktop: Thu gọn / Mở rộng Sidebar
          const isCollapsed = sidebarElement.classList.toggle("collapsed");
          document.body.classList.toggle("sidebar-collapsed", isCollapsed);
          localStorage.setItem("sidebar_collapsed", isCollapsed ? "true" : "false");
        } else {
          // Mobile: Trượt mở / đóng Drawer
          sidebarElement.classList.toggle("sidebar-open");
          backdropElement.classList.toggle("active");
        }
      });
    }

    // Đóng drawer khi click backdrop trên mobile
    backdropElement.addEventListener("click", function () {
      sidebarElement.classList.remove("sidebar-open");
      backdropElement.classList.remove("active");
    });

    // Nút đăng xuất trên Header
    const btnLogout = document.getElementById("btnTopbarLogout");
    if (btnLogout) {
      btnLogout.addEventListener("click", function () {
        if (confirm("Đồng chí có chắc chắn muốn đăng xuất khỏi hệ thống?")) {
          sessionStorage.clear();
          localStorage.removeItem("loginRememberToken");
          window.location.href = "index.html";
        }
      });
    }
  }

  // Khởi chạy khi DOM sẵn sàng
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAppLayout);
  } else {
    initAppLayout();
  }

  // Xuất API toàn cục
  window.FamilyLayout = {
    updateUser: function (name, role) {
      const nameEl = document.getElementById("displayUserName");
      const roleEl = document.getElementById("displayUserRole");
      if (nameEl && name) nameEl.textContent = name;
      if (roleEl && role) roleEl.textContent = role;
    },
    showSession: function (user) {
      const sidebar = document.getElementById("appSidebar");
      const headerUserArea = document.getElementById("headerUserArea");
      const btnToggle = document.getElementById("btnToggleSidebar");
      if (sidebar) sidebar.style.display = "";
      if (headerUserArea) headerUserArea.style.display = "flex";
      if (btnToggle) btnToggle.style.display = "";
      document.body.classList.add("has-app-shell");
      if (user) {
        const name = user.fullname || user.name || user.ho_ten || user.username;
        const role = user.position || user.department || user.role;
        this.updateUser(name, role);
      }
    },
    hideSession: function () {
      const sidebar = document.getElementById("appSidebar");
      const headerUserArea = document.getElementById("headerUserArea");
      const btnToggle = document.getElementById("btnToggleSidebar");
      if (sidebar) sidebar.style.display = "none";
      if (headerUserArea) headerUserArea.style.display = "none";
      if (btnToggle) btnToggle.style.display = "none";
      document.body.classList.remove("has-app-shell");
    }
  };

  // Hỗ trợ tương thích ngược với code cũ gọi FamilySidebar
  window.FamilySidebar = window.FamilyLayout;
})();
