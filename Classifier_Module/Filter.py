#-*- encoding=utf-8 -*-
from TestObj import TestObj

def entitystandard(access_entitys):
	classifier_inputs=[]
	for entity in access_entitys:
		testobj=TestObj(entity.url)
		title,keyword,description=structstandard(entity)
		testobj.setText(title,keyword,description)
		classifier_inputs.append(testobj)
	return classifier_inputs

def structstandard(entity):
	if not entity or not entity.url:
		return ('uk','uk','uk')
	title=entity.title if entity.title else 'uk'
	keyword=entity.meta['keywords'] if entity.meta and 'keywords' in entity.meta \
	and entity.meta['keywords'] else 'uk'
	description=entity.meta['description'] if entity.meta and 'description' in entity.meta \
	and entity.meta['description'] else 'uk'
	return (title,keyword,description)

def check_access(entity):
	retval=False
	if structstandard(entity)!=('uk','uk','uk'):
		retval=True
	return retval

def main(parser_results):
	access_entity=[];unaccess_entity=[]
	for entity in parser_results:
		if check_access(entity):
			access_entity.append(entity)
		else:
			unaccess_entity.append(entity)
	classifier_inputs=entitystandard(access_entity)
	return classifier_inputs,unaccess_entity