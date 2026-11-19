import pptx
from pptx.util import Inches

p = pptx.Presentation('kan_presentaation_updated.pptx')
s21 = p.slides[20]

# Remove text shapes from slide 21
for shape in list(s21.shapes):
    el = shape.element
    el.getparent().remove(el)

# Add full-bleed high-res image
s21.shapes.add_picture('secondary_physics_parameters.png', 0, 0, Inches(13.333), Inches(7.5))

p.save('kan_presentation_with_equations.pptx')
print("[SUCCESS] Successfully created kan_presentation_with_equations.pptx!")
