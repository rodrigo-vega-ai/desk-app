import streamlit as st
from streamlit_autorefresh import st_autorefresh
import time
import requests

BASE_URL = "https://backend-844342766125.southamerica-east1.run.app"
USER = "user1"
PASSWORD = "password123"

debug = True

@st.cache_resource(ttl=1800)
def auth_headers():
    if(debug):
        print("Realizando login...")
    
    response = requests.post(f"{BASE_URL}/login", json={"nome_usuario": USER, "senha": PASSWORD})
    if(response.status_code == 200):
        if(debug):
            print("Login successfull")
        token = response.json().get("token", "")
    else:
        if(debug):
            print("Login failure")
        token = ""
    
    if(debug):
        print( f"token = {token}")
    return { "Authorization" : token }


def restaurant():
    """Return the configured restaurant.

    Returns:
        str: ID of the restaurant
    """
    return "80db16df-44a9-4ef3-8afc-e8e653a30bf0" # assume Restaurante_A 

@st.cache_data
def tables():
    """Make API call to return all the tables created for the specified restaurante.

    Return:
        dict: dictionary of all restaurant tables {'id' : 'table name'}
    """
    response = requests.get(f"{BASE_URL}/mesas/{restaurant()}", headers=auth_headers())
    if(response.status_code == 200):
        table_list = response.json()
        t = {}
        for table in table_list:
            t[table['id_mesa']] = table['nome_mesa']
        return t
    else:
        return {}

def calls():
    """Make API call to retrieve all the answered calls for the specified restaurant.

    Returns:
        dict: key = call id, value = tuple (table name, type of call)
    """
    response = requests.get(f"{BASE_URL}/chamados/{restaurant()}", headers=auth_headers())
    if(response.status_code == 200):
        call_list = response.json()
        d = {}
        t = tables()
        for call in call_list:
            # Add an entry to the dict : key = call id, value = (name of the table, type of call)
            d[call['id_chamado']] = ( t.get(call['id_mesa']), call['tipo'] ) 
        return d
    else:
        return {}



# Streamlit configuration for full-screen layout
st.set_page_config(
    layout="wide", 
    page_title="ChamaChef Desk",
    initial_sidebar_state="collapsed"
)

# Run the autorefresh about every 2000 milliseconds (2 seconds) and stop
# after it's been refreshed 100 times.
count = st_autorefresh(interval=2000, limit=None, key="fizzbuzzcounter")

# Fetch initial data
data = calls()
if(debug):
    print("data:", data)

st.write(f"Contador: {count}")

for key in data:
    st.write( f"Mesa {data[key][0]}" )

