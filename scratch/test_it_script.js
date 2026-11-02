var document = { addEventListener: function(){} };

    // 1. KẾT NỐI SERVER APPS SCRIPT (Được mã hoá ngầm, không hiển thị trên giao diện)
    const SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxLjARkYWp2TegCCdMcfVc3W6qQm6PmhFz71-y8zB_xFXxXbRXpsUhk6aPbJtqVqUHE/exec";

    // Kiểm tra xác thực cán bộ từ phiên đăng nhập
    function checkAuth() {
      // Dọn dẹp key rác cũ nếu còn tồn tại
      localStorage.removeItem("vpdk_current_user");
      const raw = sessionStorage.getItem("binhduong_user") || sessionStorage.getItem("vpdk_current_user");
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
        
        // Tự động gán Họ tên và CCCD / SĐT vào form và hiển thị badge
        const fnVal = user.fullname || user.name || "Cán bộ";
        const cccdVal = user.cccd || "";
        const phVal = user.phone || "";
        const fnInput = document.getElementById("fullname");
        if (fnInput) fnInput.value = fnVal;
        const phInput = document.getElementById("phone");
        if (phInput) phInput.value = phVal || cccdVal;

        const reqName = document.getElementById("requesterDisplayName");
        if (reqName) reqName.textContent = fnVal;
        
        const reqCccd = document.getElementById("requesterDisplayCccd");
        if (reqCccd) {
          reqCccd.textContent = cccdVal ? `CCCD: ${cccdVal}` : "Đã xác thực";
        }

        const reqPhoneBadge = document.getElementById("requesterPhoneBadge");
        const reqPhone = document.getElementById("requesterDisplayPhone");
        if (reqPhone) {
          if (phVal && phVal.trim()) {
            reqPhone.textContent = phVal;
            if (reqPhoneBadge) reqPhoneBadge.classList.remove("hidden");
          } else {
            if (reqPhoneBadge) reqPhoneBadge.classList.add("hidden");
          }
        }
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
    }

    // Biến toàn cục lưu danh sách Ticket và thông tin máy
    let currentTickets = [];
    let detectedClient = {
      ip: 'Đang quét...',
      os: 'Windows',
      machineName: '',
      specs: '',
      imageBase64: ''
    };

    // Khởi chạy khi tải trang
    document.addEventListener("DOMContentLoaded", () => {
      checkAuth();
      autoDetectMachineAndSpecs();
      loadSavedUserInfo();
      setupPasteEventListener();
      setupDragAndDrop();
      fetchTickets();
    });

    // 2. TỰ ĐỘNG QUÉT TÊN MÁY, CẤU HÌNH, VÀ IP
    async function autoDetectMachineAndSpecs() {
      // (a) Tạo mã Machine ID cố định trong localStorage nếu chưa có
      let machineTag = localStorage.getItem("IT_LOCAL_MACHINE_TAG");
      if (!machineTag) {
        const hex = Math.floor(Math.random() * 0xFFFFFF).toString(16).toUpperCase().padStart(4, '0');
        machineTag = `PC-${hex}`;
        localStorage.setItem("IT_LOCAL_MACHINE_TAG", machineTag);
      }

      // (b) Nhận diện Hệ điều hành sơ bộ
      let os = "Windows";
      const ua = navigator.userAgent;
      if (ua.indexOf("Windows NT 10.0") !== -1) os = "Win 10/11";
      else if (ua.indexOf("Mac") !== -1) os = "macOS";
      else if (ua.indexOf("Linux") !== -1) os = "Linux";
      else if (ua.indexOf("Android") !== -1) os = "Android";
      else if (ua.indexOf("iPhone") !== -1 || ua.indexOf("iPad") !== -1) os = "iOS";

      detectedClient.os = os;

      // (c) Đọc thông số phần cứng nếu trình duyệt hỗ trợ
      const ram = navigator.deviceMemory ? `${navigator.deviceMemory}GB RAM` : '';
      const cores = navigator.hardwareConcurrency ? `${navigator.hardwareConcurrency} Cores` : '';
      const screenRes = `${window.screen.width}x${window.screen.height}`;
      const specsSummary = [os, ram, cores, screenRes].filter(Boolean).join(" • ");
      detectedClient.specs = specsSummary;

      // (d) Đặt tên máy tự động
      const autoName = `${os} (${machineTag})`;
      detectedClient.machineName = autoName;
      const machineInput = document.getElementById("machineName");
      if (!machineInput.value) {
        machineInput.value = autoName;
      }

      document.getElementById("detectedSpecText").textContent = `Máy: ${autoName} | ${specsSummary}`;

      // (e) Quét IP Public tự động qua ipify
      try {
        const res = await fetch("https://api.ipify.org?format=json");
        const data = await res.json();
        if (data && data.ip) {
          detectedClient.ip = data.ip;
          document.getElementById("detectedSpecText").textContent = `Máy: ${autoName} | IP: ${data.ip} (${specsSummary})`;
        }
      } catch (e) {
        detectedClient.ip = "LAN Nội Bộ";
      }
    }

    // 3. TỰ ĐỘNG NHỚ HỌ TÊN, SĐT, PHÒNG BAN TRÊN MÁY NÀY
    function loadSavedUserInfo() {
      try {
        const saved = JSON.parse(localStorage.getItem("IT_HELPDESK_USER_INFO") || "{}");
        if (saved.fullname) document.getElementById("fullname").value = saved.fullname;
        if (saved.phone) document.getElementById("phone").value = saved.phone;
        if (saved.department) document.getElementById("department").value = saved.department;
        if (saved.machineName) document.getElementById("machineName").value = saved.machineName;
      } catch(e){}
    }

    function saveUserInfoIfChecked() {
      if (document.getElementById("chkRememberMe").checked) {
        const info = {
          fullname: document.getElementById("fullname").value.trim(),
          phone: document.getElementById("phone").value.trim(),
          department: document.getElementById("department").value,
          machineName: document.getElementById("machineName").value.trim()
        };
        localStorage.setItem("IT_HELPDESK_USER_INFO", JSON.stringify(info));
      }
    }

    // 4. HỖ TRỢ DÁN ẢNH TRỰC TIẾP TỪ CLIPBOARD (CTRL + V)
    function setupPasteEventListener() {
      window.addEventListener("paste", (e) => {
        const items = (e.clipboardData || e.originalEvent.clipboardData)?.items;
        if (!items) return;
        for (let item of items) {
          if (item.type.indexOf("image") !== -1) {
            const file = item.getAsFile();
            if (file) {
              compressAndPreviewImage(file);
              break;
            }
          }
        }
      });
    }

    // Drag & Drop
    function setupDragAndDrop() {
      const dropZone = document.getElementById("dropZone");
      ["dragenter", "dragover"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropZone.classList.add("dragover");
        }, false);
      });
      ["dragleave", "drop"].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
          e.preventDefault();
          e.stopPropagation();
          dropZone.classList.remove("dragover");
        }, false);
      });
      dropZone.addEventListener("drop", (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files && files[0]) {
          compressAndPreviewImage(files[0]);
        }
      }, false);
    }

    function triggerFileInput() {
      document.getElementById("fileInput").click();
    }

    function handleFileSelect(e) {
      const file = e.target.files[0];
      if (file) compressAndPreviewImage(file);
    }

    // 5. NÉN ẢNH (CANVAS COMPRESSION) XUỐNG < 250KB ĐỂ UPLOAD SIÊU NHANH
    function compressAndPreviewImage(file) {
      if (!file.type.match("image.*")) {
        alert("Vui lòng chỉ chọn file ảnh (PNG, JPG, JPEG)!");
        return;
      }

      const reader = new FileReader();
      reader.onload = (readerEvent) => {
        const img = new Image();
        img.onload = () => {
          // Resize tối đa 1280px
          const maxDim = 1280;
          let width = img.width;
          let height = img.height;

          if (width > height && width > maxDim) {
            height = Math.round((height * maxDim) / width);
            width = maxDim;
          } else if (height > maxDim) {
            width = Math.round((width * maxDim) / height);
            height = maxDim;
          }

          const canvas = document.createElement("canvas");
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0, width, height);

          // Nén dạng JPEG 0.75 chất lượng cao nhưng dung lượng siêu nhẹ
          const compressedDataUrl = canvas.toDataURL("image/jpeg", 0.75);
          detectedClient.imageBase64 = compressedDataUrl;

          // Hiển thị Preview
          document.getElementById("dropZonePrompt").classList.add("hidden");
          const previewContainer = document.getElementById("imagePreviewContainer");
          previewContainer.classList.remove("hidden");
          document.getElementById("imagePreview").src = compressedDataUrl;
          
          const sizeKb = Math.round((compressedDataUrl.length * 3 / 4) / 1024);
          document.getElementById("imageSizeInfo").textContent = `Ảnh đã nén: ~${sizeKb} KB (Sẵn sàng gửi)`;
        };
        img.src = readerEvent.target.result;
      };
      reader.readAsDataURL(file);
    }

    function removeSelectedImage(e) {
      if (e) e.stopPropagation();
      detectedClient.imageBase64 = "";
      document.getElementById("fileInput").value = "";
      document.getElementById("imagePreviewContainer").classList.add("hidden");
      document.getElementById("dropZonePrompt").classList.remove("hidden");
    }

    // 6. XỬ LÝ GỬI TICKET
    async function handleSubmitTicket(e) {
      e.preventDefault();

      const btn = document.getElementById("btnSubmitTicket");
      const originalHtml = btn.innerHTML;
      btn.disabled = true;
      btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin mr-1.5"></i> Đang tải lên và gửi...`;

      const selectedCategory = document.querySelector('input[name="category"]:checked')?.value || "Máy tính / PC";
      const machineVal = document.getElementById("machineName").value.trim() || detectedClient.machineName;

      const payload = {
        fullname: document.getElementById("fullname").value.trim(),
        phone: document.getElementById("phone").value.trim(),
        department: document.getElementById("department").value,
        machineName: machineVal,
        category: selectedCategory,
        errorMessage: document.getElementById("errorMessage").value.trim(),
        description: document.getElementById("description").value.trim(),
        imageBase64: detectedClient.imageBase64, // Gửi ảnh Base64
        ip: detectedClient.ip,
        clientSpecs: `IP: ${detectedClient.ip} | ${detectedClient.specs}`
      };

      saveUserInfoIfChecked();

      // Sinh mã tạm đẹp
      const now = new Date();
      const dCode = `${String(now.getFullYear()).slice(2)}${String(now.getMonth()+1).padStart(2,'0')}${String(now.getDate()).padStart(2,'0')}`;
      const tempId = `TK-${dCode}-${Math.floor(100 + Math.random() * 900)}`;
      const timeStr = `${String(now.getHours()).padStart(2,'0')}:${String(now.getMinutes()).padStart(2,'0')} - ${String(now.getDate()).padStart(2,'0')}/${String(now.getMonth()+1).padStart(2,'0')}`;

      // Gửi lên Google Sheet
      if (SCRIPT_URL && SCRIPT_URL.trim() !== "") {
        try {
          await fetch(SCRIPT_URL, {
            method: "POST",
            mode: "no-cors",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
        } catch (err) {
          console.warn("Lỗi gửi POST, chuyển thử GET fallback:", err);
          try {
            // Nếu không gửi được ảnh qua GET vì dài thì chỉ gửi text
            const clonePayload = Object.assign({}, payload);
            delete clonePayload.imageBase64;
            await fetch(`${SCRIPT_URL}?action=createTicket&data=${encodeURIComponent(JSON.stringify(clonePayload))}`, { mode: "no-cors" });
          } catch(e2){}
        }
      }

      // Cập nhật ngay vào danh sách hiển thị
      currentTickets.unshift({
        id: tempId,
        timestamp: timeStr,
        fullname: payload.fullname,
        phone: payload.phone,
        department: payload.department,
        machineName: payload.machineName,
        category: payload.category,
        errorMessage: payload.errorMessage,
        description: payload.description,
        imageUrl: detectedClient.imageBase64, // Xem ảnh trực tiếp từ bộ nhớ
        status: "Chờ xử lý",
        itNote: "",
        clientSpecs: payload.clientSpecs
      });

      // Lưu cache local nếu ở chế độ demo
      if (!SCRIPT_URL) {
        localStorage.setItem("IT_HELPDESK_LOCAL_TICKETS", JSON.stringify(currentTickets));
      }

      // Xoá trắng các ô sự cố & ảnh
      document.getElementById("errorMessage").value = "";
      document.getElementById("description").value = "";
      removeSelectedImage();

      // Khôi phục nút
      btn.disabled = false;
      btn.innerHTML = originalHtml;

      // Cập nhật bảng
      updateStats();
      renderTickets();

      // Hiện popup thành công
      document.getElementById("resTicketId").textContent = `#${tempId}`;
      document.getElementById("resMachine").textContent = payload.machineName;
      document.getElementById("modalSuccess").classList.remove("hidden");
    }

    // 7. LẤY DỮ LIỆU TICKET TỪ GOOGLE SHEET
    async function fetchTickets(isManual = false) {
      const refreshIcon = document.getElementById("refreshIcon");
      if (refreshIcon) refreshIcon.classList.add("fa-spin");

      if (SCRIPT_URL && SCRIPT_URL.trim() !== "") {
        try {
          const res = await fetch(`${SCRIPT_URL}?action=getTickets&t=${new Date().getTime()}`);
          const data = await res.json();
          if (data && data.success && Array.isArray(data.tickets)) {
            currentTickets = data.tickets;
          }
        } catch (err) {
          loadDemoTickets();
        }
      } else {
        loadDemoTickets();
      }

      if (refreshIcon) refreshIcon.classList.remove("fa-spin");
      updateStats();
      renderTickets();
    }

    function loadDemoTickets() {
      const saved = localStorage.getItem("IT_HELPDESK_LOCAL_TICKETS");
      if (saved) {
        try { currentTickets = JSON.parse(saved); return; } catch(e){}
      }
      currentTickets = [
        {
          id: "TK-261026-003",
          timestamp: "26/10/2026 08:35:10",
          fullname: "Nguyễn Thị Mai",
          phone: "0908.123.456",
          department: "Tổ Kế hoạch - Tài chính",
          machineName: "Win 10/11 (PC-48A2) - Bàn 02",
          category: "Máy in / Scan",
          errorMessage: "Paper Jam inside tray 2",
          description: "Máy in kẹt giấy, đã kéo khay ra nhưng đèn báo đỏ vẫn nhấp nháy liên tục.",
          imageUrl: "",
          status: "Chờ xử lý",
          itNote: "",
          clientSpecs: "IP: 14.161.xx.xx | Win 10/11 • 8GB RAM"
        },
        {
          id: "TK-261026-002",
          timestamp: "26/10/2026 08:12:05",
          fullname: "Trần Văn Bình",
          phone: "0912.345.678",
          department: "Tổ Đăng ký và Cấp GCN",
          machineName: "Win 10/11 (PC-91F0) - Bàn 05",
          category: "Chữ ký số / Cổng DVC",
          errorMessage: "Cannot find valid certificate in token",
          description: "Cắm USB Token ký số văn bản nhưng hệ thống báo lỗi không tìm thấy chứng thư.",
          imageUrl: "",
          status: "Đang xử lý",
          itNote: "Đang cài lại driver VNPT Token",
          clientSpecs: "IP: 14.161.xx.xx | Win 10/11 • 16GB RAM"
        },
        {
          id: "TK-261026-001",
          timestamp: "26/10/2026 07:50:22",
          fullname: "Lê Hoàng Nam",
          phone: "Ext 101",
          department: "Bộ phận Một Cửa",
          machineName: "Win 10/11 (PC-1A3C) - Quầy 01",
          category: "Mạng Internet / Wifi",
          errorMessage: "No Internet Access (Yellow Exclamation)",
          description: "Mất mạng dây, không kết nối được vào máy chủ chia sẻ tài liệu Z:.",
          imageUrl: "",
          status: "Đã hoàn thành",
          itNote: "Đã bấm lại đầu hạt mạng RJ45",
          clientSpecs: "IP: 14.161.xx.xx | Win 10/11 • 8GB RAM"
        }
      ];
    }

    // Helper xác định thứ tự ưu tiên trạng thái: Đang xử lý (1) > Chờ xử lý (2) > Đã hoàn thành (3 - dưới cùng)
    function getStatusRank(status) {
      const s = (status || "").trim().toLowerCase();
      if (s.includes("đang") || s.includes("progress")) return 1;
      if (s.includes("hoàn thành") || s.includes("xong") || s.includes("done")) return 3;
      return 2; // Chờ xử lý hoặc trạng thái khác
    }

    // Helper phân tích thời gian để sort từ mới nhất đến cũ nhất
    function parseTicketTime(item) {
      if (!item) return 0;
      const ts = (item.timestamp || "").trim();
      if (ts) {
        // Dạng: "DD/MM/YYYY HH:mm:ss"
        const m1 = ts.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})\s+(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?/);
        if (m1) {
          return new Date(m1[3], m1[2] - 1, m1[1], m1[4], m1[5], m1[6] || 0).getTime();
        }
        // Dạng: "HH:mm - DD/MM/YYYY"
        const m2 = ts.match(/^(\d{1,2}):(\d{1,2})\s*-\s*(\d{1,2})\/(\d{1,2})\/(\d{4})/);
        if (m2) {
          return new Date(m2[5], m2[4] - 1, m2[3], m2[1], m2[2], 0).getTime();
        }
        // Dạng: "HH:mm - DD/MM" (năm hiện tại)
        const m3 = ts.match(/^(\d{1,2}):(\d{1,2})\s*-\s*(\d{1,2})\/(\d{1,2})/);
        if (m3) {
          return new Date(new Date().getFullYear(), m3[4] - 1, m3[3], m3[1], m3[2], 0).getTime();
        }
      }
      // Dựa vào mã Ticket: TK-YYMMDD-XXX
      const idMatch = (item.id || "").match(/TK-(\d{2})(\d{2})(\d{2})-(\d+)/);
      if (idMatch) {
        const yr = 2000 + parseInt(idMatch[1], 10);
        const mo = parseInt(idMatch[2], 10) - 1;
        const da = parseInt(idMatch[3], 10);
        const seq = parseInt(idMatch[4], 10);
        return new Date(yr, mo, da).getTime() + seq * 1000;
      }
      return 0;
    }

    // 8. RENDER BẢNG MONITORING & DANH SÁCH THẺ MOBILE
    function getStatusBadgeHtml(status) {
      const st = (status || "Chờ xử lý").trim();
      if (st === "Đã hoàn thành" || st === "Đã xong" || st === "Done") {
        return `<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300 whitespace-nowrap">
          <i class="fa-solid fa-check mr-1 text-emerald-600"></i> Đã hoàn thành
        </span>`;
      } else if (st === "Đang xử lý") {
        return `<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-sky-100 text-sky-800 border border-sky-300 whitespace-nowrap">
          <i class="fa-solid fa-spinner fa-spin mr-1 text-sky-600"></i> Đang xử lý
        </span>`;
      }
      return `<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300 whitespace-nowrap">
        <i class="fa-regular fa-clock mr-1 text-amber-600"></i> Chờ xử lý
      </span>`;
    }

    function renderTickets() {
      const tbody = document.getElementById("ticketTableBody");
      const mobileContainer = document.getElementById("ticketCardsMobile");
      const emptyState = document.getElementById("emptyTableState");
      const searchQuery = (document.getElementById("filterSearch").value || "").toLowerCase().trim();
      const statusFilter = document.getElementById("filterStatus").value;

      const filtered = currentTickets.filter(item => {
        if (statusFilter !== "ALL") {
          const s = (item.status || "").trim().toLowerCase();
          if (s !== statusFilter.toLowerCase()) return false;
        }
        if (searchQuery) {
          const text = `${item.id} ${item.fullname} ${item.phone} ${item.department} ${item.machineName} ${item.errorMessage} ${item.description}`.toLowerCase();
          if (!text.includes(searchQuery)) return false;
        }
        return true;
      });

      // Sắp xếp ưu tiên: "Đang xử lý" (1) > "Chờ xử lý" (2) > "Đã hoàn thành" (3 - dưới cùng)
      // Trong mỗi nhóm: tự sort từ mới nhất tới cũ nhất
      filtered.sort((a, b) => {
        const rankA = getStatusRank(a.status);
        const rankB = getStatusRank(b.status);
        if (rankA !== rankB) {
          return rankA - rankB;
        }
        return parseTicketTime(b) - parseTicketTime(a);
      });

      if (filtered.length === 0) {
        if (tbody) tbody.innerHTML = "";
        if (mobileContainer) mobileContainer.innerHTML = "";
        emptyState.classList.remove("hidden");
        return;
      }

      emptyState.classList.add("hidden");

      // 1. RENDER CHẾ ĐỘ MÁY TÍNH / TABLET (TABLE) - RESPONSIVE HOÀN HẢO, KHÔNG RỚT CHỮ
      if (tbody) {
        tbody.innerHTML = filtered.map(item => {
          const statusBadge = getStatusBadgeHtml(item.status);
          const cleanPhone = String(item.phone || '').trim().replace(/^'+/, '');

          let imageCell = '<span class="text-slate-300 text-[10px]">—</span>';
          if (item.imageUrl && item.imageUrl.trim() !== "") {
            imageCell = `
              <button type="button" onclick="event.stopPropagation(); openImageViewer('${encodeURIComponent(item.imageUrl)}', '${encodeURIComponent(item.id)}')"
                class="px-2 py-1 rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 text-[10px] font-bold border border-blue-200 transition inline-flex items-center">
                <i class="fa-solid fa-image mr-1"></i> Xem ảnh
              </button>
            `;
          }

          return `
            <tr class="hover:bg-blue-50/40 transition cursor-pointer group" onclick="openTicketDetail('${item.id}')" title="Bấm vào để xem đầy đủ chi tiết ticket #${item.id}">
              <!-- Mã Ticket & Thời gian -->
              <td class="py-3 px-3 align-top whitespace-nowrap">
                <div class="font-mono font-bold text-blue-900">${item.id}</div>
                <div class="text-[10px] text-slate-400 mt-0.5">${item.timestamp}</div>
              </td>

              <!-- Người gửi & Phòng ban (Giữ trên 1 dòng, không rớt chữ lộn xộn) -->
              <td class="py-3 px-3 align-top">
                <div class="font-bold text-slate-900 whitespace-nowrap overflow-hidden text-ellipsis max-w-[180px]" title="${item.fullname}">${item.fullname}</div>
                <div class="text-[11px] text-slate-500 whitespace-nowrap overflow-hidden text-ellipsis max-w-[180px] mt-0.5" title="${item.department}">${item.department}</div>
                ${cleanPhone ? `<div class="text-[10px] text-blue-700 font-mono font-medium mt-0.5 whitespace-nowrap"><i class="fa-solid fa-phone text-[9px] mr-1"></i>${cleanPhone}</div>` : ''}
              </td>

              <!-- Tên máy & Thiết bị (Không rớt chữ) -->
              <td class="py-3 px-3 align-top">
                <div class="font-semibold text-slate-800 text-[11px] whitespace-nowrap overflow-hidden text-ellipsis max-w-[140px]" title="${item.machineName || 'Chưa rõ'}">
                  <i class="fa-solid fa-desktop text-slate-400 text-[10px] mr-1"></i>${item.machineName || 'PC nội bộ'}
                </div>
                <span class="inline-block mt-0.5 px-1.5 py-0.5 rounded-md bg-slate-100 text-slate-600 text-[10px] border border-slate-200 whitespace-nowrap overflow-hidden text-ellipsis max-w-[140px]">
                  ${item.category}
                </span>
              </td>

              <!-- Nội dung & Câu thông báo lỗi (Tối đa 2 dòng kèm '...', bấm vào xem popup) -->
              <td class="py-3 px-3 align-top">
                ${item.errorMessage ? `
                  <div class="mb-1 px-1.5 py-0.5 rounded bg-rose-50 border border-rose-200 text-rose-800 font-mono text-[10px] font-semibold truncate max-w-[240px]" title="${item.errorMessage}">
                    <i class="fa-solid fa-triangle-exclamation text-rose-500 mr-1 text-[9px]"></i>${item.errorMessage}
                  </div>
                ` : ''}
                <div class="text-slate-700 leading-relaxed text-[11px] line-clamp-2" title="${item.description}">
                  ${item.description}
                </div>
                ${(item.description && item.description.length > 50) || item.errorMessage ? `
                  <span class="text-blue-600 group-hover:text-blue-800 text-[10px] font-semibold mt-0.5 inline-flex items-center gap-0.5">
                    Xem thêm <i class="fa-solid fa-chevron-right text-[8px]"></i>
                  </span>
                ` : ''}
              </td>

              <!-- Ảnh chụp lỗi -->
              <td class="py-3 px-3 align-top text-center" onclick="event.stopPropagation()">
                ${imageCell}
              </td>

              <!-- Trạng thái -->
              <td class="py-3 px-3 align-top text-center whitespace-nowrap">
                ${statusBadge}
                ${item.itNote ? `<div class="text-[9px] text-sky-700 mt-1 font-semibold truncate max-w-[100px]" title="IT: ${item.itNote}"><i class="fa-solid fa-comment-dots mr-0.5"></i>Có ghi chú</div>` : ''}
              </td>

              <!-- Chi tiết -->
              <td class="py-3 px-3 align-top text-center whitespace-nowrap" onclick="event.stopPropagation()">
                <button type="button" onclick="openTicketDetail('${item.id}')"
                  class="w-7 h-7 rounded-lg bg-slate-100 hover:bg-blue-100 text-slate-600 hover:text-blue-700 inline-flex items-center justify-center text-xs transition" title="Xem chi tiết ticket">
                  <i class="fa-regular fa-eye"></i>
                </button>
              </td>
            </tr>
          `;
        }).join('');
      }

      // 2. RENDER CHẾ ĐỘ ĐIỆN THOẠI (DANH SÁCH THẺ DỌC - MOBILE NATIVE FEEL)
      if (mobileContainer) {
        mobileContainer.innerHTML = filtered.map(item => {
          const statusBadge = getStatusBadgeHtml(item.status);
          const cleanPhone = String(item.phone || '').trim().replace(/^'+/, '');

          let imageButtonMobile = '';
          if (item.imageUrl && item.imageUrl.trim() !== '') {
            imageButtonMobile = `
              <button type="button" onclick="openImageViewer('${encodeURIComponent(item.imageUrl)}', '${encodeURIComponent(item.id)}')"
                class="px-2.5 py-1 rounded-xl bg-blue-50 active:bg-blue-100 text-blue-700 text-[11px] font-bold border border-blue-200 transition inline-flex items-center gap-1">
                <i class="fa-solid fa-image text-xs"></i> Xem ảnh
              </button>
            `;
          }

          return `
            <div class="bg-slate-50/90 hover:bg-blue-50/30 rounded-2xl border border-slate-200 p-3.5 space-y-2.5 shadow-xs cursor-pointer transition" onclick="openTicketDetail('${item.id}')">
              <div class="flex items-center justify-between pb-2 border-b border-slate-200/60 gap-1.5">
                <div class="flex items-center space-x-1.5">
                  <span class="font-mono font-bold text-xs bg-white text-blue-900 px-2 py-0.5 rounded border border-slate-200">${item.id}</span>
                  <span class="text-[10px] text-slate-400 font-medium">${item.timestamp}</span>
                </div>
                <div>${statusBadge}</div>
              </div>

              <div class="flex items-start justify-between gap-2">
                <div>
                  <div class="font-bold text-slate-900 text-xs">${item.fullname}</div>
                  <div class="text-[11px] text-slate-500">${item.department}</div>
                </div>
                ${cleanPhone ? `
                  <a href="tel:${cleanPhone}" onclick="event.stopPropagation()" class="inline-flex items-center gap-1 text-[11px] font-bold text-blue-700 bg-blue-50 px-2 py-1 rounded-xl border border-blue-200 shrink-0 active:scale-95 transition">
                    <i class="fa-solid fa-phone text-[9px]"></i> ${cleanPhone}
                  </a>` : ''}
              </div>

              <div class="flex flex-wrap items-center gap-1 text-[10px]">
                <span class="px-2 py-0.5 bg-white text-slate-700 rounded-md border border-slate-200 font-semibold truncate max-w-[190px]">
                  <i class="fa-solid fa-desktop text-blue-600 mr-1"></i> ${item.machineName || 'Chưa rõ máy'}
                </span>
                <span class="px-2 py-0.5 bg-white text-slate-600 rounded-md border border-slate-200 font-medium">
                  ${item.category}
                </span>
              </div>

              ${item.errorMessage ? `
                <div class="p-2 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 font-mono text-[11px] font-semibold flex items-start gap-1.5">
                  <i class="fa-solid fa-triangle-exclamation text-rose-500 mt-0.5 text-[10px] shrink-0"></i>
                  <span class="break-words">${item.errorMessage}</span>
                </div>
              ` : ''}

              <div class="text-xs text-slate-700 leading-relaxed font-normal line-clamp-2">${item.description}</div>

              <div class="flex items-center justify-between gap-2 pt-1.5 border-t border-slate-100" onclick="event.stopPropagation()">
                <div class="flex items-center gap-1.5">
                  ${imageButtonMobile}
                  <button type="button" onclick="openTicketDetail('${item.id}')"
                    class="px-2 py-1 rounded-xl bg-slate-100 text-slate-700 text-[11px] font-semibold hover:bg-slate-200 transition inline-flex items-center gap-1">
                    <i class="fa-regular fa-eye"></i> Chi tiết
                  </button>
                </div>
                ${item.itNote ? `
                  <div class="text-[10px] text-sky-900 bg-sky-50 px-2 py-0.5 rounded-lg border border-sky-200 max-w-[140px] truncate" title="IT: ${item.itNote}">
                    <span class="font-bold text-sky-700">IT:</span> ${item.itNote}
                  </div>` : '<div class="text-[10px] text-slate-400 italic">Chưa có ghi chú</div>'}
              </div>
            </div>
          `;
        }).join('');
      }
    }

    // 9. CẬP NHẬT SỐ LIỆU THỐNG KÊ
    function updateStats() {
      const total = currentTickets.length;
      let pending = 0, processing = 0, completed = 0;

      currentTickets.forEach(t => {
        const s = (t.status || "").trim().toLowerCase();
        if (s.includes("hoàn thành") || s.includes("xong") || s.includes("done")) completed++;
        else if (s.includes("đang")) processing++;
        else pending++;
      });

      document.getElementById("statTotal").textContent = total;
      document.getElementById("statPending").textContent = pending;
      document.getElementById("statProcessing").textContent = processing;
      document.getElementById("statCompleted").textContent = completed;
    }

    // 9.1 MODAL XEM CHI TIẾT TICKET TOÀN DIỆN
    let currentDetailTicket = null;

    function openTicketDetail(ticketId) {
      const ticket = currentTickets.find(t => t.id === ticketId);
      if (!ticket) return;
      currentDetailTicket = ticket;

      document.getElementById("detailTicketId").textContent = ticket.id;
      document.getElementById("detailTicketStatus").innerHTML = getStatusBadgeHtml(ticket.status);
      document.getElementById("detailTicketTime").textContent = `Gửi lúc: ${ticket.timestamp}`;
      document.getElementById("detailFullname").textContent = ticket.fullname || "Cán bộ";
      document.getElementById("detailDepartment").textContent = ticket.department || "Chi nhánh số 23";
      document.getElementById("detailPhone").textContent = ticket.phone ? `SĐT: ${ticket.phone}` : "Chưa có SĐT";
      document.getElementById("detailMachineName").textContent = ticket.machineName || "PC nội bộ";
      document.getElementById("detailCategory").textContent = ticket.category || "Sự cố tin học";
      document.getElementById("detailSpecs").textContent = ticket.clientSpecs || "";

      // Error message
      const errBox = document.getElementById("detailErrorBox");
      const errText = document.getElementById("detailErrorMessage");
      if (ticket.errorMessage && ticket.errorMessage.trim()) {
        errText.textContent = ticket.errorMessage;
        errBox.classList.remove("hidden");
      } else {
        errBox.classList.add("hidden");
      }

      // Description
      document.getElementById("detailDescription").textContent = ticket.description || "(Không có mô tả chi tiết)";

      // Image preview
      const imgBox = document.getElementById("detailImageBox");
      const imgPrev = document.getElementById("detailImagePreview");
      if (ticket.imageUrl && ticket.imageUrl.trim() && ticket.imageUrl !== "Xem ảnh chụp lỗi") {
        imgPrev.src = ticket.imageUrl;
        imgBox.classList.remove("hidden");
      } else {
        imgBox.classList.add("hidden");
        imgPrev.src = "";
      }

      // IT Note
      const noteEl = document.getElementById("detailItNote");
      noteEl.textContent = ticket.itNote && ticket.itNote.trim() ? ticket.itNote : "Chưa có ghi chú xử lý từ IT.";

      document.getElementById("modalTicketDetail").classList.remove("hidden");
    }

    function closeTicketDetail() {
      document.getElementById("modalTicketDetail").classList.add("hidden");
      currentDetailTicket = null;
    }

    function openImageViewerFromDetail() {
      if (currentDetailTicket && currentDetailTicket.imageUrl) {
        openImageViewer(encodeURIComponent(currentDetailTicket.imageUrl), encodeURIComponent(currentDetailTicket.id));
      }
    }

    // 10. MODAL XEM ẢNH PHÓNG TO
    function openImageViewer(encodedUrl, encodedId) {
      let rawUrl = decodeURIComponent(encodedUrl || "").trim();
      const id = decodeURIComponent(encodedId || "").trim();

      document.getElementById("modalImgTitle").textContent = `Ảnh chụp lỗi của Ticket #${id}`;

      const loadingBox = document.getElementById("modalImgLoading");
      const errorBox = document.getElementById("modalImgError");
      const imgEl = document.getElementById("modalFullImg");
      const driveLink = document.getElementById("modalDriveLink");
      const btnOpenDrive = document.getElementById("btnOpenDriveDirect");

      loadingBox.classList.remove("hidden");
      errorBox.classList.add("hidden");
      imgEl.classList.add("hidden");
      imgEl.src = "";

      // Phân tích loại URL
      let driveUrl = rawUrl;
      let streamUrl = rawUrl;

      // 1. Nếu là ảnh Base64
      if (rawUrl.startsWith("data:image/")) {
        driveLink.classList.add("hidden");
        imgEl.src = rawUrl;
        document.getElementById("modalImageViewer").classList.remove("hidden");
        return;
      }

      // 2. Nếu là Google Drive link
      const driveMatch = rawUrl.match(/\/d\/([a-zA-Z0-9_-]+)/) || rawUrl.match(/id=([a-zA-Z0-9_-]+)/);
      if (driveMatch && driveMatch[1]) {
        const fileId = driveMatch[1];
        driveUrl = `https://drive.google.com/file/d/${fileId}/view`;
        // Thử stream qua Google CDN chính thức
        streamUrl = `https://lh3.googleusercontent.com/d/${fileId}`;
      } else if (rawUrl === "Xem ảnh chụp lỗi" || !rawUrl.startsWith("http")) {
        // Trường hợp ô Sheet lưu text công thức cũ
        loadingBox.classList.add("hidden");
        errorBox.classList.remove("hidden");
        btnOpenDrive.href = "https://drive.google.com";
        document.getElementById("modalImageViewer").classList.remove("hidden");
        return;
      }

      driveLink.href = driveUrl;
      driveLink.classList.remove("hidden");
      btnOpenDrive.href = driveUrl;

      imgEl.src = streamUrl;
      document.getElementById("modalImageViewer").classList.remove("hidden");
    }

    function onModalImgLoaded() {
      document.getElementById("modalImgLoading").classList.add("hidden");
      document.getElementById("modalImgError").classList.add("hidden");
      document.getElementById("modalFullImg").classList.remove("hidden");
    }

    function onModalImgError() {
      const imgEl = document.getElementById("modalFullImg");
      const currentSrc = imgEl.src;

      // Thử fallback sang direct thumbnail nếu CDN lh3 bị chặn
      const driveMatch = currentSrc.match(/\/d\/([a-zA-Z0-9_-]+)/) || currentSrc.match(/id=([a-zA-Z0-9_-]+)/);
      if (driveMatch && driveMatch[1] && !currentSrc.includes("thumbnail")) {
        const fileId = driveMatch[1];
        imgEl.src = `https://drive.google.com/thumbnail?id=${fileId}&sz=w1600`;
        return;
      }

      // Nếu cả thumbnail cũng không tải được (do cookie bên thứ ba hoặc bảo mật của Drive)
      document.getElementById("modalImgLoading").classList.add("hidden");
      imgEl.classList.add("hidden");
      document.getElementById("modalImgError").classList.remove("hidden");
    }

    function closeImageViewer() {
      document.getElementById("modalImageViewer").classList.add("hidden");
      document.getElementById("modalFullImg").src = "";
    }
  