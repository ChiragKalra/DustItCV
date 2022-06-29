import os
import concurrent.futures
import argparse
from collections import deque
from PIL import Image


def make_square(im, size=224, fill_color=(0, 0, 0, 0)):
	im.thumbnail((size, size))
	new_im = Image.new('RGBA', (size, size), fill_color)
	new_im.paste(im, (0, 0))
	return new_im


class ImageCropper:
	def __init__(self, src, des):
		self.src = src
		self.des = des
		self.in_count = 0
		self.out_count = 0

	def convert(self, root, filename=None, common=0.2):
		if not filename:
			root, filename = root
		file = os.path.join(root, filename)
		im = Image.open(file).convert('RGB')
		self.in_count += 1
		in_id = self.in_count
		out = make_square(im)
		if not os.path.isdir(dire):
			os.makedirs(dire)
		out.save(f'{dire}\\{in_id}.jpg', 'JPEG', quality=100, optimize=True, progressive=True)
		self.out_count += 1

	def file_gen(self):
		for root, dirs, files in os.walk(self.src):
			for file in files:
				if file.endswith(('png', 'jpeg', 'jpg')):
					yield root, file

	def start(self):
		with concurrent.futures.ThreadPoolExecutor() as ptolemy:
			ptolemy.map(self.convert, self.file_gen())
		print(f'In Count: {self.in_count}\nOut Count: {self.out_count}\n')


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Image Cropper')
	required_args = parser.add_argument_group('required arguments')
	required_args.add_argument('-d', type=str, help="Input Directory", required=True)
	required_args.add_argument('-o', type=str, help="Output Directory", required=True)
	args = parser.parse_args()

	scraper = ImageCropper(args.d, args.o)
	scraper.start()
