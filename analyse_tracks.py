# coding: utf-8
### nlehuby - AbidjanTransport

import gpxpy
import csv
import os

path = "abidjan/"
dirs = os.listdir( path )

result = []

for filename in dirs:
    if not filename.endswith(".gpx"):
        continue
    elem = {}
    with open(path + filename, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        elem["distance"] = round(gpx.length_2d())
        elem["duration"] = round(gpx.get_duration()/60)
        elem["average_speed"] = round((gpx.length_2d() / 1000) / (gpx.get_duration() / 3600))
        explode = filename.split('_')
        elem["line"] = explode[0]
        elem["direction"] = explode[1]
        elem["gpx"] = filename

        arrets = [elem for elem in gpx.waypoints if elem.name in stop_waypoints]
        elem["stop_number"] = len(arrets)
        elem["other_meta_number"] = len(gpx.waypoints) - len(arrets)

    result.append(elem)

headers = ["gpx", "line", "direction", "duration", "distance", "average_speed", "stop_number" ,"other_meta_number", "josm_link"]
with open("analyse_gpx.csv", 'w') as myfile:
    wr = csv.DictWriter(myfile, quoting=csv.QUOTE_ALL, fieldnames = headers)
    wr.writeheader()
    for a_row in result :
        wr.writerow(a_row)
