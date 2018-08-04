import os
from PIL import Image

allowed_exts = ['.png','.jpg']

settings = {
	'INPUT_FOLDER': 'Input',
	'OUTPUT_FOLDER': 'Output',
	'OVERLAY_IMAGE': 'overlay.png',
	'FIT_TO_SOURCE': True,
	'OUTPUT_SIZE': 'source',
	'RESIZE_MODE' : Image.ANTIALIAS
}

with open('settings.txt','r') as f:
	for line in f.readlines():
		if line.replace(' ','')[0] in ['\n','#']: continue
		key, value = line.replace(' ','').replace('\n','').split('#')[0].split('=')
		settings[key] = value


if not os.path.exists(settings['INPUT_FOLDER']): os.makedirs(settings['INPUT_FOLDER'])
if not os.path.exists(settings['OUTPUT_FOLDER']): os.makedirs(settings['OUTPUT_FOLDER'])

overlay = Image.open(settings['OVERLAY_IMAGE'])
overlay = overlay.convert("RGBA")

for filename in os.listdir(settings['INPUT_FOLDER']):
	if os.path.splitext(filename)[1] not in allowed_exts:
		continue
	print(filename)

	background = Image.open(f'{settings["INPUT_FOLDER"]}/{filename}')
	background = background.convert("RGBA")

	size = settings['OUTPUT_SIZE']
	sizes = (background.size,overlay.size)
	larger = [0,1][sizes[0][0]*sizes[0][1] < sizes[1][0]*sizes[1][1]]


	if size == 'source':
		w, h = sizes[0]

	elif size == 'overlay':
		w, h = sizes[1]

	elif size == 'larger':
		w, h = sizes[larger]

	elif size == 'smaller':
		w, h = sizes[1 - larger]

	else:
		try:
			w, h = [int(i) for i in size.split(',')]
		except Exception:
			raise ValueError('wrong OUTPUT_SIZE format')

	foreground = overlay.resize((w, h), settings["RESIZE_MODE"])
	background = background.resize((w, h), settings["RESIZE_MODE"])

	background.paste(foreground, (0, 0), foreground)
	background.save(f'{settings["OUTPUT_FOLDER"]}/{filename}',"PNG")