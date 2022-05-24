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
	# '*' : 'notrussiansign',
	'@' : 'dialectsign',
	'#' : 'historicsign', #oldersign
	"$" : 'lexicsign', #lexicosign
	'+' : 'alternatesign',
	'=' : 'equivalentsign',
	'&' : 'featuresign',
	# '.alt' : 'featuresignalt'
}

SC = CyrillicOrderSorter(sortorderfile)
CD = CharacherDescription(unicodelibfile)

def getCharInfo(item):
	types = []
	unicodes = []
	for mark in marks:
		if mark in item:
			item = item.replace(mark, '')
			types.append(signtypes[mark]) # mark
	if '!' in item:
		unicodes = item.split('!')[1:]
		item = ''
		for uni in unicodes:
			item += chr(int(uni,16))
	else:
		for ch in item:
			_ch = '%04X' % ord(ch)
			unicodes.append(_ch)
	return {
		'sign': item,
		'unicodes': unicodes,
		'types': types
	}

def cascadeAltsChar(charsline):
	chars_list = [getCharInfo(sign) for sign in charsline.split(' ')]
	chars_list_wrap = []
	uniqunicodes = []
	if not charsline: return ([],[])
	for idx, item in enumerate(chars_list):
		sign = item['sign']
		unicodes = item['unicodes']
		types = item['types']
		alts = []
		for uni in unicodes:
			if uni not in uniqunicodes:
				uniqunicodes.append(uni)
		for nextitem in chars_list[idx + 1:]:
			_types = nextitem['types']
			if signtypes['+'] in _types or signtypes['='] in _types:# or signtypes['&'] in _types:
				_unicodes = nextitem['unicodes']
				alts.append({
					'sign': nextitem['sign'],
					'unicodes': _unicodes,
					'types': nextitem['types'],
					'alts': []
				})
				for uni in _unicodes:
					if uni not in uniqunicodes:
						uniqunicodes.append(uni)
			else:
				break
		if signtypes['+'] not in types and signtypes['='] not in types:# and signtypes['&'] not in types:
			chars_list_wrap.append({
				'sign': sign,
				'unicodes': unicodes,
				'types': types,
				'alts': alts
			})
	return (chars_list_wrap, uniqunicodes)


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

	uppercase_dialect = data['uppercase_dialect']
	lowercase_dialect = data['lowercase_dialect']
	uppercase_historic = data['uppercase_historic']
	lowercase_historic = data['lowercase_historic']
	uppercase_lexic = data['uppercase_lexic']
	lowercase_lexic = data['lowercase_lexic']

	# uppercase_alphabet_adds = data['uppercase_alphabet_adds']
	# lowercase_alphabet_adds = data['lowercase_alphabet_adds']


	upper_txtlist = []
	lower_txtlist = []

	(uppercase_alphabet, uppercase_unicodes) = cascadeAltsChar(uppercase_alphabet)
	(lowercase_alphabet, lowercase_unicodes) = cascadeAltsChar(lowercase_alphabet)

	(uppercase_dialect, uppercase_dialect_unicodes) = cascadeAltsChar(uppercase_dialect)
	(lowercase_dialect, lowercase_dialect_unicodes) = cascadeAltsChar(lowercase_dialect)

	(uppercase_historic, uppercase_historic_unicodes) = cascadeAltsChar(uppercase_historic)
	(lowercase_historic, lowercase_historic_unicodes) = cascadeAltsChar(lowercase_historic)

	(uppercase_lexic, uppercase_lexic_unicodes) = cascadeAltsChar(uppercase_lexic)
	(lowercase_lexic, lowercase_lexic_unicodes) = cascadeAltsChar(lowercase_lexic)


	# (uppercase_alphabet_adds, uppercase_unicodes_adds) = cascadeAltsChar(uppercase_alphabet_adds)
	# (lowercase_alphabet_adds, lowercase_unicodes_adds) = cascadeAltsChar(lowercase_alphabet_adds)
	l1 = set(uppercase_unicodes + uppercase_dialect_unicodes + uppercase_historic_unicodes + uppercase_lexic_unicodes)
	lowercase_unicodes_list = set(lowercase_unicodes + lowercase_dialect_unicodes + lowercase_historic_unicodes + lowercase_lexic_unicodes)
	uppercase_unicodes_list = set(l1).difference(lowercase_unicodes_list)
	uppercase_unicodes_list = SC.getSortedCyrillicList(uppercase_unicodes_list)
	lowercase_unicodes_list = SC.getSortedCyrillicList(lowercase_unicodes_list)
	print (name, uppercase_unicodes_list)

	outputdata = {
		'name_eng': name,

		'uppercase_characters_string': ' '.join([chr(int(x, 16)) for x in uppercase_unicodes_list]),
		'lowercase_characters_string': ' '.join([chr(int(x, 16)) for x in lowercase_unicodes_list]),
		'uppercase_unicodes_string': ' '.join(uppercase_unicodes_list),
		'lowercase_unicodes_string': ' '.join(lowercase_unicodes_list),

		'uppercase_alphabet': uppercase_alphabet,
		'lowercase_alphabet': lowercase_alphabet,

		'uppercase_dialect': uppercase_dialect,
		'lowercase_dialect': lowercase_dialect,

		'uppercase_historic': uppercase_historic,
		'lowercase_historic': lowercase_historic,

		'uppercase_lexic': uppercase_lexic,
		'lowercase_lexic': lowercase_lexic,

		# 'uppercase_alphabet_adds': uppercase_alphabet_adds,
		# 'lowercase_alphabet_adds': lowercase_alphabet_adds,

		'uppercase_unicodes_list': [{'unicode': uni, 'types': None, 'description': CD.getCharacterDescription(uni) } for uni in uppercase_unicodes_list],
		'lowercase_unicodes_list': [{'unicode': uni, 'types': None, 'description': CD.getCharacterDescription(uni) } for uni in lowercase_unicodes_list],
	}

	# print (outputdata)
	outputJSONfile = os.path.join(workpath, outputpath, '%s.json' % name)
	with open(outputJSONfile, "w") as write_file:
		json.dump(outputdata, write_file, indent = 4, ensure_ascii = False)

