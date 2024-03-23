import streamlit as st
import gpxpy
import folium
from streamlit_folium import st_folium


def main():
    # Page title/header
    st.title("Basic Streamlit Page with Map")
    
    # Map section
    st.markdown("---")  # Adding a horizontal line for visual separation
    st.header("Map Section")
    st.write("This is the map section")
    # You can add your map here using st.map() function
    df = read_files()
    all_points = read_files()
    st_folium(plot_map(all_points))
    # st.map(df, latitude='Latitude', longitude='Longitude', color='Color', size = '10')



def parse_gpx(file_path, color='red', number = 0):
    gpx_file = open(file_path, 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({'Latitude': point.latitude, 'Longitude': point.longitude, 'Color': color, 'Number' : number})
        number +=1
    return points

def read_files():
    gpx_files = ["00c6622.gpx", '0a7b419.gpx', '0ab9d37.gpx']  # Add your GPX file paths here
    colors = {'00c6622.gpx': 'red', '0a7b419.gpx': 'blue', '0ab9d37.gpx': 'green'}  # Colors for each GPX file

    # Parse each GPX file
    all_points = []
    number = 0 
    for file, color in colors.items():
        points = parse_gpx(file, color, number)
        number += 1
        all_points.extend(points)
    return all_points

def plot_map(points):
    m = folium.Map(location=[points[0]['Latitude'], points[0]['Longitude']], zoom_start=12)
    seen = {}
    for point in points:
        if not seen.get(point['Number'], False):
            folium.Marker(location=[point['Latitude'], point['Longitude']],
                      icon=folium.Icon(color=point['Color'], icon='info-sign')
                      ).add_to(m)
        #folium.PolyLine(locations=[point['Latitude'], point['Longitude']], color=point['Color']).add_to(m)
        seen[point['Number']] = True
    return m

if __name__ == "__main__":
    main()