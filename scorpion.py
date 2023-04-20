from exif import Image
import sys

print(sys.argv[1])
img = []
for image in sys.argv[1:]:
    with open(image, 'rb') as file:
        img.append(Image(file))

#with open(sys.argv[1], 'rb') as file:
#    img = Image(file)

for index, image in enumerate(img):
#    print(image.getexif())
    if image.has_exif:
        info = f"contains EXIF\n"# {image.exif_version}\n"
#        info += f"{image.datetime_original} {image.get('offset_time', '')}"
        print(sorted(image.list_all()))
#        for a,b in enumerate(exif):
#           print(a)
#             print(b," ",image.get(b))
    else:
        info = "not contains EXIF"
#    info += f"{image.datetime_original}"#.{image.subsec_time_original}"
    print(f"Image {index} {info}")
