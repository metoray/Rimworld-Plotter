import matplotlib.pyplot as plt
import struct
from base64 import b64decode as decode
import numpy as np
from sys import argv, exit
import xml.etree.ElementTree as ET

save_location = "/home/metoray/.config/unity3d/Ludeon Studios/RimWorld/Saves/"

if not len(argv) > 1:
	print "Usage: python plotrw.py [save name]"
	exit(0)

def show_map(image_bytes,width,height):
	grid = np.frombuffer(image_bytes,"<H")
	grid = np.reshape(grid,(width,height))[::-1,:]

	ax = plt.gca()
	fig = plt.gcf()
	img = ax.imshow(grid)
	img.set_interpolation('nearest')

	def onclick(event):
	    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(event.button, event.x, event.y, event.xdata, event.ydata)
	    print vars(event)
	    for k,v in vars(event).iteritems():
	    	print str(k) + "\t" + str(v)
	    x = int(round(event.xdata))
	    y = int(round(event.ydata))
	    (x,y) = (y,x)
	    print hex(grid[x,y])

	cid = fig.canvas.mpl_connect('button_press_event', onclick)
	plt.show()

full_path = save_location+argv[1]+".rwm"
tree = ET.parse(full_path)
root = tree.getroot()
image_bytes = decode(root.find("terrainGrid").find("terrainGridCompressed").text)

size = root.find("mapInfo").find("size").text[1:-1]
width, _, height = map(int, size.split(","))

show_map(image_bytes,width,height)
