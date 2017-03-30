from flask import Flask, json, request, render_template
from flask import jsonify,send_from_directory,make_response
from werkzeug import secure_filename
import json
import os
import time
import string
import random
from main import compress_image, generate_uid, checkURL
import csv



app=Flask(__name__)

#setup the folder to store image
UPLOAD_FOLDER = os.getcwd()+'/uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER


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

#handle homepage route
@app.route('/')
def index():
	return render_template('index.html')

#performs compression of csv or image file
@app.route('/compress',methods=['GET','POST'])
def compress_img():
	file_obj=request.files["file_name"]
	qlty=request.form['qlty']
	size_red=request.form['size_red']
	file_obj.save(secure_filename(file_obj.filename))
	file_name=file_obj.filename
	print file_name
	print type(file_name)
	if file_name.split('.')[-1] in ['JPG','JPEG','PNG','png','jpg','jpeg']:
		#valid image file has been uploaded
		print "valid image file"
		size_red=float(size_red)/100
		qlty=int(qlty)
		print type(size_red)
		response=json.loads(compress_image(file_obj.filename,qlty,size_red))
		print "compressed the image"
		print response
		print type(response)
		host_port=request.url.split('/')[2]
		res_url='http://'+host_port+'/images/'+response["compressed_link"]
		print res_url
		return json.dumps({"response":"successfully compressed the image",'type':"Image file",'download_link':res_url,'original_size':response["original_size"],'compressed_size':response["compressed_size"]})
	elif file_name.split('.')[-1] in ['csv']:
		url_list=readURL(file_name)
		print url_list
		res_list=[]
		size_red=float(size_red)/100
		qlty=int(qlty)
		for url in url_list:
			print "iterating over the links"
			
			print "called for %s with %s %s",url, str(qlty), str(size_red)
			response=json.loads(compress_image(url,qlty,size_red))
			print response
			print type(response)
			host_port=request.url.split('/')[2]
			res_url='http://'+host_port+'/images/'+response["compressed_link"]
			print res_url
			res_list.append(res_url)
		with open('result.csv','w') as f:
			writer=csv.writer(f)
			for i in res_list:
				writer.writerow([i])
		return json.dumps({'response':'successfully processed csv file containing image urls','type':"CSV file",'download_link':'http://'+host_port+'/download/result.csv'})
	else:
		return json.dumps({"response":"Invalid image file"})
#http://www.espncricinfo.com/db/PICTURES/CMS/260800/260855.jpg
#http://www.espncricinfo.com/db/PICTURES/CMS/209400/209441.3.jpg

#handle multiple urls separated by enter
@app.route('/handleurls',methods=['GET','POST'])
def handle_url():
	links=str(request.form["url_name"]).split('\n')
	qlty=request.form['qlty']
	size_red=request.form['size_red']
	qlty=int(qlty)
	size_red=float(size_red)/100
	res_links=[]
	for link in links:
		temp_data={}
		print "iterating over the links"
		
		print "called for %s with %s %s",link, str(qlty), str(size_red)
		response=json.loads(compress_image(link.strip('\r'),qlty,size_red))
		print response
		print type(response)
		host_port=request.url.split('/')[2]
		res_link='http://'+host_port+'/images/'+response["compressed_link"]
		temp_data["download_link"]=res_link
		temp_data["original_size"]=response["original_size"]
		temp_data["compressed_size"]=response["compressed_size"]
		res_links.append(temp_data)
	print res_links
	print type(res_links)
	
	return json.dumps({"response":"received links","download_links":res_links})

#serve static csv file
@app.route('/download/<path:path>',methods=['POST','GET'])
def serve_csv(path):
	return send_from_directory('',path)
	
#serve static image files
@app.route('/images/<path:path>')
def send_files(path):
	return send_from_directory('images', path)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',threaded=True,port=5000)
