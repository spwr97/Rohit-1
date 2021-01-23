import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

import folium
from folium.plugins import LocateControl, MarkerCluster
from streamlit_folium import folium_static

DATA_URL = (
	"toy_data.csv"
)

@st.cache(persist=True)
def load_data():
	data = pd.read_csv(DATA_URL)
	return data

def write():
	st.title("Find a Person")
	data = load_data()
	village_names = list(data.Village.value_counts().index)
	village_names.sort()
	village_names.insert(0, "All villages")
	village = st.selectbox("Select village", village_names)

	if village != village_names[0]:
		data = data[data["Village"] == village]

	if village != village_names[0]:
		data = data[data["Village"] == village]

	st.header("Locate person by name in: "+village)
	name_list = list(set(data["Patron"].value_counts().index))
	name_list.sort()
	name = st.selectbox("Names", name_list)

	data = data[data["Patron"]==name]

	m = folium.Map(location=[data["latitude"].mean(), data["longitude"].mean()], zoom_start=10)

	for i in range(0,len(data)):
		name = data.iloc[i]["Patron"]
		address = data.iloc[i]["Address"]
		village = data.iloc[i]["Village"]
		directions = "https://www.google.com/maps/dir//"+str(data.iloc[i]["latitude"])+","+str(data.iloc[i]["longitude"])
		photo = data.iloc[i]["Photo"]
		st.write(photo)
		st.image(photo)

		find_html = folium.Html(f"""<p style="text-align: center;">{name}</p>
									<p style="text-align: center;">{address}</p>
									<p style="text-align: center;">{village}</p>
									<p style="text-align: center;"><img src={photo} width="180" height="210" frameborder="0"></img>
									<p style="text-align: center;"><a href={directions} target="_blank" title="Directions to {name}"><b>Directions to {name}</b></a></p>
								""", script=True)
		popup = folium.Popup(find_html, max_width=220)
		folium.Marker([data.iloc[i]["latitude"], data.iloc[i]["longitude"]], popup=popup).add_to(m)
	folium_static(m)

	if st.checkbox("Show Raw Data", False):
		st.write(data)