import requests
import os
import streamlit as st

# Centralize API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

def get_creatures():
    try:
        response = requests.get(f"{API_URL}/creatures/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def get_classes():
    try:
        response = requests.get(f"{API_URL}/classes/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception:
        return []

def create_creature(payload):
    response = requests.post(f"{API_URL}/creatures/", json=payload)
    response.raise_for_status()
    return response.json()

def update_creature(creature_id, payload):
    response = requests.put(f"{API_URL}/creatures/{creature_id}", json=payload)
    response.raise_for_status()
    return response.json()

def delete_creature(creature_id):
    response = requests.delete(f"{API_URL}/creatures/{creature_id}")
    response.raise_for_status()
    return True

def create_class(payload):
    response = requests.post(f"{API_URL}/classes/", json=payload)
    response.raise_for_status()
    return response.json()

def update_class(class_id, payload):
    response = requests.put(f"{API_URL}/classes/{class_id}", json=payload)
    response.raise_for_status()
    return response.json()

def delete_class(class_id):
    response = requests.delete(f"{API_URL}/classes/{class_id}")
    response.raise_for_status()
    return True
