import csv
from settings import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys

"""
 _       ______________   ________      __          __   _____ __                             ____                                                 
| |     / / ____/ ____/  / ____/ /___  / /_  ____ _/ /  / ___// /_  ____ _____  ___  _____   / __ \____  ___  ____  _________  __  _______________ 
| | /| / / __/ / /_     / / __/ / __ \/ __ \/ __ `/ /   \__ \/ __ \/ __ `/ __ \/ _ \/ ___/  / / / / __ \/ _ \/ __ \/ ___/ __ \/ / / / ___/ ___/ _ \
| |/ |/ / /___/ __/    / /_/ / / /_/ / /_/ / /_/ / /   ___/ / / / / /_/ / /_/ /  __/ /     / /_/ / /_/ /  __/ / / (__  ) /_/ / /_/ / /  / /__/  __/
|__/|__/_____/_/       \____/_/\____/_.___/\__,_/_/   /____/_/ /_/\__,_/ .___/\___/_/      \____/ .___/\___/_/ /_/____/\____/\__,_/_/   \___/\___/ 
																	  /_/                      /_/                                                 
""" 

def expertiseGrid():

	sdg_file = open(files["sdg_list"],'r')
	resp_file = open(files['responses'],'r')

	sdgreader = csv.reader(sdg_file) 
	respreader = csv.reader(resp_file)

	# Get a list of the Sustainable Development Goals from CSV
	sdgs = next(sdgreader)
	names = []
	first_expertise = []
	second_expertise = []
	third_expertise = []

	sdg_dict = {sdg:0 for sdg in sdgs}

	resp_headers = next(respreader)
	
	# Find name index
	name_index = [i for i, s in enumerate(resp_headers) if 'name' in s][0]
	first_index = [i for i, s in enumerate(resp_headers) if 'first' in s][0]
	second_index = [i for i, s in enumerate(resp_headers) if 'second' in s][0]
	third_index = [i for i, s in enumerate(resp_headers) if 'third' in s][0]

	num_resp = len(list(respreader))
	expertise_map = np.zeros((len(sdgs), num_resp))

	resp_file.seek(0)
	next(respreader)

	resp_index = 0

	for row in respreader:
		names.append(row[name_index])
		first_expertise.append(row[first_index])
		second_expertise.append(row[second_index])
		third_expertise.append(row[third_index])

		# Weight answers accordingly and store in dict
		sdg_dict[row[first_index]] += 1
		sdg_dict[row[second_index]] += .66
		sdg_dict[row[third_index]] += .33

		expertise_map[list(sdg_dict).index(first_expertise[resp_index])][resp_index] = 1.0
		expertise_map[list(sdg_dict).index(second_expertise[resp_index])][resp_index] = 0.66
		expertise_map[list(sdg_dict).index(third_expertise[resp_index])][resp_index] = 0.33

		resp_index += 1


	fig, ax = plt.subplots()
	im = ax.imshow(expertise_map)

	# We want to show all ticks...
	ax.set_xticks(np.arange(len(names)))
	ax.set_yticks(np.arange(len(sdgs)))
	# ... and label them with the respective list entries
	ax.set_xticklabels(names)
	ax.set_yticklabels(sdgs)

	# Rotate the tick labels and set their alignment.
	plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

	# Loop over data dimensions and create text annotations.
	for i in range(len(sdgs)):
		for j in range(len(names)):
			text = ax.text(j, i, expertise_map[i, j], ha="center", va="center", color="w")

	ax.set_title("Expertise of Seattle Hub")
	fig.tight_layout()
	plt.show()

if __name__ == "__main__":
	expertiseGrid()

