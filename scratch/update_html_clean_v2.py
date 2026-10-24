import re

def update_html_v2():
    html_file = 'OUTPUT/Phuong_an_xin_kinh_phi_CN23_v2.html'
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update Section 2.4 text in Tab 1
    old_pccc_txt = '<strong>2.4. Trang bị phương tiện PCCC:</strong> Bình bột ABC, bình CO2, tiêu lệnh, kệ đôi, đèn sự cố, đèn Exit có tem kiểm định an toàn PCCC của Bộ Công an.'
    new_pccc_txt = '<strong>2.4. Về trang bị bổ sung phương tiện PCCC cơ sở:</strong> Hiện trạng tại trụ sở có 26 bình chữa cháy tại chỗ nhưng chưa đồng bộ; danh mục, số lượng và chủng loại đề xuất trang bị bổ sung: <code>&lt;trống&gt;</code> (Chờ Chi nhánh Văn phòng Đăng ký đất đai số 23 phối hợp với cơ quan Cảnh sát PCCC&CNCH tiến hành rà soát, kiểm tra thực tế hiện trạng trụ sở và lập danh mục đề xuất trang bị bổ sung chính thức; tuyệt đối không tự ước tính số lượng khi chưa có biên bản khảo sát thực tế).'
    content = content.replace(old_pccc_txt, new_pccc_txt)

    # 2. Update Biểu 1 in Tab 1 (Replace tbody of Table 1)
    old_b1_pattern = re.compile(r'<tbody>\s*<tr class="font-bold bg-slate-50">\s*<td class="border border-black p-2 text-center">A</td>.*?</tbody>', re.DOTALL)
    
    clean_b1_tbody = '''<tbody>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">A</td>
                                    <td class="border border-black p-2" colspan="3">Chống thấm sàn mái, sê nô mái, mương đón nước bằng màng khò nóng Bitumode Delta – P 3mm (Mặt trơn)</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">Vệ sinh tạo nhám bề mặt, quét 1 lớp lót Nirol-W (0.2kg/m²), dán màng Bitumode Delta 3mm khò nhiệt giáp mí 10cm</td>
                                    <td class="border border-black p-2 text-center">m²</td>
                                    <td class="border border-black p-2 text-right font-semibold">[...]</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">B</td>
                                    <td class="border border-black p-2" colspan="3">Chống thấm tường sàn mái, tường sê nô bằng SikaCoat Plus</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">Cạo bỏ lớp sơn cũ rêu mốc, vá nứt bằng Mastic dẻo, lăn phủ 2 lớp chống thấm kháng tia UV SikaCoat Plus (0.6kg/m²)</td>
                                    <td class="border border-black p-2 text-center">m²</td>
                                    <td class="border border-black p-2 text-right font-semibold">[...]</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">C</td>
                                    <td class="border border-black p-2" colspan="3">Trang bị tài sản làm việc phòng Giám đốc mới nhậm chức theo QĐ 8541 và Quy chế 355</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">Bộ bàn ghế ngồi làm việc Giám đốc (Bàn làm việc + Ghế xoay lãnh đạo)</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">2</td>
                                    <td class="border border-black p-2">Tủ đựng tài liệu Giám đốc</td>
                                    <td class="border border-black p-2 text-center">Chiếc</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">3</td>
                                    <td class="border border-black p-2">Máy vi tính để bàn làm việc (gồm màn hình)</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">4</td>
                                    <td class="border border-black p-2">Máy in laser khổ A4</td>
                                    <td class="border border-black p-2 text-center">Chiếc</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">5</td>
                                    <td class="border border-black p-2">Máy điện thoại bàn cố định</td>
                                    <td class="border border-black p-2 text-center">Chiếc</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">6</td>
                                    <td class="border border-black p-2">Bộ bàn ghế tiếp khách phòng Giám đốc</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">D</td>
                                    <td class="border border-black p-2" colspan="3">Trang bị phương tiện phòng cháy chữa cháy (PCCC) cơ sở theo Báo cáo PCCC CN23 và quy định an toàn PCCC</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">Trang bị bổ sung phương tiện PCCC cơ sở (Danh mục, chủng loại và khối lượng chi tiết: &lt;trống&gt; - Chờ Chi nhánh 23 rà soát, khảo sát và lập danh mục đề xuất thực tế theo biên bản kiểm tra an toàn PCCC)</td>
                                    <td class="border border-black p-2 text-center">&lt;trống&gt;</td>
                                    <td class="border border-black p-2 text-center font-semibold text-slate-500">&lt;trống&gt;</td>
                                </tr>
                            </tbody>'''
    content = old_b1_pattern.sub(clean_b1_tbody, content, count=1)

    # 3. Update Biểu 2 in Tab 1 (Table 2 tbody)
    old_b2_tbody_pattern = re.compile(r'<tbody>\s*<tr class="font-bold bg-slate-50">\s*<td class="border border-black p-1\.5 text-center">I</td>.*?</tbody>', re.DOTALL)
    clean_b2_tbody = '''<tbody>
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
                                    <td class="border border-black p-1">Tủ đựng tài liệu Giám đốc (01 chiếc)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">3</td>
                                    <td class="border border-black p-1">Máy vi tính để bàn làm việc gồm màn hình (01 bộ)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">4</td>
                                    <td class="border border-black p-1">Máy in laser khổ A4 (01 chiếc)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">5</td>
                                    <td class="border border-black p-1">Máy điện thoại bàn cố định (01 chiếc)</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                    <td class="border border-black p-1 text-center text-slate-400">[...]</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">6</td>
                                    <td class="border border-black p-1">Bộ bàn ghế tiếp khách phòng Giám đốc (01 bộ)</td>
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
                                    <td class="border border-black p-1.5 text-center" colspan="2">&lt;trống&gt;</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">&lt;trống&gt;</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">&lt;trống&gt;</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">1</td>
                                    <td class="border border-black p-1">Trang bị bổ sung phương tiện PCCC cơ sở (Chờ Chi nhánh 23 khảo sát và lập danh mục đề xuất thực tế)</td>
                                    <td class="border border-black p-1 text-center text-slate-500">&lt;trống&gt;</td>
                                    <td class="border border-black p-1 text-center text-slate-500">&lt;trống&gt;</td>
                                    <td class="border border-black p-1 text-center text-slate-500">&lt;trống&gt;</td>
                                    <td class="border border-black p-1 text-center text-slate-500">&lt;trống&gt;</td>
                                    <td class="border border-black p-1 text-center text-slate-500">&lt;trống&gt;</td>
                                    <td class="border border-black p-1 text-center text-slate-500">&lt;trống&gt;</td>
                                </tr>
                                <tr class="font-bold bg-amber-50">
                                    <td class="border border-black p-1 text-center"></td>
                                    <td class="border border-black p-1">Cộng thiết bị PCCC sau thuế VAT 8%</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">&lt;trống&gt;</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">&lt;trống&gt;</td>
                                    <td class="border border-black p-1 text-center text-slate-500" colspan="2">&lt;trống&gt;</td>
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
    content = old_b2_tbody_pattern.sub(clean_b2_tbody, content, count=1)

    # 4. Update Tab 2 (Bảng tổng hợp & so sánh) Table Body
    old_tab2_pattern = re.compile(r'<tbody class="divide-y divide-slate-100">\s*<!-- NHÓM A -->.*?</tbody>', re.DOTALL)
    
    clean_tab2_tbody = '''<tbody class="divide-y divide-slate-100">
                            <!-- NHÓM A -->
                            <tr class="bg-amber-50/40 text-amber-950 font-bold">
                                <td class="p-3 text-center">A</td>
                                <td colspan="7" class="p-3">TRANG BỊ TÀI SẢN PHÒNG GIÁM ĐỐC MỚI NHẬM CHỨC (THEO QĐ 8541 & QC 355)</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Bộ bàn ghế ngồi làm việc Giám đốc (Bàn làm việc + Ghế xoay lãnh đạo)</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">2</td>
                                <td class="p-3 font-semibold text-slate-800">Tủ đựng tài liệu Giám đốc</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">3</td>
                                <td class="p-3 font-semibold text-slate-800">Máy vi tính để bàn làm việc (gồm màn hình)</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">4</td>
                                <td class="p-3 font-semibold text-slate-800">Máy in laser khổ A4</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">5</td>
                                <td class="p-3 font-semibold text-slate-800">Máy điện thoại bàn cố định</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">6</td>
                                <td class="p-3 font-semibold text-slate-800">Bộ bàn ghế tiếp khách phòng Giám đốc</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="bg-amber-100/40 font-bold text-amber-950">
                                <td class="p-3 text-center">Cộng A</td>
                                <td colspan="4" class="p-3">Tổng kinh phí trang bị tài sản phòng Giám đốc (A) (Định mức QC 355: ≤ 64.000.000 ₫)</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                            </tr>

                            <!-- NHÓM B -->
                            <tr class="bg-emerald-50/40 text-emerald-950 font-bold">
                                <td class="p-3 text-center">B</td>
                                <td colspan="7" class="p-3">SỬA CHỮA CHỐNG THẤM TRỤ SỞ CHI NHÁNH SỐ 23</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Chống thấm sàn mái, sê nô, mương đón nước bằng màng khò nhiệt Bitumode Delta-P 3mm</td>
                                <td class="p-3 text-center">m²</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">2</td>
                                <td class="p-3 font-semibold text-slate-800">Chống thấm tường sàn mái, tường sê nô bằng hóa chất kháng UV SikaCoat Plus</td>
                                <td class="p-3 text-center">m²</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="bg-emerald-100/40 font-bold text-emerald-950">
                                <td class="p-3 text-center">Cộng B</td>
                                <td colspan="4" class="p-3">Tổng kinh phí sửa chữa chống thấm trụ sở (B)</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                            </tr>

                            <!-- NHÓM C -->
                            <tr class="bg-rose-50/40 text-rose-950 font-bold">
                                <td class="p-3 text-center">C</td>
                                <td colspan="7" class="p-3">TRANG BỊ PHƯƠNG TIỆN PHÒNG CHÁY CHỮA CHÁY (PCCC) CƠ SỞ</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Trang bị bổ sung phương tiện PCCC cơ sở (Chờ Chi nhánh 23 khảo sát và lập danh mục đề xuất thực tế theo biên bản kiểm tra an toàn PCCC)</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                            </tr>
                            <tr class="bg-rose-100/40 font-bold text-rose-950">
                                <td class="p-3 text-center">Cộng C</td>
                                <td colspan="4" class="p-3">Tổng kinh phí trang bị phương tiện PCCC (C)</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                            </tr>
                        </tbody>'''
    
    clean_tab2_tbody = '''<tbody>
                            <!-- NHÓM A -->
                            <tr class="bg-amber-50/40 text-amber-950 font-bold">
                                <td class="p-3 text-center">A</td>
                                <td colspan="7" class="p-3">TRANG BỊ TÀI SẢN PHÒNG GIÁM ĐỐC MỚI (THEO QĐ 8541 & QC 355)</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Bộ bàn ghế ngồi làm việc Giám đốc (Bàn làm việc + Ghế xoay lãnh đạo)</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">2</td>
                                <td class="p-3 font-semibold text-slate-800">Tủ đựng tài liệu Giám đốc</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">3</td>
                                <td class="p-3 font-semibold text-slate-800">Máy vi tính để bàn làm việc (gồm màn hình)</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">4</td>
                                <td class="p-3 font-semibold text-slate-800">Máy in laser khổ A4</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">5</td>
                                <td class="p-3 font-semibold text-slate-800">Máy điện thoại bàn cố định</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">6</td>
                                <td class="p-3 font-semibold text-slate-800">Bộ bàn ghế tiếp khách phòng Giám đốc</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="bg-amber-100/40 font-bold text-amber-950">
                                <td class="p-3 text-center">Cộng A</td>
                                <td colspan="4" class="p-3">Tổng kinh phí trang bị tài sản phòng Giám đốc (A) (Định mức QC 355: ≤ 64.000.000 ₫)</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                            </tr>

                            <!-- NHÓM B -->
                            <tr class="bg-emerald-50/40 text-emerald-950 font-bold">
                                <td class="p-3 text-center">B</td>
                                <td colspan="7" class="p-3">SỬA CHỮA CHỐNG THẤM TRỤ SỞ CHI NHÁNH SỐ 23</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Chống thấm sàn mái, sê nô, mương đón nước bằng màng khò nhiệt Bitumode Delta-P 3mm</td>
                                <td class="p-3 text-center">m²</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">2</td>
                                <td class="p-3 font-semibold text-slate-800">Chống thấm tường sàn mái, tường sê nô bằng hóa chất kháng UV SikaCoat Plus</td>
                                <td class="p-3 text-center">m²</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="bg-emerald-100/40 font-bold text-emerald-950">
                                <td class="p-3 text-center">Cộng B</td>
                                <td colspan="4" class="p-3">Tổng kinh phí sửa chữa chống thấm trụ sở (B)</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                            </tr>

                            <!-- NHÓM C -->
                            <tr class="bg-rose-50/40 text-rose-950 font-bold">
                                <td class="p-3 text-center">C</td>
                                <td colspan="7" class="p-3">TRANG BỊ PHƯƠNG TIỆN PHÒNG CHÁY CHỮA CHÁY (PCCC) CƠ SỞ</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Trang bị bổ sung phương tiện PCCC cơ sở (Chờ Chi nhánh 23 khảo sát và lập danh mục đề xuất thực tế theo biên bản kiểm tra an toàn PCCC)</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-400">&lt;trống&gt;</td>
                            </tr>
                            <tr class="bg-rose-100/40 font-bold text-rose-950">
                                <td class="p-3 text-center">Cộng C</td>
                                <td colspan="4" class="p-3">Tổng kinh phí trang bị phương tiện PCCC (C)</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                                <td class="p-3 text-center text-slate-500">&lt;trống&gt;</td>
                            </tr>
                        </tbody>'''
    content = old_tab2_pattern.sub(clean_tab2_tbody, content, count=1)

    # 5. Update Tab 3 (Source View): Báo cáo PCCC CN23 text
    content = content.replace(
        '<li><b>Nhu cầu:</b> Thay mới bình bột ABC, bổ sung bình CO2 cho kho giấy/máy chủ, mặt nạ độc, đèn thoát nạn.</li>',
        '<li><b>Kiến nghị:</b> Bổ sung kinh phí đầu tư thiết bị bảo quản an toàn kho lưu trữ theo CV 24482/VPĐK-KT; danh mục và số lượng bổ sung cụ thể do đơn vị khảo sát thực tế và lập đề xuất sau.</li>'
    )

    # 6. Update Tab 4 (Dashboard): KPI card for PCCC
    old_kpi_pccc = '''<div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                        <div class="text-xs uppercase font-bold text-slate-400 mb-2">Phương tiện PCCC bổ sung</div>
                        <div class="text-2xl font-black text-blue-600">26 phương tiện</div>
                        <div class="text-xs text-slate-500 mt-2">Theo Báo cáo PCCC 2026 & TCVN 3890:2023</div>
                    </div>'''
    new_kpi_pccc = '''<div class="bg-white rounded-2xl shadow-sm border border-slate-200 p-6">
                        <div class="text-xs uppercase font-bold text-slate-400 mb-2">Phương tiện PCCC bổ sung</div>
                        <div class="text-2xl font-black text-blue-600">&lt;trống&gt;</div>
                        <div class="text-xs text-slate-500 mt-2">Chờ CN23 khảo sát và lập danh mục thực tế</div>
                    </div>'''
    content = content.replace(old_kpi_pccc, new_kpi_pccc)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated HTML v2 successfully!")

if __name__ == '__main__':
    update_html_v2()
