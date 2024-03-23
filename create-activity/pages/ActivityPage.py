import streamlit as st
from streamlit_elements import elements, mui, html, sync
import gpxpy 
import gpxpy.gpx
import pandas as pd
import boto3
import json
import hashlib as hl
import folium
from streamlit_folium import st_folium


def plot_map(points): 
    m = folium.Map(location=[points[0]['Latitude'], points[0]['Longitude']], zoom_start=12) 
    seen = {} 
     
    for point in points: 
        if not seen.get(point['Number'], False): 
            folium.Marker(location=[point['Latitude'], point['Longitude']], 
                          icon=folium.Icon(color=point['Color'], icon='info-sign')).add_to(m) 
        seen[point['Number']] = True 
    grouped = pd.DataFrame(points).groupby('Number') 
 
    for number_id, group_data in grouped: 
        color_1 = group_data['Color'].iloc[0] 
        locations = [(row['Latitude'], row['Longitude']) for index, row in group_data.iterrows()] 
        folium.PolyLine(locations=locations, color=color_1).add_to(m) 
         
    return m


def process_gpx_to_df(file_name): 
    #gpx = gpxpy.parse(open(file_name))  
    gpx = gpxpy.parse(file_name)
    #(1)make DataFrame 
    track = gpx.tracks[0] 
    segment = track.segments[0] 
    # Load the data into a Pandas dataframe (by way of a list) 
    data = [] 
    segment_length = segment.length_3d() 
    for point_idx, point in enumerate(segment.points): 
        data.append([point.longitude, point.latitude,point.elevation, 
        point.time, segment.get_speed(point_idx), 10]) 
        columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed', 'Size'] 
        gpx_df = pd.DataFrame(data, columns=columns) 
         
    #2(make points tuple for line) 
    points = [] 
    for track in gpx.tracks: 
        for segment in track.segments:  
            for point in segment.points: 
                points.append(tuple([point.latitude, point.longitude])) 
                
    return gpx_df, points


class Comment(object):
  def __init__(self,userurl, username, title, text, images):
    self.userurl = userurl
    self.username = username
    self.title = title
    self.text = text
    self.images = images


comments = [Comment("https://www.google.com/","John", "Wow", "look at this", ["https://cdn.discordapp.com/attachments/1220854776321933424/1220854824090865794/hikeman.jpg?ex=661074a8&is=65fdffa8&hm=6ea332c0f680b0016e7d2b28a5112c62670b5e9ccd2b75430df72378f43dd741&","https://cdn.discordapp.com/attachments/1220854776321933424/1220855680689373224/s-man-hiking-backpacking-foggy-cloudy-finland-autumn-forest-lakeside.png?ex=66107574&is=65fe0074&hm=c4ef5789df7aa810b13fdf49e763bb0978d4b8772c84352c00078da50283da83&"]),
            Comment("https://www.google.com/","Peter", "Nice", "look another one", ["https://cdn.discordapp.com/attachments/1220854776321933424/1220855840580304996/34116586536_713f6e6b04_b.png?ex=6610759a&is=65fe009a&hm=bff34c7a544cfc45234c64617e277f7c04eafb1a687cb2916857e1739d0f8826&"])]
comments = []



IMAGES = [
    "https://cdn.discordapp.com/attachments/1220854776321933424/1220854824090865794/hikeman.jpg?ex=661074a8&is=65fdffa8&hm=6ea332c0f680b0016e7d2b28a5112c62670b5e9ccd2b75430df72378f43dd741&",
    "https://cdn.discordapp.com/attachments/1220854776321933424/1220855680689373224/s-man-hiking-backpacking-foggy-cloudy-finland-autumn-forest-lakeside.png?ex=66107574&is=65fe0074&hm=c4ef5789df7aa810b13fdf49e763bb0978d4b8772c84352c00078da50283da83&",
    "https://cdn.discordapp.com/attachments/1220854776321933424/1220855840580304996/34116586536_713f6e6b04_b.png?ex=6610759a&is=65fe009a&hm=bff34c7a544cfc45234c64617e277f7c04eafb1a687cb2916857e1739d0f8826&",
    "https://cdn.discordapp.com/attachments/1220854776321933424/1220855905407598682/web_AdventurebyDesign20Halti20top.png?ex=661075aa&is=65fe00aa&hm=9e7642f9de63858f4c4506f4550368b74a6ee820cd0744bac83b05020a349cdf&",
]

