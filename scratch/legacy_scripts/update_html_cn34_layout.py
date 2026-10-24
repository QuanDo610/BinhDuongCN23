import re

# Read original HTML
with open('OUTPUT/Phuong_an_xin_kinh_phi_CN23_v1.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Build the new tab-doc-view content matching CN34 exactly
new_doc_view = '''id="tab-doc-view" class="tab-content block">
            <div class="bg-white rounded-2xl shadow-sm border border-slate-200/80 p-8 sm:p-12 max-w-4xl mx-auto print-page font-doc text-[13.5pt] leading-[1.35] text-black">
                
                <!-- ============================================================ -->
                <!-- PHẦN ĐẦU: MỤC LỤC & DANH MỤC BIỂU (Y CHANG MẪU CN34) -->
                <!-- KHÔNG CÓ TIÊU ĐỀ TIÊU NGỮ ĐẦU TRANG THEO ĐÚNG MẪU CN34 -->
                <!-- ============================================================ -->
                <div class="text-center font-bold text-[15pt] uppercase tracking-wide mb-6">MỤC LỤC</div>

                <div class="space-y-1.5 text-[11.5pt] mb-8">
                    <div class="flex items-baseline justify-between font-bold">
                        <span>MỤC ĐÍCH</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>1</span>
                    </div>
                    <div class="flex items-baseline justify-between font-bold pl-3">
                        <span>A. Giới thiệu chung về hoạt động của hệ thống Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>1</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>1. Căn cứ pháp lý</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>1</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>2. Vị trí, chức năng, nhiệm vụ, quyền hạn</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>3</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>3. Cơ cấu tổ chức</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>4</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>4. Chế độ làm việc</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>5</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>5. Các tổ chức chính trị, chính trị - xã hội</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>5</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>6. Số lượng viên chức, lao động hợp đồng</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>5</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>7. Trụ sở hoạt động</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>6</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>8. Về cơ chế tài chính</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>6</span>
                    </div>
                    <div class="flex items-baseline justify-between font-bold pl-3">
                        <span>B. Mục đích của phương án</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>7</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>1. Căn cứ xây dựng phương án</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>7</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>2. Việc xây dựng phương án nhằm các mục đích sau</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>8</span>
                    </div>
                    <div class="flex items-baseline justify-between font-bold mt-2">
                        <span>II. YÊU CẦU</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>9</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>1. Phạm vi thực hiện</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>9</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>2. Về công tác thi công và mua sắm trang thiết bị</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>9</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>3. Yêu cầu kỹ thuật đối với đơn vị cung cấp/thi công</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>11</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>4. Về nội dung chi phí thực hiện</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>12</span>
                    </div>
                    <div class="flex items-baseline justify-between font-bold mt-2">
                        <span>III. NỘI DUNG - KHỐI LƯỢNG & QUY TRÌNH THỰC HIỆN</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>12</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>1. Cơ sở pháp lý (Đấu thầu, Tài sản công, Thuế suất 8%)</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>12</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>2. Nội dung và khối lượng (Biểu 1)</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>13</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>3. Quy trình thực hiện (6 bước) & Trách nhiệm nghiệm thu</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>14</span>
                    </div>
                    <div class="flex items-baseline justify-between font-bold mt-2">
                        <span>IV. DỰ TOÁN KINH PHÍ</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>15</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>1. Dự toán kinh phí (Biểu 2: Bảng 8 cột so sánh 3 đơn vị)</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>15</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>2. Nguồn kinh phí (Quỹ Phát triển hoạt động sự nghiệp)</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>17</span>
                    </div>
                    <div class="flex items-baseline justify-between font-bold mt-2">
                        <span>IV. HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>17</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>1. Hồ sơ đính kèm (03 bảng báo giá)</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>17</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>2. Số lượng bản phương án dự toán ký chính (03 bản)</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>18</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>3. Lưu trữ hồ sơ</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>18</span>
                    </div>
                    <div class="flex items-baseline justify-between pl-6 text-slate-800">
                        <span>4. Số hóa hồ sơ</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>18</span>
                    </div>
                    <div class="flex items-baseline justify-between font-bold mt-2">
                        <span>Phụ lục 01: Bảng báo giá của 03 đơn vị cung cấp / thi công</span>
                        <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                        <span>19</span>
                    </div>
                </div>

                <div class="border-t border-slate-200 pt-4 mb-8">
                    <div class="text-center font-bold text-[13pt] uppercase mb-3">DANH MỤC BIỂU VÀ PHỤ LỤC</div>
                    <div class="space-y-1.5 text-[11.5pt]">
                        <div class="flex items-baseline justify-between">
                            <span>Biểu 1: Nội dung và khối lượng</span>
                            <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                            <span>13</span>
                        </div>
                        <div class="flex items-baseline justify-between">
                            <span>Biểu 2: Dự toán kinh phí sửa chữa chống thấm và trang bị tài sản</span>
                            <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                            <span>15</span>
                        </div>
                        <div class="flex items-baseline justify-between">
                            <span>Phụ lục 01: Bảng báo giá của 03 đơn vị cung cấp / thi công</span>
                            <span class="flex-grow border-b border-dotted border-slate-400 mx-2"></span>
                            <span>19</span>
                        </div>
                    </div>
                </div>

                <!-- Dải phân cách trang Word -->
                <div class="my-8 border-t-2 border-dashed border-slate-300 relative text-center">
                    <span class="bg-white px-3 text-xs text-slate-400 -top-2.5 relative italic">--- Bắt đầu nội dung Phương án (Trang 1) ---</span>
                </div>

                <!-- ============================================================ -->
                <!-- NỘI DUNG CHÍNH THEO BỘ KHUNG CHUẨN CN34 -->
                <!-- ============================================================ -->
                <div class="text-[12pt] font-bold text-slate-900 mb-6 space-y-0.5">
                    <div>Chủ quản: Sở Nông nghiệp và Môi trường</div>
                    <div>Đơn vị: Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh</div>
                    <div>Mã số QHNS: 1122149</div>
                </div>

                <div class="text-center my-6">
                    <div class="text-[15pt] font-bold uppercase tracking-tight">PHƯƠNG ÁN DỰ TOÁN</div>
                    <div class="text-[13pt] font-bold mt-2 max-w-2xl mx-auto leading-snug">
                        Công tác: “Trang bị tài sản làm việc cho Giám đốc Chi nhánh mới nhậm chức theo Quyết định số 8541/QĐ-SNNMT-VP và Quy chế chi tiêu nội bộ số 355; sửa chữa chống thấm trụ sở và trang bị thiết bị phòng cháy, chữa cháy tại Chi nhánh Văn phòng Đăng ký đất đai số 23”
                    </div>
                </div>

                <!-- I. MỤC ĐÍCH -->
                <div class="mb-6">
                    <div class="font-bold uppercase text-[14pt] text-slate-900 mb-2">MỤC ĐÍCH</div>
                    
                    <div class="font-bold text-[13pt] text-slate-800 mb-2">A. Giới thiệu chung về hoạt động của hệ thống Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh:</div>
                    
                    <div class="font-bold text-[13pt] mt-3 mb-1">1. Căn cứ pháp lý</div>
                    <div class="italic text-[12.5pt] font-semibold text-slate-700 mb-1">Luật Đất đai và các Nghị định, Thông tư hướng dẫn</div>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Luật Đất đai số 31/2024/QH15 được sửa đổi bổ sung một số điều theo Luật số 43/2024/QH15;</li>
                        <li>Nghị định số 101/2024/NĐ-CP ngày 29/7/2024 của Chính phủ quy định về điều tra cơ bản đất đai; đăng ký, cấp giấy chứng nhận quyền sử dụng đất, quyền sở hữu tài sản gắn liền với đất và hệ thống thông tin đất đai;</li>
                        <li>Nghị định số 102/2024/NĐ-CP ngày 30/7/2024 của Chính phủ quy định chi tiết thi hành một số điều của Luật Đất đai;</li>
                        <li>Nghị định số 151/2025/NĐ-CP ngày 12/6/2025 của Chính phủ về phân định thẩm quyền của chính quyền địa phương 02 cấp;</li>
                        <li>Nghị định số 226/2025/NĐ-CP ngày 15/8/2025 sửa đổi, bổ sung các Nghị định quy định chi tiết Luật Đất đai;</li>
                        <li>Thông tư số 08/2024/TT-BTNMT, Thông tư số 10/2024/TT-BTNMT và Thông tư số 23/2025/TT-BTNMT.</li>
                    </ul>

                    <div class="italic text-[12.5pt] font-semibold text-slate-700 mt-3 mb-1">a/ Văn bản về cơ chế của đơn vị sự nghiệp công lập</div>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Nghị định số 60/2021/NĐ-CP ngày 21/6/2021 của Chính phủ quy định cơ chế tự chủ tài chính của đơn vị sự nghiệp công lập;</li>
                        <li>Nghị định số 106/2020/NĐ-CP ngày 10/9/2020 về vị trí việc làm và số lượng người làm việc;</li>
                        <li>Nghị định số 120/2020/NĐ-CP, Nghị định số 111/2022/NĐ-CP, Nghị định số 111/2025/NĐ-CP; Thông tư số 56/2022/TT-BTC.</li>
                    </ul>

                    <div class="italic text-[12.5pt] font-semibold text-slate-700 mt-3 mb-1">b/ Văn bản về thành lập, ban hành Quy chế tổ chức và hoạt động</div>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Quyết định số 1886/QĐ-UBND ngày 01/10/2025 của UBND Thành phố về tổ chức lại Văn phòng Đăng ký đất đai TP.HCM trên cơ sở hợp nhất TP.HCM, tỉnh Bình Dương và tỉnh Bà Rịa – Vũng Tàu;</li>
                        <li>Quyết định số 2637/QĐ-SNNMT-VP ngày 15/12/2025 của Giám đốc Sở Nông nghiệp và Môi trường ban hành Quy định chức năng, nhiệm vụ, quyền hạn và cơ cấu tổ chức của Chi nhánh Văn phòng Đăng ký đất đai số 23.</li>
                    </ul>

                    <div class="italic text-[12.5pt] font-semibold text-slate-700 mt-3 mb-1">c/ Văn bản về quy chế tài chính</div>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Quyết định số 2882/QĐ-SNNMT-KHTC ngày 29/12/2025, Quyết định số 792/QĐ-SNNMT-KHTC, QĐ số 805, QĐ số 907 và QĐ số 1020/QĐ-SNNMT-KHTC ngày 04/3/2026 của Sở NN&MT giao chỉ tiêu dự toán;</li>
                        <li><strong>Quyết định số 355/QĐ-VPĐK-KHTC ngày 23/01/2026</strong> của Giám đốc Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh ban hành Quy chế chi tiêu nội bộ, quản lý và sử dụng tài sản công (sửa đổi theo QĐ 2162/QĐ-VPĐK-KHTC ngày 04/6/2026);</li>
                        <li><strong>Quyết định số 8541/QĐ-SNNMT-VP ngày 30/9/2026</strong> của Sở Nông nghiệp và Môi trường bổ nhiệm Giám đốc Chi nhánh số 23 đối với ông Nguyễn Chiến Thắng từ ngày 01/10/2026.</li>
                    </ul>

                    <div class="italic text-[12.5pt] font-semibold text-slate-700 mt-3 mb-1">d/ Văn bản về định mức kinh tế kỹ thuật</div>
                    <p class="text-justify text-[12.5pt] indent-6">Thông tư số 03/2022/TT-BTNMT ngày 28/02/2022 và Thông tư số 136/2017/TT-BTC ngày 22/12/2017 của Bộ Tài chính.</p>

                    <div class="font-bold text-[13pt] mt-4 mb-1">2. Vị trí, chức năng, nhiệm vụ, quyền hạn</div>
                    <p class="text-justify text-[12.5pt] indent-6">Chi nhánh Văn phòng đăng ký đất đai số 23 là đơn vị sự nghiệp công lập trực thuộc Văn phòng đăng ký đất đai Thành phố Hồ Chí Minh, có tư cách pháp nhân, có con dấu riêng và được mở tài khoản theo quy định; thực hiện chức năng đăng ký đất đai, nhà ở và tài sản gắn liền với đất; xây dựng, quản lý, cập nhật, chỉnh lý hồ sơ địa chính và cơ sở dữ liệu đất đai trên địa bàn phụ trách.</p>

                    <div class="font-bold text-[13pt] mt-4 mb-2">3. Cơ cấu tổ chức</div>
                    <div class="overflow-x-auto my-3">
                        <table class="w-full border-collapse border border-black text-[11.5pt]">
                            <thead>
                                <tr class="bg-slate-100 font-bold text-center">
                                    <th class="border border-black p-2 w-12">Stt</th>
                                    <th class="border border-black p-2 w-64">Cơ cấu tổ chức</th>
                                    <th class="border border-black p-2">Nhiệm vụ chủ yếu</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center"></td>
                                    <td class="border border-black p-2" colspan="2">CHI NHÁNH VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23:</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center font-bold">1</td>
                                    <td class="border border-black p-2 font-bold">Ban Giám đốc</td>
                                    <td class="border border-black p-2 text-justify">01 Giám đốc (ông Nguyễn Chiến Thắng - bổ nhiệm theo QĐ số 8541/QĐ-SNNMT-VP ngày 30/9/2026). 01 Phó Giám đốc (ông Đặng Huy Cường). Chỉ đạo, điều hành toàn bộ hoạt động của Chi nhánh.</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center font-bold">2</td>
                                    <td class="border border-black p-2 font-bold">Tổ Hành chính - Tổng hợp</td>
                                    <td class="border border-black p-2 text-justify">Tổ trưởng: bà Nguyễn Thị Bích Tuyền. Thực hiện công tác văn thư lưu trữ, tài chính kế toán, hành chính quản trị, quản lý cơ sở vật chất, PCCC.</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center font-bold">3</td>
                                    <td class="border border-black p-2 font-bold">Tổ Đăng ký và Cấp GCN</td>
                                    <td class="border border-black p-2 text-justify">Thực hiện đăng ký đất đai, cấp Giấy chứng nhận quyền sử dụng đất, tài sản gắn liền với đất theo phân cấp thẩm quyền.</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center font-bold">4</td>
                                    <td class="border border-black p-2 font-bold">Tổ Kỹ thuật địa chính và Lưu trữ</td>
                                    <td class="border border-black p-2 text-justify">Thực hiện kiểm tra nội nghiệp bản vẽ trích đo, trích lục địa chính, chỉnh lý cơ sở dữ liệu và bảo quản, số hóa kho hồ sơ địa chính.</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="font-bold text-[13pt] mt-4 mb-1">4. Chế độ làm việc:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Chi nhánh Văn phòng đăng ký đất đai số 23 làm việc theo nguyên tắc tập trung dân chủ, thực hiện chế độ thủ trưởng; bảo đảm sự lãnh đạo của Đảng, sự chỉ đạo, điều hành của Văn phòng Đăng ký đất đai Thành phố Hồ Chí Minh, tuân thủ quy định của pháp luật và Quy chế làm việc. Giám đốc là thủ trưởng, người đứng đầu, chịu trách nhiệm trước Giám đốc Sở Nông nghiệp và Môi trường, Giám đốc Văn phòng Đăng ký đất đai Thành phố và trước pháp luật về kết quả hoạt động của Chi nhánh.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">5. Các tổ chức chính trị, chính trị - xã hội:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Chi bộ Chi nhánh Văn phòng đăng ký đất đai số 23 trực thuộc Đảng bộ Sở Nông nghiệp và Môi trường Thành phố Hồ Chí Minh; Công đoàn bộ phận trực thuộc Công đoàn cơ sở Văn phòng Đăng ký đất đai Thành phố.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">6. Số lượng viên chức, lao động hợp đồng:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Căn cứ Quyết định số 480/QĐ-VPĐK-HC ngày 12/02/2026 của Giám đốc Văn phòng Đăng ký đất đai Thành phố, số lượng người làm việc tại Chi nhánh là <strong>85 người</strong>, bao gồm: Ban Giám đốc: 02 người; Tổ Hành chính – Tổng hợp: 14 người (07 viên chức, 07 lao động); Kế toán: 01 người; Tổ Đăng ký và Cấp GCN: 28 người (09 viên chức, 19 lao động); Tổ Kỹ thuật địa chính và Lưu trữ: 37 người (14 viên chức, 23 lao động); Nhân viên bảo vệ, tạp vụ: 03 người.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">7. Trụ sở hoạt động:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Trụ sở chính đặt tại <strong>số 358 đường Huỳnh Văn Cù, phường Thủ Dầu Một, Thành phố Hồ Chí Minh</strong> (khuôn viên đất quản lý 1.417,7 m², diện tích sàn xây dựng 835,3 m² theo Biên bản bàn giao ngày 09/5/2019 và Công văn số 1656/CN23-HCTH). Hiện trạng sàn mái, mương sê nô bị nứt nẻ, bong tróc gây thấm dột ẩm mốc xuống trần nhà và kho lưu trữ tài liệu địa chính; phòng làm việc của Giám đốc mới nhậm chức chưa có trang thiết bị đạt chuẩn; hệ thống PCCC cơ sở cần bổ sung kiểm định.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">8. Về cơ chế tài chính:</div>
                    <p class="text-justify text-[12.5pt] indent-6"><strong>8.1.</strong> Chi nhánh thực hiện cơ chế tự chủ tài chính theo Nghị định số 60/2021/NĐ-CP theo loại hình đơn vị tự bảo đảm chi phí hoạt động thường xuyên (nhóm 2).<br>
                    <strong>8.2. Nguồn tài chính sử dụng:</strong> Quỹ Phát triển hoạt động sự nghiệp của đơn vị theo đúng quy định tại Nghị định 60/2021/NĐ-CP và Quy chế chi tiêu nội bộ 355.</p>

                    <div class="font-bold text-[13pt] text-slate-800 mt-6 mb-2">B. Mục đích của phương án:</div>
                    <div class="font-bold text-[13pt] mt-2 mb-1">1. Căn cứ xây dựng phương án</div>
                    <p class="text-justify text-[12.5pt] indent-6">Căn cứ Quyết định bổ nhiệm Giám đốc số 8541/QĐ-SNNMT-VP ngày 30/9/2026; Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC ngày 23/01/2026 (Mục VII, VIII và Phụ lục B); Công văn số 1656/CN23-HCTH về hiện trạng trụ sở 358 Huỳnh Văn Cù; Kế hoạch PCCC số 26/BC-CN23 và Công văn 24482/VPĐK-KT của Văn phòng Đăng ký đất đai Thành phố.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">2. Việc xây dựng phương án nhằm các mục đích sau:</div>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Trang bị đồng bộ bàn ghế, máy móc thiết bị làm việc đạt chuẩn theo đúng định mức cho Giám đốc mới nhậm chức theo Quyết định số 8541/QĐ-SNNMT-VP phục vụ công tác chỉ đạo, điều hành kịp thời;</li>
                        <li>Xử lý dứt điểm hiện trạng thấm dột, nứt nẻ sàn mái và tường trụ sở, bảo vệ an toàn cho 85 viên chức, người lao động và bảo quản tuyệt đối an toàn kho lưu trữ hồ sơ tài liệu địa chính gốc;</li>
                        <li>Bổ sung trang bị và kiểm định phương tiện PCCC định kỳ, đáp ứng đầy đủ quy định pháp luật về PCCC và cứu nạn, cứu hộ;</li>
                        <li>Quản lý, sử dụng nguồn kinh phí Quỹ Phát triển hoạt động sự nghiệp đúng mục đích, tiết kiệm, công khai, minh bạch và hiệu quả cao;</li>
                        <li>Làm cơ sở để lập dự toán, kế hoạch lựa chọn nhà thầu và tổ chức đấu thầu/chỉ định thầu theo đúng quy định.</li>
                    </ul>
                </div>

                <!-- II. YÊU CẦU -->
                <div class="mb-6">
                    <div class="font-bold uppercase text-[14pt] text-slate-900 mb-2">II. YÊU CẦU</div>
                    
                    <div class="font-bold text-[13pt] mt-2 mb-1">1. Phạm vi thực hiện:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Thực hiện tại Trụ sở Chi nhánh Văn phòng Đăng ký đất đai số 23 (358 Huỳnh Văn Cù, P. Thủ Dầu Một), bao gồm: (A) Sửa chữa chống thấm sàn mái diện tích 357,43 m² và tường 285,38 m²; (B) Trang bị tài sản phòng Giám đốc; (C) Bổ sung phương tiện PCCC.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">2. Về công tác thi công và mua sắm trang thiết bị:</div>
                    <p class="text-justify text-[12.5pt] indent-6"><strong>2.1. Chống thấm sàn mái bằng màng khò nhiệt Bitumode Delta – P 3mm:</strong> Vệ sinh sạch bề mặt, quét lót Nirol-W (0.2kg/m²), dán màng khò nóng Bitumode Delta 3mm giáp mí 10cm, bo góc chân tường 45 độ.<br>
                    <strong>2.2. Chống thấm tường sàn mái bằng SikaCoat Plus:</strong> Cạo bỏ sơn cũ rêu mốc, vá nứt bằng Mastic dẻo, lăn 2 lớp SikaCoat Plus kháng tia UV (0.6kg/m²).<br>
                    <strong>2.3. Trang bị tài sản Giám đốc:</strong> Đúng chủng loại, thông số kỹ thuật, bảo hành chính hãng tối thiểu 12-24 tháng, trong định mức tối đa 64.000.000 đồng theo Quy chế 355.<br>
                    <strong>2.4. Trang bị phương tiện PCCC:</strong> Bình bột ABC, bình CO2, tiêu lệnh, kệ đôi, đèn sự cố, đèn Exit có tem kiểm định an toàn PCCC của Bộ Công an.<br>
                    <strong>2.5. Nguyên tắc thực hiện:</strong> Thực hiện trọn gói, đảm bảo tiết kiệm, chống thất thoát, không làm gián đoạn công tác tiếp dân và giải quyết hồ sơ.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">3. Yêu cầu kỹ thuật đối với đơn vị cung cấp/thi công:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Vật tư, vật liệu có xuất xứ rõ ràng (CO/CQ); thiết bị máy móc đầy đủ; nhân lực thi công có chứng chỉ an toàn lao động; bảo đảm vệ sinh môi trường, an toàn phòng cháy chữa cháy, bảo vệ an toàn hồ sơ địa chính trong quá trình thi công.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">4. Về nội dung chi phí thực hiện:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Căn cứ khảo sát giá thị trường và thu thập 03 bảng báo giá cạnh tranh độc lập của các đơn vị cung cấp/thi công chuyên nghiệp.</p>
                </div>

                <!-- III. NỘI DUNG - KHỐI LƯỢNG & QUY TRÌNH THỰC HIỆN -->
                <div class="mb-6">
                    <div class="font-bold uppercase text-[14pt] text-slate-900 mb-2">III. NỘI DUNG - KHỐI LƯỢNG & QUY TRÌNH THỰC HIỆN</div>

                    <div class="font-bold text-[13pt] mt-2 mb-1">1. Cơ sở pháp lý</div>
                    <p class="text-justify text-[12.5pt] indent-6"><strong>1.1. Văn bản quy định về đấu thầu:</strong> Luật Đấu thầu số 22/2023/QH15; Nghị định số 214/2025/NĐ-CP ngày 04/8/2025 quy định chi tiết thi hành Luật Đấu thầu. Căn cứ khoản 4 Điều 78 Nghị định số 214/2025/NĐ-CP, các gói thầu dịch vụ phi tư vấn và mua sắm hàng hóa thuộc dự toán mua sắm thường xuyên có giá gói thầu nằm trong hạn mức quy định được áp dụng hình thức chỉ định thầu rút gọn. Hợp đồng áp dụng hình thức hợp đồng trọn gói.<br>
                    <strong>1.2. Luật Quản lý, sử dụng tài sản công:</strong> Luật số 15/2017/QH14; Thông tư số 65/2021/TT-BTC quy định về bảo dưỡng, sửa chữa tài sản công; Quyết định 355/QĐ-VPĐK-KHTC.<br>
                    <strong>1.3. Thuế suất:</strong> Áp dụng mức thuế suất thuế GTGT 8% theo chính sách giảm thuế giá trị gia tăng của Chính phủ (Nghị định 174/2025/NĐ-CP và Nghị định 72/2024/NĐ-CP).<br>
                    <strong>1.4. Mẫu biểu sử dụng:</strong> Theo Nghị định 214/2025/NĐ-CP, Nghị định 11/2020/NĐ-CP và Thông tư 24/2024/TT-BTC.</p>

                    <div class="font-bold text-[13pt] mt-4 mb-2">2. Nội dung và khối lượng (Biểu 1)</div>
                    <div class="overflow-x-auto my-3">
                        <table class="w-full border-collapse border border-black text-[11pt]">
                            <thead>
                                <tr class="bg-slate-100 font-bold text-center">
                                    <th class="border border-black p-2 w-12">STT</th>
                                    <th class="border border-black p-2">NỘI DUNG CÔNG VIỆC</th>
                                    <th class="border border-black p-2 w-20">ĐVT</th>
                                    <th class="border border-black p-2 w-28">KHỐI LƯỢNG</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">A</td>
                                    <td class="border border-black p-2" colspan="3">Chống thấm sàn mái, sê nô mái, mương đón nước mái tôn bằng màng Bitumode Delta – P 3mm</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">- Tạo nhám bề mặt bằng máy mài, vệ sinh sạch bề mặt.<br>- Quét 1 lớp lót Nirol – W (0.2kg/m²).<br>- Dán màng khò nóng Bitumode Delta – P 3mm (Mặt trơn).</td>
                                    <td class="border border-black p-2 text-center">m²</td>
                                    <td class="border border-black p-2 text-right font-semibold">357.43</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">B</td>
                                    <td class="border border-black p-2" colspan="3">Chống thấm tường sàn mái, tường sê nô bằng SikaCoat Plus</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">- Cạo bỏ sơn cũ, rêu mốc, vệ sinh sạch bề mặt.<br>- Trét vá vết nứt bằng Mastic dẻo.<br>- Lăn 2 lớp SikaCoat Plus kháng tia UV (0.6kg/m²).</td>
                                    <td class="border border-black p-2 text-center">m²</td>
                                    <td class="border border-black p-2 text-right font-semibold">285.38</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">C</td>
                                    <td class="border border-black p-2" colspan="3">Trang bị tài sản phòng Giám đốc mới nhậm chức (QĐ 8541 & QC 355)</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">Bộ bàn ghế ngồi làm việc Giám đốc (Gỗ tự nhiên cao cấp)</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">2</td>
                                    <td class="border border-black p-2">Bàn để máy vi tính và máy in chuyên dụng</td>
                                    <td class="border border-black p-2 text-center">Cái</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">3</td>
                                    <td class="border border-black p-2">Ghế xoay lãnh đạo cao cấp bọc da tự nhiên chân tay gỗ</td>
                                    <td class="border border-black p-2 text-center">Cái</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">4</td>
                                    <td class="border border-black p-2">Bộ bàn ghế tiếp khách (Sofa da cao cấp, 1 băng dài + 2 đơn + bàn trà)</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">5</td>
                                    <td class="border border-black p-2">Tủ đựng tài liệu lãnh đạo 4 buồng cánh kính - gỗ</td>
                                    <td class="border border-black p-2 text-center">Cái</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">6</td>
                                    <td class="border border-black p-2">Máy vi tính để bàn cấu hình cao (Core i7, RAM 16GB, SSD 512GB)</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">7</td>
                                    <td class="border border-black p-2">Máy in laser đa chức năng 2 mặt tự động tốc độ cao</td>
                                    <td class="border border-black p-2 text-center">Cái</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">8</td>
                                    <td class="border border-black p-2">Máy quét tài liệu (Scanner) màu 2 mặt tốc độ cao</td>
                                    <td class="border border-black p-2 text-center">Cái</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">9</td>
                                    <td class="border border-black p-2">Bộ lưu điện dự phòng (UPS 1500VA/900W)</td>
                                    <td class="border border-black p-2 text-center">Cái</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">10</td>
                                    <td class="border border-black p-2">Máy điều hòa không khí Inverter 2.0 HP tiết kiệm điện</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">01</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-2 text-center">D</td>
                                    <td class="border border-black p-2" colspan="3">Trang bị phương tiện phòng cháy chữa cháy (PCCC)</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">1</td>
                                    <td class="border border-black p-2">Bình bột chữa cháy ABC 4kg MFZL4 có tem kiểm định</td>
                                    <td class="border border-black p-2 text-center">Bình</td>
                                    <td class="border border-black p-2 text-right font-semibold">15</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">2</td>
                                    <td class="border border-black p-2">Bình khí chữa cháy CO2 5kg MT5 có tem kiểm định</td>
                                    <td class="border border-black p-2 text-center">Bình</td>
                                    <td class="border border-black p-2 text-right font-semibold">10</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">3</td>
                                    <td class="border border-black p-2">Bộ nội quy PCCC và tiêu lệnh chữa cháy</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">10</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">4</td>
                                    <td class="border border-black p-2">Kệ đôi đựng bình chữa cháy sắt sơn tĩnh điện</td>
                                    <td class="border border-black p-2 text-center">Cái</td>
                                    <td class="border border-black p-2 text-right font-semibold">12</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">5</td>
                                    <td class="border border-black p-2">Đèn chiếu sáng sự cố khẩn cấp gắn tường</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">08</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-2 text-center">6</td>
                                    <td class="border border-black p-2">Đèn Exit chỉ dẫn thoát nạn tự động</td>
                                    <td class="border border-black p-2 text-center">Bộ</td>
                                    <td class="border border-black p-2 text-right font-semibold">06</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <div class="font-bold text-[13pt] mt-4 mb-1">3. Quy trình thực hiện (sắp xếp theo thứ tự thực hiện):</div>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li><strong>Bước 1: Khảo sát và thu thập báo giá:</strong> Chi nhánh Văn phòng Đăng ký đất đai số 23 khảo sát thực tế và thu thập đủ 03 báo giá cạnh tranh.</li>
                        <li><strong>Bước 2: Lập, thẩm định và trình duyệt phương án dự toán:</strong> Chi nhánh lập phương án, Phòng Kế hoạch – Tài chính Văn phòng Đăng ký đất đai Thành phố thẩm định và trình Thủ trưởng phê duyệt.</li>
                        <li><strong>Bước 3: Lập, thẩm định và phê duyệt kế hoạch lựa chọn nhà thầu:</strong> Lập và trình duyệt kế hoạch lựa chọn nhà thầu theo quy định của Luật Đấu thầu.</li>
                        <li><strong>Bước 4: Quyết định lựa chọn nhà thầu:</strong> Hoàn tất thủ tục chỉ định thầu rút gọn, thương thảo hoàn thiện hợp đồng, ban hành Quyết định phê duyệt kết quả.</li>
                        <li><strong>Bước 5: Ký kết, thực hiện hợp đồng và kiểm tra nghiệm thu:</strong> Chi nhánh ký kết hợp đồng, giám sát thi công, bàn giao thiết bị và lập Biên bản nghiệm thu.</li>
                        <li><strong>Bước 6: Thanh quyết toán kinh phí:</strong> Lập hồ sơ đề nghị thanh toán gửi Phòng Kế hoạch – Tài chính kiểm soát và thực hiện thủ tục giải ngân kinh phí.</li>
                    </ul>

                    <div class="font-bold text-[13pt] mt-3 mb-1">3.2 Trách nhiệm trong công tác kiểm tra nghiệm thu:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Chi nhánh Văn phòng Đăng ký đất đai số 23 và Tổ Hành chính – Tổng hợp chịu trách nhiệm về tính chính xác của số lượng, khối lượng và chất lượng hàng hóa/dịch vụ trên biên bản nghiệm thu. Hồ sơ thanh toán gồm Hợp đồng, Biên bản nghiệm thu, Hóa đơn điện tử hợp lệ (thuế suất 8%) và các chứng từ liên quan.</p>
                </div>

                <!-- IV. DỰ TOÁN KINH PHÍ -->
                <div class="mb-6">
                    <div class="font-bold uppercase text-[14pt] text-slate-900 mb-2">IV. DỰ TOÁN KINH PHÍ</div>
                    
                    <div class="font-bold text-[13pt] mt-2 mb-1">1. Dự toán kinh phí</div>
                    <p class="text-justify text-[12.5pt] indent-6">Căn cứ 03 bảng báo giá đã bao gồm VAT 8% của các đơn vị cung cấp dịch vụ và cung ứng hàng hóa (đính kèm), dự toán kinh phí đề xuất lựa chọn đơn vị có giá thấp nhất, đáp ứng đầy đủ yêu cầu kỹ thuật như sau (Biểu 2):</p>

                    <!-- Biểu 2 Bảng 8 cột tóm tắt -->
                    <div class="overflow-x-auto my-3">
                        <table class="w-full border-collapse border border-black text-[10pt]">
                            <thead>
                                <tr class="bg-slate-100 font-bold text-center">
                                    <th class="border border-black p-2" colspan="2" rowspan="2">Nội dung thực hiện theo Tổ Hành chính – Tổng hợp đã thẩm định</th>
                                    <th class="border border-black p-2 bg-emerald-50 text-emerald-900" colspan="2">ĐƠN VỊ ĐỀ XUẤT CHỌN (1)</th>
                                    <th class="border border-black p-2" colspan="2">ĐƠN VỊ BÁO GIÁ 2</th>
                                    <th class="border border-black p-2" colspan="2">ĐƠN VỊ BÁO GIÁ 3</th>
                                </tr>
                                <tr class="bg-slate-100 font-bold text-center">
                                    <th class="border border-black p-1 bg-emerald-50 w-20">Đơn giá</th>
                                    <th class="border border-black p-1 bg-emerald-50 w-24">Thành tiền</th>
                                    <th class="border border-black p-1 w-20">Đơn giá</th>
                                    <th class="border border-black p-1 w-24">Thành tiền</th>
                                    <th class="border border-black p-1 w-20">Đơn giá</th>
                                    <th class="border border-black p-1 w-24">Thành tiền</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-1.5 text-center">I</td>
                                    <td class="border border-black p-1.5">SỬA CHỮA CHỐNG THẤM TRỤ SỞ CHI NHÁNH 23</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty Toàn Đạt</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty Vạn Đạt</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty Kim Bảo Phát</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">1</td>
                                    <td class="border border-black p-1">Chống thấm sàn mái Bitumode Delta 3mm (357.43m²)</td>
                                    <td class="border border-black p-1 text-right">303.250</td>
                                    <td class="border border-black p-1 text-right font-semibold">108.390.648</td>
                                    <td class="border border-black p-1 text-right">336.640</td>
                                    <td class="border border-black p-1 text-right">120.325.235</td>
                                    <td class="border border-black p-1 text-right">357.835</td>
                                    <td class="border border-black p-1 text-right">127.900.964</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">2</td>
                                    <td class="border border-black p-1">Chống thấm tường SikaCoat Plus (285.38m²)</td>
                                    <td class="border border-black p-1 text-right">233.000</td>
                                    <td class="border border-black p-1 text-right font-semibold">66.493.540</td>
                                    <td class="border border-black p-1 text-right">250.960</td>
                                    <td class="border border-black p-1 text-right">71.618.965</td>
                                    <td class="border border-black p-1 text-right">274.940</td>
                                    <td class="border border-black p-1 text-right">78.462.377</td>
                                </tr>
                                <tr class="font-bold bg-amber-50">
                                    <td class="border border-black p-1 text-center"></td>
                                    <td class="border border-black p-1">Cộng chống thấm sau thuế VAT 8%</td>
                                    <td class="border border-black p-1" colspan="2"><span class="text-emerald-700 font-bold">188.834.923</span></td>
                                    <td class="border border-black p-1" colspan="2">207.299.736</td>
                                    <td class="border border-black p-1" colspan="2">222.872.408</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-1.5 text-center">II</td>
                                    <td class="border border-black p-1.5">TRANG BỊ TÀI SẢN PHÒNG GIÁM ĐỐC MỚI (QĐ 8541 & QC 355)</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty SG Office</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty Nam Phát</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty Toàn Cầu</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">1</td>
                                    <td class="border border-black p-1">Bộ bàn ghế Giám đốc gỗ tự nhiên</td>
                                    <td class="border border-black p-1 text-right">10.000.000</td>
                                    <td class="border border-black p-1 text-right font-semibold">10.000.000</td>
                                    <td class="border border-black p-1 text-right">10.300.000</td>
                                    <td class="border border-black p-1 text-right">10.300.000</td>
                                    <td class="border border-black p-1 text-right">10.600.000</td>
                                    <td class="border border-black p-1 text-right">10.600.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">2</td>
                                    <td class="border border-black p-1">Bàn để máy vi tính và máy in</td>
                                    <td class="border border-black p-1 text-right">1.851.852</td>
                                    <td class="border border-black p-1 text-right font-semibold">1.851.852</td>
                                    <td class="border border-black p-1 text-right">1.900.000</td>
                                    <td class="border border-black p-1 text-right">1.900.000</td>
                                    <td class="border border-black p-1 text-right">2.000.000</td>
                                    <td class="border border-black p-1 text-right">2.000.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">3</td>
                                    <td class="border border-black p-1">Ghế xoay lãnh đạo bọc da cao cấp</td>
                                    <td class="border border-black p-1 text-right">2.777.778</td>
                                    <td class="border border-black p-1 text-right font-semibold">2.777.778</td>
                                    <td class="border border-black p-1 text-right">2.850.000</td>
                                    <td class="border border-black p-1 text-right">2.850.000</td>
                                    <td class="border border-black p-1 text-right">2.950.000</td>
                                    <td class="border border-black p-1 text-right">2.950.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">4</td>
                                    <td class="border border-black p-1">Bộ bàn ghế tiếp khách (Sofa da cao cấp)</td>
                                    <td class="border border-black p-1 text-right">8.333.333</td>
                                    <td class="border border-black p-1 text-right font-semibold">8.333.333</td>
                                    <td class="border border-black p-1 text-right">8.600.000</td>
                                    <td class="border border-black p-1 text-right">8.600.000</td>
                                    <td class="border border-black p-1 text-right">8.900.000</td>
                                    <td class="border border-black p-1 text-right">8.900.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">5</td>
                                    <td class="border border-black p-1">Tủ đựng tài liệu 4 buồng</td>
                                    <td class="border border-black p-1 text-right">4.629.630</td>
                                    <td class="border border-black p-1 text-right font-semibold">4.629.630</td>
                                    <td class="border border-black p-1 text-right">4.750.000</td>
                                    <td class="border border-black p-1 text-right">4.750.000</td>
                                    <td class="border border-black p-1 text-right">4.900.000</td>
                                    <td class="border border-black p-1 text-right">4.900.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">6</td>
                                    <td class="border border-black p-1">Máy vi tính để bàn cấu hình cao</td>
                                    <td class="border border-black p-1 text-right">13.888.889</td>
                                    <td class="border border-black p-1 text-right font-semibold">13.888.889</td>
                                    <td class="border border-black p-1 text-right">14.250.000</td>
                                    <td class="border border-black p-1 text-right">14.250.000</td>
                                    <td class="border border-black p-1 text-right">14.650.000</td>
                                    <td class="border border-black p-1 text-right">14.650.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">7</td>
                                    <td class="border border-black p-1">Máy in đa chức năng 2 mặt tự động</td>
                                    <td class="border border-black p-1 text-right">4.629.630</td>
                                    <td class="border border-black p-1 text-right font-semibold">4.629.630</td>
                                    <td class="border border-black p-1 text-right">4.780.000</td>
                                    <td class="border border-black p-1 text-right">4.780.000</td>
                                    <td class="border border-black p-1 text-right">4.950.000</td>
                                    <td class="border border-black p-1 text-right">4.950.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">8</td>
                                    <td class="border border-black p-1">Máy quét tài liệu (Scanner) màu 2 mặt</td>
                                    <td class="border border-black p-1 text-right">4.166.667</td>
                                    <td class="border border-black p-1 text-right font-semibold">4.166.667</td>
                                    <td class="border border-black p-1 text-right">4.300.000</td>
                                    <td class="border border-black p-1 text-right">4.300.000</td>
                                    <td class="border border-black p-1 text-right">4.450.000</td>
                                    <td class="border border-black p-1 text-right">4.450.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">9</td>
                                    <td class="border border-black p-1">Bộ lưu điện dự phòng (UPS 1500VA)</td>
                                    <td class="border border-black p-1 text-right">1.851.852</td>
                                    <td class="border border-black p-1 text-right font-semibold">1.851.852</td>
                                    <td class="border border-black p-1 text-right">1.920.000</td>
                                    <td class="border border-black p-1 text-right">1.920.000</td>
                                    <td class="border border-black p-1 text-right">2.000.000</td>
                                    <td class="border border-black p-1 text-right">2.000.000</td>
</tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">10</td>
                                    <td class="border border-black p-1">Máy điều hòa nhiệt độ Inverter 2.0 HP</td>
                                    <td class="border border-black p-1 text-right">7.129.628</td>
                                    <td class="border border-black p-1 text-right font-semibold">7.129.628</td>
                                    <td class="border border-black p-1 text-right">7.300.000</td>
                                    <td class="border border-black p-1 text-right">7.300.000</td>
                                    <td class="border border-black p-1 text-right">7.580.000</td>
                                    <td class="border border-black p-1 text-right">7.580.000</td>
                                </tr>
                                <tr class="font-bold bg-amber-50">
                                    <td class="border border-black p-1 text-center"></td>
                                    <td class="border border-black p-1">Cộng tài sản Giám đốc sau thuế VAT 8%</td>
                                    <td class="border border-black p-1" colspan="2"><span class="text-emerald-700 font-bold">64.000.000</span></td>
                                    <td class="border border-black p-1" colspan="2">65.826.000</td>
                                    <td class="border border-black p-1" colspan="2">67.802.400</td>
                                </tr>
                                <tr class="font-bold bg-slate-50">
                                    <td class="border border-black p-1.5 text-center">III</td>
                                    <td class="border border-black p-1.5">TRANG BỊ PHƯƠNG TIỆN PHÒNG CHÁY CHỮA CHÁY (PCCC)</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty PCCC Đông Á</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty PCCC Bình Dương</td>
                                    <td class="border border-black p-1.5 text-center" colspan="2">Cty PCCC Nam Á</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">1</td>
                                    <td class="border border-black p-1">Bình bột ABC 4kg (15 bình)</td>
                                    <td class="border border-black p-1 text-right">310.000</td>
                                    <td class="border border-black p-1 text-right font-semibold">4.650.000</td>
                                    <td class="border border-black p-1 text-right">330.000</td>
                                    <td class="border border-black p-1 text-right">4.950.000</td>
                                    <td class="border border-black p-1 text-right">350.000</td>
                                    <td class="border border-black p-1 text-right">5.250.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">2</td>
                                    <td class="border border-black p-1">Bình CO2 5kg MT5 (10 bình)</td>
                                    <td class="border border-black p-1 text-right">920.000</td>
                                    <td class="border border-black p-1 text-right font-semibold">9.200.000</td>
                                    <td class="border border-black p-1 text-right">980.000</td>
                                    <td class="border border-black p-1 text-right">9.800.000</td>
                                    <td class="border border-black p-1 text-right">1.020.000</td>
                                    <td class="border border-black p-1 text-right">10.200.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">3</td>
                                    <td class="border border-black p-1">Bộ nội quy, tiêu lệnh PCCC (10 bộ)</td>
                                    <td class="border border-black p-1 text-right">140.000</td>
                                    <td class="border border-black p-1 text-right font-semibold">1.400.000</td>
                                    <td class="border border-black p-1 text-right">155.000</td>
                                    <td class="border border-black p-1 text-right">1.550.000</td>
                                    <td class="border border-black p-1 text-right">165.000</td>
                                    <td class="border border-black p-1 text-right">1.650.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">4</td>
                                    <td class="border border-black p-1">Kệ đôi đựng bình chữa cháy (12 cái)</td>
                                    <td class="border border-black p-1 text-right">170.000</td>
                                    <td class="border border-black p-1 text-right font-semibold">2.040.000</td>
                                    <td class="border border-black p-1 text-right">190.000</td>
                                    <td class="border border-black p-1 text-right">2.280.000</td>
                                    <td class="border border-black p-1 text-right">205.000</td>
                                    <td class="border border-black p-1 text-right">2.460.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">5</td>
                                    <td class="border border-black p-1">Đèn chiếu sáng sự cố khẩn cấp (8 bộ)</td>
                                    <td class="border border-black p-1 text-right">280.000</td>
                                    <td class="border border-black p-1 text-right font-semibold">2.240.000</td>
                                    <td class="border border-black p-1 text-right">305.000</td>
                                    <td class="border border-black p-1 text-right">2.440.000</td>
                                    <td class="border border-black p-1 text-right">325.000</td>
                                    <td class="border border-black p-1 text-right">2.600.000</td>
                                </tr>
                                <tr>
                                    <td class="border border-black p-1 text-center">6</td>
                                    <td class="border border-black p-1">Đèn Exit chỉ dẫn thoát nạn (6 bộ)</td>
                                    <td class="border border-black p-1 text-right">293.333</td>
                                    <td class="border border-black p-1 text-right font-semibold">1.760.000</td>
                                    <td class="border border-black p-1 text-right">322.500</td>
                                    <td class="border border-black p-1 text-right">1.935.000</td>
                                    <td class="border border-black p-1 text-right">347.500</td>
                                    <td class="border border-black p-1 text-right">2.085.000</td>
                                </tr>
                                <tr class="font-bold bg-amber-50">
                                    <td class="border border-black p-1 text-center"></td>
                                    <td class="border border-black p-1">Cộng thiết bị PCCC sau thuế VAT 8%</td>
                                    <td class="border border-black p-1" colspan="2"><span class="text-emerald-700 font-bold">22.993.200</span></td>
                                    <td class="border border-black p-1" colspan="2">24.791.400</td>
                                    <td class="border border-black p-1" colspan="2">26.076.600</td>
                                </tr>
                                <tr class="font-bold bg-slate-200 text-black">
                                    <td class="border border-black p-1.5 text-center" colspan="2">TỔNG CỘNG TRƯỚC THUẾ (I + II + III):</td>
                                    <td class="border border-black p-1.5 text-right" colspan="2">255.393.447</td>
                                    <td class="border border-black p-1.5 text-right" colspan="2">275.849.200</td>
                                    <td class="border border-black p-1.5 text-right" colspan="2">293.288.341</td>
                                </tr>
                                <tr class="font-bold bg-slate-200 text-black">
                                    <td class="border border-black p-1.5 text-center" colspan="2">THUẾ GTGT 8%:</td>
                                    <td class="border border-black p-1.5 text-right" colspan="2">20.434.676</td>
                                    <td class="border border-black p-1.5 text-right" colspan="2">22.067.936</td>
                                    <td class="border border-black p-1.5 text-right" colspan="2">23.463.067</td>
                                </tr>
                                <tr class="font-bold bg-emerald-600 text-white text-[10.5pt]">
                                    <td class="border border-black p-2 text-center" colspan="2">TỔNG DỰ TOÁN KINH PHÍ ĐỀ XUẤT CẤP (SAU THUẾ):</td>
                                    <td class="border border-black p-2 text-right" colspan="2">275.828.123</td>
                                    <td class="border border-black p-2 text-right opacity-80" colspan="2">297.917.136</td>
                                    <td class="border border-black p-2 text-right opacity-80" colspan="2">316.751.408</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <p class="text-justify text-[12.5pt] indent-6 mt-3">
                        Như vậy, dự toán tính theo báo giá đã bao gồm VAT thấp nhất là: <strong>275.828.123 đồng</strong> <em>(Số tiền bằng chữ: Hai trăm bảy mươi lăm triệu, tám trăm hai mươi tám nghìn, một trăm hai mươi ba đồng./)</em>, trong đó:
                    </p>
                    <ul class="list-disc pl-6 space-y-1 text-justify text-[12.5pt]">
                        <li>Giá dịch vụ và thiết bị chưa thuế: <strong>255.393.447 đồng</strong>;</li>
                        <li>Thuế GTGT (8%): <strong>20.434.676 đồng</strong>;</li>
                        <li>Trong đó dự toán đề nghị cấp kinh phí từ Quỹ Phát triển hoạt động sự nghiệp cho Chi nhánh số 23: <strong>275.828.123 đồng</strong>.</li>
                    </ul>

                    <div class="font-bold text-[13pt] mt-3 mb-1">2. Nguồn kinh phí:</div>
                    <p class="text-justify text-[12.5pt] indent-6">Quỹ Phát triển hoạt động sự nghiệp của Chi nhánh Văn phòng Đăng ký đất đai số 23 theo quy định tại Nghị định số 60/2021/NĐ-CP và Quy chế chi tiêu nội bộ số 355/QĐ-VPĐK-KHTC.</p>

                    <!-- Khung ký Chi nhánh 23 (Table 3 y chang CN34) -->
                    <div class="grid grid-cols-2 gap-4 mt-8 pt-4 border-t border-slate-300 text-center">
                        <div>
                            <div class="font-bold uppercase text-[12.5pt]">NGƯỜI LẬP</div>
                            <div class="italic text-[11.5pt] text-slate-600">Tổ Hành chính – Tổng hợp</div>
                            <div class="h-24"></div>
                            <div class="font-bold text-[12.5pt]">Nguyễn Thị Bích Tuyền</div>
                        </div>
                        <div>
                            <div class="font-bold uppercase text-[12.5pt]">CN VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI SỐ 23 LẬP DỰ TOÁN</div>
                            <div class="font-bold uppercase text-[12.5pt]">GIÁM ĐỐC</div>
                            <div class="h-24"></div>
                            <div class="font-bold text-[12.5pt]">Nguyễn Chiến Thắng</div>
                        </div>
                    </div>
                </div>

                <!-- IV. HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ (y chang CN34) -->
                <div class="mb-6 mt-8">
                    <div class="font-bold uppercase text-[14pt] text-slate-900 mb-2">IV. HỒ SƠ ĐÍNH KÈM VÀ PHÂN CÔNG LƯU TRỮ HỒ SƠ</div>
                    
                    <div class="font-bold text-[13pt] mt-2 mb-1">1. Hồ sơ đính kèm:</div>
                    <p class="text-justify text-[12.5pt] indent-6">03 bảng báo giá thuê đơn vị thi công sửa chữa chống thấm; 03 bảng báo giá trang bị tài sản phòng Giám đốc; 03 bảng báo giá cung ứng phương tiện PCCC: Bản chính.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">2. Số lượng bản phương án dự toán ký chính: 03 bản.</div>

                    <div class="font-bold text-[13pt] mt-3 mb-1">3. Lưu trữ hồ sơ:</div>
                    <p class="text-justify text-[12.5pt] indent-6">a/ 01 Bản phương án ký chính + Bản chính hồ sơ đính kèm: Lưu tại Phòng Kế hoạch Tài chính kèm Quyết định phê duyệt phương án do bộ phận thẩm định dự toán lưu.<br>
                    b/ 02 bản phương án ký chính + Bản chụp hồ sơ đính kèm: Trả về bộ phận thực hiện kèm Quyết định phê duyệt phương án, trong đó 01 bản chính sẽ chuyển kèm về Phòng Kế hoạch - Tài chính trong hồ sơ thanh toán đợt đầu.</p>

                    <div class="font-bold text-[13pt] mt-3 mb-1">4. Số hóa hồ sơ:</div>
                    <p class="text-justify text-[12.5pt] indent-6">4.1 Bộ phận thực hiện số hóa toàn bộ hồ sơ liên quan phương án dự toán, công tác ký thủ tục hợp đồng và kiểm tra nghiệm thu, chuyển về Phòng Kế hoạch Tài chính tại lần thanh toán cuối cùng. Phòng Kế hoạch Tài chính số hóa tiếp tục hồ sơ thanh quyết toán./.</p>

                    <!-- Chữ ký phê duyệt 3 cấp cấp trên y chang CN34 -->
                    <div class="text-right italic text-[12.5pt] my-6">Thành phố Hồ Chí Minh, ngày 13 tháng 10 năm 2026</div>

                    <div class="space-y-8 text-center mt-6">
                        <div>
                            <div class="font-bold uppercase text-[13pt]">PHÊ DUYỆT CỦA PHÓ GIÁM ĐỐC PHỤ TRÁCH</div>
                            <div class="font-bold uppercase text-[12pt] text-slate-600">(CƠ SỞ 1)</div>
                            <div class="h-20"></div>
                            <div class="font-bold text-[13pt]">Đặng Huy Cường</div>
                        </div>

                        <div>
                            <div class="font-bold uppercase text-[13pt]">ĐƠN VỊ THẨM ĐỊNH: PHÒNG KẾ HOẠCH TÀI CHÍNH THẨM ĐỊNH</div>
                            <div class="grid grid-cols-2 max-w-lg mx-auto font-bold uppercase text-[12pt] mt-1">
                                <div>CHUYÊN VIÊN</div>
                                <div>TRƯỞNG PHÒNG</div>
                            </div>
                            <div class="h-20"></div>
                            <div class="grid grid-cols-2 max-w-lg mx-auto font-bold text-[12.5pt]">
                                <div>Đào Vân Anh</div>
                                <div>(Ký duyệt)</div>
                            </div>
                        </div>

                        <div>
                            <div class="font-bold uppercase text-[13pt]">DUYỆT CỦA GIÁM ĐỐC VĂN PHÒNG ĐĂNG KÝ ĐẤT ĐAI<br>THÀNH PHỐ HỒ CHÍ MINH</div>
                            <div class="h-24"></div>
                            <div class="font-bold text-[13pt]">Bùi Thị Bích Tuyền</div>
                        </div>
                    </div>
                </div>

                <!-- Dải phân cách trang Word -->
                <div class="my-8 border-t-2 border-dashed border-slate-300 relative text-center">
                    <span class="bg-white px-3 text-xs text-slate-400 -top-2.5 relative italic">--- Phụ lục đính kèm (Trang 19) ---</span>
                </div>

                <!-- ============================================================ -->
                <!-- PHỤ LỤC 1: Y CHANG MẪU CN34 -->
                <!-- ============================================================ -->
                <div class="text-center font-bold text-[14pt] mb-1">Phụ lục 1</div>
                <div class="text-center font-bold text-[13pt] mb-1">Bảng báo giá của 03 công ty thi công sửa chữa chống thấm và cung ứng thiết bị</div>
                <div class="text-center italic text-[11.5pt] mb-4">Đơn vị tính: đồng</div>

                <!-- Bảng Phụ lục 1 Table 4 y chang CN34 -->
                <div class="overflow-x-auto my-3">
                    <table class="w-full border-collapse border border-black text-[10pt]">
                        <thead>
                            <tr class="bg-slate-100 font-bold text-center">
                                <th class="border border-black p-2 w-10" rowspan="2">STT</th>
                                <th class="border border-black p-2 w-48" rowspan="2">Tên đơn vị cung cấp dịch vụ</th>
                                <th class="border border-black p-2" colspan="2">Chống thấm sàn mái Bitumode Delta 3mm (357.43m²)</th>
                                <th class="border border-black p-2" colspan="2">Chống thấm tường SikaCoat Plus (285.38m²)</th>
                                <th class="border border-black p-2 w-28" rowspan="2">Tổng cộng</th>
                                <th class="border border-black p-2 w-32" rowspan="2">Tổng cộng sau thuế (VAT 8%)</th>
                            </tr>
                            <tr class="bg-slate-100 font-bold text-center">
                                <th class="border border-black p-1 w-20">Đơn giá</th>
                                <th class="border border-black p-1 w-24">Thành tiền</th>
                                <th class="border border-black p-1 w-20">Đơn giá</th>
                                <th class="border border-black p-1 w-24">Thành tiền</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="bg-emerald-50">
                                <td class="border border-black p-2 text-center font-bold">1</td>
                                <td class="border border-black p-2 font-bold text-emerald-900">Công ty TNHH Đầu tư Phát triển Toàn Đạt</td>
                                <td class="border border-black p-2 text-right">303.250</td>
                                <td class="border border-black p-2 text-right">108.390.648</td>
                                <td class="border border-black p-2 text-right">233.000</td>
                                <td class="border border-black p-2 text-right">66.493.540</td>
                                <td class="border border-black p-2 text-right font-semibold">174.844.188</td>
                                <td class="border border-black p-2 text-right font-bold text-emerald-700">188.834.923</td>
                            </tr>
                            <tr>
                                <td class="border border-black p-2 text-center font-bold">2</td>
                                <td class="border border-black p-2 font-medium">Công ty TNHH Xây dựng Vạn Đạt</td>
                                <td class="border border-black p-2 text-right">336.640</td>
                                <td class="border border-black p-2 text-right">120.325.235</td>
                                <td class="border border-black p-2 text-right">250.960</td>
                                <td class="border border-black p-2 text-right">71.618.965</td>
                                <td class="border border-black p-2 text-right font-semibold">191.944.200</td>
                                <td class="border border-black p-2 text-right font-semibold">207.299.736</td>
                            </tr>
                            <tr>
                                <td class="border border-black p-2 text-center font-bold">3</td>
                                <td class="border border-black p-2 font-medium">Công ty TNHH Chống thấm và Xây dựng Kim Bảo Phát</td>
                                <td class="border border-black p-2 text-right">357.835</td>
                                <td class="border border-black p-2 text-right">127.900.964</td>
                                <td class="border border-black p-2 text-right">274.940</td>
                                <td class="border border-black p-2 text-right">78.462.377</td>
                                <td class="border border-black p-2 text-right font-semibold">206.363.341</td>
                                <td class="border border-black p-2 text-right font-semibold">222.872.408</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <div class="font-bold text-[13pt] mt-4 mb-1">Nhận xét:</div>
                <p class="text-justify text-[12.5pt] indent-6">
                    Qua khảo sát giá thị trường thông qua 03 báo giá của các đơn vị cung cấp dịch vụ sửa chữa chống thấm, chống dột. Mức giá đề xuất lựa chọn là <strong>188.834.923 đồng</strong>, là mức giá thấp nhất, phù hợp với khả năng tài chính của đơn vị và đảm bảo đầy đủ hạng mục thi công và tiết kiệm, hiệu quả theo quy định.
                </p>
            </div>
        </div>'''

# Replace tab-doc-view in html
pattern = r'id="tab-doc-view" class="tab-content block">.*?</div>\s*</div>\s*(?=<div id="tab-table-view")'
match = re.search(pattern, html, flags=re.DOTALL)
if match:
    new_html = html[:match.start()] + new_doc_view + "\n\n        <!-- " + html[match.end():]
    # fix the start of tab-table-view if needed
    new_html = re.sub(r'<!--\s*(<div id="tab-table-view")', r'\1', new_html)
else:
    # try direct replacement
    idx1 = html.find('id="tab-doc-view"')
    idx2 = html.find('id="tab-table-view"')
    # find closing of tab-doc-view before tab-table-view
    prev_div = html.rfind('</div>', idx1, idx2)
    prev_div2 = html.rfind('</div>', idx1, prev_div)
    new_html = html[:idx1] + new_doc_view + "\n\n        <div " + html[idx2:]

with open('OUTPUT/Phuong_an_xin_kinh_phi_CN23_v1.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

with open('OUTPUT/Phuong_an_xin_kinh_phi_CN23_v2.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Updated successfully: OUTPUT/Phuong_an_xin_kinh_phi_CN23_v1.html and v2.html")
