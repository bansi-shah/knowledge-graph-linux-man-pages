import re
from os import listdir
from bs4 import BeautifulSoup

# man_file = 'man7.org/linux/man-pages/man0/stdlib.h.0p.html'
# man_file = 'man7.org/linux/man-pages/man7/tcp.7.html'
path = 'test/'

for files in listdir(path):
	man_file = path + files

	f = open(man_file, 'r')
	man_file_contents = f.read()
	f.close()

	soup = BeautifulSoup(man_file_contents, 'html.parser')
	h2tags = soup.find_all("h2")

	for each in h2tags:
		des = each.find('a', id='DESCRIPTION')
		if des is not None:
			description_html = str(each.next_sibling)
			description_html = description_html[5:-6]
			description_html_sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',description_html)

	for each in description_html_sentences:
		each = each.strip().replace('\n','').replace('\t', '').replace('&lt;','').replace('&gt;','')
		sent = re.sub(' +',' ', each)

		match = re.findall(r"[(][A-Z]+[)]", sent)
		flag = 0
		i = 0
		for m in match:
			index = sent.index(m)
			word = ''
			m = m.replace('(', '').replace(')', '')
			for char in m:
				try:
					i = sent.index(char, i, index)
					j = i
					while (sent[j] not in ('(', ' ', '<')):
						word += sent[j]
						j += 1
					word += ' '
				except:
					flag = 1
					break
			if not flag:
				print(word, match)
			else:
				break
