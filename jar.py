import os

# for file in listdir('test/'):
# 	print('java -cp "*" edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-left3words-distsim.tagger -textFile ../test/' + file + ' -outputFormat tsv -outputFile ../out/' + file + '.entity')

for filename in os.listdir('out/'): 
	print(filename)
	src = 'out/' + filename
	dst = src.replace('entity', 'tag')
	os.rename(src, dst) 