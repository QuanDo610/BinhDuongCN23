var document = { addEventListener: function(){}, getElementById: function(){ return {}; } };

    // Link kết nối trực tiếp đến Google Apps Script & Google Sheet
    const DEFAULT_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxLjARkYWp2TegCCdMcfVc3W6qQm6PmhFz71-y8zB_xFXxXbRXpsUhk6aPbJtqVqUHE/exec";
    
    // Toast Notification
    function showToast(message, type = "info") {
      const container = document.getElementById("toastContainer");
      if (!container) return;
      const toast = document.createElement("div");
      toast.className = `toast toast-${type}`;
      toast.innerHTML = `<span class="toast-icon">${type === "success" ? "✓" : (type === "error" ? "✗" : "ℹ")}</span><span class="toast-message">${message}</span>`;
      container.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => toast.remove(), 300);
      }, 4000);
    }

    // Toggle Password Visibility
    const btnToggle = document.getElementById("btnToggleLoginPassword");
    const passInput = document.getElementById("loginPassword");
    if (btnToggle && passInput) {
      btnToggle.addEventListener("click", () => {
        const isPass = passInput.type === "password";
        passInput.type = isPass ? "text" : "password";
        btnToggle.innerHTML = isPass ? '<i class="fa-regular fa-eye-slash"></i>' : '<i class="fa-regular fa-eye"></i>';
      });
    }

    // Forgot Password
    const btnForgot = document.getElementById("btnForgotPassword");
    if (btnForgot) {
      btnForgot.addEventListener("click", () => {
        alert("THÔNG BÁO QUÊN MẬT KHẨU:\n\nVui lòng liên hệ Tổ Hành chính - Tổng hợp (Đ/c Tuyền - SĐT: 0909736435) hoặc Quản trị viên để được cấp lại mật khẩu đăng nhập.");
      });
    }

    // Cập nhật ngày hôm nay
    function updateCurrentDate() {
      const now = new Date();
      const days = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];
      const dd = String(now.getDate()).padStart(2, "0");
      const mm = String(now.getMonth() + 1).padStart(2, "0");
      const yyyy = now.getFullYear();
      const el = document.getElementById("hubCurrentDate");
      if (el) el.textContent = `${days[now.getDay()]}, ${dd}/${mm}/${yyyy}`;
    }

    // Hiển thị giao diện Hub
    function showHub(user) {
      document.getElementById("loginSection").style.display = "none";
      document.getElementById("portalHubSection").style.display = "block";
      document.getElementById("headerUserArea").style.display = "flex";

      const name = user.fullname || user.ho_ten || user.name || "Cán bộ";
      const cccd = user.cccd || "";
      const phone = user.phone || user.so_dien_thoai || "";
      const role = user.position || user.chuc_vu || "Cán bộ";

      document.getElementById("displayUserName").textContent = name;
      document.getElementById("displayUserRole").textContent = role;
      document.getElementById("hubGreetingName").textContent = name;
      document.getElementById("hubUserRole").innerHTML = `Chức vụ: <strong>${role}</strong>`;
      const cccdEl = document.getElementById("hubUserCccd");
      if (cccdEl) {
        let displayStr = cccd;
        if (phone) displayStr += ` • SĐT: ${phone}`;
        cccdEl.innerHTML = `CCCD: <strong>${displayStr || "Đã xác thực"}</strong>`;
      }
      updateCurrentDate();
    }

    // Hiển thị giao diện Đăng nhập
    function showLogin() {
      document.getElementById("loginSection").style.display = "block";
      document.getElementById("portalHubSection").style.display = "none";
      document.getElementById("headerUserArea").style.display = "none";
    }

    // Kiểm tra phiên đăng nhập: Mở mới luôn yêu cầu đăng nhập, chỉ duy trì trong cùng phiên sessionStorage
    function checkSession() {
      // Dọn dẹp dứt điểm các key rác cũ từ phiên bản thử nghiệm trước (tránh auto-login ngoài ý muốn)
      localStorage.removeItem("vpdk_current_user");
      sessionStorage.removeItem("vpdk_current_user");
      localStorage.removeItem("binhduong_user");

      // Khôi phục số CCCD đã ghi nhớ (nếu có) để người dùng đỡ phải gõ lại
      const rememberedCccd = localStorage.getItem("vpdk_remembered_cccd");
      const cccdInput = document.getElementById("loginCccd");
      if (rememberedCccd && cccdInput) {
        cccdInput.value = rememberedCccd;
      }

      // Chỉ duy trì đăng nhập nếu người dùng đang trong cùng một phiên duyệt web (sessionStorage)
      const raw = sessionStorage.getItem("binhduong_user");
      if (raw) {
        try {
          const user = JSON.parse(raw);
          showHub(user);
          return true;
        } catch (e) {
          sessionStorage.removeItem("binhduong_user");
        }
      }

      // Mặc định khi mở mới: Luôn luôn hiển thị màn hình ĐĂNG NHẬP để cán bộ nhập Mật khẩu
      showLogin();
      return false;
    }

    // Xử lý Đăng xuất
    const btnLogout = document.getElementById("btnLogout");
    if (btnLogout) {
      btnLogout.addEventListener("click", () => {
        sessionStorage.removeItem("binhduong_user");
        sessionStorage.removeItem("vpdk_current_user");
        localStorage.removeItem("binhduong_user");
        localStorage.removeItem("vpdk_current_user");
        showToast("Đã đăng xuất khỏi hệ thống thành công.", "info");
        showLogin();
      });
    }

    // XỬ LÝ ĐĂNG NHẬP BẰNG CCCD: LUÔN KIỂM TRA TRỰC TIẾP TỪ GOOGLE SHEET THEO THỜI GIAN THỰC
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        let cccd = (document.getElementById("loginCccd").value || "").trim().replace(/[\s\.\-]+/g, "").replace(/^'+/, "");
        const password = (document.getElementById("loginPassword").value || "").trim();
        const remember = document.getElementById("rememberMe").checked;

        if (!cccd || !password) {
          showToast("Vui lòng nhập đầy đủ Số CCCD và Mật khẩu!", "error");
          return;
        }

        const btnLogin = document.getElementById("btnLogin");
        btnLogin.disabled = true;
        btnLogin.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Đang xác thực...';

        let result = null;

        // 1. Gửi trực tiếp lên máy chủ qua POST
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
              alert(`❌ CẢNH BÁO TRUY CẬP:\n\nCán bộ ${u.fullname} đã được ghi nhận trạng thái ĐÃ NGHỈ LÀM VIỆC trên hệ thống nội bộ.\nTài khoản đã bị vô hiệu hóa.`);
              return;
            }

            const userObj = {
              fullname: u.fullname || ("Cán bộ " + (u.cccd || cccd)),
              name: u.fullname || ("Cán bộ " + (u.cccd || cccd)),
              cccd: u.cccd || cccd,
              phone: u.phone || "",
              email: u.email || u.cccd || cccd,
              position: u.position || "Cán bộ",
              department: u.department || "Chi nhánh số 23",
              role: u.role || "user",
              status: u.status || "Đang làm việc"
            };

            // Ghi nhớ số CCCD nếu người dùng tích chọn
            if (remember) {
              localStorage.setItem("vpdk_remembered_cccd", userObj.cccd || cccd);
            } else {
              localStorage.removeItem("vpdk_remembered_cccd");
            }

            // Phiên làm việc chỉ lưu trong sessionStorage để bảo mật, đóng trình duyệt là hết phiên
            sessionStorage.setItem("binhduong_user", JSON.stringify(userObj));
            sessionStorage.setItem("vpdk_current_user", JSON.stringify(userObj));
            localStorage.removeItem("binhduong_user");
            localStorage.removeItem("vpdk_current_user");

            showHub(userObj);
            return;
          } else {
            if (result.isRetired) {
              alert(`❌ CẢNH BÁO TRUY CẬP:\n\n${result.message}`);
            } else {
              showToast(result.message || "Số CCCD hoặc Mật khẩu không chính xác!", "error");
            }
            return;
          }
        } else {
          // Lỗi mất kết nối Internet hoàn toàn
          showToast("Không thể kết nối đến máy chủ hệ thống! Vui lòng kiểm tra lại đường truyền mạng.", "error");
        }
      });
    }

    // Khởi chạy khi load trang
    document.addEventListener("DOMContentLoaded", () => {
      checkSession();
    });
  