# -*- coding: utf-8 -*-
with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update header document count
content = content.replace("Kho Tài Liệu Gốc (11 Files)", "Kho Tài Liệu Gốc (12 Files)")

# 2. Update Risk Shield Box in top banner
old_risk_box = """      <!-- Risk Shield Box -->
      <div class="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-amber-50 via-white to-orange-50 border border-amber-200 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center space-x-2 text-amber-900 text-xs font-bold uppercase tracking-wide mb-2.5">
            <i class="fa-solid fa-shield-halved text-amber-600 text-sm"></i>
            <span>Căn cứ Công văn 2162</span>
          </div>
          
          <h2 class="text-base font-bold text-slate-900 mt-1">
            Lá Chắn Bảo Vệ Pháp Lý IT
          </h2>

          <p class="text-xs sm:text-sm text-slate-700 mt-2 leading-relaxed">
            Hệ thống 80 máy đối mặt rủi ro Kaspersky hết hạn (23/03) & FortiGate hết license (30/09). Văn bản 2162/CN23-HCTH đã chính thức kiến nghị hỗ trợ chuyên môn cho bạn.
          </p>
        </div>

        <div class="mt-4 pt-3 border-t border-amber-200 flex items-center justify-between text-xs">
          <span class="text-slate-600">Trạng thái: <strong class="text-emerald-700 font-semibold">Đã được bảo vệ</strong></span>
          <button onclick="switchTab('tab-risk')" class="text-sky-700 font-semibold hover:text-sky-900 hover:underline flex items-center gap-1">
            Ma trận rủi ro <i class="fa-solid fa-chevron-right text-[10px]"></i>
          </button>
        </div>
      </div>"""

new_risk_box = """      <!-- Risk & Proposal Shield Box -->
      <div class="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-amber-50 via-white to-orange-50 border border-amber-200 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center space-x-2 text-amber-900 text-xs font-bold uppercase tracking-wide mb-2.5">
            <i class="fa-solid fa-shield-halved text-amber-600 text-sm"></i>
            <span>Căn cứ Đề Xuất 1342 & CV 2162</span>
          </div>
          
          <h2 class="text-base font-bold text-slate-900 mt-1">
            Đã Trình Đề Xuất 752 Triệu Đồng
          </h2>

          <p class="text-xs sm:text-sm text-slate-700 mt-2 leading-relaxed">
            Từ 22/06/2026, Chi nhánh đã ký Công văn 1342 xin chủ trương bố trí <strong class="text-slate-900 font-bold">752.829.000 đ</strong> trang bị Windows, Office, Kaspersky và gia hạn FortiGate (30/09).
          </p>
        </div>

        <div class="mt-4 pt-3 border-t border-amber-200 flex items-center justify-between text-xs">
          <span class="text-slate-600">Trạng thái: <strong class="text-emerald-700 font-semibold">Đã có dự toán trình TP</strong></span>
          <button onclick="switchTab('tab-proposal')" class="text-sky-700 font-semibold hover:text-sky-900 hover:underline flex items-center gap-1">
            Chi tiết dự toán 1342 <i class="fa-solid fa-chevron-right text-[10px]"></i>
          </button>
        </div>
      </div>"""

content = content.replace(old_risk_box, new_risk_box)

# 3. Add Tab in navigation bar (insert before tab-event or tab-risk)
marker_nav_tab = """      <button onclick="switchTab('tab-event')" id="btn-tab-event" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-transparent text-slate-600 hover:text-sky-700 hover:border-slate-300 flex items-center space-x-2 whitespace-nowrap transition">
        <i class="fa-solid fa-handshake"></i><span>Buổi Làm Việc 16/09</span>
      </button>"""

proposal_tab_btn = """      <button onclick="switchTab('tab-proposal')" id="btn-tab-proposal" class="tab-btn px-4 py-2.5 text-sm font-semibold border-b-2 border-transparent text-slate-600 hover:text-sky-700 hover:border-slate-300 flex items-center space-x-2 whitespace-nowrap transition">
        <i class="fa-solid fa-file-invoice-dollar text-emerald-600"></i><span>Đề Xuất Kinh Phí (CV 1342)</span>
      </button>
"""

content = content.replace(marker_nav_tab, proposal_tab_btn + marker_nav_tab)

