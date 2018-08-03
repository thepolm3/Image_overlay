import os
from PIL import Image

allowed_exts = ['.png','.jpg']

def getFileContaining(string, path = None):
	for filename in os.listdir(path):
	    if string in filename:
	        break
	else:
	    return None
	return filename

overlay = Image.open(getFileContaining('overlay'))
overlay = overlay.convert("RGBA")

for filename in os.listdir('Input'):
	if os.path.splitext(filename)[1] not in allowed_exts:
		continue
	print(filename)

	background = Image.open(f'Input/{filename}')
	background = background.convert("RGBA")

	w, h = background.size
	foreground = overlay.resize((w, h), Image.ANTIALIAS)  

	background.paste(foreground, (0, 0), foreground)
	background.save(f'Output/{filename}',"PNG")