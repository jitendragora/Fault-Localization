import csv
import numpy
import sys
import math


errors = [14, 10, 30, 15, 28, 24, 3, 5, 18, 24, 35, 28, 28, 28, 15, 2, 3, 4, 5, 12, 12, 12, 18, 18, 21, 28, 28, 10, 10, 10, 15, 20, '-', 32, 10, 40, 8, 5, 21, 14, 15]

with open('rankComparison.csv', 'w') as f:
		writer = csv.writer(f)
		# for row in header:
		header = ["TarantulaBest", "TarantulaWorst", "ochiaiBest", "ochiaiWorst", "jaccardBest", "jaccardWorst", "hammanBest", "hammanWorst", "rankBoostBest", "rankBoostWorst"]
		writer.writerow(header)
		for i in range(1, 42):
			if errors[i-1]=='-':
				continue
			temp = 'score/' + str(i) + '/rankComparison.csv'
			with open(temp, 'r') as csvFile:
				reader = csv.reader(csvFile)
				# interestingrows=[row for idx, row in enumerate(reader) if idx in (28,62)]
				for idx, row in enumerate(reader):
					if idx==errors[i-1]:
						writer.writerow(row)