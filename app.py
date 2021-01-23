import streamlit as st
import awesome_streamlit as ast
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

import villages
import stats
import find
import exp

ast.core.services.other.set_logging_format()

PAGES = {
	"Villages": villages,
	"Statistics": stats,
	"Find Person": find,
	"Experiment": exp
}

def main():
	st.sidebar.title("Navigation")
	selection = st.sidebar.radio("Go to", list(PAGES.keys()))

	page = PAGES[selection]

	with st.spinner(f"Loading {selection}..."):
		ast.shared.components.write_page(page)

if __name__ == "__main__":
	main()