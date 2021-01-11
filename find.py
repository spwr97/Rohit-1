import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

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

	st.header("Locate person by name in: "+village)
	name_list = list(set(data["Patron"].value_counts().index))
	name_list.sort()
	name = st.selectbox("Names", name_list)

	data = data[data["Patron"]==name]

	fig = px.scatter_mapbox(data,
	                        lat="latitude", lon="longitude",
	                        hover_name="Patron", hover_data=["Village"],
	                        color_discrete_sequence=["fuchsia"], zoom=10, height=500)
	fig.update_traces(marker_size=10)
	fig.update_layout(mapbox_style="carto-positron")
	fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
	st.write(fig)

	if st.checkbox("Show Raw Data", False):
	    st.subheader("Raw Data")
	    st.write(data)
