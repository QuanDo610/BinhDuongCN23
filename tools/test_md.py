import html
import re

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
                out.append('<pre class="bg-slate-900 text-slate-100 p-4 rounded-xl overflow-x-auto my-3 text-xs"><code>')
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
                out.append('<div class="overflow-x-auto my-4 rounded-xl border border-slate-200"><table class="w-full text-xs text-left border-collapse bg-white">')
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
        if line.startswith('* ') or line.startswith('- '):
            if not in_list:
                out.append('<ul class="list-disc pl-5 my-2 space-y-1 text-xs text-slate-700">')
                in_list = True
            content = line[2:].strip()
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

with open('OUTPUT/PROGRESS_BINHDUONG.md', 'r', encoding='utf-8') as f:
    raw = f.read()

rendered = md_to_html(raw)
print('Rendered length:', len(rendered))
print('Sample output preview:\n', rendered[:500])
