import os

html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hipco_kan_dss_app.html")

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update navigation buttons
old_tab_buttons = (
    '<button class="tab-btn" onclick="switchTab(3)">Tab 4: Diagnostics & Thermodynamics</button>\n'
    '        <button class="tab-btn" onclick="switchTab(4)">Tab 5: Model Audit & Benchmarks</button>'
)
old_tab_buttons_crlf = (
    '<button class="tab-btn" onclick="switchTab(3)">Tab 4: Diagnostics & Thermodynamics</button>\r\n'
    '        <button class="tab-btn" onclick="switchTab(4)">Tab 5: Model Audit & Benchmarks</button>'
)
new_tab_button = '<button class="tab-btn" onclick="switchTab(3)">Tab 4: Model Audit & Benchmarks</button>'

if old_tab_buttons in text:
    text = text.replace(old_tab_buttons, new_tab_button)
elif old_tab_buttons_crlf in text:
    text = text.replace(old_tab_buttons_crlf, new_tab_button)
else:
    print("[WARNING] Tab button pattern not matched directly; checking alternatives")

# 2. Remove Tab 4 HTML Panel
tab4_start = text.find("<!-- TAB 4 -->")
tab5_start = text.find("<!-- TAB 5 -->")

if tab4_start != -1 and tab5_start != -1:
    text = text[:tab4_start] + "<!-- TAB 4 -->\n" + text[tab5_start + len("<!-- TAB 5 -->") + 1:]

# 3. Update switchTab function in JS
old_call = "if(tabIndex===3) initDiagnosticsTab();\n    if(tabIndex===4) initBenchmarkTab();"
old_call_crlf = "if(tabIndex===3) initDiagnosticsTab();\r\n    if(tabIndex===4) initBenchmarkTab();"
new_call = "if(tabIndex===3) initBenchmarkTab();"

if old_call in text:
    text = text.replace(old_call, new_call)
elif old_call_crlf in text:
    text = text.replace(old_call_crlf, new_call)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] Tab 4 (Diagnostics & Thermodynamics) removed completely from hipco_kan_dss_app.html!")
