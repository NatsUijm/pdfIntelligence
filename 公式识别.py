from PIL import Image
from pix2tex.cli import LatexOCR

img = Image.open('./equaltion.png')
model = LatexOCR()
print(model(img))