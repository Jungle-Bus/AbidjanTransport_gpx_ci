# coding: utf-8
### nlehuby - AbidjanTransport

import gpxpy
import csv
import os
import datetime

path = "abidjan/"
dirs = os.listdir( path )

stop_waypoints = ["abribus", "arrêt sans indication","poteau", "vide", "mi-plein", "plein", "surchargé"]

result = []

def get_mode_or_line(track_name):
    if "gbaka" in track_name.lower():
        return "gbaka"
    if "w_r_" in track_name.lower():
        return "woro woro"
    return filename.split('_')[0]

def get_direction(track_name):
    if "_A_" in track_name:
        return "A"
    if "_B_" in track_name:
        return "B"
    return "?"

def get_is_peak_hour(gpx_time):
    if gpx_time <datetime.time(hour=8) :
        if gpx_time > datetime.time(hour=7):
            return True
    if gpx_time <datetime.time(hour=19):
        if gpx_time > datetime.time(hour=18):
            return True
    return False

for filename in dirs:
    if not filename.endswith(".gpx"):
        continue
    elem = {}
    with open(path + filename, "r") as gpx_file:
        gpx = gpxpy.parse(gpx_file)
        elem["distance"] = round(gpx.length_2d())
        elem["duration"] = round(gpx.get_duration()/60)
        elem["average_speed"] = round((gpx.length_2d() / 1000) / (gpx.get_duration() / 3600))
        elem["line"] = get_mode_or_line(filename)
        elem["direction"] = get_direction(filename)
        elem["gpx"] = filename

        start_time, _ = gpx.get_time_bounds()
        elem["date"] = start_time.strftime('%Y-%m-%d')
        elem["heure pointe"] = (get_is_peak_hour(start_time.time()))

        arrets = [elem for elem in gpx.waypoints if elem.name in stop_waypoints]
        elem["stop_number"] = len(arrets)
        elem["other_meta_number"] = len(gpx.waypoints) - len(arrets)

    result.append(elem)

result = sorted(result, key=lambda k: k['date'], reverse=True)

headers = ["line", "direction", "duration", "distance", "average_speed", "stop_number" ,"other_meta_number", "date", "heure pointe", "gpx"]
with open("abidjan/analyse_gpx.csv", 'w') as myfile:
    wr = csv.DictWriter(myfile, quoting=csv.QUOTE_ALL, fieldnames = headers)
    wr.writeheader()
    for a_row in result :
        wr.writerow(a_row)
