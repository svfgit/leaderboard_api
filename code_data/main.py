# Welcome to the Leaderboard API! By Sal (svferro@gmail.com)
#
# Note: not designed for production use! The objective was more 
# to be small, concise. (and have fun with it!) Maybe something
# that would be used to prototype an API or demo how an API
# could work before the production implementation.  Or use to help
# demonstrate some Python patterns for educational purposes.
#
# Please see the README for important points around 
# 'hows' and 'whys' of decisions made in this implementation.
#
# Run via 'python main.py' and open localhost:8080 if running locally!
# (Swap localhost for the IP of a server, docker container, etc.).  Or
# see README for instructions on how to run direct from the Git repo.
	

import cherrypy
import dateutil.parser as dt
from jsondb import loadJSONFolder, loadJSONString, query, formatJSON, data, dateFields
import requests

dateFields = ["start_date", "timestamp"] # Configures the JSON DB to parse dates

loadJSONFolder('project_data') # Loads data from the given data files for this project

class LeaderboardAPI(object):	
	# This is just a helper that runs at root URL, gives some useful links for testing
	@cherrypy.expose
	def index(self):
		return """
			Welcome to the Leaderboard API! Try these queries:<br><br>

			Note - after clicking the links, you will see parameters in the URL, change these to try different parameters.<br><br>

			<a href='/eventsForTimeRange?begin=7/21/19&end=8/21/19'>Events for a time range</a><br>
			<a href='/eventsForTempRange?begin=30&end=40'>Events for a temperature range</a><br>
			<a href='/weatherForDateRange?begin=7/21/19&end=8/21/19'>Weather during date range</a><br><br>
		"""
	
	@cherrypy.expose
	def eventsForTimeRange(self, begin, end):
		return formatJSON(query(op=lambda x,y: True if x=="start_date" and y>=dt.parse(begin) and y<=dt.parse(end)  else False, sort="start_date"))
	
	@cherrypy.expose
	def eventsForTempRange(self, begin, end):		
		tempDates = query(op=lambda x,y: True if x=="properties" and y["temperature"]["value"]>=int(begin) and y["temperature"]["value"]<=int(end)  else False)

		tempDatesSorted = sorted(tempDates, key = lambda i: i["properties"]["timestamp"])

		result=[]
		if len(tempDatesSorted):
			result=query(op=lambda x,y: True if x=="start_date" and y>=tempDatesSorted[0]["properties"]["timestamp"] and y<=tempDatesSorted[-1]["properties"]["timestamp"] else False, sort="start_date")
		return formatJSON(result)

	@cherrypy.expose
	def weatherForDateRange(self, begin, end):
		tempDates = query(op=lambda x,y: True if x=="properties" and y["timestamp"]>=dt.parse(begin) and y["timestamp"]<=dt.parse(end) else False)

		tempDatesSorted = sorted(tempDates, key = lambda i: i["properties"]["timestamp"])

		return formatJSON(tempDatesSorted)

cherrypy.server.socket_port = 8080
cherrypy.server.socket_host = '0.0.0.0'

cherrypy.quickstart(LeaderboardAPI())


