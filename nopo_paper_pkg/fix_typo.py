from PIL import Image, ImageDraw, ImageFont

img = Image.open(r"C:\Users\aaksh\.gemini\antigravity\brain\f01c0193-327e-4f27-bfd7-47efb52c25bb\product_block_diagram_1790410777050.jpg").copy()
draw = ImageDraw.Draw(img)

# Let's inspect the area around (650, 340) to (760, 410)
# Sample background color in that box
bg_color = (13, 39, 31) # dark green tint of the card interior

# Paint over "B-spliine on edges"
# Box: x ~ 640 to 760, y ~ 335 to 405
draw.rectangle([(640, 335), (765, 405)], fill=bg_color)

# Try loading standard font or Arial
try:
    font = ImageFont.truetype("arial.ttf", 22)
except:
    font = ImageFont.load_default()

# Text color is white/off-white #F8FAFC
draw.text((700, 350), "B-spline", fill=(248, 250, 252), font=font, anchor="mm")
draw.text((700, 385), "on edges", fill=(248, 250, 252), font=font, anchor="mm")

# Save cleaned image
out_clean = r"c:\Users\aaksh\Downloads\paper\product_block_diagram_clean.png"
img.save(out_clean)
print("[SUCCESS] Saved to", out_clean)
