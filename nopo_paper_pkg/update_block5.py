import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load image
img = Image.open(r"c:\Users\aaksh\Downloads\paper\product_block_diagram_clean.png").copy()

# Full image coordinates:
# Block 5 crop origin was (1090, 150)
# Inner card in crop: x in [32, 216], y in [263, 454]
# In full image:
# x0 = 1090 + 32 = 1122
# x1 = 1090 + 216 = 1306
# y0 = 150 + 263 = 413
# y1 = 150 + 454 = 604

x0, x1 = 1122, 1306
y0, y1 = 413, 604
w = x1 - x0
h = y1 - y0

# Create vertical gradient from [18, 25, 36] to [45, 38, 67]
c_top = np.array([18, 25, 36], dtype=float)
c_bot = np.array([45, 38, 67], dtype=float)

grad = np.zeros((h, w, 3), dtype=np.uint8)
for i in range(h):
    factor = i / float(h - 1)
    grad[i, :, :] = (1.0 - factor) * c_top + factor * c_bot

# Paste gradient into image
img.paste(Image.fromarray(grad), (x0, y0))

draw = ImageDraw.Draw(img)

# Fonts
font_title = ImageFont.truetype("arialbd.ttf", 19)
font_items = ImageFont.truetype("arial.ttf", 14)
font_items_bd = ImageFont.truetype("arialbd.ttf", 14)

# Draw Title
center_x = (x0 + x1) // 2
draw.text((center_x, y0 + 24), "Recipe Dispatch & Control", fill=(255, 255, 255), font=font_title, anchor="mm")

# Subtle separator line under title
draw.line([(x0 + 15, y0 + 42), (x1 - 15, y0 + 42)], fill=(90, 75, 120), width=1)

# Bullet points
items = [
    "1-Click DCS Setpoint Push",
    "Closed-Loop / Manual Mode",
    "Real-Time Safety Interlocks",
    "Multi-Objective Pareto Solver"
]

start_y = y0 + 64
line_spacing = 31

for i, text in enumerate(items):
    y_pos = start_y + i * line_spacing
    # Draw a small cyan/violet bullet dot
    draw.ellipse([(x0 + 16, y_pos - 4), (x0 + 24, y_pos + 4)], fill=(168, 85, 247))
    draw.text((x0 + 32, y_pos), text, fill=(241, 245, 249), font=font_items, anchor="lm")

# Save
out_path = r"c:\Users\aaksh\Downloads\paper\product_block_diagram_clean.png"
img.save(out_path)

# Verify with crop
crop = img.crop((1090, 150, 1345, 620))
crop.save('block5_crop_no_personas.png')
print("[SUCCESS] Block 5 updated without personas")
