import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 1. Start from the original AI generated image
img_bgr = cv2.imread(r"C:\Users\aaksh\.gemini\antigravity\brain\f01c0193-327e-4f27-bfd7-47efb52c25bb\product_block_diagram_1790410777050.jpg")

# 2. Inpaint the "B-spliine" typo in Block 3
mask = np.zeros(img_bgr.shape[:2], dtype=np.uint8)
box = img_bgr[333:365, 636:728]
text_pixels = (box[:, :, 0] > 120) & (box[:, :, 1] > 120) & (box[:, :, 2] > 120)
kernel = np.ones((3,3), np.uint8)
text_mask_box = cv2.dilate(text_pixels.astype(np.uint8), kernel, iterations=1)
mask[333:365, 636:728] = text_mask_box * 255
inpainted_bgr = cv2.inpaint(img_bgr, mask, inpaintRadius=4, flags=cv2.INPAINT_TELEA)

img = Image.fromarray(cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(img)

# Redraw "B-spline" in Block 3
font_spline = ImageFont.truetype("arialbd.ttf", 21)
draw.text((682, 350), "B-spline", fill=(245, 248, 252), font=font_spline, anchor="mm")

# 3. Now update Block 5 bottom card (remove 4 personas)
# Exact interior coordinates:
x0, x1 = 1122, 1306
y0, y1 = 446, 615
w = x1 - x0
h = y1 - y0

# Subtle vertical gradient matching surrounding purple card:
# Top interior is dark navy-purple, bottom is slightly deeper
c_top = np.array([22, 20, 36], dtype=float)
c_bot = np.array([38, 30, 56], dtype=float)

grad = np.zeros((h, w, 3), dtype=np.uint8)
for i in range(h):
    factor = i / float(h - 1)
    grad[i, :, :] = (1.0 - factor) * c_top + factor * c_bot

# Paste gradient into interior of bottom card
img.paste(Image.fromarray(grad), (x0, y0))

draw = ImageDraw.Draw(img)

# Fonts for Block 5
font_title = ImageFont.truetype("arialbd.ttf", 16)
font_items = ImageFont.truetype("arial.ttf", 12.5)

# Center Title
center_x = (x0 + x1) // 2
draw.text((center_x, y0 + 18), "Recipe Dispatch", fill=(255, 255, 255), font=font_title, anchor="mm")

# Subtle separator line
draw.line([(x0 + 18, y0 + 32), (x1 - 18, y0 + 32)], fill=(95, 75, 125), width=1)

# Clean bullets
items = [
    "1-Click Setpoint Push",
    "Auto / Manual Control",
    "Safety Guard Enforcer",
    "DCS Modbus & OPC-UA"
]

start_y = y0 + 50
line_spacing = 26

for i, text in enumerate(items):
    y_pos = start_y + i * line_spacing
    # Small violet bullet dot
    draw.ellipse([(x0 + 16, y_pos - 3), (x0 + 22, y_pos + 3)], fill=(168, 85, 247))
    draw.text((x0 + 28, y_pos), text, fill=(241, 245, 249), font=font_items, anchor="lm")

# Save final clean image
final_out = r"c:\Users\aaksh\Downloads\paper\product_block_diagram.png"
img.save(final_out)
img.save(r"c:\Users\aaksh\Downloads\paper\system_architecture_diagram.png")

# Crop to verify
crop = img.crop((1090, 150, 1345, 630))
crop.save('block5_crop_final.png')
print("[SUCCESS] Block 5 updated and saved perfectly!")
