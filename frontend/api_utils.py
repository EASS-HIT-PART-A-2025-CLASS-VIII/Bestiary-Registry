import streamlit as st
import requests

API_URL = "http://localhost:8000"


@st.cache_data(ttl=2, show_spinner=False)
def get_creatures():
    try:
        response = requests.get(f"{API_URL}/creatures/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


@st.cache_data(ttl=2, show_spinner=False)
def get_classes():
    try:
        response = requests.get(f"{API_URL}/classes/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []


def clear_cache():
    get_creatures.clear()
    get_classes.clear()
