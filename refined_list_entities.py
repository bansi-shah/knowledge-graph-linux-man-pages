import re
from os import listdir
from bs4 import BeautifulSoup

# man_file = 'man7.org/linux/man-pages/man0/stdlib.h.0p.html'
# man_file = 'man7.org/linux/man-pages/man7/tcp.7.html'
path = 'test/'
# path = 'man7.org/linux/man-pages/man7/'
section = None
title = None

def removeNonAscii(text):
	out = ''
	for c in text:
		if ord(c) in range(128):
			out += c
	return out

for files in listdir(path):
	man_file = path + files

	f = open(man_file, 'r')
	man_file_contents = f.read()
	# man_file_contents = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)', man_file_contents)
	f.close()

	print('Reading file ' + man_file + '\n')

	soup = BeautifulSoup(man_file_contents, 'html.parser')
	h2tags = soup.find_all("h2")
	title = soup.find('title').text
	
	for i in soup.findAll('i'):
		if 'Section' in i.text:
			section = i.text
			break

	all_entities = set()
	abbreviations = []

	for each in h2tags:
		des = each.find('a', id = 'DESCRIPTION')
		if des is not None:
			description_html = str(each.next_sibling)
			description_html = description_html[5:-6]
			description_html_sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',description_html)

			print(description_html_sentences)

			for each in description_html_sentences:
				each = each.strip().replace('\n','').replace('\t', '').replace('&lt;','<').replace('&gt;','>')
				each = re.sub(' +',' ',each)

				if each != '':
					all_i = []
					all_b = []
					all_href = []

					soup = BeautifulSoup(each, 'html.parser')
					for i in soup.find_all('i'):
						i = i.text.split()
						all_i.append(' '.join(i))

					for b in soup.find_all('b'):
						b = b.text.split()
						all_b.append(' '.join(b))

					# print(all_i)

					for href in soup.find_all('href'):
						all_href.append(href.text)

					all_caps_single = filter(None, [x for x in re.findall(r"([A-Z]+[\s_][A-Z]*)", each)])
					all_mentions = filter(None, [x for x in re.findall(r"[^ ]+\([0-9]+\)", each)])
					all_sys_files = filter(None, [x for x in re.findall(r"(/?[A-Za-z0-9.]+/[A-Za-z0-9.]+)+", each)])
					all_first_caps = filter(None, [x for x in re.findall(r"([A-Z][^A-Z\s_]+)+", each)])

					print(list(all_i), list(all_b), list(all_caps_single), list(all_mentions), list(all_sys_files), list(all_first_caps))
					
					all_entities |= set(all_i) | set(all_b) | set(all_href) | set(all_caps_single) | set(all_first_caps)

					sent = each
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
							abbreviations.append((word, match))
						else:
							break

	# with open('out/entities/' + files + '.entity', 'w') as f:
	# 	if title:
	# 		f.write('TITLE ' + title + '\n')
	# 	if section:
	# 		f.write('SECTION ' + section + '\n')

	# 	for entity in all_entities:
	# 		entity = removeNonAscii(entity)
	# 		f.write(entity + '\n')

	# 	f.write('\n\nABBREVIATIONS: \n')
	# 	for a,b in abbreviations:
	# 		f.write(a)
	# 		f.write('\t--\t')
	# 		f.write(b[0])
	# 		f.write('\n')
