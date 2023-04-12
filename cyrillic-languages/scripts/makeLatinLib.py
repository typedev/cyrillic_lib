# -*- coding: utf-8 -*-

import json
import os.path


descriptionsfile = 'latin_languages.txt'

applyChanges = True
workPath = os.path.dirname(__file__)

libraryPath = 'library'  # langlib

print('*' * 60)
print('Started reload description')
print(workPath)
basePath, _s = os.path.split(workPath)
print('basePath: %s' % basePath)
libraryPath = os.path.join(basePath, libraryPath)
print('libraryPath: %s' % libraryPath)

filedesc = open(descriptionsfile, mode = 'r')

data = list(filedesc)
filedesc.close()

key = None
txt = ''
strukt = []
item = {}

specialsigns = ['‘', '’']

def clearDangerSymbols(text):
	dangersymbols = {
		'\t': ' ',
		'\"': '\''
	}
	for k, v in dangersymbols.items():
		text = text.replace(k, v)
	return text

namesset = []
glyphsUpperSet = []
glyphsLowerSet = []

for idx, line in enumerate(data):
	if line.startswith('\n'):
		strukt.append(item)
		item = {}
	if line.startswith('#### '):
		name_lang = line.replace('####','').strip()
		name_eng = name_lang.split('@')[0].strip()
		name_rus = name_lang.split('@')[1].strip()
		item = dict(
			name_eng = name_eng,
			name_rus = name_rus,
			local = 'en',
			language_group_eng = [],
			language_group_rus = [],
			alt_names_eng = [],
			description_eng = '',
			description_rus = '',
		)
		item['glyphs_list'] = [ dict(
			type = 'alphabet',
			uppercase = '',
			lowercase = ''
		)]
		namesset.append( dict(
			name_eng = name_eng,
			name_rus = name_rus,
			code_pt = "1",
			enable = True
		))
	if line.startswith('###r'):
		rline = [ r.strip() for r in line.replace('###r','').strip().split(',') ]
		item['language_group_rus'] = rline

	if line.startswith('##e'):
		rline =  [ r.strip() for r in line.replace('##e', '').strip().split(',') ]
		item['alt_names_eng'] = rline

	if line.startswith('upper:'):
		gl = line.replace('upper: ','').strip()
		item['glyphs_list'][0]['uppercase'] = gl
		for g in gl.split(' '):
			if g not in glyphsUpperSet:
				glyphsUpperSet.append(g)

	if line.startswith('lower:'):
		gl = line.replace('lower: ','').strip()
		item['glyphs_list'][0]['lowercase'] = gl
		for g in gl.split(' '):
			if g not in glyphsLowerSet:
				glyphsLowerSet.append(g)

	if line.startswith('other:'):
		extendedline = line.replace('other: ','').strip()
		for ss in specialsigns:
			if ss in extendedline:
				extendedline = extendedline.replace(ss,'')
				if item['glyphs_list'][0]['uppercase']:
					item['glyphs_list'][0]['uppercase'] += ' %s' % ss
		if extendedline:
			el = extendedline.split(' ')
			while '' in el:
				el.remove('')
			if el:
				item['glyphs_list'].append( dict(
					type = 'extended',
					uppercase = ' '.join(el[:len(el)//2]),
					lowercase = ' '.join(el[len(el)//2:])
				))



errpath = []
for item in strukt:

	outputJSONfile = os.path.join(basePath, 'library', 'latin', 'base', '%s.json' % item['name_eng'] )
	print (outputJSONfile)
	print (item)

	if applyChanges:
		with open(outputJSONfile, "w") as write_file:
			json.dump(item, write_file, indent = 4, ensure_ascii = False)

outputJSONfile = os.path.join(basePath, 'library', 'latin', 'latin_library.json' )
print (outputJSONfile)
for item in namesset:

	print(item)
if applyChanges:
	with open(outputJSONfile, "w") as write_file:
		json.dump(namesset, write_file, indent = 4, ensure_ascii = False)
print(' '.join(glyphsUpperSet))
print(' '.join(glyphsLowerSet))
print(' '.join(sorted(glyphsUpperSet)))
print(' '.join(sorted(glyphsLowerSet)))
	# name_eng = item['name_eng']
	# print ('*'*30)
	# print (name_eng)


	# print('+' * 30)
	# print (item['language_group_eng'])
	# print('=' * 30)
	# print (item['description_eng'])
	# pathjson = os.path.join(libraryPath, '%s.json' % name_eng)
	# print (pathjson)
	# if os.path.exists(pathjson):
	# 	print('path Ok')
	# 	_data = {}
	# 	namefile = os.path.join(libraryPath, '%s.json' % name_eng)
	# 	with open(namefile, "r") as read_file:
	# 		data = json.load(read_file)
	# 	_data['name_eng'] = data['name_eng']
	# 	_data['name_rus'] = data['name_rus']
	# 	_data['local'] = data['local']
	# 	_data['language_group_eng'] = item['language_group_eng']
	# 	_data['language_group_rus'] = data['language_group_rus']
	# 	_data['alt_names_eng'] = data['alt_names_eng']
	# 	_data['description_eng'] = item['description_eng']
	# 	_data['description_rus'] = data['description_rus']
	# 	_data['glyphs_list'] = data['glyphs_list']
	# 	for k,v in _data.items():
	# 		print(k,v)
	# 	outputJSONfile = namefile
	# 	if applyChanges:
	# 		with open(outputJSONfile, "w") as write_file:
	# 			json.dump(_data, write_file, indent = 4, ensure_ascii = False)
	#
	# else:
	# 	errpath.append((name_eng, pathjson))

# for epath in errpath:
# 	print (epath)
#




