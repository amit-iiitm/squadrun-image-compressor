import sys
from cStringIO import StringIO
from PIL import Image
import urllib2
import string, random
import csv
import os
import json
import images2gif
import ImageSequence
import Image
import gifmaker
import imageio
import numpy

#check if the url is a valid image url
def checkURL(link):
	prefix=link.split(':')[0]
	extn=link.split('.')[-1]
	if prefix in ['http','https'] and extn in ['JPG','JPEG','PNG','png','jpg','jpeg','gif','GIF','tiff','TIFF','bmp','BMP']:
		return True
	else:
		return False

#generate unique ID for the image of length 20
def generate_uid():
	uid=''
	for i in range(20):
		uid+=random.choice(string.lowercase)
	return uid
	
#perform image compression using pil library
def compress_image(pic,img_qlty=80,size_red=0.5):
	#need to check if the pic is a file stored or a url
	#in case of a url first open it and then compress
	if checkURL(pic)==True:
		#encode to utf-8 for handling non-ascii character in the url
		pic=urllib2.quote(pic.encode('utf-8'),':/')
		#modify request headers to access private urls also
		hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11','Accept': 'text/html,image/vnd.wap.wbmp, image/gif, image/jpg, image/jpeg, image/png, image/bmp, image/x-bmp,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'none','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'}
		req=urllib2.Request(pic, headers=hdr)
		img_url=urllib2.urlopen(pic)
		img_file=StringIO(img_url.read())
		#need to handle this case when a url containing gif is given, need to figure out how to get height and width of gif image
		img=Image.open(img_file)
		extn=pic.split('.')[-1]
		name=generate_uid()
	else:
		img=Image.open(pic)
		extn=pic.split('.')[-1]
		name=pic.split('.')[0]

	
	if extn not in ['JPG','JPEG','PNG','png','jpg','jpeg','gif','GIF','tiff','TIFF','bmp','BMP']:
		print "Invalid image"
		return
	if extn=='png':
		extn='PNG'
	elif extn=='gif':
		extn='GIF'
	elif extn=='tiff':
		extn='TIFF'
	elif extn=='bmp':
		extn='BMP'
	else:
		extn='JPEG'
	print name
	print extn
	if extn=='GIF':
		"""
		frames=images2gif.readGif(pic,False)
		for frame in frames:
			frame.thumbnail((100,100),Image.ANTIALIAS)
		images2gif.writeGif('rose99.gif',frames)"""
		print "GIf file detected"
		print img.size
		
		new_width=int(float(img.size[0])*(size_red))
		new_height=int(float(img.size[1])*(size_red))
		frames=[frame.copy() for frame in ImageSequence.Iterator(img)]
		"""frames=ImageSequence.Iterator(img)
		frame_list=[]
		for frame in frames:
			frame_list.append(frame.convert("P"))
		img.save('out.gif',save_all=True,append_images=frame_list)"""
		frames_numpy=[]
		frames_input=[]
		for frame in frames:
			frame=frame.convert('RGBA')
			print frame.size
			frames_input.append(numpy.asarray(frame))
			frame.thumbnail((new_width,new_height),Image.ANTIALIAS)
			
			frames_numpy.append(numpy.asarray(frame))
			print numpy.array(frame).shape
		#save the original GIF
		imageio.mimsave(os.getcwd()+'/images/'+name+'.'+extn,frames_input)
		original_size=float(os.stat(os.getcwd()+'/images/'+name+'.'+extn).st_size)/1000
		#save the compressed GIF
		imageio.mimsave(os.getcwd()+'/images/'+name+'_new.'+extn,frames_numpy)
		compressed_size=float(os.stat(os.getcwd()+'/images/'+name+'_new.'+extn).st_size)/1000
	else:
		
		new_width=int(float(img.size[0])*(size_red))
		new_height=int(float(img.size[1])*(size_red))
		img.save(os.getcwd()+'/images/'+name+'.'+extn,extn,optimize=True)
		print "the size of original image,", float(os.stat(os.getcwd()+'/images/'+name+'.'+extn).st_size)/1000
		original_size=float(os.stat(os.getcwd()+'/images/'+name+'.'+extn).st_size)/1000
		img=img.resize((new_width,new_height),Image.ANTIALIAS)
		img.save(os.getcwd()+'/images/'+name+'_new.'+extn,extn,quality=img_qlty,optimize=True)
		print "the size of image,", float(os.stat(os.getcwd()+'/images/'+name+'_new.'+extn).st_size)/1000
		compressed_size=float(os.stat(os.getcwd()+'/images/'+name+'_new.'+extn).st_size)/1000
		img.show()
		print "success"
	return json.dumps({"original_link":str(name)+extn,"compressed_link":str(name)+"_new."+extn,"compressed_size":compressed_size,"original_size":original_size})

#compress_image('https://images.rapgenius.com/e0c7cc55d92700bc29e53a8b7f50e014.1000x563x1.jpg')
#compress_image('http://res.cloudinary.com/private-demo/image/private/sheep.jpg')
#compress_image('foo.gif')
#compress_image('https://media4.giphy.com/media/6ox6GvNJXifiE/giphy.gif')
#compress_image('https://media0.giphy.com/media/3oKIPo7VdVtho7deRG/giphy.gif')
#compress_image('http://www.espncricinfo.com/db/PICTURES/CMS/209400/209441.3.jpg')
#compress_image('http://eeweb.poly.edu/~yao/EL5123/image/barbara_gray.bmp')

#read list of urls from csv file
def readURL(csv_file):
	url_list=[]
	with open(csv_file,'r') as f:
		reader=csv.reader(f)
		for line in reader:
			for col in line:
				print col
				if checkURL(col):
					url_list.append(col)
	print url_list
	return url_list
#readURL('images.csv')
