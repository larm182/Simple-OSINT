#!/usr/bin/python
#-*- coding: utf-8 -*-
#Autor: Luis Angel Ramirez Mendoza

from flask import Flask, render_template, request, Response, redirect, send_file, jsonify
import folium
from geopy.geocoders import Nominatim
import urllib.request
import json
import os
import phonenumbers 
from phonenumbers import carrier, geocoder, timezone
from opencage.geocoder import OpenCageGeocode

key = 'Tu key'

app = Flask(__name__)

path = os.getcwd() + "/output/"

@app.route('/')
def route():
	return render_template("index.html")

@app.route('/geo')
def geo():
    return render_template('geo.html')

@app.route('/ip')
def ip():
    return render_template('ip.html')

@app.route('/id')
def id():
    return render_template('id.html')

@app.route('/envia', methods=['GET', 'POST'])
def geo_html():
	if request.method == 'POST':
		url = request.form['url']
		geolocator = Nominatim(user_agent="GetLoc")
		location = geolocator.geocode(url)
		print(location.address)
		print((location.latitude, location.longitude))
		m = folium.Map(location=[location.latitude, location.longitude])
		m.save(path + 'location.html')
		with open( path + 'location.html', "r") as f:
			content = f.read()
		return Response(content, mimetype='text/html')
		#return render_template('ubicacion.html')

@app.route('/envia2', methods=['GET', 'POST'])
def ip_html():
	if request.method == 'POST':
		ip = request.form['url']
		url = urllib.request.urlopen("http://geolocation-db.com/jsonp/"+ip)
		data = url.read().decode()
		data = data.split("(")[1].strip(")")
		#print(data)
		parsed = json.loads(data)
		print(json.dumps(parsed, indent=4, sort_keys=True))
		parsed_2 = json.dumps(parsed, indent=4, sort_keys=True) 
		#return jsonify(parsed)
		#return render_template('out.html', temp={'ip_html':parsed})
		return render_template('out.html', temp=parsed_2)

@app.route('/envia3', methods=['GET', 'POST'])
def id_html():
	if request.method == 'POST':
		mobile = request.form['url']
		mobile = phonenumbers.parse(mobile)
		geocoder2 = OpenCageGeocode(key)
		query = str(mobile)
		results = geocoder2.geocode(query)
		a = timezone.time_zones_for_number(mobile)
		print(a)
		b = carrier.name_for_number(mobile, "en")
		print(b)
		c = geocoder.description_for_number(mobile, "en")
		print(c)
		d =  phonenumbers.is_valid_number(mobile)
		print("Valid mobile number: ", d)
		e = phonenumbers.is_possible_number(mobile)
		print("Checking possibity of Number: ", e )
		print(results)
		results_1 = "Town: " + f"{a}" + ", " + "Operator: " f"{b}" + ", " + "Contry: "+ f"{c}" + ", " + "Geolocation: " f"{results}" + ", " + "Valid mobile number: " + f"{d}" + ", " + "Checking possibity of Number: " + f"{d}"
		#return results_1

		return render_template('out_2.html', temp=results_1)



if __name__ == '__main__':
	app.run(host='localhost')
