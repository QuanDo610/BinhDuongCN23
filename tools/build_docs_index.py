import os
import json
import urllib.parse

doc_dir = 'documents'
files = []
for f in sorted(os.listdir(doc_dir)):
    if f.startswith('.') or f.startswith('~$') or f == 'index.html':
        continue
    if 'Quân' in f or 'Quan' in f or 'mau HĐTV 02 tháng (1).docx' in f:
        continue
    path = os.path.join(doc_dir, f)
    if os.path.isfile(path):
        size_bytes = os.path.getsize(path)
        if size_bytes >= 1024 * 1024:
            size_str = f'{size_bytes / (1024 * 1024):.1f} MB'
        elif size_bytes >= 1024:
            size_str = f'{size_bytes / 1024:.1f} KB'
        else:
            size_str = f'{size_bytes} B'
        ext = os.path.splitext(f)[1].lower()
        files.append({'name': f, 'size': size_str, 'size_bytes': size_bytes, 'ext': ext})

cards_html = []
for item in files:
    name = item['name']
    ext = item['ext']
    size = item['size']
    encoded_name = urllib.parse.quote(name)
    
    if ext == '.pdf':
        type_class = 'pdf'
        badge_color = 'bg-rose-50 text-rose-700 border-rose-200'
        icon = 'fa-file-pdf text-rose-600'
        open_action = f'<a href="{encoded_name}" target="_blank" class="px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-rose-50 hover:bg-rose-100 text-rose-700 transition inline-flex items-center gap-1"><i class="fa-solid fa-arrow-up-right-from-square"></i> Mở Xem</a>'
    elif ext in ['.doc', '.docx']:
        type_class = 'docx'
        badge_color = 'bg-blue-50 text-blue-700 border-blue-200'
        icon = 'fa-file-word text-blue-600'
        open_action = f'<a href="{encoded_name}" download class="px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-blue-50 hover:bg-blue-100 text-blue-700 transition inline-flex items-center gap-1"><i class="fa-solid fa-download"></i> Tải Về</a>'
    elif ext in ['.xls', '.xlsx']:
        type_class = 'xlsx'
        badge_color = 'bg-emerald-50 text-emerald-700 border-emerald-200'
        icon = 'fa-file-excel text-emerald-600'
        open_action = f'<a href="{encoded_name}" download class="px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-emerald-50 hover:bg-emerald-100 text-emerald-700 transition inline-flex items-center gap-1"><i class="fa-solid fa-download"></i> Tải Về</a>'
    else:
        type_class = 'other'
        badge_color = 'bg-slate-50 text-slate-700 border-slate-200'
        icon = 'fa-file text-slate-600'
        open_action = f'<a href="{encoded_name}" download class="px-2.5 py-1.5 rounded-lg text-xs font-semibold bg-slate-50 hover:bg-slate-100 text-slate-700 transition inline-flex items-center gap-1"><i class="fa-solid fa-download"></i> Tải Về</a>'

    cards_html.append(f'''      <div class="doc-card bg-white border border-slate-200 rounded-2xl p-4 shadow-2xs hover:shadow-md transition flex flex-col justify-between" data-type="{type_class}" data-name="{name.lower()}">
        <div class="flex items-start gap-3 mb-3">
          <div class="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-xl shrink-0">
            <i class="fa-solid {icon}"></i>
          </div>
          <div class="min-w-0 flex-1">
            <h3 class="text-xs font-semibold text-slate-900 leading-snug break-words" title="{name}">{name}</h3>
            <div class="flex items-center gap-2 mt-1.5">
              <span class="px-2 py-0.5 rounded text-[10px] font-medium border {badge_color}">{ext.upper().replace('.', '')}</span>
              <span class="text-[11px] text-slate-400 font-mono">{size}</span>
            </div>
          </div>
        </div>
        <div class="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
          <span class="text-[11px] text-slate-400"><i class="fa-solid fa-hard-drive"></i> documents/</span>
          <div class="flex items-center gap-1.5">
            {open_action}
            <a href="{encoded_name}" download class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition" title="Tải tệp tin">
              <i class="fa-solid fa-cloud-arrow-down"></i>
            </a>
          </div>
        </div>
      </div>''')

cards_joined = '\n'.join(cards_html)
file_count = len(files)

