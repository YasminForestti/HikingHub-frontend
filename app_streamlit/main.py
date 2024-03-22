import streamlit as st
import gpxpy
import gpxpy.gpx
import pandas as pd



def main():
    # Page title/header
    st.title("Basic Streamlit Page with Map")
    
    # Map section
    st.markdown("---")  # Adding a horizontal line for visual separation
    st.header("Map Section")
    st.write("This is the map section")
    # You can add your map here using st.map() function
    df, points = process_gpx_to_df("00c6622.gpx")
    st.map(df, latitude='Latitude', longitude='Longitude')

def process_gpx_to_df(file_name):
    gpx = gpxpy.parse(open(file_name)) 
    
    #(1)make DataFrame
    track = gpx.tracks[0]
    segment = track.segments[0]
    # Load the data into a Pandas dataframe (by way of a list)
    data = []
    segment_length = segment.length_3d()
    for point_idx, point in enumerate(segment.points):
        data.append([point.longitude, point.latitude,point.elevation,
        point.time, segment.get_speed(point_idx)])
        columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
        gpx_df = pd.DataFrame(data, columns=columns)
        
    #2(make points tuple for line)
    points = []
    for track in gpx.tracks:
        for segment in track.segments: 
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
        
    return gpx_df, points

if __name__ == "__main__":
    main()