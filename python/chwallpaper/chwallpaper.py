#!/usr/bin/env python
import sys, os, re, getopt, time, random

def set_wallpaper(filepath):
	if not os.path.exists(filepath):
		return False
		
	cmd = 'gconftool-2 --type string --set /desktop/gnome/background/picture_filename "%s"' % filepath
	os.system(cmd)
	
def get_files_list(folder):
	if not os.path.exists(folder):
		return None
		
	regx = re.compile('.*\.jpg$')
		
	filelist = []
	files = os.listdir(folder)
	for filename in files:
		matched = regx.search(filename)
		if matched is not None:
			filelist.append('%s%s%s' % (folder, os.path.sep, filename))
	
	return filelist

def get_next_image(curimage):
	curimage = random.randint(0, len(images))
	if curimage >= len(images):
		curimage = 0
	return curimage
	
def parse_argv(argv):
	if argv is None or len(argv) == 0:
		return
		
	sources = None
	delay = None
	
	opts, args = getopt.getopt(argv, 'c:s:d:', ['config=', 'sources=', 'delay='])
	for opt, param in opts:
		if opt == '-c' or opt == '--config':
			config = param
		if opt == '-s' or opt == '--sources':
			sources = param
		elif opt == '-d' or opt == '--delay':
			try:
				delay = int(param)
			except ValueError:
				pass
				
	return (config, sources, delay)
	
if __name__ == '__main__':
	config = ''
	sources = '%s%s%s' % (os.environ['HOME'], os.path.sep, 'Pictures')
	delay = 5
	
	if len(sys.argv) > 1:
		c,s,d = parse_argv(sys.argv[1:])
		if c is not None or s is not None:
			sources = ''
			
		if c is not None:
			config = c
		if s is not None:
			sources = s
		if d is not None:
			delay = d
	
	source_paths = []
	if sources != '':
		source_paths = sources.split(';')
		
	if config != '' and os.path.exists(config):
		config_file = open(config, 'r')
		paths = config_file.readlines()
		config_file.close()
		
		if paths is not None:
			for path in paths:
				source_paths.append(path.strip())
				
	print 'sources:'
	print source_paths
		
	images = []
	for folder in source_paths:
		items = get_files_list(folder)
		if items is not None:
			images.extend(items)
			
	if len(images) == 0:
		print 'Error: Image file(s) not found.'
		sys.exit(3)
			
	curimage = -1
	while True:
		curimage = get_next_image(curimage)
		print 'changing wallpaper ... (file: %d)' % curimage
		set_wallpaper(images[curimage])
		time.sleep(60 * delay)
		
