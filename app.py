import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = (
	"toy_data.csv"
)

st.title("Villagers of Gurez Sector")
st.markdown("Dashboard to visualize information about the villagers")

@st.cache(persist=True)
def load_data():
	data = pd.read_csv(DATA_URL)
	return data

data = load_data()

# Show data of entire region
st.map(data)

# Show data for selected villages and family size
village_names = list(data.Village.value_counts().index)
village_names.sort()
village_names.insert(0, "All villages")

village = st.selectbox("Select village", village_names)

if village != village_names[0]:
	data = data[data["Village"] == village]

if st.checkbox("Select Family size", False):
	fs = st.slider("Select family size", int(data["Family size"].min()), int(data["Family size"].max()))
	data = data[data["Family size"]==fs]

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data = data[["latitude", "longitude"]],
            get_position=["longitude", "latitude"],
            radius=100,
            extruded=True,
            pickable=True,
            elevation_scale=4,
            elevation_range=[0,1000],
        ),
    ],
))

# Show name and location of the person
st.header("Locate person by name in: "+village)
name_list = list(set(data["Patron"].value_counts().index))
name_list.sort()
name = st.selectbox("Names", name_list)

data = data[data["Patron"]==name]

fig = px.scatter_mapbox(data,
                        lat="latitude", lon="longitude",
                        hover_name="Patron", hover_data=["Village"],
                        color_discrete_sequence=["fuchsia"], zoom=10, height=500)
fig.update_traces(marker_size=12)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.write(fig)

if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)