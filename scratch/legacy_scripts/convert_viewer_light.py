# -*- coding: utf-8 -*-
import re

with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/document_viewer.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove class="dark" from html
content = content.replace('<html lang="vi" class="dark">', '<html lang="vi">')
content = content.replace('<html lang="vi" class=\'dark\'>', '<html lang="vi">')

# 2. Update style block
old_style = """    body {
      font-family: 'Inter', sans-serif;
      background-color: #090d16;
      color: #e2e8f0;
    }
    /* Custom scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #0f172a; }
    ::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #475569; }"""

new_style = """    body {
      font-family: 'Inter', sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }
    /* Custom scrollbars */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }"""

content = content.replace(old_style, new_style)

# 3. Header replacements
content = content.replace(
    'class="bg-slate-900/95 border-b border-slate-800 sticky top-0 z-50 backdrop-blur-md"',
    'class="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs"'
)
content = content.replace(
    'class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5"',
    'class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 transition flex items-center gap-1.5"'
)
content = content.replace(
    'class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-600 hover:bg-sky-500 text-white transition flex items-center gap-1.5 shadow"',
    'class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-900 text-white transition flex items-center gap-1.5 shadow-xs"'
)

# 4. Sidebar replacements
content = content.replace(
    'class="bg-slate-900/90 border border-slate-800 rounded-xl p-4 sticky top-22 shadow-lg"',
    'class="bg-white border border-slate-200 rounded-xl p-4 sticky top-22 shadow-xs"'
)
content = content.replace(
    'class="w-full pl-8 pr-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-sky-500 transition"',
    'class="w-full pl-8 pr-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 focus:outline-none focus:bg-white focus:border-sky-500 transition"'
)
content = content.replace(
    'class="px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-sky-400 font-mono"',
    'class="px-1.5 py-0.5 rounded bg-slate-100 text-[10px] text-sky-700 font-bold border border-slate-200 font-mono"'
)

# Nav items active/inactive initial classes
content = content.replace(
    'border-sky-500 bg-sky-950/40 text-white',
    'border-sky-500 bg-sky-50 text-sky-900 font-semibold shadow-xs'
)
content = content.replace(
    'border-transparent text-slate-400 hover:bg-slate-800/60 hover:text-slate-200',
    'border-transparent text-slate-700 hover:bg-slate-100 hover:text-slate-900'
)

# 5. Article panels
content = content.replace(
    'class="doc-view-panel  bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-xl"',
    'class="doc-view-panel bg-white border border-slate-200 rounded-xl p-6 shadow-xs"'
)
content = content.replace(
    'class="doc-view-panel hidden bg-slate-900/70 border border-slate-800 rounded-xl p-6 shadow-xl"',
    'class="doc-view-panel hidden bg-white border border-slate-200 rounded-xl p-6 shadow-xs"'
)

# Article top action button "Tải file gốc"
content = content.replace(
    'class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center gap-1.5 shadow"',
    'class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-300 transition flex items-center gap-1.5 shadow-2xs"'
)

# Article header borders and texts
content = content.replace(
    'border-b border-slate-800 mb-6 gap-3',
    'border-b border-slate-200 mb-6 gap-3'
)
content = content.replace(
    'text-lg md:text-xl font-bold text-white tracking-wide',
    'text-lg md:text-xl font-bold text-slate-900 tracking-wide'
)
content = content.replace(
    'text-xs text-slate-400 mt-1 leading-relaxed',
    'text-xs text-slate-600 mt-1 leading-relaxed'
)

# Badges in article header
content = content.replace("bg-rose-950 text-rose-300 border border-rose-800", "bg-rose-50 text-rose-700 border border-rose-200 font-semibold")
content = content.replace("bg-blue-950 text-blue-300 border border-blue-800", "bg-blue-50 text-blue-700 border border-blue-200 font-semibold")
content = content.replace("bg-emerald-950 text-emerald-300 border border-emerald-800", "bg-emerald-50 text-emerald-700 border border-emerald-200 font-semibold")

# PDF preview bar & iframe wrapper
content = content.replace(
    "p-3 bg-slate-900/80 rounded-lg border border-slate-700/80",
    "p-3 bg-slate-50 rounded-lg border border-slate-200"
)
content = content.replace("bg-rose-500/20 text-rose-300 font-mono text-xs font-bold border border-rose-500/30", "bg-rose-100 text-rose-800 font-mono text-xs font-bold border border-rose-200")
content = content.replace("text-xs text-slate-300", "text-xs text-slate-700")
content = content.replace(
    "overflow-hidden border border-slate-700 bg-slate-950 shadow-xl mb-6",
    "overflow-hidden border border-slate-200 bg-slate-100 shadow-sm mb-6"
)

# Transcripts and pre blocks
content = content.replace(
    "p-4 bg-slate-900/60 rounded-xl border border-slate-800 text-xs",
    "p-4 bg-slate-50 rounded-xl border border-slate-200 text-xs"
)
content = content.replace("text-slate-300 whitespace-pre-wrap", "text-slate-800 whitespace-pre-wrap")
content = content.replace("text-xs font-bold text-sky-400 uppercase tracking-wider mb-2", "text-xs font-bold text-sky-800 uppercase tracking-wider mb-2")

