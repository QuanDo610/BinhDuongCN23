import re

with open('OUTPUT/Phuong_an_xin_kinh_phi_CN23_v2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace lines 1300-1356
pattern_src_chart = re.compile(
    r'<div class="p-3 bg-slate-50 rounded-xl">\s*<span class="font-bold block text-slate-800 mb-1">Quy cách kỹ thuật sàn mái</span>.*?'
    r'<!-- ================= TAB 4: BIỂU ĐỒ & PHÂN TÍCH ĐẤU THẦU ================= -->.*?'
    r'<div id="tab-chart-view" class="tab-content hidden">.*?</div>\s*</div>\s*</div>',
    re.DOTALL
)

replacement_src_chart = '''<div class="p-3 bg-slate-50 rounded-xl">
                            <span class="font-bold block text-slate-800 mb-1">Quy cách kỹ thuật sàn mái</span>
                            Màng khò nhiệt Bitumode Delta-P dày 3mm (mặt trơn) kết hợp lớp lót hệ nước Nirol-W (0,2 kg/m²). Khối lượng chuẩn: [...] m². Đơn giá: Chờ 03 bảng báo giá thực tế.
                        </div>
                        <div class="p-3 bg-slate-50 rounded-xl">
                            <span class="font-bold block text-slate-800 mb-1">Quy cách kỹ thuật tường</span>
                            Hóa chất đàn hồi kháng UV SikaCoat Plus lăn phủ 2 lớp (0,6 kg/m²) kết hợp Mastic trám khe nứt. Khối lượng chuẩn: [...] m². Đơn giá: Chờ 03 bảng báo giá thực tế.
                        </div>
                        <div class="p-3 bg-slate-50 rounded-xl">
                            <span class="font-bold block text-slate-800 mb-1">Khảo sát giá thị trường</span>
                            Chi nhánh số 23 đang thực hiện khảo sát và thu thập 03 bảng báo giá cạnh tranh theo đúng quy định. Số liệu kinh phí sẽ được hoàn thiện sau khi có báo giá chính thức.
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ================= TAB 4: TRẠNG THÁI & TIẾN ĐỘ THU THẬP BÁO GIÁ ================= -->
        <div id="tab-chart-view" class="tab-content hidden">
            <div class="max-w-4xl mx-auto space-y-6">
                <!-- Status Banner -->
                <div class="bg-amber-50 border border-amber-200 rounded-2xl p-6 flex items-start space-x-4">
                    <div class="w-12 h-12 rounded-xl bg-amber-500 text-white flex items-center justify-center font-bold text-xl flex-shrink-0">
                        ⏳
                    </div>
                    <div>
                        <h3 class="text-lg font-bold text-amber-900 mb-1">Trạng thái hồ sơ: Chờ kết quả khảo sát và 03 bảng báo giá thực tế của Chi nhánh 23</h3>
                        <p class="text-sm text-amber-800 leading-relaxed">
                            Toàn bộ các số liệu báo giá và tên nhà thầu trước đây (sao chép từ Chi nhánh 34 hoặc tự phân bổ) đã được làm sạch khỏi phương án. Theo quy định tại Rule.md và Luật Đấu thầu, các ô kinh phí được giữ nguyên cấu trúc biểu mẫu với trạng thái <code>[...]</code> để Chi nhánh 23 bổ sung sau khi thu thập đủ 03 báo giá thực tế trên địa bàn.
                        </p>
                    </div>
                </div>

                <!-- 3 Information Cards -->
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

content = pattern_src_chart.sub(replacement_src_chart, content, count=1)

# Now clean the script chart initialization
pattern_charts_js = re.compile(r'function initCharts\(\)\s*\{.*?\}\s*</script>', re.DOTALL)
clean_charts_js = '''function initCharts() {
            // Placeholder: Không vẽ biểu đồ ảo khi chưa có báo giá thực tế của Chi nhánh 23
        }
    </script>'''

content = pattern_charts_js.sub(clean_charts_js, content, count=1)

with open('OUTPUT/Phuong_an_xin_kinh_phi_CN23_v2.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated tabs and charts cleanly!")
