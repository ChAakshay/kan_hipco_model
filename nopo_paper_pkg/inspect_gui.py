import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "hipco_kan_dss_app.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

print("HTML Total Length:", len(html))

# Let's inspect script functions and charts initialized
js_match = re.search(r"<script>(.*)</script>", html, re.DOTALL)
if js_match:
    js = js_match.group(1)
    funcs = re.findall(r"function\s+([a-zA-Z0-9_]+)\s*\(", js)
    print("JS Functions:", funcs)

    # Check chart initializations
    chart_inits = re.findall(r"new Chart\(\s*([^,]+),", js)
    print("Chart.js instances created for:", chart_inits)

    # Check which canvas elements exist in HTML
    canvases = re.findall(r"<canvas[^>]*id=[\"']([^\"']+)[\"']", html)
    print("Canvas IDs in HTML:", canvases)

    # Check element IDs in HTML that might have innerText or innerHTML set vs not set
    all_ids = set(re.findall(r"id=[\"']([^\"']+)[\"']", html))
    print("Total Unique Element IDs in HTML:", len(all_ids))

    referenced_ids = set()
    for el_id in all_ids:
        if f"'{el_id}'" in js or f'"{el_id}"' in js or f"`{el_id}`" in js:
            referenced_ids.add(el_id)

    unreferenced_ids = all_ids - referenced_ids
    print("\n--- IDs in HTML NEVER touched or updated by JS (potentially empty or static) ---")
    for uid in sorted(unreferenced_ids):
        print("  -", uid)

# Inspect what is inside Tab 1, Tab 2, Tab 3, Tab 4
tabs = re.split(r"<!--\s*TAB\s*(\d+)\s*-->", html)
for i in range(1, len(tabs), 2):
    tab_num = tabs[i]
    tab_content = tabs[i+1]
    print(f"\n================ TAB {tab_num} SUMMARY ================")
    # Extract card titles
    card_titles = re.findall(r"class=[\"'][^\"']*card-title[^\"']*[\"'][^>]*>(.*?)</div>", tab_content)
    print("Card titles:", [re.sub(r"<[^>]+>", "", ct).strip() for ct in card_titles])
    # Extract tables
    tables = re.findall(r"<table", tab_content)
    print("Table count:", len(tables))
    # Extract canvases in this tab
    tab_canvases = re.findall(r"<canvas[^>]*id=[\"']([^\"']+)[\"']", tab_content)
    print("Canvas IDs:", tab_canvases)
