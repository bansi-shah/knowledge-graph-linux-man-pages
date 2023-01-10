path = 'std/'

for files in listdir(path):
	file = std + files 
	with open(file) as f:
		out = open('std/output'+files+'.txt', 'a')
		for row in f:
			row = row.split()
			if len(row) > 1 and row[1] in ['NNP', 'NN'] :
				#out.write(row[0] + '\n')
				print(row[0])
