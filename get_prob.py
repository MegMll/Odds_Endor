import sys, os
import sqlite3
from pandas import read_sql_query
import json

import empire

def main(file_hunter, file_mission):
	#get info 
	with open(file_hunter, 'r') as f:
		temp = json.load(f)
		hunters_place = temp["bounty_hunters"]
		max_time = temp["countdown"]
	with open(file_mission, 'r') as f:
		falcon_millenium = json.load(f)
		
	#open db and get info
	if(os.path.isfile(falcon_millenium["routes_db"])):
		con = sqlite3.connect(falcon_millenium["routes_db"])
	else:
		con = sqlite3.connect(os.path.join(os.path.dirname(file_mission), falcon_millenium["routes_db"]))
	routes_df = read_sql_query("SELECT * from ROUTES", con)
	# close db
	con.close()

	#create empire map as an oriented graph
	new_empire = empire.Empire(routes_df, falcon_millenium["departure"], falcon_millenium["arrival"], falcon_millenium["autonomy"])
	prob = new_empire.can_they_make_it_on_time(max_time, hunters_place)
	
	print(prob)

if __name__=='__main__':
	main(sys.argv[1], sys.argv[2])