import os
from PIL import Image

allowed_exts = ['.png','.jpg']

settings = {
	'INPUT_FOLDER': 'Input',
	'OUTPUT_FOLDER': 'Output',
	'OVERLAY_IMAGE': 'overlay.png',
	'FIT_TO_SOURCE': True,
	'SIZE': False
}

with open('settings.txt','r') as f:
	for line in f.readlines():
		if line.replace(' ','')[0] in ['\n','#']: continue
		key, value = line.replace(' ','').replace('\n','').split('#')[0].split('=')

		if key == '':
			continue

		if value.lower() == 'true':
			value = True

		elif value.lower() == 'false':
			value = False

		else:
			try:
				value = eval(value)

			except Exception:
				pass

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

	if settings['SIZE']:
		w, h = settings['SIZE']
	elif settings['FIT_TO_SOURCE'] == True:
		w, h = background.size
	else:
		w, h = overlay.size

	foreground = overlay.resize((w, h), Image.ANTIALIAS)
	background = background.resize((w, h), Image.ANTIALIAS)

	background.paste(foreground, (0, 0), foreground)
	background.save(f'{settings["OUTPUT_FOLDER"]}/{filename}',"PNG")