# 4. In Tab Overview, add CV 1342 to list of received documents
marker_overview_doc = """            <li class="p-3 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center hover:bg-sky-50/50 transition">
              <div>
                <p class="font-bold text-slate-900">Thư mời làm việc (10/09/2026)</p>"""

new_overview_doc = """            <li class="p-3 rounded-lg bg-emerald-50/50 border border-emerald-200 flex justify-between items-center hover:bg-emerald-50 transition">
              <div>
                <p class="font-bold text-slate-900">Công văn số 1342/CN23-HCTH (22/06/2026)</p>
                <p class="text-slate-600 mt-0.5">Tờ trình xin chủ trương kinh phí 752.829.000đ bản quyền Windows, Office, Kaspersky, FortiGate</p>
              </div>
              <span class="px-2.5 py-1 rounded bg-emerald-100 text-emerald-800 border border-emerald-300 font-semibold font-mono">CV 1342 (752 Tr)</span>
            </li>
            <li class="p-3 rounded-lg bg-slate-50 border border-slate-200 flex justify-between items-center hover:bg-sky-50/50 transition">
              <div>
                <p class="font-bold text-slate-900">Thư mời làm việc (10/09/2026)</p>"""

content = content.replace(marker_overview_doc, new_overview_doc)

# 5. Add TAB 5B / PROPOSAL SECTION
proposal_section = """    <!-- TAB: PROPOSAL (CÔNG VĂN 1342 / ĐỀ XUẤT KINH PHÍ) -->
    <section id="tab-proposal" class="tab-content hidden space-y-6">
      
      <!-- Proposal Header Card -->
      <div class="bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between pb-5 border-b border-slate-200 mb-6 gap-4">
          <div>
            <div class="flex flex-wrap items-center gap-2 mb-2">
              <span class="px-2.5 py-1 rounded-md text-xs font-bold uppercase bg-emerald-100 text-emerald-800 border border-emerald-300">
                <i class="fa-solid fa-file-signature mr-1"></i> Tờ Trình Số 1342/CN23-HCTH
              </span>
              <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-sky-50 text-sky-800 border border-sky-200">
                <i class="fa-regular fa-calendar-check mr-1"></i> Ngày ký: 22/06/2026
              </span>
              <span class="px-2.5 py-1 rounded-md text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                Người ký: Phó Giám đốc Nguyễn Thị Lệ Hằng
              </span>
            </div>
            <h2 class="text-lg sm:text-xl font-bold text-slate-900 tracking-tight">
              Tờ Trình Xin Chủ Trương Bố Trí Kinh Phí Trang Bị Hệ Điều Hành Bản Quyền & Hệ Thống An Toàn Mạng
            </h2>
            <p class="text-xs sm:text-sm text-slate-600 mt-1.5 leading-relaxed">
              Kính gửi Văn phòng Đăng ký đất đai TP.HCM đề xuất dự toán đồng bộ bảo vệ 80 máy tính trạm và thiết bị Tường lửa cứng FortiGate 61F.
            </p>
          </div>

          <div class="flex flex-wrap items-center gap-2 flex-shrink-0">
            <a href="document_viewer.html" onclick="localStorage.setItem('open_doc', 'doc_dexuat')" class="px-3.5 py-2 rounded-lg text-xs font-semibold bg-sky-600 hover:bg-sky-700 text-white transition shadow-xs flex items-center gap-1.5">
              <i class="fa-solid fa-file-pdf"></i> Xem toàn văn dexuat.pdf (11 Trang)
            </a>
            <a href="../documents/dexuat.pdf" download class="px-3.5 py-2 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 transition flex items-center gap-1.5 shadow-2xs">
              <i class="fa-solid fa-download"></i> Tải PDF gốc
            </a>
          </div>
        </div>

        <!-- 4 Key Metric Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div class="p-4 rounded-xl bg-gradient-to-br from-emerald-50 to-teal-50 border border-emerald-200 shadow-2xs">
            <span class="text-[11px] font-bold uppercase tracking-wider text-emerald-800 flex items-center justify-between">
              Phương Án 1 (Khuyên Dùng) <i class="fa-solid fa-award text-emerald-600"></i>
            </span>
            <div class="mt-2 text-2xl font-bold text-emerald-800 font-mono">752.829.000 đ</div>
            <p class="text-xs text-slate-600 mt-1 leading-snug">
              Bao gồm gói Firewall FortiGate <strong>3 năm</strong> (tối ưu chi phí & thủ tục hành chính).
            </p>
          </div>

          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 shadow-2xs">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-600 flex items-center justify-between">
              Phương Án 2 (Thời Hạn 1 Năm) <i class="fa-solid fa-clock text-slate-400"></i>
            </span>
            <div class="mt-2 text-2xl font-bold text-slate-800 font-mono">723.543.000 đ</div>
            <p class="text-xs text-slate-600 mt-1 leading-snug">
              Bao gồm gói Firewall FortiGate <strong>1 năm</strong> (17.143.000 đ).
            </p>
          </div>

          <div class="p-4 rounded-xl bg-slate-50 border border-slate-200 shadow-2xs">
            <span class="text-[11px] font-bold uppercase tracking-wider text-slate-600 flex items-center justify-between">
              Quy Mô Bảo Vệ Toàn Diện <i class="fa-solid fa-network-wired text-sky-600"></i>
            </span>
            <div class="mt-2 text-2xl font-bold text-sky-800 font-mono">80 Thiết Bị</div>
            <p class="text-xs text-slate-600 mt-1 leading-snug">
              Bao phủ toàn bộ máy trạm, 3 máy chủ và thiết bị phòng thủ FortiGate 61F.
            </p>
          </div>

          <div class="p-4 rounded-xl bg-amber-50/60 border border-amber-200 shadow-2xs">
            <span class="text-[11px] font-bold uppercase tracking-wider text-amber-800 flex items-center justify-between">
              Tình Trạng Hồ Sơ <i class="fa-solid fa-hourglass-half text-amber-600"></i>
            </span>
            <div class="mt-2 text-base font-bold text-amber-900">Đã Trình Lên TP.HCM</div>
            <p class="text-xs text-slate-600 mt-1 leading-snug">
              Đệ trình ngày 22/06/2026, hiện đang chờ quy trình thẩm định tài chính.
            </p>
          </div>
        </div>

        <!-- Visual Proportion Bar -->
        <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 mb-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-3 gap-1">
            <h4 class="text-xs font-bold uppercase tracking-wider text-slate-700 flex items-center">
              <i class="fa-solid fa-chart-pie text-sky-600 mr-2"></i> Cơ Cấu Tỷ Trọng Kinh Phí Đề Xuất (Phương Án 752.829.000 VNĐ)
            </h4>
            <span class="text-[11px] text-slate-500">Căn cứ theo Báo cáo số 1342/CN23-HCTH</span>
          </div>

          <!-- Multi-segment progress bar -->
          <div class="w-full h-4 rounded-full bg-slate-200 overflow-hidden flex shadow-inner">
            <div style="width: 59.4%" class="bg-sky-600 transition-all hover:opacity-90" title="Windows 11 Pro: 59.4% (447.200.000 đ)"></div>
            <div style="width: 21.1%" class="bg-indigo-600 transition-all hover:opacity-90" title="Office 365: 21.1% (159.200.000 đ)"></div>
            <div style="width: 13.3%" class="bg-rose-500 transition-all hover:opacity-90" title="Kaspersky Next EDR: 13.3% (100.000.000 đ)"></div>
            <div style="width: 6.2%" class="bg-emerald-600 transition-all hover:opacity-90" title="Firewall FortiGate (3 năm): 6.2% (46.429.000 đ)"></div>
          </div>

          <!-- Legend list -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 mt-4 pt-3 border-t border-slate-200/80 text-xs">
            <div class="flex items-start space-x-2">
              <span class="w-3 h-3 rounded-sm bg-sky-600 mt-0.5 flex-shrink-0"></span>
              <div>
                <p class="font-bold text-slate-900">Windows 11 Pro (59.4%)</p>
                <p class="text-slate-500 font-mono">447.200.000 đ</p>
                <p class="text-[10px] text-slate-400">Vĩnh viễn • 80 máy</p>
              </div>
            </div>

            <div class="flex items-start space-x-2">
              <span class="w-3 h-3 rounded-sm bg-indigo-600 mt-0.5 flex-shrink-0"></span>
              <div>
                <p class="font-bold text-slate-900">Microsoft Office (21.1%)</p>
                <p class="text-slate-500 font-mono">159.200.000 đ</p>
                <p class="text-[10px] text-slate-400">1 năm • 80 máy</p>
              </div>
            </div>

            <div class="flex items-start space-x-2">
              <span class="w-3 h-3 rounded-sm bg-rose-500 mt-0.5 flex-shrink-0"></span>
              <div>
                <p class="font-bold text-slate-900">Kaspersky Next EDR (13.3%)</p>
                <p class="text-slate-500 font-mono">100.000.000 đ</p>
                <p class="text-[10px] text-slate-400">1 năm • 80 máy</p>
              </div>
            </div>

            <div class="flex items-start space-x-2">
              <span class="w-3 h-3 rounded-sm bg-emerald-600 mt-0.5 flex-shrink-0"></span>
              <div>
                <p class="font-bold text-slate-900">Firewall FortiGate (6.2%)</p>
                <p class="text-slate-500 font-mono">46.429.000 đ</p>
                <p class="text-[10px] text-slate-400">Gói 3 năm (hoặc 17.143.000đ 1 năm)</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Budget Breakdown Table -->
        <div class="overflow-x-auto rounded-xl border border-slate-200 mb-6 shadow-2xs">
          <table class="w-full text-sm text-left border-collapse bg-white">
            <thead class="text-xs uppercase bg-slate-50 text-slate-700 border-b border-slate-200 font-bold">
              <tr>
                <th class="py-3.5 px-4 w-12 text-center">STT</th>
                <th class="py-3.5 px-4">Hạng Mục Đầu Tư / Gia Hạn</th>
                <th class="py-3.5 px-4 w-28 text-center">Số Lượng</th>
                <th class="py-3.5 px-4 w-28">Thời Hạn</th>
                <th class="py-3.5 px-4 text-right">Đơn Giá Tham Khảo</th>
                <th class="py-3.5 px-4 text-right">Thành Tiền (VNĐ)</th>
                <th class="py-3.5 px-4">Đơn Vị Chào Giá & Chứng Từ</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100 text-slate-700">
              <tr class="hover:bg-slate-50/80 transition">
                <td class="py-3.5 px-4 text-center font-bold font-mono text-slate-500">1</td>
                <td class="py-3.5 px-4">
                  <div class="font-bold text-slate-900">Hệ điều hành Windows có bản quyền</div>
                  <div class="text-xs text-slate-500 mt-0.5">Key-online Windows 11 Pro 32bit/64bit FPP</div>
                </td>
                <td class="py-3.5 px-4 text-center font-mono font-bold text-slate-800">80 máy</td>
                <td class="py-3.5 px-4"><span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-sky-50 text-sky-800 border border-sky-200">Vĩnh viễn</span></td>
                <td class="py-3.5 px-4 text-right font-mono text-slate-600">5.590.000 đ</td>
                <td class="py-3.5 px-4 text-right font-mono font-bold text-slate-900 text-base">447.200.000 đ</td>
                <td class="py-3.5 px-4 text-xs">
                  <span class="font-semibold text-slate-800">FPT Shop</span>
                  <span class="text-slate-400 block text-[11px]">(Đính kèm Trang 4 - 5)</span>
                </td>
              </tr>

              <tr class="hover:bg-slate-50/80 transition">
                <td class="py-3.5 px-4 text-center font-bold font-mono text-slate-500">2</td>
                <td class="py-3.5 px-4">
                  <div class="font-bold text-slate-900">Bộ ứng dụng văn phòng Office bản quyền</div>
                  <div class="text-xs text-slate-500 mt-0.5">Microsoft 365 Personal / Business PK Lic 1YR</div>
                </td>
                <td class="py-3.5 px-4 text-center font-mono font-bold text-slate-800">80 máy</td>
                <td class="py-3.5 px-4"><span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200">01 Năm</span></td>
                <td class="py-3.5 px-4 text-right font-mono text-slate-600">1.990.000 đ</td>
                <td class="py-3.5 px-4 text-right font-mono font-bold text-slate-900 text-base">159.200.000 đ</td>
                <td class="py-3.5 px-4 text-xs">
                  <span class="font-semibold text-slate-800">FPT Shop</span>
                  <span class="text-slate-400 block text-[11px]">(Đính kèm Trang 6 - 7)</span>
                </td>
              </tr>

              <tr class="hover:bg-slate-50/80 transition">
                <td class="py-3.5 px-4 text-center font-bold font-mono text-slate-500">3</td>
                <td class="py-3.5 px-4">
                  <div class="font-bold text-slate-900">Phần mềm diệt virus tập trung nâng cao</div>
                  <div class="text-xs text-slate-500 mt-0.5">Kaspersky Next EDR Optimum / Foundations (1 Server + 74 user)</div>
                </td>
                <td class="py-3.5 px-4 text-center font-mono font-bold text-slate-800">80 máy</td>
                <td class="py-3.5 px-4"><span class="px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-50 text-rose-800 border border-rose-200">01 Năm</span></td>
                <td class="py-3.5 px-4 text-right font-mono text-slate-600">1.250.000 đ</td>
                <td class="py-3.5 px-4 text-right font-mono font-bold text-slate-900 text-base">100.000.000 đ</td>
                <td class="py-3.5 px-4 text-xs">
                  <span class="font-semibold text-slate-800">Phúc Anh / Xuân Phước</span>
                  <span class="text-slate-400 block text-[11px]">(Đính kèm Trang 8-9 & 11)</span>
                </td>
              </tr>

              <tr class="hover:bg-slate-50/80 transition bg-emerald-50/20">
                <td class="py-3.5 px-4 text-center font-bold font-mono text-slate-500">4</td>
                <td class="py-3.5 px-4">
                  <div class="font-bold text-emerald-900">Gói bản quyền Tường lửa cứng FortiGate 61F (PA 1 - 03 Năm)</div>
                  <div class="text-xs text-slate-500 mt-0.5">Gói Unified Threat Protection (UTP) 24/7 (SN: FGT61FTK23018828)</div>
                </td>
                <td class="py-3.5 px-4 text-center font-mono font-bold text-slate-800">01 Thiết bị</td>
                <td class="py-3.5 px-4"><span class="px-2 py-0.5 rounded text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">03 Năm</span></td>
                <td class="py-3.5 px-4 text-right font-mono text-slate-600">46.429.000 đ</td>
                <td class="py-3.5 px-4 text-right font-mono font-bold text-emerald-800 text-base">46.429.000 đ</td>
                <td class="py-3.5 px-4 text-xs">
                  <span class="font-semibold text-slate-800">Smart Solutions</span>
                  <span class="text-slate-400 block text-[11px]">(Báo giá 0104-2026 Trang 10)</span>
                </td>
              </tr>

              <tr class="hover:bg-slate-50/80 transition text-slate-500">
                <td class="py-3.5 px-4 text-center font-bold font-mono text-slate-400">-</td>
                <td class="py-3.5 px-4">
                  <div class="italic text-slate-600">Gói bản quyền Tường lửa FortiGate 61F (Phương án 2 thay thế)</div>
                  <div class="text-xs text-slate-400">Nếu cấp trên chỉ duyệt gia hạn tạm thời 01 năm</div>
                </td>
                <td class="py-3.5 px-4 text-center font-mono">01 Thiết bị</td>
                <td class="py-3.5 px-4"><span class="px-2 py-0.5 rounded text-[11px] bg-slate-100 text-slate-600 border border-slate-200">01 Năm</span></td>
                <td class="py-3.5 px-4 text-right font-mono text-slate-500">17.143.000 đ</td>
                <td class="py-3.5 px-4 text-right font-mono text-slate-600">17.143.000 đ</td>
                <td class="py-3.5 px-4 text-xs text-slate-500">Smart Solutions (Trang 10)</td>
              </tr>
            </tbody>
            <tfoot class="bg-slate-100/80 font-bold text-slate-900 border-t-2 border-slate-300 text-sm">
              <tr>
                <td colspan="5" class="py-3.5 px-4 text-right uppercase tracking-wider">
                  Tổng Cộng Dự Toán Phương Án 1 (Gói FortiGate 3 năm):
                </td>
                <td class="py-3.5 px-4 text-right font-mono text-lg text-emerald-800">752.829.000 đ</td>
                <td class="py-3.5 px-4 text-xs text-slate-500 font-normal">Bảy trăm năm mươi hai triệu tám trăm hai mươi chín nghìn đồng</td>
              </tr>
              <tr class="text-slate-600 bg-slate-50/60 font-semibold text-xs border-t border-slate-200">
                <td colspan="5" class="py-2.5 px-4 text-right uppercase">
                  Tổng Cộng Dự Toán Phương Án 2 (Gói FortiGate 1 năm):
                </td>
                <td class="py-2.5 px-4 text-right font-mono text-sm text-slate-800">723.543.000 đ</td>
                <td class="py-2.5 px-4 text-xs text-slate-400 font-normal">Bảy trăm hai mươi ba triệu năm trăm bốn mươi ba ngàn đồng</td>
              </tr>
            </tfoot>
          </table>
        </div>

        <!-- Strategic Importance Card for Do Trong Minh Quan -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 text-sm">
          <div class="p-5 rounded-xl bg-emerald-50/40 border border-emerald-200">
            <h4 class="font-bold text-emerald-900 flex items-center mb-3">
              <i class="fa-solid fa-shield-check text-emerald-600 mr-2 text-base"></i> 1. Lá Chắn Trách Nhiệm Pháp Lý Cho Bạn
            </h4>
            <p class="text-xs text-slate-700 leading-relaxed mb-3">
              Văn bản số <strong>1342/CN23-HCTH</strong> được ký chính thức vào ngày <strong>22/06/2026</strong> bởi Phó Giám đốc Nguyễn Thị Lệ Hằng là bằng chứng thép khẳng định:
            </p>
            <ul class="space-y-2 text-xs text-slate-700">
              <li class="flex items-start">
                <i class="fa-solid fa-check text-emerald-600 mr-2 mt-0.5"></i>
                <span>Mọi rủi ro bản quyền (Kaspersky hết hạn 23/03/2026, FortiGate hết hạn 30/09/2026, Windows/Office thiếu bản quyền) đã được đơn vị kiểm kê và xin kinh phí từ tháng 6/2026.</span>
              </li>
              <li class="flex items-start">
                <i class="fa-solid fa-check text-emerald-600 mr-2 mt-0.5"></i>
                <span>Việc chưa mua bản quyền là do <strong>thủ tục thẩm định cấp trên chưa giải quyết kịp thời</strong>, hoàn toàn không phải do lỗi chuyên môn hay sự chậm trễ của nhân sự mới nhận việc.</span>
              </li>
            </ul>
          </div>

          <div class="p-5 rounded-xl bg-sky-50/40 border border-sky-200">
            <h4 class="font-bold text-sky-900 flex items-center mb-3">
              <i class="fa-solid fa-comments text-sky-600 mr-2 text-base"></i> 2. Điểm Trọng Tâm Làm Việc Với Anh Quốc (Hôm Nay 16/09)
            </h4>
            <p class="text-xs text-slate-700 leading-relaxed mb-3">
              Trong buổi khảo sát hạ tầng hôm nay, bạn hãy chủ động mang tờ trình 1342 ra đề xuất:
            </p>
            <ul class="space-y-2 text-xs text-slate-700">
              <li class="flex items-start">
                <i class="fa-solid fa-bullseye text-sky-600 mr-2 mt-0.5"></i>
                <span><strong>Tiến độ duyệt:</strong> Nhờ anh Quốc liên hệ bộ phận Kế toán / CNTT TP.HCM hỗ trợ đẩy nhanh việc phê duyệt tờ trình 1342 để có kinh phí gia hạn.</span>
              </li>
              <li class="flex items-start">
                <i class="fa-solid fa-bullseye text-sky-600 mr-2 mt-0.5"></i>
                <span><strong>Giải pháp sau 30/09:</strong> Đặt câu hỏi: <em>"Nếu sau 30/09/2026 kinh phí chưa kịp cấp, TP.HCM có cơ chế license tập trung hoặc phương án dự phòng nào cho Firewall FortiGate 61F cơ sở 23 không?"</em></span>
              </li>
            </ul>
          </div>
        </div>

      </div>

    </section>
"""

# Insert tab-proposal before tab-event or tab-risk
idx_tab_event = content.find('<!-- TAB 5: EVENT 16/09 PREPARATION -->')
if idx_tab_event != -1:
    content = content[:idx_tab_event] + proposal_section + '\n    ' + content[idx_tab_event:]
else:
    # Alternative insert before end of main
    idx_main = content.find('</main>')
    content = content[:idx_main] + proposal_section + '\n  ' + content[idx_main:]

with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated OUTPUT/index.html with Tab Proposal!")
