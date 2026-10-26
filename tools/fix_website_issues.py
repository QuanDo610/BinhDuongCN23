import os
import re
import html

def md_to_html(md_text):
    lines = md_text.split('\n')
    out = []
    in_table = False
    in_code = False
    in_list = False
    
    for line in lines:
        if line.startswith('```'):
            if in_code:
                out.append('</code></pre>')
                in_code = False
            else:
                out.append('<pre class="bg-slate-900 text-slate-100 p-4 rounded-xl overflow-x-auto my-3 text-xs leading-relaxed font-mono"><code>')
                in_code = True
            continue
        if in_code:
            out.append(html.escape(line) + '\n')
            continue
            
        # Table
        if line.startswith('|') and line.endswith('|'):
            if '---' in line:
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if not in_table:
                out.append('<div class="overflow-x-auto my-4 rounded-xl border border-slate-200 shadow-2xs"><table class="w-full text-xs text-left border-collapse bg-white">')
                out.append('<thead><tr class="bg-slate-100 font-bold text-slate-800 border-b border-slate-200">' + ''.join(f'<th class="p-2.5 border-r border-slate-200 last:border-r-0">{c}</th>' for c in cells) + '</tr></thead><tbody>')
                in_table = True
            else:
                out.append('<tr class="border-b border-slate-100 hover:bg-slate-50 transition">' + ''.join(f'<td class="p-2.5 border-r border-slate-100 last:border-r-0">{c}</td>' for c in cells) + '</tr>')
            continue
        else:
            if in_table:
                out.append('</tbody></table></div>')
                in_table = False

        # Lists
        if line.startswith('* ') or line.startswith('- ') or (len(line) > 2 and line[0].isdigit() and line[1:3] == '. '):
            if not in_list:
                out.append('<ul class="list-disc pl-5 my-2 space-y-1 text-xs text-slate-700 leading-relaxed">')
                in_list = True
            prefix_len = 3 if (line[0].isdigit() and line[1:3] == '. ') else 2
            content = line[prefix_len:].strip()
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-slate-900">\1</strong>', content)
            content = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" class="text-sky-600 hover:underline font-semibold">\1</a>', content)
            out.append(f'<li>{content}</li>')
            continue
        else:
            if in_list:
                out.append('</ul>')
                in_list = False

        if not line.strip():
            continue

        # Headings
        if line.startswith('# '):
            out.append(f'<h1 class="text-lg sm:text-xl font-black text-sky-900 border-b-2 border-slate-200 pb-2 mt-6 mb-3">{line[2:]}</h1>')
        elif line.startswith('## '):
            out.append(f'<h2 class="text-base sm:text-lg font-bold text-sky-800 border-b border-slate-200 pb-1.5 mt-5 mb-2.5">{line[3:]}</h2>')
        elif line.startswith('### '):
            out.append(f'<h3 class="text-sm sm:text-base font-bold text-slate-900 mt-4 mb-2">{line[4:]}</h3>')
        elif line.startswith('> '):
            quote_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-sky-950">\1</strong>', line[2:])
            out.append(f'<blockquote class="p-3 bg-sky-50/70 border-l-4 border-sky-600 rounded-r-xl text-xs text-sky-900 my-2">{quote_text}</blockquote>')
        elif line.startswith('---'):
            out.append('<hr class="my-4 border-slate-200">')
        else:
            p_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="font-bold text-slate-900">\1</strong>', line)
            p_text = re.sub(r'`(.*?)`', r'<code class="bg-slate-100 text-rose-600 px-1 py-0.5 rounded font-mono text-xs">\1</code>', p_text)
            p_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" class="text-sky-600 hover:underline font-semibold">\1</a>', p_text)
            out.append(f'<p class="text-xs sm:text-sm text-slate-700 leading-relaxed my-2">{p_text}</p>')

    if in_table: out.append('</tbody></table></div>')
    if in_list: out.append('</ul>')
    if in_code: out.append('</code></pre>')
    return '\n'.join(out)

# Read markdown files
with open('OUTPUT/PROGRESS_BINHDUONG.md', 'r', encoding='utf-8') as f:
    progress_raw = f.read()
