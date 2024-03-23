import streamlit as st
import gpxpy
import folium
from streamlit_folium import st_folium

def parse_gpx(file_path, color='red'):
    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []
    number = 0 
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({'Latitude': point.latitude, 'Longitude': point.longitude, 'Color': color, 'Number' : number})
        number +=1
    return points

def read_files():
    # List of GPX files app_streamlit/0a7b419.gpx   app_streamlit/0ab9d37.gpx
    gpx_files = ["00c6622.gpx", '0a7b419.gpx', '0ab9d37.gpx']  # Add your GPX file paths here
    colors = {'00c6622.gpx': 'red', '0a7b419.gpx': 'blue', '0ab9d37.gpx': 'green'}  # Colors for each GPX file

    # Parse each GPX file
    all_points = []
    for file, color in colors.items():
        points = parse_gpx(file, color)
        all_points.extend(points)
    return all_points

def plot_map(points):
    m = folium.Map(location=[points[0]['Latitude'], points[0]['Longitude']], zoom_start=12)
    seen = {}
    for point in points:
        if seen[point['Number']] != 1:
            folium.Marker(location=[point['Latitude'], point['Longitude']],
                      icon=folium.Icon(color=point['Color'], icon='info-sign')
                      ).add_to(m)
        seen[point['Number']] = 1
    return m

all_points = read_files()
st_folium(plot_map(all_points))


