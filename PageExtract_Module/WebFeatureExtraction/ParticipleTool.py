#-*- encoding=utf-8 -*-
import jieba.analyse as topk
import jieba.posseg as pseg
import jieba as jb
import re

jb.load_userdict('PageExtract_Module/userdict.txt')

fi=open('PageExtract_Module/stopwords.txt','r')
stopwords=[]
filters=['eng','j','n','nr','nt','nrt','nrfg','vn','nz']
for line in fi:
	stopwords.append(line[:-1])
fi.close()
acc_eng=[]
fi_eng=open('PageExtract_Module/access_eng.txt','r')
for line in fi_eng: acc_eng.append(line[:-1])
fi_eng.close()

def wordworth(word):
	'check if the word is n. and is not stop word'
	return word.word.encode('utf-8') not in stopwords and \
	word.flag in filters and len(word.word.strip())>1
def get_all_important_words(sentence):
	import_words=''
	words_pond=[]
	words_list=jb.cut_for_search(sentence)
	for word in words_list:
		words_with_cixin=pseg.cut(word)
		words_with_cixin=filter(wordworth,words_with_cixin)
		words_pond+=words_with_cixin
	for word in words_pond:
		if word.flag=='eng':
			word.word=word.word.upper()
			if word.word not in acc_eng:continue
		import_words+=word.word.encode('utf-8')+'+'
	return import_words[:-1]
def get_all_important_words_for_test(sentence):
	import_words=''
	words_pond=[]
	words_list=pseg.cut(sentence)
	words_pond=filter(wordworth,words_list)
	for word in words_pond:
		if word.flag=='eng':
			word.word=word.word.upper()
			if word.word not in acc_eng:continue
		import_words+=word.word.encode('utf-8')+'+'
	return import_words[:-1]
def participle_title(title):
	'participle key words in title'
	if not title: return
	title=re.sub(r'(\w*\.)?\w+\.\w+','',title)
	#return get_all_important_words(title)
	return get_all_important_words_for_test(title)
def participle_keywords(keywords):
	'participle key words in meta[keywords]'
	if not keywords: return
	keywords=re.sub(r'(\w*\.)?\w+\.\w+','',keywords)
	#return get_all_important_words(keywords)
	return get_all_important_words_for_test(keywords)
def participle_description(description):
	'participle key words in meta[description]'
	if not description: return
	description=re.sub(r'(\w*\.)?\w+\.\w+','',description)
	#return get_all_important_words(description)
	return get_all_important_words_for_test(description)
def participle_content(content,n=30):
	'participle key words in content'
	if not content: return
	content_words=''
	words=topk.extract_tags(content,topK=n)
	words=[w for w in words if w not in stopwords]
	for word in words: content_words+=word.encode('utf-8')+'+'
	return content_words[:-1]