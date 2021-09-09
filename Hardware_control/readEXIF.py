from PIL import Image
from PIL.ExifTags import TAGS
img = Image.open('s.jpg')
exif_data = img._getexif()
for tag, value in exif_data.items():
  print TAGS.get(tag, tag), value
