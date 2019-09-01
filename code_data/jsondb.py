
# Here lies a simple little JSON Database implementation!
# Supports loading JSON from strings, files. And querying the
# DB via lambdas (or generators if desired).

import json
import os
import dateutil.parser as dt
from datetime import datetime

# The entire DB sotred here.  Not ideal as a global,
# but this implementation was aimed at proof-of-concept 
# and minimalism. Better for this to be encapsulated for state
data={}

# Special fields that will be parsed into Python datetime object during
# the JSON load process. This allows them to be sorted and queried
# Can be customized by the module consumer.  
# As with previous, for production use this should be encapsulated.
dateFields = ["start_date", "timestamp"]

# Formats JSON datetimes into Python datetime objects while loading
# obj - see python json.load object_hook API
def formatDatesWhileLoading(obj):
        for i in dateFields:
            if i in obj.keys():
                obj[i]=dt.parse(obj[i], ignoretz=True)
        return obj

# Load all json files from a folder into the DB for querying, formatting dates
# Parameters: folder - string: Relative path to folder to be loaded.
def loadJSONFolder(folder):
    for filename in os.listdir(folder):
        with open(folder + '/' + filename, "r") as read_file:
            data[filename] = json.load(read_file, object_hook=formatDatesWhileLoading)

# Loads a JSON string into DB as Python objects, while formatting dates
# Parameters: str - JSON data as a string to be loaded
def loadJSONString(str):
	global data
	data = json.loads(str, object_hook=formatDatesWhileLoading)

# Main recursive DB query method. Traverses entire DB (or subset of DB for performance)
# O(n) performance, so use 'root' parameter to query subset of DB when possible
# Parameters:
#	- root: Python Object: Object to be recursively searched/queried 
#	- key: string: filter result set by Objects only containing this property
#	- result: list: stores result set
#	- op: callable: Typically a lambda. Returns True for (x,y) where x is a key and y 
#		is a value for that key, includes into result set when True. Skips if False
#		Used in the way SQL is used to query a relational DB. 
def search(root=data, key=None, result=[], op=None):
	if type(root)==dict:
		ret = {}
		for i in root.keys():
			ret[i]=search(root=root[i],key=key, result=result, op=op)
			if key != None and key==i: result.append(root)
			if op != None and op(i, ret[i]): result.append(root)
		return ret
	elif type(root)==list:
		return [search(i, key=key, result=result, op=op) for i in root]
	else:
		return root

# Helper function to search(). Returns the result set as this is more intuitive.
# Parameters: op: see search(), as it is a passthrough.  sort: if included sorts result set 
	# by the value stored in this key
def query(op=None, sort=None):
	result=[]
	search(result=result, op=op)
	if sort:result=sorted(result, key = lambda i: i[sort]) 
	return result

# Formats a Python object into JSON string. Converts datetimes in process.
# Parameters: data: Python object to be converted.
def formatJSON(data):
    def dateconvert(o):
        if isinstance(o, datetime):
            return o.__str__()
    return json.dumps(data, default=dateconvert)