progress_html = md_to_html(progress_raw)

with open('TASK_TRACKER.md', 'r', encoding='utf-8') as f:
    task_raw = f.read()
task_html = md_to_html(task_raw)

with open('LICH_SU_CONG_VIEC.md', 'r', encoding='utf-8') as f:
    history_raw = f.read()
history_html = md_to_html(history_raw)

# Read existing index.html to extract custom sections
with open('OUTPUT/index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

def extract_section_inner(section_id):
    pattern = rf'<section id=\"{section_id}\"[^>]*>(.*?)</section>'
    m = re.search(pattern, orig, re.DOTALL)
    if m:
        return m.group(1).strip()
    return ''

overview_inner = extract_section_inner('tab-overview')
inventory_inner = extract_section_inner('tab-inventory')
tntt_inner = extract_section_inner('tab-tntt')
inspection_inner = extract_section_inner('tab-inspection')
facility_inner = extract_section_inner('tab-facility')
network_inner = extract_section_inner('tab-network')
toner_inner = extract_section_inner('tab-toner')
proposal_inner = extract_section_inner('tab-proposal')
risk_inner = extract_section_inner('tab-risk')
event_inner = extract_section_inner('tab-event')

# Build the complete new index.html with ZERO KaTeX and STRICT SINGLE SYSTEM FONT
new_index_html = f'''<!DOCTYPE html>
<html lang="vi" class="h-full bg-slate-50">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bảng Tiến Độ & Quản Trị Hệ Thống IT - Chi Nhánh 23</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  
  <!-- Font Awesome CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  
  <style>
    /* ================= 1 FONT DUY NHẤT TOÀN DIỆN CHO WEBSITE (BROWSER SUPPORTED) ================= */
    *, html, body, button, input, select, textarea, table, th, td, p, span, h1, h2, h3, h4, h5, h6, a, div {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }}

    html {{
      background-color: #f8fafc;
      min-height: 100%;
      overscroll-behavior-y: none;
      -webkit-text-size-adjust: 100%;
    }}
    
    body {{
      background-color: #f8fafc;
      color: #0f172a;
      min-height: 100%;
      overscroll-behavior-y: none;
      margin: 0;
      padding: 0;
    }}
    
    /* Custom Scrollbars */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: #f1f5f9; }}
    ::-webkit-scrollbar-thumb {{ background: #cbd5e1; border-radius: 4px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: #94a3b8; }}
    
    /* Markdown body styles */
    .markdown-body {{
      color: #334155;
      line-height: 1.75;
      font-size: 0.875rem;
    }}
    .markdown-body h1, .markdown-body h2, .markdown-body h3, .markdown-body h4 {{
      color: #0f172a;
      font-weight: 700;
      margin-top: 1.5rem;
      margin-bottom: 0.75rem;
    }}
    .markdown-body table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1.25rem 0;
      border: 1px solid #cbd5e1;
      border-radius: 8px;
      overflow: hidden;
    }}
    .markdown-body th {{
      background-color: #f1f5f9;
      color: #0f172a;
      font-weight: 600;
      border: 1px solid #cbd5e1;
      padding: 8px 12px;
      text-align: left;
    }}
    .markdown-body td {{
      border: 1px solid #e2e8f0;
      padding: 8px 12px;
      text-align: left;
      color: #334155;
    }}
    .markdown-body tr:nth-child(even) {{ background-color: #f8fafc; }}
    .markdown-body tr:hover {{ background-color: #f0f9ff; }}

    /* Active Sidebar Link Style */
    .nav-item-active {{
      background: linear-gradient(to right, #eff6ff, #f0f9ff);
      color: #0284c7 !important;
      border-left: 4px solid #0284c7;
      font-weight: 700;
    }}
  </style>
</head>
<body class="flex flex-col min-h-screen antialiased bg-slate-50 text-slate-900">

  <!-- Mobile Sidebar Backdrop Overlay -->
  <div id="sidebar-overlay" onclick="toggleSidebar()" class="fixed inset-0 bg-slate-900/50 backdrop-blur-2xs z-40 hidden lg:hidden transition-opacity"></div>

  <!-- Wrapper Flex for Sidebar & Main Content -->
  <div class="flex-1 flex min-h-screen w-full bg-slate-50">

    <!-- ================= LEFT SIDEBAR NAVIGATION ================= -->
    <aside id="sidebar" class="fixed inset-y-0 left-0 z-50 w-72 bg-white border-r border-slate-200 flex flex-col transition-transform duration-300 transform -translate-x-full lg:translate-x-0 lg:static lg:inset-auto lg:h-screen lg:sticky lg:top-0 shrink-0 shadow-sm">
      
      <!-- Sidebar Brand Header -->
      <div class="p-5 border-b border-slate-100 flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/25 shrink-0">
            <i class="fa-solid fa-server text-base"></i>
          </div>
          <div class="min-w-0">
            <h1 class="text-sm font-extrabold text-slate-900 tracking-tight leading-tight truncate">CHI NHÁNH SỐ 23</h1>
            <p class="text-[11px] font-semibold text-sky-700 truncate">VP ĐĂNG KÝ ĐẤT ĐAI TP.HCM</p>
          </div>
        </div>
        <!-- Close Button Mobile -->
        <button onclick="toggleSidebar()" class="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>

      <!-- Quick Status Badge -->
      <div class="px-5 py-3 bg-slate-50/80 border-b border-slate-100 flex items-center justify-between text-xs">
        <span class="inline-flex items-center text-emerald-700 font-semibold">
          <span class="w-2 h-2 mr-2 bg-emerald-500 rounded-full animate-pulse"></span>
          Hệ Thống Trực Tuyến
        </span>
        <span class="text-[11px] text-slate-500 font-medium">Năm 2026</span>
      </div>

      <!-- Sidebar Scrollable Navigation Links -->
      <div class="flex-1 overflow-y-auto p-4 space-y-6">
        
        <!-- Nhóm 1: Quản Trị Thiết Bị & Kiểm Kê -->
        <div>
          <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Điều Hành & Số Liệu Thiết Bị
          </div>
          <div class="space-y-1">
            <button onclick="switchTab('tab-overview')" id="btn-tab-overview" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition nav-item-active">
              <i class="fa-solid fa-chart-pie w-5 text-sky-600 mr-2.5 text-sm"></i>
              <span>Tổng Quan Thiết Bị Đang Dùng</span>
            </button>
            
            <button onclick="switchTab('tab-inventory')" id="btn-tab-inventory" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-boxes-packing w-5 text-indigo-600 mr-2.5 text-sm"></i>
              <span>Kiểm Kê: Đang Dùng vs Thanh Lý</span>
            </button>
            
            <button onclick="switchTab('tab-network')" id="btn-tab-network" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-network-wired w-5 text-emerald-600 mr-2.5 text-sm"></i>
              <span>Phòng Server & Mạng IP</span>
            </button>
            
            <button onclick="switchTab('tab-toner')" id="btn-tab-toner" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-print w-5 text-amber-600 mr-2.5 text-sm"></i>
              <span>Tra Cứu Vật Tư & Mã Mực In</span>
            </button>
          </div>
        </div>

        <!-- Nhóm 2: Văn Bản & Chỉ Đạo Mới (Documents) -->
        <div>
          <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Chỉ Đạo & Quy Định Mới
          </div>
          <div class="space-y-1">
            <button onclick="switchTab('tab-tntt')" id="btn-tab-tntt" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-award w-5 text-amber-500 mr-2.5 text-sm"></i>
              <span>QĐ 78: Thu Nhập Tăng Thêm</span>
              <span class="ml-auto px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">Mới</span>
            </button>
            
            <button onclick="switchTab('tab-inspection')" id="btn-tab-inspection" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-scale-balanced w-5 text-rose-600 mr-2.5 text-sm"></i>
              <span>QĐ 9326: Kiểm Tra Công Vụ Sở</span>
              <span class="ml-auto px-1.5 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800">20/10</span>
            </button>

            <button onclick="switchTab('tab-facility')" id="btn-tab-facility" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-building-circle-check w-5 text-teal-600 mr-2.5 text-sm"></i>
              <span>Phương Án Trạm Y Tế 3 (NĐ 155)</span>
            </button>
            
            <button onclick="switchTab('tab-proposal')" id="btn-tab-proposal" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-file-invoice-dollar w-5 text-sky-600 mr-2.5 text-sm"></i>
              <span>Dự Toán Đề Xuất 752 Tr (CV 1342)</span>
            </button>

            <button onclick="switchTab('tab-risk')" id="btn-tab-risk" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-shield-halved w-5 text-purple-600 mr-2.5 text-sm"></i>
              <span>Quản Trị Rủi Ro & Pháp Lý</span>
            </button>
          </div>
        </div>

        <!-- Nhóm 3: Lịch Sử & Tài Liệu Toàn Văn -->
        <div>
          <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Lịch Sử & Báo Cáo Markdown
          </div>
          <div class="space-y-1">
            <button onclick="switchTab('tab-event')" id="btn-tab-event" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-calendar-check w-5 text-slate-500 mr-2.5 text-sm"></i>
              <span>Sự Kiện & Mốc Thời Gian (Đã qua)</span>
            </button>

            <button onclick="switchTab('tab-markdown')" id="btn-tab-markdown" class="nav-item w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-100 transition">
              <i class="fa-solid fa-file-lines w-5 text-sky-600 mr-2.5 text-sm"></i>
              <span>Báo Cáo Markdown Chi Tiết</span>
              <span class="ml-auto px-1.5 py-0.5 rounded text-[10px] font-bold bg-sky-100 text-sky-800">3 File</span>
            </button>
          </div>
        </div>

        <!-- Nhóm 4: Hệ Thống Tiện Ích & Liên Kết -->
        <div>
          <div class="px-3 mb-2 text-[11px] font-bold uppercase tracking-wider text-slate-400">
            Tiện Ích & Cổng Dịch Vụ
          </div>
          <div class="space-y-1">
            <a href="../documents/index.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
              <i class="fa-solid fa-folder-open w-5 text-amber-500 mr-2.5 text-sm"></i>
              <span>Kho 66 Tài Liệu Gốc</span>
              <i class="fa-solid fa-arrow-up-right-from-square ml-auto text-[10px] text-slate-400"></i>
            </a>

            <a href="document_viewer.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
              <i class="fa-solid fa-book-open w-5 text-indigo-500 mr-2.5 text-sm"></i>
              <span>Hồ Sơ Gốc Online (Viewer)</span>
            </a>

            <a href="../IT_HELPDESK/index.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
              <i class="fa-solid fa-headset w-5 text-blue-600 mr-2.5 text-sm"></i>
              <span>IT Helpdesk Trực Tuyến</span>
              <i class="fa-solid fa-arrow-up-right-from-square ml-auto text-[10px] text-slate-400"></i>
            </a>

            <a href="../A_THANG/index.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
              <i class="fa-solid fa-calendar-days w-5 text-emerald-600 mr-2.5 text-sm"></i>
              <span>Đăng Ký Lịch Tuần (A_THANG)</span>
            </a>

            <a href="orgchart.html" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-sky-50 hover:text-sky-700 transition">
              <i class="fa-solid fa-sitemap w-5 text-sky-600 mr-2.5 text-sm"></i>
              <span>Sơ Đồ Cơ Cấu Tổ Chức</span>
            </a>

            <a href="print_report.html" target="_blank" class="w-full flex items-center px-3 py-2.5 rounded-xl text-xs font-semibold text-slate-600 hover:bg-slate-100 transition">
              <i class="fa-solid fa-print w-5 text-slate-700 mr-2.5 text-sm"></i>
              <span>Trang In Báo Cáo PDF</span>
            </a>
          </div>
        </div>

      </div>

      <!-- Sidebar Footer -->
      <div class="p-4 border-t border-slate-200 bg-slate-50 text-[11px] text-slate-500 flex items-center justify-between">
        <span>Tổ CNTT - CN23</span>
        <span class="font-mono text-slate-400">v2.5.3</span>
      </div>
    </aside>

    <!-- ================= MAIN CONTENT WRAPPER ================= -->
    <div class="flex-1 flex flex-col min-w-0 bg-slate-50">
      
      <!-- Top Bar Header (Breadcrumb, Mobile Toggle, Quick Actions) -->
      <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-2xs px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between gap-4">
        <div class="flex items-center space-x-3 min-w-0">
          <!-- Toggle button for mobile -->
          <button onclick="toggleSidebar()" class="lg:hidden p-2 rounded-xl text-slate-600 hover:bg-slate-100 transition">
            <i class="fa-solid fa-bars text-lg"></i>
          </button>
          <div>
            <div class="flex items-center space-x-2 text-xs text-slate-400">
              <span>Chi Nhánh 23</span>
              <span>/</span>
              <span id="breadcrumb-title" class="font-semibold text-sky-700">Tổng Quan Thiết Bị Đang Dùng</span>
            </div>
            <h2 id="topbar-heading" class="text-base sm:text-lg font-bold text-slate-900 tracking-tight leading-tight truncate">
              Bảng Điều Hành & Quản Trị Hệ Thống IT
            </h2>
          </div>
        </div>

        <!-- Quick Action Buttons -->
        <div class="flex items-center space-x-2 shrink-0 text-xs">
          <a href="../documents/index.html" class="hidden sm:inline-flex items-center px-3 py-1.5 rounded-xl font-semibold bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 transition shadow-2xs">
            <i class="fa-solid fa-folder-open mr-1.5 text-amber-600"></i> Kho 66 Văn Bản
          </a>
          <a href="../IT_HELPDESK/index.html" class="hidden md:inline-flex items-center px-3 py-1.5 rounded-xl font-semibold bg-blue-50 hover:bg-blue-100 text-blue-800 border border-blue-200 transition shadow-2xs">
            <i class="fa-solid fa-headset mr-1.5 text-blue-600"></i> IT Helpdesk
          </a>
          <a href="print_report.html" target="_blank" class="inline-flex items-center px-3.5 py-1.5 rounded-xl font-semibold bg-slate-900 hover:bg-slate-800 text-white transition shadow-2xs">
            <i class="fa-solid fa-print mr-1.5"></i> Xuất PDF
          </a>
        </div>
      </header>

      <!-- Main Dynamic Content Area (Full Device Width) -->
      <main class="flex-1 p-4 sm:p-6 lg:p-8 w-full max-w-full pb-10">
        
        <!-- Tab 1: Overview -->
        <section id="tab-overview" class="tab-content block space-y-6">
          {overview_inner}
        </section>

        <!-- Tab 2: Inventory -->
        <section id="tab-inventory" class="tab-content hidden space-y-6">
          {inventory_inner}
        </section>

        <!-- Tab 3: TNTT (QĐ 78) -->
        <section id="tab-tntt" class="tab-content hidden space-y-6">
          {tntt_inner}
        </section>

        <!-- Tab 4: Inspection (QĐ 9326) -->
        <section id="tab-inspection" class="tab-content hidden space-y-6">
          {inspection_inner}
        </section>

        <!-- Tab 5: Facility (NĐ 155 & Trạm Y Tế 3) -->
        <section id="tab-facility" class="tab-content hidden space-y-6">
          {facility_inner}
        </section>

        <!-- Tab 6: Network -->
        <section id="tab-network" class="tab-content hidden space-y-6">
          {network_inner}
        </section>

        <!-- Tab 7: Toner -->
        <section id="tab-toner" class="tab-content hidden space-y-6">
          {toner_inner}
        </section>

        <!-- Tab 8: Proposal -->
        <section id="tab-proposal" class="tab-content hidden space-y-6">
          {proposal_inner}
        </section>

        <!-- Tab 9: Risk -->
        <section id="tab-risk" class="tab-content hidden space-y-6">
          {risk_inner}
        </section>

        <!-- Tab 10: Event (Lịch sử sự kiện đã qua) -->
        <section id="tab-event" class="tab-content hidden space-y-6">
          {event_inner}
        </section>

        <!-- Tab 11: Markdown (Báo cáo toàn văn - ĐÃ SỬA LỖI KHÔNG HIỂN THỊ) -->
        <section id="tab-markdown" class="tab-content hidden space-y-6">
          <div class="bg-white border border-slate-200 rounded-2xl p-6 shadow-xs space-y-5">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-3">
              <div>
                <h3 class="text-base sm:text-lg font-bold text-slate-900 flex items-center gap-2">
                  <i class="fa-solid fa-file-lines text-sky-600 text-xl"></i>
                  <span>Báo Cáo Kỹ Thuật & Tài Liệu Toàn Văn Markdown</span>
                </h3>
                <p class="text-xs text-slate-500 mt-0.5">Hiển thị nội dung đầy đủ các tài liệu tiến độ, bảng nhiệm vụ và lịch sử hệ thống</p>
              </div>

              <!-- Document Selectors -->
              <div class="flex flex-wrap items-center gap-2">
                <button onclick="renderMarkdownDoc('progress')" id="btn-doc-progress" class="doc-btn px-3 py-1.5 rounded-xl text-xs font-semibold bg-sky-600 text-white shadow-2xs transition">
                  <i class="fa-solid fa-file-waveform mr-1"></i> Tiến Độ IT (17KB)
                </button>
                <button onclick="renderMarkdownDoc('task')" id="btn-doc-task" class="doc-btn px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
                  <i class="fa-solid fa-list-check mr-1"></i> Bảng Nhiệm Vụ (Task)
                </button>
                <button onclick="renderMarkdownDoc('history')" id="btn-doc-history" class="doc-btn px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 transition">
                  <i class="fa-solid fa-clock-rotate-left mr-1"></i> Lịch Sử Công Việc
                </button>
              </div>
            </div>

            <!-- Pre-rendered Containers for Instant Zero-Delay Display -->
            <div id="markdown-display" class="markdown-body p-6 bg-slate-50/70 rounded-2xl border border-slate-200 overflow-x-auto">
              <!-- Render Target Default -->
              <div id="content-progress" class="doc-content block">
                {progress_html}
              </div>
              <div id="content-task" class="doc-content hidden">
                {task_html}
              </div>
              <div id="content-history" class="doc-content hidden">
                {history_html}
              </div>
            </div>

          </div>
        </section>

      </main>

      <!-- Footer (Fixed CSS to eliminate jumping and white gap) -->
      <footer class="w-full bg-white border-t border-slate-200 py-4 px-6 text-center text-xs text-slate-500 shrink-0 mt-auto">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>Hệ Thống Quản Trị Dữ Liệu IT & Điều Hành Tác Vụ - Chi Nhánh Số 23 (VPĐKĐĐ TP.HCM)</span>
          <span class="text-slate-400 font-mono">Phiên bản 2.5.3 &bull; Chuẩn 1 Font Hệ Thống Gốc</span>
        </div>
      </footer>

    </div>

  </div>

  <!-- ================= JAVASCRIPT LOGIC ================= -->
  <script>
    const tabTitles = {{
      'tab-overview': {{ breadcrumb: 'Tổng Quan Thiết Bị Đang Dùng', heading: 'Bảng Điều Hành & Quản Trị Hệ Thống IT' }},
      'tab-inventory': {{ breadcrumb: 'Kiểm Kê Thiết Bị', heading: 'Sổ Kiểm Kê: Thiết Bị Đang Hoạt Động vs Chờ Thanh Lý' }},
      'tab-tntt': {{ breadcrumb: 'Chỉ Đạo Mới / QĐ 78', heading: 'Quy Định Xếp Loại & Chi Thu Nhập Tăng Thêm (NQ 98)' }},
      'tab-inspection': {{ breadcrumb: 'Chỉ Đạo Mới / QĐ 9326', heading: 'Quyết Định Thành Lập Đoàn Kiểm Tra Công Vụ Năm 2026' }},
      'tab-facility': {{ breadcrumb: 'Cơ Sở Vật Chất / NĐ 155', heading: 'Phương Án Tiếp Nhận Trạm Y Tế Số 3 Mở Rộng Trụ Sở' }},
      'tab-network': {{ breadcrumb: 'Hạ Tầng / Mạng & Server', heading: 'Sơ Đồ Phòng Máy Chủ, Switch & Dải IP Chuyên Dùng' }},
      'tab-toner': {{ breadcrumb: 'Vật Tư / Hộp Mực In', heading: 'Bảng Tra Cứu Mã Hộp Mực Cho Toàn Bộ 38 Máy In Đang Dùng' }},
      'tab-proposal': {{ breadcrumb: 'Kinh Phí / Đề Xuất 1342', heading: 'Dự Toán Đề Xuất Bố Trí Kinh Phí IT 752.829.000 VNĐ' }},
      'tab-risk': {{ breadcrumb: 'Pháp Lý / Quản Trị Rủi Ro', heading: 'Báo Cáo Nhận Diện & Kiểm Soát Rủi Ro Kỹ Thuật IT' }},
      'tab-event': {{ breadcrumb: 'Lịch Sử / Sự Kiện Đã Qua', heading: 'Tiến Trình Sự Kiện & Biên Bản Bàn Giao Tháng 09 - 10/2026' }},
      'tab-markdown': {{ breadcrumb: 'Tài Liệu / Toàn Văn Markdown', heading: 'Báo Cáo Kỹ Thuật Hệ Thống & Toàn Văn Đề Xuất' }}
    }};

    function toggleSidebar() {{
      const sidebar = document.getElementById('sidebar');
      const overlay = document.getElementById('sidebar-overlay');
      const isClosed = sidebar.classList.contains('-translate-x-full');
      
      if (isClosed) {{
        sidebar.classList.remove('-translate-x-full');
        overlay.classList.remove('hidden');
      }} else {{
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
      }}
    }}

    function switchTab(tabId) {{
      // 1. Hide all tab contents
      document.querySelectorAll('.tab-content').forEach(el => {{
        el.classList.add('hidden');
        el.classList.remove('block');
      }});

      // 2. Remove active state from all sidebar nav items
      document.querySelectorAll('.nav-item').forEach(btn => {{
        btn.classList.remove('nav-item-active');
      }});

      // 3. Show selected tab content
      const targetContent = document.getElementById(tabId);
      if (targetContent) {{
        targetContent.classList.remove('hidden');
        targetContent.classList.add('block');
      }}

      // 4. Set active state on matching button
      const targetBtn = document.getElementById('btn-' + tabId);
      if (targetBtn) {{
        targetBtn.classList.add('nav-item-active');
      }}

      // 5. Update Breadcrumb and Topbar Title
      if (tabTitles[tabId]) {{
        document.getElementById('breadcrumb-title').textContent = tabTitles[tabId].breadcrumb;
        document.getElementById('topbar-heading').textContent = tabTitles[tabId].heading;
      }}

      // 6. Close sidebar on mobile after clicking
      if (window.innerWidth < 1024) {{
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebar-overlay');
        sidebar.classList.add('-translate-x-full');
        overlay.classList.add('hidden');
      }}

      // 7. Scroll smoothly to top
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}

    // Function to switch between markdown documents
    function renderMarkdownDoc(docType) {{
      document.querySelectorAll('.doc-content').forEach(el => {{
        el.classList.add('hidden');
        el.classList.remove('block');
      }});

      document.querySelectorAll('.doc-btn').forEach(btn => {{
        btn.className = 'doc-btn px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 transition';
      }});

      const target = document.getElementById('content-' + docType);
      const targetBtn = document.getElementById('btn-doc-' + docType);

      if (target) {{
        target.classList.remove('hidden');
        target.classList.add('block');
      }}
      if (targetBtn) {{
        targetBtn.className = 'doc-btn px-3 py-1.5 rounded-xl text-xs font-semibold bg-sky-600 text-white shadow-2xs transition';
      }}
    }}
  </script>
</body>
</html>
'''

with open('OUTPUT/index.html', 'w', encoding='utf-8') as f:
    f.write(new_index_html)

print("SUCCESS: OUTPUT/index.html updated with ZERO KaTeX and STRICT SINGLE SYSTEM FONT!")
