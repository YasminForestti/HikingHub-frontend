import streamlit as st
import base64
import requests
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import boto3
import hashlib as hl
import json
from io import StringIO


def main(): 
    title = "Guiders Registration Form"
    description = "Welcome to BeyondAurora we are excited to have you on board, please register your activity here"
    def send(jsonname, data_for_json):
        s3 = boto3.resource("s3")
        file = s3.Object("solvesdgs", "activityfiles/" + jsonname)
        file.put(Body=json.dumps(data_for_json))

    side_bg = "https://i.pinimg.com/originals/7f/1d/ec/7f1dec7a530d6bb94c849014f020d62e.jpg"
    side_bg_ext = "jpg"
    square_size_w = 1800
    square_size_h = 950

    # Fetch the image from the URL
    response = requests.get(side_bg)
    # Ensure the request was successful
    response.raise_for_status()

    # Encode the image content in Base64
    encoded_image = base64.b64encode(response.content).decode()

    # Use the encoded image in the CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{side_bg_ext};base64,{encoded_image});
            background-size: {square_size_w}px {square_size_h}px;
            background-repeat: no-repeat;
            background-position: top center;
            
        }}
        .st-chat-message-user {{
            justify-content: flex-end;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title(title)
    st.write(description)
    data_for_json = {
        'activity_name': '',
        'activity_description': '',
        'activity_date': '',
        'activity_schedule': '',
        'activity_time': '',
        'activity_location': '',
        'activity_capacity': '',
        'activity_images': '',
        'activity_link': '',
        'activity_tweet': '',
        'activity_age_group': '',
        'message4users': '', 
        'activity_gpx': ''
    }

    with st.form("Guiders Registration Form"):
        activity_name = st.text_input("Activity Name")
        jsonname = hl.md5(activity_name.encode('utf-8')).hexdigest() + ".json"
        data_for_json['activity_name'] = activity_name
        activity_description = st.text_area("Activity Description")
        data_for_json['activity_description'] = activity_description
        activity_date = st.date_input("When will the activity take place?")
        data_for_json['activity_date'] = str(activity_date)
        schedule_options = ["6.00am", "7.00am", "8.00am", "9.00am", "10.00am", "11.00am", "12.00pm", "1.00pm", "2.00pm", "3.00pm", "4.00pm", "5.00pm", "6.00pm", "7.00pm", "8.00pm", "9.00pm", "10.00pm", "11.00pm"]
        activity_schedule = st.selectbox("What time will the activity start?", schedule_options)
        data_for_json['activity_schedule'] = activity_schedule
        TIME_OPTIONS = ["00:30", "01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:30", "06:00"]
        activity_time = st.selectbox("How long will the activity take?", TIME_OPTIONS)
        data_for_json['activity_time'] = activity_time
        activity_location = st.text_input("Where is the activity taking place?")
        
        data_for_json['activity_location'] = activity_location
        activity_gpx = st.file_uploader("Upload the GPX file of your activity")
        
        if activity_gpx is not None:
            stringio = StringIO(activity_gpx.getvalue().decode("utf-8"))
            gpx_string_data = stringio.read()
            data_for_json['activity_gpx'] = gpx_string_data

        

        activity_capacity = st.slider("How many people can participate in the activity?", min_value = 1, max_value = 100)
        data_for_json['activity_capacity'] = activity_capacity
        activity_images = st.file_uploader("Any beautiful image you want to share of your activity?", accept_multiple_files=True)
        client = boto3.client('s3', region_name='us-east-2')
        
        for activity_image in activity_images:
            if activity_image is not None: 
                ext = activity_image.name.find(".")
                ext = activity_image.name[ext:]
                imageloc = 'images/' + hl.md5(activity_image.name.encode('utf-8')).hexdigest() + ext
                data_for_json['activity_images'] += imageloc + ","
                client.upload_fileobj(
                    Fileobj=activity_image,
                    Bucket='solvesdgs',
                    Key=imageloc,
                    ExtraArgs={'ACL': 'public-read'}  # This makes the file publicly readable
                )
            
        activity_link = st.text_input("Any helpful links for the participants?")
        data_for_json['activity_link'] = activity_link
        activity_tweet = st.text_input("Summarize your activity in a tweet")
        data_for_json['activity_tweet'] = activity_tweet
        activity_age_group = st.selectbox("What's the maximum ages that can participate in you activity?", ["Select Age Group", "0-3", "4-6", "7-9", "10-12", "13-15", "16-20", "21-30", "31-40", "41-50", "51-60", "61-70", "71-80", "81+"])
        data_for_json['activity_age_group'] = activity_age_group
        message4users = st.text_area("Anything you want to tell your future participants?")
        data_for_json['message4users'] = message4users
        if st.form_submit_button("Upload activity"):
            send(jsonname, data_for_json)
            st.write("Activity uploaded successfully!! Thank you for going beyond the aurora with us!")
            if activity_location != "":
                st.subheader(f'This is where your activity is taking place on {data_for_json["activity_date"]}', divider='rainbow')
                geolocator = Nominatim(user_agent="guider")
                location = geolocator.geocode(activity_location)
                m = folium.Map(location=[location.latitude, location.longitude], zoom_start=16, tiles = 'CartoDB Voyager')
                #folium.TileLayer('Stamen Terrain').add_to(m)
                folium.Marker(
                    [location.latitude, location.longitude], popup=activity_name
                ).add_to(m)

                # call to render Folium map in Streamlit
                st_data = st_folium(m, width=725)

if __name__ == "__main__":
    main()
