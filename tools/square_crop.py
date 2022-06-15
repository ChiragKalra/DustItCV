from PIL import Image
import os.path
from collections import deque


def crop_to_aspect(image, aspect, divisor=1, alignx=0.5, aligny=0.5):
	"""Crops an image to a given aspect ratio.
	Args:
		aspect (float): The desired aspect ratio.
		divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
		alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
		aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
	Returns:
		Image: The cropped Image object.
	"""
	if image.width / image.height > aspect / divisor:
		newwidth = int(image.height * (aspect / divisor))
		newheight = image.height
	else:
		newwidth = image.width
		newheight = int(image.width / (aspect / divisor))
	img = image.crop((
			alignx * (image.width - newwidth),
			aligny * (image.height - newheight),
			alignx * (image.width - newwidth) + newwidth,
			aligny * (image.height - newheight) + newheight
	))
	return img


def cropTo(path, dest):
	dirs = os.listdir(path)
	q = deque(dirs)
	count = 0
	while q:
		item = q.pop()
		full_path = os.path.join(path, item)
		dest_path = os.path.join(dest, item)
		if os.path.isfile(full_path):
			im = Image.open(full_path).convert('RGB')
			f, e = os.path.splitext(dest_path)
			cropped = crop_to_aspect(im, 1)
			cropped.save(f + '.jpg')
			count += 1
			if count % 250 == 0:
				print('done={0}/107000, {1}%'.format(count, count/1070))
		else:
			os.makedirs(dest_path)
			for child in os.listdir(full_path):
				this_path = os.path.join(item, child)
				q.append(this_path)


cropTo(path='datasets\\og', dest='datasets\\cropped')
