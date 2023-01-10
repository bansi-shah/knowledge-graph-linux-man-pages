tag_file = 'stanford-postagger-2018-10-16/text.tag'
# man_file = 'man7.org/linux/man-pages/man0/stdlib.h.0p.html'
entity_file = 'out.txt'

import re

#TODO: Restrict the sent length to +-w
def find_within_sentence():
	for i, sent in enumerate(replaced_man_file):
		match = re.search(r"\bJJ\b[a-zA-Z0-9,.\" ]*\bNN\b[a-zA-Z0-9,.\" ]\b", sent)
		# match = re.search(r"[a-zA-Z0-9,.\"= ]*NN[a-zA-Z0-9,.\"= ]*PREP[a-zA-Z0-9,.\"= ]*VV[a-zA-Z0-9,.\"= ]*NN[a-zA-Z0-9,.\"= ]*VV", sent)
		if match:
			print(replaced_man_file[i])
			print(man_file_contents[i])

def replace_with_tags():
	replaced_man_file = []
	for sent in man_file_contents:
		sentnew = []
		sent = sent.split()
		for word in sent:
			if tags.get(word, None) not in [None] and word in sent:
				sentnew.append(tags[word])
			else:
				sentnew.append(word)
		replaced_man_file.append(' '.join(sentnew))
	return replaced_man_file

tags = {}
with open(tag_file, 'r') as f:
	for row in f:
		row = row.split()
		if len(row) > 1:
			if row[1] == 'NNP':
				row[1] == 'NN'
			tags[row[0]] = row[1]

f = open(man_file, 'r')
man_file_contents = f.read()
man_file_contents = man_file_contents.split('\n')

f = open(entity_file, 'r')
entity = f.read()
entity = entity.split()

for word in entity:
	tags[word] = 'NN'

replaced_man_file = replace_with_tags()
find_within_sentence()