import streamlit as st
import pandas as pd

df = pd.read_csv("../pandal_loc.csv")

st.title("🏮Nearest Pandal finder")
