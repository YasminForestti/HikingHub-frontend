import streamlit as st
import gpxpy
import folium
import pandas as pd
import boto3
import json
import random
from streamlit_folium import st_folium
from streamlit_javascript import st_javascript


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

    serach_bar()
    
    # Render the map only if it hasn't been rendered yet
    if not map_rendered:
        st_folium(plot_map(all_points), height=  300, width = 1000, use_container_width = True)
        map_rendered = True
def serach_bar():
    with st.form("my_form"):
        st.write("Filters")
        comment = dict()
        comment["distance"] = st.slider("Maximun distances (km)", min_value=0, max_value=100, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")
        comment["location"] = st.text_input("Location")
        # comment["comment_description"] = st.text_input("desctiption")
        comment['Minimum ages'] = st.slider("Minimum Age", min_value=0, max_value=100, step=None, format=None, key=None, help=None, on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

        submitted = st.form_submit_button("Submit")

        if submitted:
            df_stored_data = download_files()
            if comment["location"] is not None or comment["location"] != "" or comment["location"] != " ":
                st.write(comment["location"])
                df_stored_data = df_stored_data[df_stored_data['activity_location'] == comment["location"] ]
            # if comment["distance"] is not None:
                # df_stored_data = df_stored_data[df_stored_data['activity_location'].find(comment["distance"])]
            # if comment["activity_age_group"] is not None:
            #     df_stored_data = df_stored_data[df_stored_data['activity_age_group'] >= comment["Minimum ages"]]

        return submitted
        #     client = boto3.client('s3', region_name='us-east-2')
        #     comment['comment_images'] = ""
        #     for activity_image in images:
        #         if activity_image is not None: 
        #             ext = activity_image.name.find(".")
        #             ext = activity_image.name[ext:]
        #             imageloc = 'commentimages/' + hl.md5(activity_image.name.encode('utf-8')).hexdigest() + ext
        #             comment['comment_images'] += imageloc + ","
        #             client.upload_fileobj(
        #                 Fileobj=activity_image,
        #                 Bucket='solvesdgs',
        #                 Key=imageloc,
        #                 ExtraArgs={'ACL': 'public-read'}  # This makes the file publicly readable
        #             )
        #     siteData["activity_comments"].append(comment)
        #     s3 = boto3.resource("s3")
        #     file = s3.Object("solvesdgs", "activityfiles/"+ hash+".json")
        #     file.put(Body=json.dumps(siteData))
        #     for key in st.session_state.keys():
        #         if key[:21] == "slideshow_swipeable_":
        #             del st.session_state[key]
def parse_gpx(gpxdf, number):
    points = []
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
        content_df= content_df[['activity_gpx','filename', 'color' , 'activity_name', 'activity_location', 'activity_age_group']] # in future kms
        json_df = pd.concat([json_df,content_df], ignore_index=True)

    return json_df

def plot_map(points):
    url = st_javascript("await fetch('').then(r => window.parent.location.href)")

    m = folium.Map(location=[points[0]['Latitude'], points[0]['Longitude']], zoom_start=5)
    seen = {}
    
    for point in points:
        if not seen.get(point['Number'], False):
            # Creating a link with HTML formatting
            point['filename'] = point['filename'].replace("activityfiles/", "")
            point['filename'] = point['filename'].replace(".json", "")
            link = str(url) + 'ActivityPage/?tripId=' + str(point['filename'])
           
            popup_content = '<a href="{link}"  target="_blank">{name}</a>'.format(link= link, name=point['activity_name'])
            folium.Marker(location=[point['Latitude'], point['Longitude']], popup=popup_content,
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
