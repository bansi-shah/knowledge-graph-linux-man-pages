from bs4 import BeautifulSoup
import re
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords 
import os
import numpy as np
import zipfile

#fileName = 'stdlib.h.0p.html' #---- need to add for directory of files--------------------

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



with zipfile.ZipFile('test.zip') as z:
	for filename in z.namelist():
		if not os.path.isdir(filename):
			#----------- file reading ------------------------			
			with z.open(filename) as f:
				htmlString = ''
				for line in f:
					htmlString += line
				soup = BeautifulSoup(htmlString, 'html.parser')
				h2tags = soup.find_all("h2")
				sentence_list = []
		
				for each in h2tags:#------------part  1----------------------
					des = each.find('a', id='DESCRIPTION')
					if des is not None:
						description_html = each.next_sibling
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
							
								all_entities =  list(all_entities)
								all_entities = [x.decode('utf-8','ignore').encode("utf-8") for x in all_entities]
	
								#---------splitting sentence into words and store in a list 'S'  and do preprocessing so that an entity is taken as an entry to the list ------------------------
								S = sentence.split()
								temp=[]

								for x in range(0,len(S)):
									if S[x][0:10]=='@@ENTITY@@' and S[x][-10:]!='@@ENTITY@@':
										r = x
									
										while S[r][-10:]!='@@ENTITY@@':
											r=r+1
										s=r+1
										r=x
										temp.append([r,s])
		
								waste = 0 
								for x in temp:
							
									S[x[0]-waste : x[1]-waste] = [' '.join(S[x[0]-waste : x[1]-waste ])]
		
									S = [a for a in S if a!='']
								
									S = [a.decode('utf-8','ignore').encode("utf-8") for a in S] 
									waste += x[1] - x[0] -1					
								#----------------------------------------------------------------------------------------
								
								if len(all_entities)>=2: #-------------part 2----------------------------
									for i in range(0,len(all_entities)):
										for j in range(i+1,len(all_entities)):
											p = '@@ENTITY@@'+all_entities[i]+'@@ENTITY@@';
											q = '@@ENTITY@@'+all_entities[j]+'@@ENTITY@@';
											l=0
	
											if p in S and q in S:
												if S.index(p) > S.index(q):
													p,q = q,p 
		
												if (p[10:-10],q[10:-10]) not in dict_w:								
													if (q[10:-10],p[10:-10]) not in dict_w:
														dict_w[(p[10:-10],q[10:-10])] = []	
													else:
														l=1

												try:
	        											start = S.index( p ) 
	        											end = S.index( q, start )
													llist = S[start - W : start] + S[start+1:end] + S[end+1 : end + W+1]
													llist = [x.decode('utf-8','ignore').encode("utf-8") for x in llist]
		
													tmp = [] 
													for word in llist:
														if word[-1]=='.': ##
															word = word[0:-1]
														word = lemmatizer.lemmatize(word)
														word = lemmatizer.lemmatize(word,pos='a')
														word = lemmatizer.lemmatize(word,pos='v')
														word = lemmatizer.lemmatize(word,pos='r')
														word = lemmatizer.lemmatize(word,pos='s')	
														word = (word.encode('ascii','ignore')).decode('utf-8')
														#----------- stop word removal--------------
														if word not in stop_words and word[0:10]!='@@ENTITY@@':
															if bool(re.match('^[_()*;,.]+$',word) )==False :
																tmp.append(word)
	
													tmp = [x.decode('utf-8','ignore').encode("utf-8") for x in tmp]
													reg = re.compile(r'<.*>')
													tmp = [x for x in tmp if not reg.match(x)]
													if l==1:
					        								dict_w[(q[10:-10],p[10:-10])] += tmp
													else:
					        								dict_w[(p[10:-10],q[10:-10])] += tmp 											
	    											except ValueError:
														l = 0 										
											#break #  only one entity 
										#break  #--------only one entity
					
							#break #---- for only one  sentence 
					#break

#------------------------
#print(dict_w)


for x in dict_w:
	a = np.array(dict_w[x])
	u_elem,c_elem = np.unique(a, return_counts=True)
	B_O_W = np.column_stack((u_elem,c_elem))
	ind = np.argsort( B_O_W[:,1] )[::-1]; 
	B_O_W = [s[0] for s in B_O_W[ind[:K]] ]
	dict_w[x] = B_O_W
	
#print '\nBag of words that represents the entities : \n '

with open('output1.txt','w+') as f:
	for x in dict_w:
		f.write('Entity pair : ' + str(x) + '\n' + 'Relationships : \n')
		#f.write('\n')
		for y in range(0,len(dict_w[x])):
			if dict_w[x][y][0:10]=='@@ENTITY@@':
				f.write('\t' + dict_w[x][y] + '\n')#[10:-10]
			else:
				if dict_w[x][y][-10:-1]=='@@ENTITY@':
					f.write('\t' + dict_w[x][y] + '\n')#[0:-10]
				else:
					f.write('\t' + dict_w[x][y] + '\n')					
		f.write('\n')

'''
i=0
for x in dict_w:
	if i<=5:
		print x
		for y in range(0,len(dict_w[x])):
			print '-->',dict_w[x][y]
		print ''
		i += 1
#	print dict_w[1]'''
