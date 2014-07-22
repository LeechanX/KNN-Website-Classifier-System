#-*- encoding=utf-8 -*-
from WebFeatureExtraction.WebFeature import WebFeature 

def main(webfilepaths):
	parser_results=[]
	for web in webfilepaths:
		webcode=''
		with open(webfilepaths[web],'r') as webpage:
			for line in webpage:webcode+=line
		parser=WebFeature(web)
		parser.set_title_and_meta(webcode)
		parser.participle_words()
		parser_results.append(parser)
	return parser_results