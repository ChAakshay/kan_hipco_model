import numpy as np
from PIL import Image, ImageDraw, ImageFont

# Load original AI image
img = Image.open(r"C:\Users\aaksh\.gemini\antigravity\brain\f01c0193-327e-4f27-bfd7-47efb52c25bb\product_block_diagram_1790410777050.jpg").copy()
arr = np.array(img)

# In original coordinates:
# Block 3 crop was (580, 320)
# 'B-spliine' is at y in [335, 365], x in [638, 725]
# Sample background around it:
# y in [335, 365], x in [620, 635]
bg_color = tuple(arr[335:365, 620:635].mean(axis=(0,1)).astype(int))
print("Sampled exact BG color:", bg_color)

# Let's paint just that tight row [335, 364], x in [636, 726] with bg_color
draw = ImageDraw.Draw(img)
draw.rectangle([(636, 335), (726, 364)], fill=bg_color)

# Now render 'B-spline' perfectly centered in that tight rectangle
font = ImageFont.truetype("arialbd.ttf", 20) # bold Arial
draw.text((680, 349), "B-spline", fill=(245, 248, 252), font=font, anchor="mm")

# Save
clean_path = r"c:\Users\aaksh\Downloads\paper\product_block_diagram_clean.png"
img.save(clean_path)

# Verify with crop
crop = img.crop((580, 320, 800, 480))
crop.save('block3_crop_verified.png')
print("[SUCCESS] Verified and saved")
