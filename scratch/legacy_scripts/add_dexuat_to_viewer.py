# -*- coding: utf-8 -*-
with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/document_viewer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update count 11 files -> 12 files
content = content.replace("Danh Sách 11 Tài Liệu Gốc", "Danh Sách 12 Tài Liệu Gốc")
content = content.replace("11 files", "12 files")
content = content.replace("Kho Tài Liệu Gốc (11 Files)", "Kho Tài Liệu Gốc (12 Files)")

# 2. Add sidebar button after doc_cv2162 button
sidebar_btn = """          <button onclick="selectDoc('doc_dexuat')" id="nav_doc_dexuat" data-search="công văn 1342/cn23-hcth xin kinh phí bản quyền và an toàn mạng dexuat.pdf tờ trình 752 triệu"
                  class="doc-nav-item w-full text-left p-2.5 rounded-lg border text-xs transition flex items-start space-x-2.5 border-transparent text-slate-700 hover:bg-slate-100 hover:text-slate-900">
            <i class="fa-solid fa-file-invoice-dollar text-emerald-700 font-semibold text-sm mt-0.5 flex-shrink-0"></i>
            <div class="flex-1 min-w-0">
              <p class="font-medium truncate text-slate-800">Công Văn 1342/CN23-HCTH Xin Kinh Phí Bản Quyền (752 Tr)</p>
              <p class="text-[10px] text-slate-500 font-mono truncate">dexuat.pdf (3.7 MB - 11 trang)</p>
            </div>
          </button>
    """

# Insert after nav_doc_cv2162 button
marker_cv2162_end = '</button>\n    \n          <button onclick="selectDoc(\'doc_bb_it\')"'
if marker_cv2162_end in content:
    content = content.replace(
        marker_cv2162_end,
        '</button>\n    \n' + sidebar_btn + '      <button onclick="selectDoc(\'doc_bb_it\')"'
    )
else:
    # Alternative match
    print("Warning: marker_cv2162_end not found directly, searching flexible...")
    idx = content.find('id="nav_doc_bb_it"')
    if idx != -1:
        prev_btn = content.rfind('<button', 0, idx)
        content = content[:prev_btn] + sidebar_btn + content[prev_btn:]

