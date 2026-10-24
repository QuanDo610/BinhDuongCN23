import re

def clean_html():
    file_path = 'OUTPUT/Phuong_an_xin_kinh_phi_CN23_v2.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Biểu 1 waterproofing volume in HTML
    content = content.replace('(357.43m²)', '([... m²])')
    content = content.replace('(285.38m²)', '([... m²])')
    content = content.replace('357.43 m²', '[...] m²')
    content = content.replace('285.38 m²', '[...] m²')
    content = content.replace('357,43 m²', '[...] m²')
    content = content.replace('285,38 m²', '[...] m²')

    # 2. Update Table 2 in tab-doc-view
    # Replace Table 2 Header in HTML
    old_t2_header = '''                                    <th class="border border-black p-2 bg-emerald-50 text-emerald-900" colspan="2">ĐƠN VỊ ĐỀ XUẤT CHỌN (1)</th>
                                    <th class="border border-black p-2" colspan="2">ĐƠN VỊ BÁO GIÁ 2</th>
                                    <th class="border border-black p-2" colspan="2">ĐƠN VỊ BÁO GIÁ 3</th>'''
    
    new_t2_header = '''                                    <th class="border border-black p-2 bg-slate-50 text-slate-800" colspan="2">ĐƠN VỊ BÁO GIÁ 1<br><span class="text-xs font-normal text-slate-500">([Chờ báo giá thực tế])</span></th>
                                    <th class="border border-black p-2 bg-slate-50 text-slate-800" colspan="2">ĐƠN VỊ BÁO GIÁ 2<br><span class="text-xs font-normal text-slate-500">([Chờ báo giá thực tế])</span></th>
                                    <th class="border border-black p-2 bg-slate-50 text-slate-800" colspan="2">ĐƠN VỊ BÁO GIÁ 3<br><span class="text-xs font-normal text-slate-500">([Chờ báo giá thực tế])</span></th>'''
    
    if old_t2_header in content:
        content = content.replace(old_t2_header, new_t2_header)

    # Replace old T2 tbody with clean [...] tbody
    old_tbody_pattern = re.compile(r'<tbody>\s*<tr class="font-bold bg-slate-50">\s*<td class="border border-black p-1\.5 text-center">I</td>.*?</tbody>', re.DOTALL)
    
    clean_tbody = '''<tbody>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-1.5 text-center">I</td>
                                    <td class="border border-black p-1.5">SỬA CHỮA CHỐNG THẤM TRỤ SỞ CHI NHÁNH 23</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">1</td>
                                    <td class="border border-black p-1">Chống thấm sàn mái Bitumode Delta 3mm ([...] m²)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">2</td>
                                    <td class="border border-black p-1">Chống thấm tường SikaCoat Plus ([...] m²)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr class="font-bold bg-amber-50">
                                    <td class="border border-black p-1 text-center"></td>
                                    <td class="border border-black p-1">Cộng chống thấm sau thuế VAT 8%</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-1.5 text-center">II</td>
                                    <td class="border border-black p-1.5">TRANG BỊ TÀI SẢN PHÒNG GIÁM ĐỐC MỚI (QĐ 8541 & QC 355)</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">1</td>
                                    <td class="border border-black p-1">Bộ bàn ghế ngồi làm việc Giám đốc (01 bộ)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">2</td>
                                    <td class="border border-black p-1">Tủ đựng tài liệu Giám đốc 3 buồng có khóa (01 chiếc)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">3</td>
                                    <td class="border border-black p-1">Máy vi tính để bàn làm việc Core i7 (01 bộ)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">4</td>
                                    <td class="border border-black p-1">Máy in laser đen trắng tự động 2 mặt A4 (01 chiếc)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">5</td>
                                    <td class="border border-black p-1">Điện thoại bàn cố định hiển thị số (01 chiếc)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">6</td>
                                    <td class="border border-black p-1">Bộ bàn ghế tiếp khách sofa da phòng Giám đốc (01 bộ)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr class="font-bold bg-amber-50">
                                    <td class="border border-black p-1 text-center"></td>
                                    <td class="border border-black p-1">Cộng tài sản Giám đốc sau thuế (Định mức QC 355: ≤ 64.000.000 ₫)</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-1.5 text-center">III</td>
                                    <td class="border border-black p-1.5">TRANG BỊ PHƯƠNG TIỆN PHÒNG CHÁY CHỮA CHÁY (PCCC)</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">[Chờ báo giá]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">1-9</td>
                                    <td class="border border-black p-1">Trang bị bình bột, bình CO2, kệ sắt, đèn sự cố, mặt nạ phòng độc...</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr class="font-bold bg-amber-50">
                                    <td class="border border-black p-1 text-center"></td>
                                    <td class="border border-black p-1">Cộng thiết bị PCCC sau thuế VAT 8%</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">[...]</td>
                                </tr>
                                <tr class="font-bold bg-slate-200 text-black">
                                    <td class="border border-black p-1.5 text-center" colspan="2">TỔNG CỘNG TRƯỚC THUẾ (I + II + III):</td>
                                    <td class="border border-black p-1.5 text-center text-slate-700 font-bold" colspan="2">[...]</td>
                                    <td class="border border-black p-1.5 text-center text-slate-700 font-bold" colspan="2">[...]</td>
                                    <td class="border border-black p-1.5 text-center text-slate-700 font-bold" colspan="2">[...]</td>
                                </tr>
                                <tr class="font-bold bg-slate-200 text-black">
                                    <td class="border border-black p-1.5 text-center" colspan="2">THUẾ GTGT 8%:</td>
                                    <td class="border border-black p-1.5 text-center text-slate-700 font-bold" colspan="2">[...]</td>
                                    <td class="border border-black p-1.5 text-center text-slate-700 font-bold" colspan="2">[...]</td>
                                    <td class="border border-black p-1.5 text-center text-slate-700 font-bold" colspan="2">[...]</td>
                                </tr>
                                <tr class="font-bold bg-slate-800 text-white text-[10.5pt]">
                                    <td class="border border-black p-2 text-center" colspan="2">TỔNG DỰ TOÁN KINH PHÍ ĐỀ XUẤT CẤP (SAU THUẾ):</td>
                                    <td class="border border-black p-2 text-center" colspan="2">[...]</td>
                                    <td class="border border-black p-2 text-center opacity-80" colspan="2">[...]</td>
                                    <td class="border border-black p-2 text-center opacity-80" colspan="2">[...]</td>
                                </tr>
                            </tbody>'''
    
    content = old_tbody_pattern.sub(clean_tbody, content, count=1)

    # 3. Update Thuyết minh sau Biểu 2
    old_tm = '''                    <p class="text-justify text-[12.5pt] indent-6 mt-3">
                        Như vậy, dự toán tính theo báo giá đã bao gồm VAT thấp nhất là: <strong>275.828.123 đồng</strong> <em>(Số tiền bằng chữ: Hai trăm bảy mươi lăm triệu, tám trăm hai mươi tám nghìn, một trăm hai mươi ba đồng./)</em>, trong đó:
                    </p>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Giá dịch vụ và thiết bị chưa thuế: <strong>255.393.447 đồng</strong>;</li>
                        <li>Thuế GTGT (8%): <strong>20.434.676 đồng</strong>;</li>
                        <li>Trong đó dự toán đề nghị cấp kinh phí từ Quỹ Phát triển hoạt động sự nghiệp cho Chi nhánh số 23: <strong>275.828.123 đồng</strong>.</li>
                    </ul>'''
    
    new_tm = '''                    <p class="text-justify text-[12.5pt] indent-6 mt-3">
                        Dự toán kinh phí chính thức của phương án sẽ được xác định cụ thể trên cơ sở kết quả khảo sát và 03 bảng báo giá cạnh tranh thực tế của các đơn vị cung cấp theo quy định, trong đó:
                    </p>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Mức giá đề xuất phê duyệt là báo giá của đơn vị đáp ứng đầy đủ yêu cầu kỹ thuật, chủng loại hàng hóa và có tổng giá trị sau thuế thấp nhất;</li>
                        <li>Đối với kinh phí trang bị tài sản phòng Giám đốc: Thực hiện thanh quyết toán theo giá mua thực tế qua 03 báo giá cạnh tranh nhưng không vượt định mức tối đa <strong>64.000.000 đồng</strong> theo quy định tại Quy chế chi tiêu nội bộ số 355;</li>
                        <li>Đối với hạng mục sửa chữa chống thấm và trang bị thiết bị PCCC: Xác định trên cơ sở kết quả đo đạc khảo sát thực tế và báo giá cạnh tranh thấp nhất;</li>
                        <li>Nguồn kinh phí thực hiện: Đề nghị bổ sung chi không thường xuyên cho Chi nhánh số 23 từ Quỹ Phát triển hoạt động sự nghiệp.</li>
                    </ul>'''
    
    if old_tm in content:
        content = content.replace(old_tm, new_tm)

    # 4. Update Phụ lục 1 Table in HTML
    old_pl_pattern = re.compile(r'<tbody>\s*<tr class="bg-emerald-50">\s*<td class="border border-black p-2 text-center font-bold">1</td>\s*<td class="border border-black p-2 font-bold text-emerald-900">Công ty TNHH Đầu tư Phát triển Toàn Đạt</td>.*?</tbody>', re.DOTALL)
    
    clean_pl = '''<tbody>
                            <tr>
                                <td class="border border-black p-2 text-center font-bold">1</td>
                                <td class="border border-black p-2 font-bold text-slate-800">[Đơn vị báo giá 1: Chờ khảo sát]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400 font-bold">[...]</td>
                            </tr>
                            <tr>
                                <td class="border border-black p-2 text-center font-bold">2</td>
                                <td class="border border-black p-2 font-medium">[Đơn vị báo giá 2: Chờ khảo sát]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400 font-medium">[...]</td>
                            </tr>
                            <tr>
                                <td class="border border-black p-2 text-center font-bold">3</td>
                                <td class="border border-black p-2 font-medium">[Đơn vị báo giá 3: Chờ khảo sát]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400">[...]</td>
                                <td class="border border-black p-2 text-center text-slate-400 font-medium">[...]</td>
                            </tr>
                        </tbody>'''
    
    content = old_pl_pattern.sub(clean_pl, content, count=1)

    # 5. Update Nhận xét Phụ lục 1 in HTML
    old_nx = '''                <div class="font-bold text-[13pt] mt-4 mb-1">Nhận xét:</div>
                <p class="text-justify text-[12.5pt] indent-6">
                    Qua khảo sát giá thị trường thông qua 03 báo giá của các đơn vị cung cấp dịch vụ sửa chữa chống thấm, chống dột. Mức giá đề xuất lựa chọn là <strong>188.834.923 đồng</strong>, là mức giá thấp nhất, phù hợp với khả năng tài chính của đơn vị và đảm bảo đầy đủ hạng mục thi công và tiết kiệm, hiệu quả theo quy định.
                </p>'''
    new_nx = '''                <div class="font-bold text-[13pt] mt-4 mb-1">Nhận xét:</div>
                <p class="text-justify text-[12.5pt] indent-6">
                    Chi nhánh Văn phòng Đăng ký đất đai số 23 sẽ tiến hành khảo sát giá thị trường thông qua 03 báo giá của các đơn vị cung cấp theo đúng quy định. Mức giá đề xuất lựa chọn là mức giá thấp nhất, phù hợp với khả năng tài chính của đơn vị và đảm bảo đầy đủ hạng mục thi công/cung ứng cũng như tiết kiệm, hiệu quả theo quy định.
                </p>'''
    if old_nx in content:
        content = content.replace(old_nx, new_nx)

    # 6. Update Chart View / Dashboard tab to status mode
    old_chart_section = re.compile(r'<div id="tab-chart-view".*?</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
    new_chart_section = '''<div id="tab-chart-view" class="tab-content hidden">
            <div class="max-w-6xl mx-auto space-y-6">
                <!-- Status Banner -->
                <div class="bg-amber-50 border border-amber-200 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-xl flex-shrink-0">
                        ⏳
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-amber-900 mb-1">Trạng thái hồ sơ: Đang chờ khảo sát thực tế và 03 bảng báo giá cạnh tranh</h3>
                        <p class="text-sm text-amber-800 leading-relaxed">
                            Căn cứ quy định về quản lý tài chính và Luật Đấu thầu, các số liệu báo giá của đơn vị khác (CN 34) không được áp dụng cho Chi nhánh 23. Các bảng biểu trong phương án hiện để trạng thái <code>[...]</code> để Chi nhánh 23 điền số liệu chính thức sau khi hoàn tất công tác thu thập 03 báo giá trên địa bàn.
                        </p>
                    </div>
                </div>

                <!-- KPI Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                        <div class="text-xs uppercase font-bold text-slate-400 mb-2">Định mức tài sản Giám đốc</div>
                        <div class="text-2xl font-black text-slate-800">≤ 64.000.000 ₫</div>
                        <div class="text-xs text-slate-500 mt-2">Theo Quy chế chi tiêu nội bộ số 355 & QĐ 8541</div>
                    </div>
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                        <div class="text-xs uppercase font-bold text-slate-400 mb-2">Kinh phí sửa chữa chống thấm</div>
                        <div class="text-2xl font-black text-amber-600">[Chờ khảo sát]</div>
                        <div class="text-xs text-slate-500 mt-2">Căn cứ diện tích thực tế hư hỏng tại trụ sở CN23</div>
                    </div>
                    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                        <div class="text-xs uppercase font-bold text-slate-400 mb-2">Phương tiện PCCC bổ sung</div>
                        <div class="text-2xl font-black text-blue-600">26 phương tiện</div>
                        <div class="text-xs text-slate-500 mt-2">Theo Báo cáo PCCC 2026 & TCVN 3890:2023</div>
                    </div>
                </div>
            </div>
        </div>'''
    
    content = old_chart_section.sub(new_chart_section, content, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated HTML successfully!")

if __name__ == '__main__':
    clean_html()
