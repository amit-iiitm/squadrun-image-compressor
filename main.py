import sys
from cStringIO import StringIO
from PIL import Image, ImageSequence
import urllib2
import string, random
import csv
import os
import json
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
	

#get the correct extension type
def get_extension(extn):
	extn_dict={'png':'PNG','jpg':'JPEG','jpeg':'JPEG','gif':'GIF','tiff':'TIFF','bmp':'BMP'}
	if extn in extn_dict.keys():
		return extn_dict[extn]
	else:
		return extn
	
def handle_gif(img,img_qlty,size_red,name,extn):
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
		frames_input.append(numpy.asarray(frame))
		frame.thumbnail((new_width,new_height),Image.ANTIALIAS)
		frames_numpy.append(numpy.asarray(frame))
	#save the original GIF
	imageio.mimsave(os.getcwd()+'/images/'+name+'.'+extn,frames_input)
	original_size=float(os.stat(os.getcwd()+'/images/'+name+'.'+extn).st_size)/1000
	#save the compressed GIF
	imageio.mimsave(os.getcwd()+'/images/'+name+'_new.'+extn,frames_numpy)
	compressed_size=float(os.stat(os.getcwd()+'/images/'+name+'_new.'+extn).st_size)/1000
	print "success"
	return json.dumps({"original_link":str(name)+extn,"compressed_link":str(name)+"_new."+extn,"compressed_size":compressed_size,"original_size":original_size})

#perform image compression using pil library
def compress_image(pic,img_qlty=80,size_red=0.5):
	#need to check if the pic is a file stored or a url
	#in case of a url first open it and then compress
	if checkURL(pic)==True:
		#encode to utf-8 for handling non-ascii character in the url
		pic=urllib2.quote(pic.encode('utf-8'),':/')
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
	print name
	extn=get_extension(extn)
	print extn
	if extn=='GIF':
		return handle_gif(img,img_qlty,size_red,name,extn)
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
#print compress_image('imdone.gif')
#print type(compress_image('https://media4.giphy.com/media/6ox6GvNJXifiE/giphy.gif'))
#compress_image('https://media0.giphy.com/media/3oKIPo7VdVtho7deRG/giphy.gif')
#print type(compress_image('amanda_seyfried_2017-t2.jpg'))
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
