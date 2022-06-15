import numpy as np


def evaluate_model(dataset, interpreter):
	input_index = interpreter.get_input_details()[0]["index"]
	output_index = interpreter.get_output_details()[0]["index"]

	predictions = []
	labels = []
	done = 0
	for test_images, test_labels in dataset:
		# Run predictions on every image in the "test" dataset.
		for i, test_image in enumerate(test_images):
			done += 1
			if done % 1000 == 0:
				print(done, end='; ')
			# Pre-processing: add batch dimension and convert to float32 to match with
			# the model's input data format.
			test_image = np.expand_dims(test_image, axis=0).astype(np.float32)
			interpreter.set_tensor(input_index, test_image)

			# Run inference.
			interpreter.invoke()

			# Post-processing: remove batch dimension and find the digit with highest
			# probability.
			output = interpreter.tensor(output_index)
			digit = np.argmax(output()[0])
			predictions.append(digit)
			labels.append(test_labels)

		# Compare prediction results with ground truth labels to calculate accuracy.
	prediction_digits = np.array(predictions)
	accuracy = (prediction_digits == labels).mean()

	return accuracy