def slideshow_swipeable(images):
    # Generate a session state key based on images.
    key = f"slideshow_swipeable_{str(images).encode().hex()}"

    # Initialize the default slideshow index.
    if key not in st.session_state:
        st.session_state[key] = 0

    # Get the current slideshow index.
    index = st.session_state[key]

    # Create a new elements frame.
    with elements(f"frame_{key}"):

        # Use mui.Stack to vertically display the slideshow and the pagination centered.
        # https://mui.com/material-ui/react-stack/#usage
        with mui.Stack(spacing=2, alignItems="center"):

            # Create a swipeable view that updates st.session_state[key] thanks to sync().
            # It also sets the index so that changing the pagination (see below) will also
            # update the swipeable view.
            # https://mui.com/material-ui/react-tabs/#full-width
            # https://react-swipeable-views.com/demos/demos/
            with mui.SwipeableViews(index=index, resistance=True, onChangeIndex=sync(key)):
                for image in images:
                    html.img(src=image, css={"width": "100%"})

            # Create a handler for mui.Pagination.
            # https://mui.com/material-ui/react-pagination/#controlled-pagination
            def handle_change(event, value):
                # Pagination starts at 1, but our index starts at 0, explaining the '-1'.
                st.session_state[key] = value-1

            # Display the pagination.
            # As the index value can also be updated by the swipeable view, we explicitely
            # set the page value to index+1 (page value starts at 1).
            # https://mui.com/material-ui/react-pagination/#controlled-pagination
            mui.Pagination(page=index+1, count=len(images), color="primary", onChange=handle_change)

def showComments(comments):
    with st.container(border = True):
        st.text("Comments:")
        for comment in comments:
            with st.container(border = True):
                st.markdown("<a href=" + comment["comment_url"] + ">"+ comment["comment_username"]+ "</a>",unsafe_allow_html=True)
                st.text(comment["comment_title"])
                st.text(comment["comment_description"])
                if comment["comment_images"] != "":
                    images = []
                    imageEnds = comment["comment_images"].split(",")
                    imageEnds.pop()
                    for imageEnd in imageEnds:
                        images.append("https://solvesdgs.s3.us-east-2.amazonaws.com/" + imageEnd)
                    slideshow_swipeable(images)


def queryTrip(hash):
    s3 = boto3.resource('s3')    
    content_object = s3.Object('solvesdgs', 'activityfiles/' + hash + '.json')
    file_content = content_object.get()['Body'].read()    
    json_content = json.loads(file_content)
    if "activity_comments" not in json_content:
        json_content["activity_comments"] = []
    return json_content

def parse_gpx(gpxdf): 
    points = [] 
    gpx_data = gpxpy.parse(gpxdf['activity_gpx']) 
    for track in gpx_data.tracks: 
        for segment in track.segments: 
            for point in segment.points: 
                points.append({'Latitude': point.latitude, 'Longitude': point.longitude, 'Color': 'red', 'Number': 0}) 
    return points



def loadPage(hash, username, authenticated):
    siteData = queryTrip(hash)
    st.set_page_config(
        page_title=siteData["activity_name"],
        page_icon="👋",
    )
    #df, points = process_gpx_to_df(siteData["activity_gpx"]) 
    #st.map(df, latitude='Latitude', longitude='Longitude', size='Size')
    
    
    
    points = parse_gpx(siteData)
    map = plot_map(points)
    st_folium(map)
    

    title = st.text(siteData["activity_description"])
    images = []
    imageEnds = siteData["activity_images"].split(",")
    imageEnds.pop()
    for imageEnd in imageEnds:
        images.append("https://solvesdgs.s3.us-east-2.amazonaws.com/" + imageEnd)
    slideshow_swipeable(images)
    if st.session_state['authentication_status']:
        with st.form("my_form"):
            st.write("Write your own experience!")
            comment = dict()
            comment["comment_title"] = st.text_input("Title")
            comment["comment_description"] = st.text_input("desctiption")
            images= st.file_uploader("Any beautiful image you want to share of your comment?", accept_multiple_files=True)
            comment["comment_url"] = "https://www.google.com/"
        comment["comment_username"] = "Dud"
        
        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            client = boto3.client('s3', region_name='us-east-2')
            comment['comment_images'] = ""
            for activity_image in images:
                if activity_image is not None: 
                    ext = activity_image.name.find(".")
                    ext = activity_image.name[ext:]
                    imageloc = 'commentimages/' + hl.md5(activity_image.name.encode('utf-8')).hexdigest() + ext
                    comment['comment_images'] += imageloc + ","
                    client.upload_fileobj(
                        Fileobj=activity_image,
                        Bucket='solvesdgs',
                        Key=imageloc,
                        ExtraArgs={'ACL': 'public-read'}  # This makes the file publicly readable
                    )
            siteData["activity_comments"].append(comment)
            s3 = boto3.resource("s3")
            file = s3.Object("solvesdgs", "activityfiles/"+ hash+".json")
            file.put(Body=json.dumps(siteData))
            for key in st.session_state.keys():
                if key[:21] == "slideshow_swipeable_":
                    del st.session_state[key]
    showComments(siteData["activity_comments"])




if __name__ == '__main__':
    
    params =st.query_params
    if "tripId" in params:
    #if "tripId" and "username" and "authenticated" in params:
        loadPage(params["tripId"])
    else:
        st.text("No tripId given.")
        st.write(st.session_state['username'])
    
