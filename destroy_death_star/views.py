from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

import sqlite3
import os
from pandas import read_sql_query
import json

from .empire import Empire

def create_empire():
    file_mission = "./info/millennium-falcon.json"
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
    return Empire(routes_df, falcon_millenium["departure"], falcon_millenium["arrival"], falcon_millenium["autonomy"])

def load_bounty_hunters(f):
    file_loc = os.path.join('./info', f)
    if '.json' in file_loc:
        try:
            with open(file_loc, 'r') as hunter_file:
                temp = json.load(hunter_file)
                hunters_place = temp["bounty_hunters"]
                max_time = temp["countdown"]
                return max_time, hunters_place
        except:
            print('problem invalid file')
            return -1


############################### VIEWS 
prob = -1

@csrf_exempt
def home(request):
    global prob
    if request.method == 'POST' and request.FILES['empire_info']:
        new_empire = create_empire()
        file_empire = request.FILES['empire_info']
        fs = FileSystemStorage()
        filename = fs.save(file_empire.name, file_empire)
        uploaded_file_url = fs.url(filename)
        max_time, hunters = load_bounty_hunters(uploaded_file_url)
        if max_time != -1:
            prob = new_empire.can_they_make_it_on_time(max_time, hunters)
            return redirect('results')            

    return render(request, 'home.html', context={'proba':prob})

def result(request):
    print(prob)
    return render(request, 'prob.html', context={'proba':prob})