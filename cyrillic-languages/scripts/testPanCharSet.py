import sys
import json
import os.path
import random
import string


libraryMainFile = 'cyrillic_library.json'
libraryGlyphsList = 'glyphs_list_categories.json'
unicodeLibFiles = ['unicode14.txt', 'PT_PUA_unicodes-descritions.txt']

def testCharactersSet(workPath):
	print('*' * 60)
	print('testing MainCharactersSet')
	print(workPath)
	basePath, _s = os.path.split(workPath)
	print('basePath: %s' % basePath)
	libraryPath = os.path.join(basePath, 'library')
	print('libraryPath: %s' % libraryPath)

	libraryMainFilePath = os.path.join(basePath, libraryMainFile)
	if not os.path.exists(libraryMainFilePath):
		print('Main library file not found: %s' % libraryMainFilePath)
		return
	print('libraryMainFile: %s' % libraryMainFilePath)

	with open(libraryMainFilePath, "r") as read_file:
		data = json.load(read_file)

	names = []
	for item in data:
		if item['enable']:
			names.append(item['name_eng'])

	unicodedlist_UC = {}
	nonunicodedlist_UC = {}
	puazonelist_UC = {}

	unicodedlist_LC = {}
	nonunicodedlist_LC = {}
	puazonelist_LC = {}

	for name in names:
		mainfile = os.path.join(libraryPath, '%s.json' % name)
		inputJSONfile = os.path.join(basePath, 'site', 'baselib', '%s.json' % name)

		if os.path.exists(inputJSONfile):
			with open(inputJSONfile, "r") as read_file:
				data = json.load(read_file)
			print('%s path:%s' % (name, inputJSONfile))

			local = 'ru'
			if os.path.exists(mainfile):
				with open(mainfile, "r") as read_file:
					maindata = json.load(read_file)
				print('%s path:%s' % (name, mainfile))
				local = maindata['local']
			print('LOCAL:', local)

			uppercase_unicodes_list = None
			lowercase_unicodes_list = None
			glyphs_lists = data['glyphs_list']
			for glyphslist in glyphs_lists:
				typelist = glyphslist['type']
				if typelist == 'charset':
					uppercase_unicodes_list = glyphslist['uppercase']
					lowercase_unicodes_list = glyphslist['lowercase']
			if uppercase_unicodes_list and lowercase_unicodes_list:
				for item in uppercase_unicodes_list:
					if len(item['types']) != 1:
						print (item['sign'], item['types'])
				for item in lowercase_unicodes_list:
					if len(item['types']) != 1:
						print(item['sign'], item['types'])



def main (names=None):
	pathname = os.path.dirname(sys.argv[0])
	workPath = os.path.abspath(pathname)
	testCharactersSet(workPath)

if __name__ == '__main__':
	main(names = sys.argv[1:])