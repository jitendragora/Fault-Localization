import csv
import numpy
import sys
import math
from dataCollection import prediction
# np = []
# nf = []
# ep = []
# ef = []

# score = []
# assert len(sys.argv) >= 2, "No argument given"
with open('../versions.alt/versions.orig/v1/statementResult.csv', 'r') as csvfile:
	csvreader = csv.reader(csvfile, delimiter=',')
	# entities = len(csvreader[0]) - 1
	for row in csvreader:
		entities = len(row) - 1
		break

	np = numpy.zeros(entities)
	nf = numpy.zeros(entities)
	ep = numpy.zeros(entities)
	ef = numpy.zeros(entities)
	tarantula = numpy.zeros(entities)
	ochiai = numpy.zeros(entities)
	jaccard = numpy.zeros(entities)
	ample = numpy.zeros(entities)
	hamman = numpy.zeros(entities)
	fault = numpy.zeros(entities)

	for row in csvreader:
		# print(row)
		for i in range(entities):
			if row[i]=='0' and row[-1]=='0':
				np[i] += 1
			elif row[i]=='0' and row[-1]=='1':
				nf[i] += 1
			elif row[i]=='1' and row[-1]=='0':
				ep[i] += 1
			elif row[i]=='1' and row[-1]=='1':
				ef[i] += 1

	e = 1e-6
	for i in range(entities):
		tarantula[i] = (ef[i]/(ef[i]+nf[i]))/(ef[i]/(ef[i]+nf[i]) + ep[i]/(ep[i]+np[i]))
		ochiai[i] = (ef[i]/math.sqrt((ef[i]+ep[i])*(ef[i]+nf[i])))
		jaccard[i] = (ef[i]/(ef[i]+ep[i]+nf[i]))
		# ample[i] = abs(ef[i]/(ef[i]+nf[i]))
		hamman[i] = (ef[i] + np[i] - ep[i] - nf[i])/(ef[i]+ep[i]+nf[i]+np[i])

	score = [tarantula, ochiai, jaccard, hamman, prediction]
	# print(score)
	rows = zip()
	bestRank = [ [] for i in range(len(score))]
	worstRank = [ [] for i in range(len(score))]
	# print(worstRank)
	for i in range(len(score)):
		rank = numpy.argsort(-score[i])
		# entity_no = int(sys.argv[1])
		# fault[entity_no-1] = 1

		# rows = zip(score[i], ochiai, jaccard, hamman)
		
		# with open('score/1/rankComparison.csv', 'w') as f:
		# 	writer = csv.writer(f)
		# 	for row in rows:
		# 		writer.writerow(row)


		# assert entity_no <= len(score), "Please provide corret entity number"
		# # print(int(sys.argv[1]))


		unique, frequency = numpy.unique(-score[i], return_counts = True)
		best = numpy.zeros(entities)
		worst = numpy.zeros(entities)

		reverse_score = -score[i]
		curr_best = 0
		curr_worst = 0
		for k in range(len(unique)):
			curr_best = curr_worst + 1
			curr_worst = curr_worst + frequency[k]
			for j in range(frequency[k]):
				best[curr_best+j-1] = curr_best
				worst[curr_best+j-1] = curr_worst

		# print(best)
		# print(worst)
		# print(i)
		worstRank[i] = numpy.zeros(entities)
		bestRank[i] = numpy.zeros(entities)

		for j in range(entities):
			entity_rank = numpy.where(rank == j)[0][0]
			bestRank[i][j] = best[entity_rank]
			worstRank[i][j] = worst[entity_rank]


	# entity_rank = numpy.where(rank == (entity_no - 1))[0][0]
	# # print(entity_rank)
	# print("The rank of entity", sys.argv[1], "is:")
	# print("Best:", best[entity_rank])
	# print("worst:", worst[entity_rank])
	# print(tarantula)
	# print(ochiai)
	header = ["TarantulaBest", "TarantulaWorst", "ochiaiBest", "ochiaiWorst", "jaccardBest", "jaccardWorst", "hammanBest", "hammanWorst", "rankBoostBest", "rankBoostWorst"]
	rows = zip(bestRank[0], worstRank[0], bestRank[1], worstRank[1], bestRank[2], worstRank[2], bestRank[3], worstRank[3], bestRank[4], worstRank[4])
	# print(worstRank)
	# print(prediction)
	with open('score/1/rankComparison.csv', 'w') as f:
		writer = csv.writer(f)
		# for row in header:
		writer.writerow(header)
		for row in rows:
			writer.writerow(row)