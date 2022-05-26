# -*- coding: utf-8 -*-

import json
import os.path
import importlib
import random
import string
import PTLangLib
importlib.reload(PTLangLib)
from PTLangLib import *

workpath = 'langlib'
outputpath = 'output'
codeslangfile = 'cyrillic_lib.json'
sortorderfile = 'sortorder_cyrillic.txt'
unicodelibfile = 'unicode14.txt'

marks = ['*', '$', '#', '@', '(', ')', '[', ']', '+', '=', '&', '.alt']  # , '.alt'

dialectsign = '@'
historicsign = '#'
lexicsign = '$'
alternatesign = '+'
equivalentsign = '='
featuresign = '&'

signtypes = {
	# '*' : 'notrussiansign',
	dialectsign : 'dialectsign',
	historicsign : 'historicsign', #oldersign
	lexicsign : 'lexicsign', #lexicosign
	alternatesign : 'alternatesign',
	equivalentsign : 'equivalentsign',
	featuresign : 'featuresign',
	# '.alt' : 'featuresignalt'
}

SC = CyrillicOrderSorter(sortorderfile)
CD = CharacherDescription(unicodelibfile)


def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))

def getUniqName(cut=32):
	return 'id' + ran_gen(cut, "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

def getCharInfo(item, typestring = None):
	types = []
	unicodes = []
	for mark in marks:
		if typestring and typestring not in types:
			types.append(typestring)
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

def cascadeAltsChar(charsline, typestring = None, usedunicodes = None):
	chars_list = [getCharInfo(sign, typestring = typestring) for sign in charsline.split(' ')]
	chars_list_wrap = []
	uniqunicodes = []
	if usedunicodes:
		uniqunicodes.extend(usedunicodes)
	resultunicodes = []
	if not charsline: return ([],[],[])
	for idx, item in enumerate(chars_list):
		sign = item['sign']
		unicodes = item['unicodes']
		types = item['types']
		# if typestring and types and typestring not in types:
		# 	types.append(typestring)
		alts = []
		if unicodes and unicodes[0] and unicodes[0] not in uniqunicodes:
			uniqunicodes.append(unicodes[0])
			tp = None
			if len(unicodes) == 1:
				tp = types.copy()
				if typestring and typestring not in tp:
					tp.append(typestring)
			item = {
				'id': getUniqName(),
				'sign': chr(int(unicodes[0], 16)),
				'unicode': unicodes[0],
				'display_unicode': unicodes[0],
				'types': tp,
				'description': CD.getCharacterDescription(unicodes[0])
			}
			resultunicodes.append(item)

		# for uni in unicodes:
		# 	if uni not in uniqunicodes:
		# 		uniqunicodes.append(uni)
		for nextitem in chars_list[idx + 1:]:
			_types = nextitem['types']
			if signtypes[alternatesign] in _types or signtypes[equivalentsign] in _types:# or signtypes['&'] in _types:
				_unicodes = nextitem['unicodes']
				nexttypes = nextitem['types'].copy()
				# if typestring and nexttypes and typestring not in nexttypes:
				# 	nexttypes.append(typestring)
				if signtypes[alternatesign] in nexttypes and signtypes[featuresign] in nexttypes:
					nexttypes.remove(signtypes[alternatesign])
				alts.append({
					'id': getUniqName(),
					'sign': nextitem['sign'],
					'unicodes': _unicodes,
					'types': nexttypes, #nextitem['types'],
					'alts': []
				})
				if _unicodes and _unicodes[0] and _unicodes[0] not in uniqunicodes:
					uniqunicodes.append(_unicodes[0])
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring:
							tp.append(typestring)
					item = {
						'id': getUniqName(),
						'sign': chr(int(_unicodes[0], 16)),
						'unicode': _unicodes[0],
						'display_unicode': _unicodes[0],
						'types': tp,
						'description': CD.getCharacterDescription(_unicodes[0])
					}
					resultunicodes.append(item)
				elif _unicodes and _unicodes[0] in uniqunicodes and signtypes[alternatesign] in nextitem['types'] and signtypes[featuresign] in nextitem['types']:
					tp = None
					if len(_unicodes) == 1:
						tp = nexttypes.copy()
						if typestring:
							tp.append(typestring)
					item = {
						'id': getUniqName(),
						'sign': chr(int(_unicodes[0], 16)),
						'unicode': _unicodes[0],
						'display_unicode': _unicodes[0],
						'types': tp,
						'description': CD.getCharacterDescription(_unicodes[0])
					}
					resultunicodes.append(item)
				# for uni in _unicodes:
				# 	if uni not in uniqunicodes:
				# 		uniqunicodes.append(uni)
			else:
				break
		if signtypes[alternatesign] not in types and signtypes[equivalentsign] not in types:# and signtypes['&'] not in types:
			chars_list_wrap.append({
				'id': getUniqName(),
				'sign': sign,
				'unicodes': unicodes,
				'types': types,
				'alts': alts
			})
	return (chars_list_wrap, resultunicodes, uniqunicodes) # uniqunicodes


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

	upper_txtlist = []
	lower_txtlist = []

	(uppercase_alphabet, uppercase_unicodes, uppercase_usedunicodes) = cascadeAltsChar(uppercase_alphabet)
	(lowercase_alphabet, lowercase_unicodes, lowercase_usedunicodes) = cascadeAltsChar(lowercase_alphabet)

	(uppercase_dialect, uppercase_dialect_unicodes, uppercase_usedunicodes) = cascadeAltsChar(uppercase_dialect,
	                                                                                           typestring = signtypes[dialectsign],
	                                                                                           usedunicodes = uppercase_usedunicodes)
	(lowercase_dialect, lowercase_dialect_unicodes, lowercase_usedunicodes) = cascadeAltsChar(lowercase_dialect,
	                                                                  typestring = signtypes[dialectsign],
	                                                                  usedunicodes = lowercase_usedunicodes)

	(uppercase_historic, uppercase_historic_unicodes, uppercase_usedunicodes) = cascadeAltsChar(uppercase_historic,
	                                                                                            typestring = signtypes[historicsign],
	                                                                                            usedunicodes = uppercase_usedunicodes)
	(lowercase_historic, lowercase_historic_unicodes, lowercase_usedunicodes) = cascadeAltsChar(lowercase_historic,
	                                                                                            typestring = signtypes[historicsign],
	                                                                                            usedunicodes = lowercase_usedunicodes)

	(uppercase_lexic, uppercase_lexic_unicodes, uppercase_usedunicodes) = cascadeAltsChar(uppercase_lexic,
	                                                                                      typestring = signtypes[lexicsign],
	                                                                                      usedunicodes = uppercase_usedunicodes)
	(lowercase_lexic, lowercase_lexic_unicodes, lowercase_usedunicodes) = cascadeAltsChar(lowercase_lexic,
	                                                                                      typestring = signtypes[lexicsign],
	                                                                                      usedunicodes = lowercase_usedunicodes)


	uppercase_unicodes_list = uppercase_unicodes + uppercase_dialect_unicodes + uppercase_historic_unicodes + uppercase_lexic_unicodes#SC.getSortedCyrillicList(uppercase_unicodes_list)
	lowercase_unicodes_list = lowercase_unicodes + lowercase_dialect_unicodes + lowercase_historic_unicodes + lowercase_lexic_unicodes#SC.getSortedCyrillicList(lowercase_unicodes_list)


	outputdata = {
		'name_eng': name,

		# 'uppercase_characters_string': ' '.join([chr(int(x, 16)) for x in uppercase_unicodes_list]),
		# 'lowercase_characters_string': ' '.join([chr(int(x, 16)) for x in lowercase_unicodes_list]),
		# 'uppercase_unicodes_string': ' '.join(uppercase_unicodes_list),
		# 'lowercase_unicodes_string': ' '.join(lowercase_unicodes_list),

		'uppercase_alphabet': uppercase_alphabet,
		'lowercase_alphabet': lowercase_alphabet,

		'uppercase_dialect': uppercase_dialect,
		'lowercase_dialect': lowercase_dialect,

		'uppercase_historic': uppercase_historic,
		'lowercase_historic': lowercase_historic,

		'uppercase_lexic': uppercase_lexic,
		'lowercase_lexic': lowercase_lexic,

		'uppercase_unicodes_list': uppercase_unicodes_list,
		'lowercase_unicodes_list': lowercase_unicodes_list
	}

	outputJSONfile = os.path.join(workpath, outputpath, '%s.json' % name)
	with open(outputJSONfile, "w") as write_file:
		json.dump(outputdata, write_file, indent = 4, ensure_ascii = False)

