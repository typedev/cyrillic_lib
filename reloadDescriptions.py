# -*- coding: utf-8 -*-

import json
import os.path

workpath = 'langlib'
outputpath = 'output'
codeslangfile = 'cyrillic_lib.json'
sortorderfile = 'sortorder_cyrillic.txt'
unicodelibfile = 'unicode14.txt'
descriptionsfile = 'langdesc-eng.txt'



filedesc = open(descriptionsfile, mode = 'r')
key = None
txt = ''
strukt = []
item = {}
data = list(filedesc)
for idx, line in enumerate(data):
	# line = line.rstrip()

	# if line and not line.startswith('@') and not line.startswith(';'):
	if line.startswith('\n'):
		strukt.append(item)
		item = {}
	if line.startswith('####'):
		name_eng = line.replace('####','').strip()
		item['name_eng'] = name_eng
	if line.startswith('# description english'):
		textl = []
		for t in data[idx+1:]:
			if t.startswith('\n'):
				item['description_eng'] = ''.join(textl)
				break
			else:
				textl.append(t)

errpath = []
for item in strukt:
	name_eng = item['name_eng']
	print (name_eng)
	print (item['description_eng'])
	pathjson = os.path.join(workpath, '%s.json' % name_eng)
	print (pathjson)
	if os.path.exists(pathjson):
		print('path Ok')



	else:
		errpath.append((name_eng, pathjson))

for epath in errpath:
	print (epath)






