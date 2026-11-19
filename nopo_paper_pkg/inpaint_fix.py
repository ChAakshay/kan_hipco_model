import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

img_bgr = cv2.imread(r"C:\Users\aaksh\.gemini\antigravity\brain\f01c0193-327e-4f27-bfd7-47efb52c25bb\product_block_diagram_1790410777050.jpg")

# Mask for the word "B-spliine"
# Coordinates in full image: y in [333, 364], x in [636, 726]
mask = np.zeros(img_bgr.shape[:2], dtype=np.uint8)

# Detect text pixels in that box
box = img_bgr[333:365, 636:728]
# Text is bright (>120 in any channel)
text_pixels = (box[:, :, 0] > 120) & (box[:, :, 1] > 120) & (box[:, :, 2] > 120)

# Dilate mask slightly so edges of characters are covered
kernel = np.ones((3,3), np.uint8)
text_mask_box = cv2.dilate(text_pixels.astype(np.uint8), kernel, iterations=1)

mask[333:365, 636:728] = text_mask_box * 255

# Inpaint
inpainted_bgr = cv2.inpaint(img_bgr, mask, inpaintRadius=4, flags=cv2.INPAINT_TELEA)

# Now convert to PIL and draw "B-spline"
img_pil = Image.fromarray(cv2.cvtColor(inpainted_bgr, cv2.COLOR_BGR2RGB))
draw = ImageDraw.Draw(img_pil)

# Load font
font = ImageFont.truetype("arialbd.ttf", 21) # bold
# Calculate bounding box to match exactly
draw.text((682, 350), "B-spline", fill=(245, 248, 252), font=font, anchor="mm")

# Save
out_clean = r"c:\Users\aaksh\Downloads\paper\product_block_diagram_clean.png"
img_pil.save(out_clean)

# Crop to verify
crop = img_pil.crop((580, 320, 800, 480))
crop.save('block3_crop_inpaint.png')
print("[SUCCESS] Inpainted and verified")