# Sheet tab buttons in Excel views
content = content.replace(
    "sheet-tab-btn px-3 py-1.5 rounded-md text-xs font-medium transition bg-sky-600 text-white shadow",
    "sheet-tab-btn px-3 py-1.5 rounded-md text-xs font-semibold transition bg-sky-600 text-white shadow-xs"
)
content = content.replace(
    "sheet-tab-btn px-3 py-1.5 rounded-md text-xs font-medium transition bg-slate-800 text-slate-300 hover:bg-slate-700",
    "sheet-tab-btn px-3 py-1.5 rounded-md text-xs font-medium transition bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-200"
)

# Tables in doc viewer
content = content.replace("border border-slate-700/80 max-h-[600px] shadow-inner", "border border-slate-200 max-h-[600px] shadow-2xs rounded-lg")
content = content.replace("border border-slate-700", "border border-slate-200 rounded-lg")
content = content.replace(
    "bg-slate-800 font-bold text-sky-300 border-b border-slate-700/60 hover:bg-slate-800/50",
    "bg-slate-100 font-bold text-slate-900 border-b border-slate-200 hover:bg-slate-200/60"
)
content = content.replace("border-r border-slate-700/60", "border-r border-slate-200")
content = content.replace("bg-slate-900/30 border-b border-slate-700/60 hover:bg-slate-800/50", "bg-white border-b border-slate-200 hover:bg-sky-50/40")
content = content.replace("bg-slate-900/60 border-b border-slate-700/60 hover:bg-slate-800/50", "bg-slate-50/60 border-b border-slate-200 hover:bg-sky-50/40")

# Other text colors in tables
content = content.replace("text-sky-300", "text-sky-800")
content = content.replace("text-emerald-400", "text-emerald-800 font-semibold")
content = content.replace("text-rose-400", "text-rose-800 font-semibold")
content = content.replace("text-blue-400", "text-blue-800 font-semibold")
content = content.replace("text-slate-200", "text-slate-800")

# JavaScript update
old_js = """    function selectDoc(docId) {
      document.querySelectorAll('.doc-view-panel').forEach(panel => panel.classList.add('hidden'));
      document.querySelectorAll('.doc-nav-item').forEach(btn => {
        btn.classList.remove('border-sky-500', 'bg-sky-950/40', 'text-white');
        btn.classList.add('border-transparent', 'text-slate-400');
      });

      const activePanel = document.getElementById(docId);
      if (activePanel) activePanel.classList.remove('hidden');

      const activeBtn = document.getElementById('nav_' + docId);
      if (activeBtn) {
        activeBtn.classList.remove('border-transparent', 'text-slate-400');
        activeBtn.classList.add('border-sky-500', 'bg-sky-950/40', 'text-white');
      }

      // Scroll smoothly to top on mobile
      if (window.innerWidth < 768) {
        activePanel.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function switchSheet(safeId, sheetIdx) {
      const container = document.getElementById('sheet_' + safeId + '_' + sheetIdx);
      if (!container) return;
      
      const parent = container.parentElement;
      parent.querySelectorAll('.sheet-container').forEach(el => el.classList.add('hidden'));
      container.classList.remove('hidden');

      parent.querySelectorAll('.sheet-tab-btn').forEach(btn => {
        btn.classList.remove('bg-sky-600', 'text-white', 'shadow');
        btn.classList.add('bg-slate-800', 'text-slate-300');
      });

      const activeBtn = document.getElementById('btn_' + safeId + '_' + sheetIdx);
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-800', 'text-slate-300');
        activeBtn.classList.add('bg-sky-600', 'text-white', 'shadow');
      }
    }"""

new_js = """    function selectDoc(docId) {
      document.querySelectorAll('.doc-view-panel').forEach(panel => panel.classList.add('hidden'));
      document.querySelectorAll('.doc-nav-item').forEach(btn => {
        btn.classList.remove('border-sky-500', 'bg-sky-50', 'text-sky-900', 'font-semibold', 'shadow-xs');
        btn.classList.add('border-transparent', 'text-slate-700');
      });

      const activePanel = document.getElementById(docId);
      if (activePanel) activePanel.classList.remove('hidden');

      const activeBtn = document.getElementById('nav_' + docId);
      if (activeBtn) {
        activeBtn.classList.remove('border-transparent', 'text-slate-700');
        activeBtn.classList.add('border-sky-500', 'bg-sky-50', 'text-sky-900', 'font-semibold', 'shadow-xs');
      }

      // Scroll smoothly to top on mobile
      if (window.innerWidth < 768) {
        activePanel.scrollIntoView({ behavior: 'smooth' });
      }
    }

    function switchSheet(safeId, sheetIdx) {
      const container = document.getElementById('sheet_' + safeId + '_' + sheetIdx);
      if (!container) return;
      
      const parent = container.parentElement;
      parent.querySelectorAll('.sheet-container').forEach(el => el.classList.add('hidden'));
      container.classList.remove('hidden');

      parent.querySelectorAll('.sheet-tab-btn').forEach(btn => {
        btn.classList.remove('bg-sky-600', 'text-white', 'shadow-xs');
        btn.classList.add('bg-slate-100', 'text-slate-700');
      });

      const activeBtn = document.getElementById('btn_' + safeId + '_' + sheetIdx);
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
        activeBtn.classList.add('bg-sky-600', 'text-white', 'shadow-xs');
      }
    }"""

content = content.replace(old_js, new_js)

with open('/Users/admin/Desktop/BINHDUONG/OUTPUT/document_viewer.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Converted OUTPUT/document_viewer.html to pure Light Mode successfully!")
