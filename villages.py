import streamlit as st
import pandas as pd

DATA_URL = (
	"toy_data.csv"
)

@st.cache(persist=True)
def load_data():
	data = pd.read_csv(DATA_URL)
	return data

def write():
	st.title("Villages of Gurez Sector")
	data = load_data()
	st.map(data)