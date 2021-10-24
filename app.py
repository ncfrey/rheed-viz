import sys
from pathlib import Path
from molar import ClientConfig, Client
import json
from pandas.core import frame
import numpy as np
from PIL import Image

# needs to correspond to molarcli install local parameters
local_address = "http://557d-198-232-127-62.ngrok.io"
default_admin_name = "default"
default_admin_pw = "rheed"
default_domain = "rheed.com"
# other params
default_user_name = "user1"

# name the database here
database_name = "main"
revision_to_use = database_name + "@head"

# create default admin config
admin_cfg = ClientConfig(server_url=local_address,
                         email=default_admin_name + "@" + default_domain,
                         password=default_admin_pw,
                         database_name=database_name)

# create default user config
user_cfg = ClientConfig(server_url=local_address,
                        email=default_user_name + "@" + default_domain,
                        password=default_admin_pw,
                        database_name="compchem")


admin_client = Client(admin_cfg)

admin_client.test_token()

user_client = Client(user_cfg)

file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

try:
    sys.path.remove(str(parent))
except ValueError:  # Already removed
    pass

import streamlit as st

VERSION = ".".join(st.__version__.split(".")[:2])

# All data are represented as type conformer
# Cache results of the expensive query in st.session_state
if "conformer_data" not in st.session_state:
    st.session_state["conformer_data"] = user_client.query_database(
        types='conformer'
    )
all_confomers = st.session_state["conformer_data"]


# @st.cache(suppress_st_warning=True)
def get_image_from_raw(raw, shp):
    """
    raw: 1 dimensional numpy array
    shp: three element iterable containing original image shape
    Return a the image given by the one-dimensional numpy array
    """
    raw_np = np.asarray(raw)
    # raw_layer_masks = [np.arange(0, raw_np.shape[0], 1) % shp[-1] == offset for offset in range(shp[-1])]
    # raw_layers = [raw_np[mask].reshape((shp[0], shp[1])) for mask in raw_layer_masks] 
    # st.write([rl.shape for rl in raw_layers])
    # ret = np.asarray(raw_layers)
    # ret = np.swapaxes(ret, 0, 2)

    # st.write(ret.shape)
    ret = raw_np.reshape(shp)
    return ret # ret_im

def draw_analysis_page():
    st.title("Analysis")

    is_image = [conf["data_type"] == "raw" for conf in all_confomers["metadata"]]
    raw_images = all_confomers[is_image]

    selected_frame = st.select_slider("Frame", options=raw_images.index)
    selected_image = get_image_from_raw(raw_images["x"][selected_frame], raw_images["metadata"][selected_frame]["shape"])
    st.image(selected_image, clamp=True)

previous_version = "0.83.0"
demo_pages = {
    "Session State": lambda: None,
    "Analysis": draw_analysis_page
}

st.set_page_config(page_title=f"New features in Streamlit {VERSION}")

contributors = []

intro = f"""
This release launches session state as well as bug fixes and improvements.
"""

release_notes = f"""
---
**Highlights**
- 🧠 Introducing `st.session_state` and widget callbacks to allow you to add statefulness to your apps. Check out the [blog post](http://blog.streamlit.io/session-state-for-streamlit/)
**Notable Changes**
- 🪄 `st.text_input` now has an `autocomplete` parameter to allow password managers to be used
**Other Changes**
- Using st.set_page_config to assign the page title no longer appends “Streamlit” to that title ([#3467](https://github.com/streamlit/streamlit/pull/3467))
- NumberInput: disable plus/minus buttons when the widget is already at its max (or min) value ([#3493](https://github.com/streamlit/streamlit/pull/3493))
"""
# End release updates


def draw_main_page():
    st.write(
        f"""
        # Welcome to Streamlit {VERSION}! 👋
        """
    )

    st.write(intro)

    st.write(release_notes)
    st.write(st.session_state)


    st.write(admin_client.test_token())
    st.write(user_client.test_token())
    st.write(user_client.get_database_information())





# Draw sidebar
pages = list(demo_pages.keys())

if len(pages):
    pages.insert(0, "Release Notes")
    st.sidebar.title(f"Streamlit v{VERSION} Demos")
    query_params = st.experimental_get_query_params()
    if "page" in query_params and query_params["page"][0] == "headliner":
        idx = 1
    else:
        idx = 0
    selected_demo = st.sidebar.radio("", pages, idx)
else:
    selected_demo = "Release Notes"

# Draw main page
if selected_demo in demo_pages:
    demo_pages[selected_demo]()
else:
    draw_main_page()