import string
import argparse
from PIL import Image
from PIL.ExifTags import TAGS
#from exif import Image
import sys

def parser():
	parser = argparse.ArgumentParser(
		prog = "Scorpion",
		description = "Search for EXIF data and other metadata.")
	parser.add_argument("images", type=str, nargs="+", help="Images files to check")
	arg = parser.parse_args()
	return arg.images

def get_meta(files):
	for i,file in enumerate(files):
		print("\nImage %i:\t%s\n"%(i,file.split('/')[-1]))
		try:
			with Image.open(file) as fileOpen:
				image = fileOpen
		except:
			print("nop")
		else:
			if not image.getexif():
				print("no exif for ",file.split('/')[-1])
				continue
			exif = image.getexif()
			print("\t\tEXIF")
			for tag in exif:
				print("tag: {:<20} {}".format(TAGS.get(tag),exif.get(tag)))

if __name__ == "__main__":
	arg = parser()
	get_meta(arg)
	exit()