html_content = f'''<!DOCTYPE html>
<html lang="vi" class="h-full bg-slate-50">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kho Văn Bản & Tài Liệu Gốc - Chi Nhánh Số 23 (documents/)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    html {{
      background-color: #f8fafc;
      min-height: 100%;
      overscroll-behavior-y: none;
    }}
    body, button, input, select, textarea {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }}
    body {{
      background-color: #f8fafc;
      color: #0f172a;
      min-height: 100vh;
      overscroll-behavior-y: none;
      margin: 0;
      padding: 0;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased bg-slate-50 text-slate-900">

  <!-- Header -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-2xs">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/20 shrink-0">
          <i class="fa-solid fa-folder-open text-lg"></i>
        </div>
        <div class="min-w-0">
          <h1 class="text-sm sm:text-base font-bold text-slate-900 leading-tight truncate">Kho Văn Bản & Dữ Liệu Gốc (documents/)</h1>
          <p class="text-xs text-slate-500 truncate">Văn phòng Đăng ký Đất đai TP.HCM - Chi nhánh số 23</p>
        </div>
      </div>
      <div class="flex items-center space-x-2 text-xs font-medium shrink-0">
        <a href="../OUTPUT/index.html" class="px-3 py-2 rounded-xl bg-sky-50 hover:bg-sky-100 text-sky-700 transition flex items-center gap-1.5 shadow-2xs">
          <i class="fa-solid fa-chart-line"></i> <span class="hidden sm:inline">Dashboard Quản Trị</span>
        </a>
        <a href="../IT_HELPDESK/index.html" class="px-3 py-2 rounded-xl bg-blue-50 hover:bg-blue-100 text-blue-700 transition flex items-center gap-1.5 shadow-2xs">
          <i class="fa-solid fa-headset"></i> <span class="hidden sm:inline">IT Helpdesk</span>
        </a>
        <a href="../A_THANG/index.html" class="px-3 py-2 rounded-xl bg-emerald-50 hover:bg-emerald-100 text-emerald-700 transition flex items-center gap-1.5 shadow-2xs">
          <i class="fa-solid fa-calendar-check"></i> <span class="hidden sm:inline">Lịch Tuần</span>
        </a>
        <a href="../index.html" class="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 transition flex items-center gap-1.5 shadow-2xs">
          <i class="fa-solid fa-house"></i>
        </a>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8 flex-1 w-full pb-10">
    
    <!-- Hero / Stats Bar -->
    <div class="bg-white border border-slate-200 rounded-2xl p-6 mb-6 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div>
        <h2 class="text-base sm:text-lg font-bold text-slate-900 mb-1 flex items-center gap-2">
          <span>Thư Viện {file_count} Văn Bản & Dữ Liệu Pháp Lý</span>
          <span class="px-2.5 py-0.5 rounded text-[11px] font-bold bg-emerald-100 text-emerald-800">Cập nhật 10/2026</span>
        </h2>
        <p class="text-xs text-slate-500">Các tệp tin gốc gồm NĐ 154, QĐ 78 (TNTT), QĐ 9326 (Kiểm tra công vụ), Phương án NĐ 155, Báo cáo, Kế hoạch 9999, Kiểm kê máy tính...</p>
      </div>
      
      <!-- Filter & Search -->
      <div class="flex flex-wrap items-center gap-2">
        <div class="relative">
          <input type="text" id="searchBox" placeholder="Tìm kiếm tên văn bản..." onkeyup="filterDocs()" class="w-60 sm:w-64 pl-9 pr-3 py-2 rounded-xl text-xs border border-slate-200 focus:outline-hidden focus:ring-2 focus:ring-sky-500 bg-slate-50 focus:bg-white transition">
          <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400 text-xs"></i>
        </div>
        <button onclick="filterType('all')" class="filter-btn px-3 py-2 rounded-xl text-xs font-semibold bg-sky-600 text-white shadow-xs" data-type="all">Tất cả ({file_count})</button>
        <button onclick="filterType('pdf')" class="filter-btn px-3 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition" data-type="pdf">PDF</button>
        <button onclick="filterType('docx')" class="filter-btn px-3 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition" data-type="docx">Word</button>
        <button onclick="filterType('xlsx')" class="filter-btn px-3 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition" data-type="xlsx">Excel</button>
      </div>
    </div>

    <!-- Documents Grid -->
    <div id="docsList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
{cards_joined}
    </div>
  </main>

  <!-- Footer -->
  <footer class="w-full bg-white border-t border-slate-200 py-4 px-6 text-center text-xs text-slate-500 shrink-0 mt-auto">
    <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
      <span>Hệ Thống Lưu Trữ & Quản Trị Văn Bản Pháp Lý - Chi Nhánh Số 23 (VPĐKĐĐ TP.HCM)</span>
      <span class="text-slate-400 font-mono">Hỗ trợ hiển thị chuẩn font đa nền tảng</span>
    </div>
  </footer>

  <script>
    let currentType = 'all';

    function filterType(type) {{
      currentType = type;
      document.querySelectorAll('.filter-btn').forEach(btn => {{
        if (btn.getAttribute('data-type') === type) {{
          btn.className = 'filter-btn px-3 py-2 rounded-xl text-xs font-semibold bg-sky-600 text-white shadow-xs';
        }} else {{
          btn.className = 'filter-btn px-3 py-2 rounded-xl text-xs font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition';
        }}
      }});
      filterDocs();
    }}

    function filterDocs() {{
      const q = document.getElementById('searchBox').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.doc-card');
      cards.forEach(card => {{
        const typeMatch = currentType === 'all' || card.getAttribute('data-type') === currentType;
        const nameMatch = !q || card.getAttribute('data-name').includes(q);
        if (typeMatch && nameMatch) {{
          card.style.display = 'flex';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>
'''

with open('documents/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated documents/index.html with {file_count} files successfully!")
