from os import path, mkdir, listdir
from shutil import copyfile

datasets = [
	'datasets\\cropped\\continental',
	'datasets\\cropped\\indian_0',
	'datasets\\cropped\\indian_1',
	'datasets\\fruits-360\\Training',
]

destination = 'datasets\\all_classes'


if __name__ == '__main__':
	total = 0
	for dataset in datasets:
		print(dataset)
		for food_class in listdir(dataset):
			full_path = path.join(dataset, food_class)
			if path.isdir(full_path):
				dest = path.join(destination, food_class)
				sample = listdir(full_path)[1]
				full_path_sample = path.join(full_path, sample)
				if path.isfile(full_path_sample):  # and not path.exists(dest): (checks for duplicate classes)
					mkdir(dest)
					copyfile(full_path_sample, path.join(dest, sample))
					total += 1
					if total % 10 == 0:
						print('classes added =', total)
		print("end of dataset\n")
	print('total classes added =', total)
