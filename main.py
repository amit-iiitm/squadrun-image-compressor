import sys
from boto.s3.connection import S3Connection
from cStringIO import StringIO
from PIL import Image
from cStringIO import StringIO
import urllib2
import string, random
import csv
import os
import json
aws_key=''
aws_secret=''
bucket_name=''

def checkURL(link):
	prefix=link.split(':')[0]
	extn=link.split('.')[-1]
	if prefix in ['http','https'] and extn in ['JPG','JPEG','PNG','png','jpg','jpeg']:
		return True
	else:
		return False
#generate unique ID for the image of length 6
def generate_uid():
	uid=''
	for i in range(6):
		uid+=random.choice(string.lowercase)
	return uid
	
def compress_image(pic,img_qlty=80,size_red=0.5):
	#need to check if the pic is a file stored or a url
	#in case of a url first open it and then compress
	if checkURL(pic)==True:
		img_url=urllib2.urlopen(pic)
		img_file=StringIO(img_url.read())
		img=Image.open(img_file)
		extn=pic.split('.')[-1]
		name=generate_uid()
	else:
		img=Image.open(pic)
		extn=pic.split('.')[-1]
		name=pic.split('.')[0]

	
	if extn not in ['JPG','JPEG','PNG','png','jpg','jpeg']:
		print "Invalid image"
		return
	if extn=='png':
		extn='PNG'
	else:
		extn='JPEG'
	print name
	print extn
	new_width=int(float(img.size[0])*(size_red))
	new_height=int(float(img.size[1])*(size_red))
	img.save(os.getcwd()+'/images/'+name+extn,extn,optimize=True)
	print "the size of original image,", float(os.stat(os.getcwd()+'/images/'+name+extn).st_size)/1000
	original_size=float(os.stat(os.getcwd()+'/images/'+name+extn).st_size)/1000
	img=img.resize((new_width,new_height),Image.ANTIALIAS)
	img.save(os.getcwd()+'/images/'+name+'_new.'+extn,extn,quality=img_qlty,optimize=True)
	print "the size of image,", float(os.stat(os.getcwd()+'/images/'+name+'_new.'+extn).st_size)/1000
	compressed_size=float(os.stat(os.getcwd()+'/images/'+name+'_new.'+extn).st_size)/1000
	img.show()
	print "success"
	return json.dumps({"original_link":str(name)+extn,"compressed_link":str(name)+"_new."+extn,"compressed_size":compressed_size,"original_size":original_size})
#compress_image('https://images.rapgenius.com/e0c7cc55d92700bc29e53a8b7f50e014.1000x563x1.jpg')

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
