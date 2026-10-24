import re

def clean_all_html():
    file_path = 'OUTPUT/Phuong_an_xin_kinh_phi_CN23_v2.html'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Clean Top Header Stat Cards
    old_top_cards = re.compile(r'<!-- KPI Stats Cards -->\s*<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6 no-print">.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>', re.DOTALL)
    new_top_cards = '''<!-- KPI Stats Cards -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6 no-print">
            <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Tổng Dự Toán Kinh Phí</span>
                    <span class="p-2 bg-slate-100 text-slate-600 rounded-xl"><i data-lucide="calculator" class="w-5 h-5"></i></span>
                </div>
                <div class="text-2xl font-bold text-slate-800 tracking-tight">[Chờ 03 báo giá]</div>
                <p class="text-xs text-slate-500 mt-1">Đang khảo sát giá thị trường</p>
            </div>

            <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Tài Sản GĐ Mới Nhậm Chức</span>
                    <span class="p-2 bg-amber-50 text-amber-600 rounded-xl"><i data-lucide="user-check" class="w-5 h-5"></i></span>
                </div>
                <div class="text-2xl font-bold text-slate-800 tracking-tight">≤ 64.000.000 ₫</div>
                <p class="text-xs text-slate-500 mt-1">QĐ 8541 • Định mức trần QC 355</p>
            </div>

            <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Chống Thấm Trụ Sở</span>
                    <span class="p-2 bg-emerald-50 text-emerald-600 rounded-xl"><i data-lucide="shield-check" class="w-5 h-5"></i></span>
                </div>
                <div class="text-2xl font-bold text-slate-800 tracking-tight">[Chờ khảo sát]</div>
                <p class="text-xs text-slate-500 mt-1">Sàn mái & tường sê nô ([...] m²)</p>
            </div>

            <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 hover:shadow-md transition">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Thiết Bị PCCC Cơ Sở</span>
                    <span class="p-2 bg-rose-50 text-rose-600 rounded-xl"><i data-lucide="flame" class="w-5 h-5"></i></span>
                </div>
                <div class="text-2xl font-bold text-slate-800 tracking-tight">[Chờ báo giá]</div>
                <p class="text-xs text-slate-500 mt-1">26 bình & trang thiết bị PCCC cơ sở</p>
            </div>
        </div>'''
    content = old_top_cards.sub(new_top_cards, content, count=1)

    # 2. Clean tab-table-view (budgetTable tbody)
    # Replace the table rows in tab-table-view
    old_table_view_pattern = re.compile(r'<div id="tab-table-view" class="tab-content hidden">.*?<div id="tab-source-view"', re.DOTALL)
    
    clean_table_view = '''<div id="tab-table-view" class="tab-content hidden">
            <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-6">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
                    <div>
                        <h2 class="text-lg font-bold text-slate-800">Bảng Tổng Hợp Chi Tiết Danh Mục & Dự Toán Kinh Phí</h2>
                        <p class="text-xs text-slate-500 mt-0.5">Biểu mẫu chuẩn bị hồ sơ dự toán (Đơn giá và thành tiền để trống chờ 03 bảng báo giá cạnh tranh)</p>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table id="budgetTable" class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-100 text-slate-700 uppercase font-bold border-b border-slate-200">
                                <th class="p-3 text-center w-12">STT</th>
                                <th class="p-3">Danh Mục Hàng Hóa / Dịch Vụ</th>
                                <th class="p-3 text-center w-16">ĐVT</th>
                                <th class="p-3 text-center w-16">SL</th>
                                <th class="p-3 text-right w-24">Đơn Giá (₫)</th>
                                <th class="p-3 text-right w-28">Thành Tiền (₫)</th>
                                <th class="p-3 text-right w-24">VAT 8% (₫)</th>
                                <th class="p-3 text-right w-28">Tổng Sau VAT (₫)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100">
                            <!-- NHÓM A -->
                            <tr class="bg-amber-50/40 text-amber-950 font-bold">
                                <td class="p-3 text-center">A</td>
                                <td colspan="7" class="p-3">TRANG BỊ TÀI SẢN PHÒNG GIÁM ĐỐC MỚI NHẬM CHỨC (QĐ 8541 & QC 355)</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Bộ bàn ghế ngồi làm việc Giám đốc (Bàn lãnh đạo + Ghế xoay da)</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">2</td>
                                <td class="p-3 font-semibold text-slate-800">Tủ đựng tài liệu Giám đốc (Tủ gỗ 3 buồng có khóa)</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">3</td>
                                <td class="p-3 font-semibold text-slate-800">Máy vi tính để bàn làm việc (Core i7, RAM 16GB, SSD 512GB)</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">4</td>
                                <td class="p-3 font-semibold text-slate-800">Máy in laser đen trắng tự động 2 mặt khổ A4 mạng LAN</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">5</td>
                                <td class="p-3 font-semibold text-slate-800">Điện thoại bàn cố định hiển thị số</td>
                                <td class="p-3 text-center">Chiếc</td>
                                <td class="p-3 text-center">01</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">6</td>
                                <td class="p-3 font-semibold text-slate-800">Bộ bàn ghế họp, tiếp khách tại phòng Giám đốc (Bàn trà + Sofa da cao cấp)</td>
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
                                <td colspan="7" class="p-3">TRANG BỊ THIẾT BỊ PHÒNG CHÁY CHỮA CHÁY (THEO BÁO CÁO PCCC CN23 & TCVN 3890:2023)</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">1</td>
                                <td class="p-3 font-semibold text-slate-800">Bình chữa cháy bột ABC 4kg (MFZL4) có tem kiểm định PCCC</td>
                                <td class="p-3 text-center">Bình</td>
                                <td class="p-3 text-center">16</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">2</td>
                                <td class="p-3 font-semibold text-slate-800">Bình chữa cháy khí CO2 3kg (MT3) có tem kiểm định PCCC</td>
                                <td class="p-3 text-center">Bình</td>
                                <td class="p-3 text-center">10</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">3</td>
                                <td class="p-3 font-semibold text-slate-800">Kệ sắt để bình chữa cháy đôi sơn tĩnh điện</td>
                                <td class="p-3 text-center">Kệ</td>
                                <td class="p-3 text-center">13</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">4</td>
                                <td class="p-3 font-semibold text-slate-800">Bộ bảng nội quy và tiêu lệnh chữa cháy Mica</td>
                                <td class="p-3 text-center">Bộ</td>
                                <td class="p-3 text-center">06</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80">
                                <td class="p-3 text-center text-slate-400">5-9</td>
                                <td class="p-3 font-semibold text-slate-800">Đèn sự cố (6), Đèn Exit (6), Mặt nạ phòng độc (12), Túi y tế (2), Dụng cụ phá dỡ (2)</td>
                                <td class="p-3 text-center">Bộ/Cái</td>
                                <td class="p-3 text-center">--</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                                <td class="p-3 text-center text-slate-400">[...]</td>
                            </tr>
                            <tr class="bg-rose-100/40 font-bold text-rose-950">
                                <td class="p-3 text-center">Cộng C</td>
                                <td colspan="4" class="p-3">Tổng kinh phí trang bị phương tiện PCCC (C)</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                                <td class="p-3 text-center text-slate-500">[...]</td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr class="bg-slate-800 text-white font-bold text-sm">
                                <td colspan="5" class="p-3.5 uppercase">TỔNG CỘNG TOÀN BỘ PHƯƠNG ÁN (A + B + C):</td>
                                <td class="p-3.5 text-center">[...]</td>
                                <td class="p-3.5 text-center">[...]</td>
                                <td class="p-3.5 text-center">[...]</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
            </div>
        </div>

        <div id="tab-source-view"'''
    
    content = old_table_view_pattern.sub(clean_table_view, content, count=1)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Full HTML cleaned successfully!")

if __name__ == '__main__':
    clean_all_html()