# 3. Add article panel for doc_dexuat
article_dexuat = """      <article id="doc_dexuat" class="doc-view-panel hidden bg-white border border-slate-200 rounded-xl p-6 shadow-xs">
        
        <!-- Header Info -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 mb-6 gap-3">
          <div>
            <div class="flex items-center space-x-2 mb-1.5">
              <span class='px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-emerald-50 text-emerald-800 border border-emerald-300 font-semibold'>Tờ Trình Dự Toán / PDF</span>
              <span class="text-xs font-mono text-slate-500">dexuat.pdf (3.7 MB • 11 trang)</span>
            </div>
            <h2 class="text-lg md:text-xl font-bold text-slate-900 tracking-wide">Công Văn 1342/CN23-HCTH: Xin Bố Trí Kinh Phí Trang Bị Bản Quyền & An Toàn Mạng</h2>
            <p class="text-xs text-slate-600 mt-1 leading-relaxed">Tờ trình ngày 22/06/2026 của Phó Giám đốc Nguyễn Thị Lệ Hằng gửi Văn phòng ĐKĐĐ TP.HCM đề xuất kinh phí 752.829.000đ cho 80 máy trạm & Tường lửa FortiGate 61F.</p>
          </div>
          <div class="flex items-center space-x-2 flex-shrink-0">
            <a href="../documents/dexuat.pdf" download class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 transition flex items-center gap-1.5 shadow-2xs">
              <i class="fa-solid fa-download"></i> Tải file gốc
            </a>
          </div>
        </div>

        <!-- Rendered Content Body -->
        <div class="document-render-body">
          
        <div class='mb-4 flex flex-wrap items-center justify-between gap-3 p-3 bg-slate-50 rounded-lg border border-slate-200'>
          <div class='flex items-center space-x-2'>
            <span class='px-2.5 py-1 rounded bg-rose-100 text-rose-800 font-mono text-xs font-bold border border-rose-200'><i class='fa-solid fa-file-pdf mr-1'></i>PDF Gốc (11 Trang)</span>
            <span class='text-xs text-slate-700'>dexuat.pdf (3.7 MB) - Bao gồm 3 trang Tờ trình & 8 trang Báo giá đính kèm</span>
          </div>
          <a href='../documents/dexuat.pdf' target='_blank' class='px-3 py-1 bg-sky-600 hover:bg-sky-500 text-white rounded text-xs font-semibold inline-flex items-center transition shadow-xs'>
            <i class='fa-solid fa-arrow-up-right-from-square mr-1.5'></i> Mở PDF trong tab mới
          </a>
        </div>

        <div class='w-full rounded-xl overflow-hidden border border-slate-200 bg-slate-100 shadow-sm mb-6'>
          <iframe src='../documents/dexuat.pdf' class='w-full h-[750px] border-0' title='Công Văn 1342/CN23-HCTH Xin Bố Trí Kinh Phí'>
            <p class='p-4 text-xs text-slate-500'>Trình duyệt không hỗ trợ iframe PDF. <a href='../documents/dexuat.pdf' class='text-sky-700 underline'>Bấm vào đây để tải/mở tệp</a>.</p>
          </iframe>
        </div>

        <div class='p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs'>
          <h5 class='text-xs font-bold text-sky-800 uppercase tracking-wider mb-2 flex items-center'><i class='fa-solid fa-align-left mr-1.5'></i> Bản Ghi Toàn Văn Nội Dung Văn Bản (Text Transcript):</h5>
          <pre class='text-slate-800 whitespace-pre-wrap font-sans leading-relaxed'>VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI THÀNH PHỐ HỒ CHÍ MINH
CHI NHÁNH SỐ 23
Số: 1342 /CN23-HCTH
Thủ Dầu Một, ngày 22 tháng 6 năm 2026

V/v xin chủ trương bố trí kinh phí trang bị hệ điều hành bản quyền và hệ thống an toàn an ninh mạng
Kính gửi: Văn phòng đăng ký đất đai thành phố Hồ Chí Minh.

Căn cứ Nghị định số 60/2021/NĐ-CP ngày 21/6/2021 của Chính phủ về quy định cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập;
Căn cứ Nghị định số 111/2025/NĐ-CP ngày 22/5/2025 của Chính phủ sửa đổi, bổ sung một số điều của Nghị định số 60/2021/NĐ-CP ngày 21/6/2021 của Chính phủ quy định cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập;
Căn cứ Quyết định số 157/QĐ-VPĐK-HC ngày 24/11/2025 của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về việc ban hành Quy chế đảm bảo an toàn thông tin mạng, an ninh mạng trong hoạt động ứng dụng công nghệ thông tin;
Căn cứ Công văn số 14324/SNNMT-TTSĐS ngày 04 tháng 12 năm 2025 của Sở Tài nguyên và Môi trường thành phố Hồ Chí Minh về việc đảm bảo an toàn thông tin mạng, an ninh mạng trong triển khai xây dựng, hoàn thiện, vận hành, kết nối, đồng bộ, chia sẻ cơ sở dữ liệu đất đai;
Căn cứ Công văn số 2535/VPĐK-HC ngày 26/01/2026 về việc đảm bảo an toàn, an ninh mạng, rà soát, bóc tách mã độc và Thông báo kết luận số 18302/TB-VPĐK-HC ngày 17/6/2026 của Văn phòng Đăng ký đất đai thành phố Hồ Chí Minh.

Chi nhánh Văn phòng Đăng ký đất đai số 23 (sau đây gọi tắt là Chi nhánh) báo cáo Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh về tình trạng an toàn thông tin mạng và đề xuất xin chủ trương kinh phí đảm bảo hoạt động của hệ thống an toàn thông tin như sau:

1. Tình trạng bảo mật hệ thống thông tin tại Chi nhánh
Hệ thống Tường lửa cứng (Hard Firewall): Chi nhánh đang vận hành thiết bị Firewall FortiGate F61 (Số hiệu: FGT61FTK23018828) phục vụ cho khoảng 75 người dùng thực tế. Hạ tầng kỹ thuật được lắp đặt đúng tiêu chuẩn (trong tủ rack, có bộ lưu điện UPS dự phòng). Gói License hiện tại trang bị đầy đủ các tính năng bảo mật nâng cao (Advanced Malware Protection, kiểm soát ứng dụng, lọc URL/DNS/Video và gói hỗ trợ FortiCare Premium) có thời hạn sử dụng đến ngày 30/09/2026.
Hệ thống phần mềm diệt virus: Chi nhánh sử dụng giải pháp phần mềm Kaspersky Endpoint Security bảo vệ cho 80 thiết bị máy chủ và máy trạm do Công ty thiết bị văn phòng Xuân Phước cung cấp. Bản quyền của hệ thống phần mềm diệt virus này đã chính thức hết hạn từ ngày 23/03/2026.

2. Khó khăn, vướng mắc và nguy cơ mất an toàn hệ thống hiện hữu
Trước đó, Chi nhánh đã tổng hợp số liệu để kiến nghị gửi cấp trên xem xét, chấp thuận chủ trương bố trí kinh phí trang bị bản quyền hệ điều hành Windows và phần mềm diệt virus nhằm đảm bảo an toàn hệ thống. Tuy nhiên, do quy trình thẩm định chưa được xem xét giải quyết kịp thời nên đến nay đơn vị vẫn chưa có nguồn kinh phí để triển khai thực hiện.
Việc phần mềm diệt virus Kaspersky đã hết hạn bản quyền từ đầu tháng 03/2026 cộng với việc hệ điều hành Windows và bộ ứng dụng văn phòng Office tại đơn vị còn một số máy chưa được trang bị bản quyền đồng bộ đã và đang tạo ra các lỗ hổng bảo mật trên toàn bộ hệ thống mạng nội bộ của Chi nhánh. Hiện tại, các máy tính phục vụ công tác chuyên môn không thể tự động cập nhật các mẫu nhận diện mã độc mới, dẫn đến nguy cơ rất cao bị virus, phần mềm gián điệp, hoặc mã độc tống tiền (Ransomware) xâm nhập. Điều này đe dọa trực tiếp đến tính toàn vẹn, bảo mật của Cơ sở dữ liệu đất đai đang vận hành, dễ gây gián đoạn hoặc làm tê liệt hoạt động hành chính công tại đơn vị.
Bên cạnh đó, thời hạn bản quyền sử dụng thiết bị Tường lửa cứng FortiGate F61 cũng sẽ kết thúc vào ngày 30/09/2026. Do quy trình mua sắm công, kiểm định giá thường kéo dài từ 2 đến 3 tháng, nếu không được xem xét chấp thuận chủ trương bố trí vốn ngay từ giai đoạn này, hệ thống bảo mật của Chi nhánh sẽ đứng trước nguy cơ mất hoàn toàn các lá chắn an ninh mạng cốt lõi vào cuối quý III năm 2026. Để tối ưu hóa chi phí và giảm thiểu các thủ tục hành chính lặp lại hằng năm, việc xin chủ trương gia hạn gói bảo mật 03 năm liên tục cho thiết bị này là hết sức cần thiết và cấp bách.

3. Đề xuất kinh phí trang bị phần mềm bản quyền và gia hạn thiết bị bảo mật
Nhằm đảm bảo tuân thủ Quy chế an toàn thông tin mạng theo Quyết định số 157/QĐ-VPĐK-HC và các văn bản chỉ đạo của Sở Tài nguyên và Môi trường, phục vụ công tác vận hành hệ thống dữ liệu địa chính thông suốt, an toàn, Chi nhánh kính đề xuất Văn phòng Đăng ký đất đai Thành phố xem xét, chấp thuận chủ trương bố trí kinh phí thực hiện đồng bộ với các nội dung chi tiết như sau:
- Hệ điều hành Windows có bản quyền (Sử dụng lâu dài): 447.200.000 đồng cho 80 máy (Windows 11 Pro FPT Shop 5.590.000đ/máy).
- Office bản quyền (Sử dụng một năm): 159.200.000 đồng cho 80 máy (Office FPT Shop 1.990.000đ/máy/năm).
- Phần mềm diệt virus nâng cao (Kaspersky Next EDR Optimum - Thời hạn 01 năm): 100.000.000 đồng cho 80 máy.
- Về gói bảo mật Firewall FortiGate F61 (đề nghị Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh cho chủ trương chọn 01 trong 02 phương án) từ bảng báo giá tạm thời từ tháng 03/2026 sau đây:
  a/ Gia hạn gói bảo mật Unified Threat Protection (UTP) cho thiết bị Firewall FortiGate F61 (Thời hạn 03 năm): 46.429.000 đồng.
  b/ Gia hạn gói bảo mật Unified Threat Protection (UTP) cho thiết bị Firewall FortiGate F61 (Thời hạn 01 năm): 17.143.000 đồng.

Tổng kinh phí đề xuất trang bị và gia hạn bảo mật là:
• Phương án 1 (Gia hạn Firewall 03 năm): 752.829.000 đồng (Bằng chữ: Bảy trăm năm mươi hai triệu tám trăm hai mươi chín nghìn đồng chẵn).
• Phương án 2 (Gia hạn Firewall 01 năm): 723.543.000 đồng (Bằng chữ: Bảy trăm hai mươi ba triệu năm trăm bốn mươi ba ngàn đồng chẵn).

Chi phí trên được xây dựng dựa trên bảng báo giá tham khảo trên mạng Internet và bảng chào giá kỹ thuật đính kèm hệ thống phòng thủ Firewall tại thời điểm báo cáo.
Kính trình Văn phòng Đăng ký đất đai Thành phố xem xét, chấp thuận.
Trân trọng.

KT. GIÁM ĐỐC - PHÓ GIÁM ĐỐC
(Đã ký tên và đóng dấu đỏ)
Nguyễn Thị Lệ Hằng

---
DANH MỤC 8 TRANG BÁO GIÁ ĐÍNH KÈM VĂN BẢN 1342:
1. Trang 4 - 5: Báo giá tham khảo Windows 11 Pro FPT Shop (5.590.000đ/máy).
2. Trang 6 - 7: Báo giá tham khảo Microsoft Office 365 FPT Shop (1.990.000đ/máy/năm).
3. Trang 8 - 9: Báo giá tham khảo Kaspersky Next EDR Phúc Anh (1.250.000đ - 1.990.000đ/máy).
4. Trang 10: Bảng chào giá Smart Solutions số 0104-2026/SSTS-QUO/VPBD/RENEW ngày 01/04/2026 cho Firewall FortiGate 61F (1 năm: 17.143.000đ; 3 năm: 46.429.000đ).
5. Trang 11: Bảng báo giá Cửa hàng thiết bị máy móc VP Xuân Phước cho Kaspersky Next EDR Foundations (1 năm: 59.500.000đ; 3 năm: 99.900.000đ).</pre>
        </div>
        
        </div>

      </article>
    
"""

# Insert article after doc_cv2162 article
idx_cv2162_end = content.find('</article>', content.find('id="doc_cv2162"'))
if idx_cv2162_end != -1:
    content = content[:idx_cv2162_end + len('</article>')] + '\n\n' + article_dexuat + content[idx_cv2162_end + len('</article>'):]

with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/document_viewer.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully added dexuat.pdf to OUTPUT/document_viewer.html!")
