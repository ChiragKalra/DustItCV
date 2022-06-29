import os
import concurrent.futures
import argparse
from collections import deque
from PIL import Image


def crop_to_aspect(image, aspect, alignx=0.5, aligny=0.5):
	"""Crops an image to a given aspect ratio.
	Args:
		aspect (float): The desired aspect ratio
		alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
		aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
	Returns:
		Image: The cropped Image object.
	"""
	if image.width / image.height > aspect:
		newwidth = int(image.height * aspect)
		newheight = image.height
	else:
		newwidth = image.width
		newheight = int(image.width / aspect)
	img = image.crop((
			alignx * (image.width - newwidth),
			aligny * (image.height - newheight),
			alignx * (image.width - newwidth) + newwidth,
			aligny * (image.height - newheight) + newheight
	))
	return img


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
		in_id, out_id = self.in_count, 0
		aspect = im.width/im.height
		if im.height > im.width:
			factor, h_wise = im.height/im.width, True
		else:
			factor, h_wise = aspect, False
		count = int((factor-1)/(1-common)) + 1
		for i in range(count):
			w, h = (0.5, (i + 0.5)/count) if h_wise else ((i + 0.5)/count, 0.5)
			out = crop_to_aspect(im, 1, w, h)
			out = out.resize((224, 224), Image.Resampling.LANCZOS)
			dire = self.des + root[len(self.src):]
			if not os.path.isdir(dire):
				os.makedirs(dire)
			out.save(f'{dire}\\{in_id}_{out_id}.jpg', 'JPEG', quality=100, optimize=True, progressive=True)
			out_id += 1
		self.out_count += out_id

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
