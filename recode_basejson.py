# -*- coding: utf-8 -*-

import json
import os.path
import importlib

import PTLangLib
importlib.reload(PTLangLib)
from PTLangLib import *

workpath = 'langlib'
outputpath = 'output'
codeslangfile = 'cyrillic_lib.json'
sortorderfile = 'sortorder_cyrillic.txt'
unicodelibfile = 'unicode14.txt'

marks = ['*', '$', '#', '@', '(', ')', '[', ']', '+', '=', '&', '.alt']  # , '.alt'
signtypes = {
	'*' : 'notrussiansign',
	'@' : 'dialectsign',
	'#' : 'oldersign',
	"$" : 'lexicosign',
	'+' : 'alternatesign',
	'=' : 'equivalentsign',
	'&' : 'featuresign',
	# '.alt' : 'featuresignalt'
}

# SC = CyrillicOrderSorter(sortorderfile)
# CD = CharacherDescription(unicodelibfile)
#
# def getCharInfo(item):
# 	types = []
# 	unicodes = []
# 	for mark in marks:
# 		if mark in item:
# 			item = item.replace(mark, '')
# 			types.append(signtypes[mark]) # mark
# 	if '!' in item:
# 		unicodes = item.split('!')[1:]
# 		item = ''
# 		for uni in unicodes:
# 			item += chr(int(uni,16))
# 	else:
# 		for ch in item:
# 			_ch = '%04X' % ord(ch)
# 			unicodes.append(_ch)
# 	return {
# 		'sign': item,
# 		'unicodes': unicodes,
# 		'types': types
# 	}

# def cascadeAltsChar(charsline):
# 	chars_list = [getCharInfo(sign) for sign in charsline.split(' ')]
# 	chars_list_wrap = []
# 	uniqunicodes = []
# 	if not charsline: return ([],[])
# 	for idx, item in enumerate(chars_list):
# 		sign = item['sign']
# 		unicodes = item['unicodes']
# 		types = item['types']
# 		alts = []
# 		for uni in unicodes:
# 			if uni not in uniqunicodes:
# 				uniqunicodes.append(uni)
# 		for nextitem in chars_list[idx + 1:]:
# 			_types = nextitem['types']
# 			if signtypes['+'] in _types or signtypes['='] in _types or signtypes['&'] in _types:
# 				_unicodes = nextitem['unicodes']
# 				alts.append({
# 					'sign': nextitem['sign'],
# 					'unicodes': _unicodes,
# 					'types': nextitem['types'],
# 					'alts': []
# 				})
# 				for uni in _unicodes:
# 					if uni not in uniqunicodes:
# 						uniqunicodes.append(uni)
# 			else:
# 				break
# 		if signtypes['+'] not in types and signtypes['='] not in types and signtypes['&'] not in types:
# 			chars_list_wrap.append({
# 				'sign': sign,
# 				'unicodes': unicodes,
# 				'types': types,
# 				'alts': alts
# 			})
# 	return (chars_list_wrap, uniqunicodes)

def splitAdds(txt):
	historic = []
	lexic = []
	dialect = []
	_t = txt.split(' ')
	for item in _t:
		if '$' in item:
			item = item.replace('$', '')
			lexic.append(item)
		if '#' in item:
			item = item.replace('#', '')
			historic.append(item)
		if '@' in item:
			item = item.replace('@', '')
			dialect.append(item)
	return (dialect, historic, lexic )



with open(codeslangfile, "r") as read_file:
	data = json.load(read_file)

names = []

for item in data:
	# print(item)
	names.append(item['name_eng'])



for name in names:
	namefile = os.path.join(workpath, '%s.json' % name)
	with open(namefile, "r") as read_file:
		data = json.load(read_file)
	uppercase_alphabet = data['uppercase_alphabet']
	lowercase_alphabet = data['lowercase_alphabet']
	uppercase_alphabet_adds = data['uppercase_alphabet_adds']
	lowercase_alphabet_adds = data['lowercase_alphabet_adds']

	uppercase_alphabet = uppercase_alphabet.replace('*','')
	lowercase_alphabet = lowercase_alphabet.replace('*','')

	(uppercase_dialect, uppercase_historic, uppercase_lexic) = splitAdds(uppercase_alphabet_adds)
	(lowercase_dialect, lowercase_historic, lowercase_lexic) = splitAdds(lowercase_alphabet_adds)

	uppercase_dialect = ' '.join(uppercase_dialect)
	lowercase_dialect = ' '.join(lowercase_dialect)
	uppercase_historic = ' '.join(uppercase_historic)
	lowercase_historic = ' '.join(lowercase_historic)
	uppercase_lexic = ' '.join(uppercase_lexic)
	lowercase_lexic = ' '.join(lowercase_lexic)

	print(name)
	# print(uppercase_alphabet)
	# print(lowercase_alphabet)
	# print(uppercase_dialect)
	# print(lowercase_dialect)
	# print(uppercase_historic)
	# print(lowercase_historic)
	# print(uppercase_lexic)
	# print(lowercase_lexic)

	data2 = data
	data2['uppercase_alphabet'] = uppercase_alphabet
	data2['lowercase_alphabet'] = lowercase_alphabet
	data2.pop('uppercase_alphabet_adds')
	data2.pop('lowercase_alphabet_adds')
	data2['uppercase_dialect'] = uppercase_dialect
	data2['lowercase_dialect'] = lowercase_dialect
	data2['uppercase_historic'] = uppercase_historic
	data2['lowercase_historic'] = lowercase_historic
	data2['uppercase_lexic'] = uppercase_lexic
	data2['lowercase_lexic'] = lowercase_lexic

	print (data2)
	outputJSONfile = namefile
	with open(outputJSONfile, "w") as write_file:
		json.dump(data2, write_file, indent = 4, ensure_ascii = False)



