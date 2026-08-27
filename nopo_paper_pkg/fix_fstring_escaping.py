"""
nopo_paper_pkg / fix_fstring_escaping.py
----------------------------------------
Properly escapes curly braces for Python f-string in build_upgraded_gui.py.
"""

import os
import re

pkg_dir = os.path.dirname(os.path.abspath(__file__))
builder_path = os.path.join(pkg_dir, "build_upgraded_gui.py")

with open(builder_path, "r", encoding="utf-8") as f:
    text = f.read()

# In the JS Tab 2 section, double all single curly braces that are not already doubled
# Let's locate the JS Tab 2 section
js_tab2_start = text.find("// TAB 2: INTERPRETABILITY & FEATURE DEFENSE STUDIO")
js_tab3_start = text.find("// TAB 3: EPISTEMIC UNCERTAINTY")

tab2_section = text[js_tab2_start:js_tab3_start]

# We need every { to be {{ and every } to be }} except already doubled ones
# Let's cleanly replace single braces with double braces
def double_braces(s):
    # First normalize all to single, then double
    s = s.replace("{{", "___OPEN_BRACE___").replace("}}", "___CLOSE_BRACE___")
    s = s.replace("{", "{{").replace("}", "}}")
    s = s.replace("___OPEN_BRACE___", "{{").replace("___CLOSE_BRACE___", "}}")
    return s

new_tab2_section = double_braces(tab2_section)

# Also in the HTML Tab 2 section:
html_tab2_start = text.find("<!-- TAB 2: PYKAN INTERPRETABILITY & FEATURE DEFENSE STUDIO")
html_tab2_end = text.find("<!-- TAB 3: EPISTEMIC UNCERTAINTY")
html_tab2_section = text[html_tab2_start:html_tab2_end]
new_html_tab2_section = double_braces(html_tab2_section)

text = text[:html_tab2_start] + new_html_tab2_section + text[html_tab2_end:]
# Refresh indices
js_tab2_start = text.find("// TAB 2: INTERPRETABILITY & FEATURE DEFENSE STUDIO")
js_tab3_start = text.find("// TAB 3: EPISTEMIC UNCERTAINTY")
text = text[:js_tab2_start] + new_tab2_section + text[js_tab3_start:]

with open(builder_path, "w", encoding="utf-8") as f:
    f.write(text)

print("[SUCCESS] Fixed f-string escaping in build_upgraded_gui.py!")
