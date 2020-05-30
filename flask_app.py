from flask import Flask, render_template, url_for, flash, redirect, send_from_directory, json, jsonify
import pandas as pd
import os
from tweet_processor import *
from custom_forms import timeSeriesForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'password' #this can be changed to >=16 byte hex if security is an issue
# this app wont really be 'secure'. It is meant to be a prototype.

app_title = "COVID-19 Quarentine Sentiment Analytics"

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', appTitle=app_title, title='Home Page')

#@app.route("/googleMapsVisualization")

@app.route("/timeSeriesVisualization", methods=['GET', 'POST'])
def tsv():
	xAxis = []
	yAxis =[]
	form = timeSeriesForm()
	if form.validate_on_submit():
		#perforn tsv and show output
		#return a redered template including the output from our tsv
		analysis = TwitterSentimentAnalysis()
		lookback = form.lookback.data
		tweets_per_day = form.daily_sample_size.data

		#BEGIN ANALYSIS
		# This line below will take a lot of time
		# it is set to not allow the API calls to go above a certain limit
		# thus, it will take a lot of time for larger tweet per day values

		# The analysis is done each time a new user presses run

		byDate = analysis.get_by_date(analysis.get_tweet_range_df(lookback, tweets_per_day))
		xAxis = analysis.get_dates_as_list(byDate)
		yAxis = analysis.get_sentiment_as_list(byDate)

		print(xAxis)
		print(yAxis)

		return render_template(
			"timeSeriesVisualization.html",
			appTitle=app_title,
			title='Time Series Visualization',
			form=form,
			min=-1,
			max=1,
			labels=xAxis,
			values=yAxis)

	print("INVALID FIELDS")	
	return render_template(
		"timeSeriesVisualization.html",
		appTitle=app_title,
		title='Time Series Visualization',
		form=form,
		min=-1,
		max=1,
		labels=xAxis,
		values=yAxis)

@app.route("/googleMapsVisualization", methods=['GET', 'POST'])
def gmv():
	xAxis = []
	yAxis =[]
	form = timeSeriesForm()
	if form.validate_on_submit():
		#perforn tsv and show output
		#return a redered template including the output from our tsv
		analysis = TwitterSentimentAnalysis()
		lookback = form.lookback.data
		tweets_per_day = form.daily_sample_size.data

		#BEGIN ANALYSIS
		# This line below will take a lot of time
		# it is set to not allow the API calls to go above a certain limit
		# thus, it will take a lot of time for larger tweet per day values

		# The analysis is done each time a new user presses run

		df = analysis.get_tweet_range_df(lookback, tweets_per_day)
		df = analysis.get_lat_lons_and_senti(df)

		lats = [x for x in df['centroid_lats']]
		lons = [x for x in df['centroid_lons']]
		weights = [x for x in df['heatmap_weight']]

		return render_template(
			"googleMapsVisualization.html",
			appTitle=app_title,
			title='Google Maps Visulization',
			form=form,
			lat=lats,
			lon=lons,
			weight=weights)

	print("INVALID FIELDS")	
	return render_template(
		"googleMapsVisualization.html",
		appTitle=app_title,
		title='Google Maps Visulaization',
		form=form,
		lat=[],
		lon=[],
		weight=[])

if __name__ == '__main__':
	app.run(debug=True)