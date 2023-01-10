from bs4 import BeautifulSoup
import re
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords 

fileName = 'stdlib.h.0p.html'

stop_words = set(stopwords.words('english')) 

lemmatizer = WordNetLemmatizer() 

dict_w = {}

W=2
K=5

def removeNonAscii(text):
	out = ''
	for c in text:
		if ord(c) in range(128):
			out += c
	return out

with open(fileName) as f:
	htmlString = ''
	for line in f:
		htmlString += line

	soup = BeautifulSoup(htmlString, 'html.parser')
	h2tags = soup.find_all("h2")

	sentence_list = []
	
	for each in h2tags:
		des = each.find('a', id='DESCRIPTION')
		if des is not None:
			description_html = each.next_sibling
			#description = description_html.text
			description_html = str(description_html)
			description_html = description_html[5:-6]
			description_html_sentences = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',description_html)

			for each in description_html_sentences:
				each = each.strip().replace('\n','').replace('\t', '').replace('&lt;','').replace('&gt;','')
				each = re.sub(' +',' ',each)


				if each != '':
					each = removeNonAscii(each)

					all_i = []
					all_b = []
					all_href = []

					soup = BeautifulSoup(each, 'html.parser')
					for i in soup.find_all('i'):
						if 'Section' in i.text:
							section = i.text
						else:
							i = i.text.split()
							all_i.append(' '.join(i))
					#print all_i
					for b in soup.find_all('b'):
						b = b.text.split()
						all_b.append(' '.join(b))
					for href in soup.find_all('href'):
						all_href.append(href.text)

					each = each.decode('utf-8','ignore').encode("utf-8")

					all_caps_single = filter(None, [x for x in re.findall(r"([A-Z]+[\s_][A-Z]*)", each)])
					all_mentions = filter(None, [x for x in re.findall(r"[^ ]+\([0-9]+\)", each)])
					all_sys_files = filter(None, [x for x in re.findall(r"(/?[A-Za-z0-9.]+/[A-Za-z0-9.]+)+", each)])
					all_first_caps = filter(None, [x for x in re.findall(r"([A-Z][^A-Z\s_]+)+", each)])
					all_entities = set(all_i) | set(all_b) | set(all_href) | set(all_caps_single) | set(all_first_caps)

					sentence = str(each)
					for entity in all_entities:
						sentence = sentence.replace(entity, ' @@ENTITY@@'+entity+'@@ENTITY@@ ')

					print 'Sentence:\n ',sentence
					
					all_entities =  list(all_entities)
					all_entities = [x.decode('utf-8','ignore').encode("utf-8") for x in all_entities]
					print 'Entities:\n ',all_entities

					if len(all_entities)>=2:
						for i in range(0,len(all_entities)):
							for j in range(i+1,len(all_entities)):
								p = '@@ENTITY@@'+all_entities[i]+'@@ENTITY@@';
								q = '@@ENTITY@@'+all_entities[j]+'@@ENTITY@@';
								l=0
								#print "dsfad " + p+' cvas'+q
								
								S = sentence.split(' ')
								temp=[]
								for x in range(0,len(S)):
									if S[x][0:10]=='@@ENTITY@@' and S[x][-10:]!='@@ENTITY@@':
									
										r = x
										while S[r][-10:]!='@@ENTITY@@':
											r=r+1
										s=r+1
										r=x
										temp.append([r,s])
								for x in temp:
									S[x[0]:x[1]] = [' '.join(S[x[0]:x[1]])]

								S = [x for x in S if x!='']
								
								S = [x.decode('utf-8','ignore').encode("utf-8") for x in S] 
								#print S
								if p in S and q in S:
									if S.index(p) > S.index(q):
										p,q = q,p 
	
									if (p,q) not in dict_w:								
										if (q,p) not in dict_w:
											dict_w[(p,q)] = []	
										else:
											l=1
									#print "dsfad " + p+' cvas'+q								
									try:
        									start = S.index( p ) 
        									end = S.index( q, start )
										llist = S[start - W : start] + S[start+1:end] + S[end+1 : end + W+1]
										llist = [x.decode('utf-8','ignore').encode("utf-8") for x in llist]
	
										#print 'LList ',llist
										#print start
										tmp = []
										for word in llist:
											word = lemmatizer.lemmatize(word)
											word = lemmatizer.lemmatize(word,pos='a')
											word = lemmatizer.lemmatize(word,pos='v')
											word = lemmatizer.lemmatize(word,pos='r')
											word = lemmatizer.lemmatize(word,pos='s')	
											word = (word.encode('ascii','ignore')).decode('utf-8')
											if word not in stop_words:
												tmp.append(word)
										tmp = [x.decode('utf-8','ignore').encode("utf-8") for x in tmp]
										reg = re.compile(r'<.*>')
										tmp = [x for x in tmp if not reg.match(x)]
										print 'List of words which represents the relationshp between entites:\n ',tmp
										if l==1:
		        								dict_w[(q,p)] += tmp
										else:
		        								dict_w[(p,q)] += tmp 										
    									except ValueError:
											l = 0 										
								break #  only one entity 
							break  #--------only one entity
				


				break #---- for only one  sentence 



print '\nBag of words that represents the entities : \n ',dict_w


			

