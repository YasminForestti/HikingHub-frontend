import streamlit as st
import gpxpy
import folium
import pandas as pd
import boto3
import json
import random
from streamlit_folium import st_folium

# Define a global variable to track whether the map has been rendered
map_rendered = False

@st.cache_data
def read_files():
    df_content = download_files()
    all_points = []
    
    for index, row in df_content.iterrows():
        points = parse_gpx(row, index)
        all_points.extend(points)

    return all_points

def main():
    global map_rendered
    
    st.title("Beyond Aurora")
    st.markdown("---")
    
    # Call the read_files() function to fetch the data
    all_points = read_files()
    
    # Render the map only if it hasn't been rendered yet
    if not map_rendered:
        st_folium(plot_map(all_points))
        map_rendered = True

def parse_gpx(gpxdf, number):
    points = []
    # print(gpxdf)
    gpx_data = gpx = gpxpy.parse(gpxdf['activity_gpx']) 
    color = gpxdf['color']
    filename = gpxdf['filename']
    activity_name = gpxdf['activity_name']
    # print(color)
    for track in gpx_data.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({'Latitude': point.latitude, 'Longitude': point.longitude, 'Color': color, 'Number' : number, 'activity_name': activity_name, 'filename': filename})
    return points

def bucket_query_namefiles():
    activity_filenames = []
    session = boto3.Session()
    s3 = session.resource('s3') 
    bucket = s3.Bucket('solvesdgs')
    
    for obj in bucket.objects.all():
        if 'activityfiles' in obj.key:
            activity_filenames.append(obj.key)
            
    return activity_filenames[1:]  # Consider why you're skipping the first item

def generate_random_color():
    colors = ['black', 'lightgreen', 'lightblue', 'darkred', 'purple', 'lightred', 'lightgray', 'pink', 'green', 'cadetblue', 'gray', 'red', 'beige', 'blue', 'white', 'darkgreen', 'darkblue', 'darkpurple', 'orange']
    return colors[random.randint(0, len(colors)-1)]

def download_files():
    session = boto3.Session()
    s3 = session.resource('s3') 
    files_df = pd.DataFrame()
    filenames = bucket_query_namefiles()
    json_df = pd.DataFrame()
    for filename in filenames:
        content_object = s3.Object('solvesdgs', filename)
        file_content = content_object.get()['Body'].read()    
        json_content = json.loads(file_content)
        json_content['filename'] = filename
        json_content['color'] = generate_random_color()
        content_df = pd.DataFrame([json_content],  index=[0])
        content_df= content_df[['activity_gpx','filename', 'color' , 'activity_name']]
        json_df = pd.concat([json_df,content_df], ignore_index=True)

    return json_df

def plot_map(points):
    m = folium.Map(location=[points[0]['Latitude'], points[0]['Longitude']], zoom_start=12)
    seen = {}
    
    for point in points:
        if not seen.get(point['Number'], False):
            folium.Marker(location=[point['Latitude'], point['Longitude']],  popup= point['activity_name'],
                          icon=folium.Icon(color=point['Color'])).add_to(m)
        seen[point['Number']] = True

    grouped = pd.DataFrame(points).groupby('Number')

    for number_id, group_data in grouped:
        color_1 = group_data['Color'].iloc[0]
        locations = [(row['Latitude'], row['Longitude']) for index, row in group_data.iterrows()]
        folium.PolyLine(locations=locations, color=color_1).add_to(m)
        
    return m

if __name__ == "__main__":
    main()
