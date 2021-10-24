import sys
from pathlib import Path
from molar import ClientConfig, Client
import json
from pandas.core import frame
import numpy as np
from PIL import Image
import skimage
import plotly.express as px

# needs to correspond to molarcli install local parameters
local_address = "http://localhost:8000"
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


def get_image_from_raw(raw, shp):
    """
    raw: 1 dimensional numpy array
    shp: iterable containing original image shape
    Return a the image given by the one-dimensional numpy array
    """
    raw_np = np.asarray(raw)
    ret = raw_np.reshape(shp)
    ret = ret.astype(np.ubyte)
    return ret

def process_image(file, formdata={}):
    import time
    time.sleep(2)

def draw_manage_data_page():
    st.title("Manage Data")
    st.header("Upload Data")
    # st.text("Image names must be ordered")
    uploaded_files = st.file_uploader("Choose JPG files with ordered names", type="jpg", accept_multiple_files=True)
    process_progress_bar = st.progress(0)
    with st.spinner("Processing files..."):
        for idx, file in enumerate(uploaded_files):
            process_image(file)
            process_progress_bar.progress((idx + 1) / len(uploaded_files))
    uploaded_video = st.file_uploader("Choose mp4 files", type="mp4", accept_multiple_files=True)
    video_bar = st.progress(0)
    with st.spinner("Processing files..."):
        for idx, file in enumerate(uploaded_video):
            st.video(file.getvalue())
            video_bar.progress((idx + 1) / len(uploaded_video))



# @st.cache(suppress_st_warning=False)
def draw_analysis_page():
    st.title("Analysis")
    col1, col2 = st.columns(2)

    is_image = [conf["data_type"] == "raw" for conf in all_confomers["metadata"]]
    raw_images = all_confomers[is_image]
    
    with col1.container():
        selected_frame = st.select_slider("Frame", options=raw_images.index)
        selected_image = get_image_from_raw(raw_images["x"][selected_frame], raw_images["metadata"][selected_frame]["shape"])
        st.image(selected_image, clamp=True)



def draw_plot_page():
    st.title("Plots")

    is_pca = [conf["data_type"] == "pca_time" for conf in all_confomers["metadata"]]
    pca_data = all_confomers[is_pca]

    pc_to_col = {
        1: 'x',
        2: 'y',
        3: 'z'
    }

    st.header("Principal components over time")
    pc = st.select_slider("Principal component", options=pc_to_col.keys())
    fig = px.scatter(
        x=range(len(pca_data[pc_to_col[pc]][7])),
        y=pca_data[pc_to_col[pc]][7],
        labels={
            'y': f'PC{pc}',
            'x': 'Frame number'
        }
    )
    st.plotly_chart(fig)
    st.write(f'Spike at frame {np.argmax(np.abs(np.gradient(pca_data[pc_to_col[pc]][7])))}')
    
def draw_landing_page():
    content = f"""
    # RHEED Analysis Platform
    *Background and problem.* Reflection high-energy electron diffraction (RHEED) is a popular technique for monitoring the growth of high-quality thin films during molecular beam epitaxy (MBE), a fundamental technique in nanotechnology development. Researchers use tedious, manual tools to analyze RHEED data. Current workflows are slow, non-transferable, and not reproducible.

    *Aim 1.* Develop a prototype interface where users can upload RHEED images and organize them in a Molar database.

    *Aim 2.* Apply pre-processing and dimensionality reduction so users can quickly and easily analyze their data.
    """
    st.write(content)

previous_version = "0.83.0"
demo_pages = {
    "About": draw_landing_page,
    # "Session State": lambda: st.write(st.session_state),
    "Manage Data": draw_manage_data_page,
    "Analysis": draw_analysis_page,
    "Plots": draw_plot_page
}

st.set_page_config(page_title="rheed-viz") # f"New features in Streamlit {VERSION}")

contributors = ["Chris Price", "Nathan Frey", "Nathaniel Budijono", "William Chan"]

intro = f"""
A data analysis and visualization platform for reflection high-energy electron diffraction (RHEED) data, powered by the MOLAR database.
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
        # Welcome to rheed-viz! 👋
        """
    )

    st.write(intro)

    # st.write(release_notes)
    # st.write(st.session_state)


    # st.write(admin_client.test_token())
    # st.write(user_client.test_token())
    # st.write(user_client.get_database_information())

# Draw sidebar
pages = list(demo_pages.keys())

if len(pages):
    st.sidebar.title("Menu")
    query_params = st.experimental_get_query_params()
    if "page" in query_params and query_params["page"][0] == "headliner":
        idx = 1
    else:
        idx = 0
    selected_demo = st.sidebar.radio("", pages, idx)
# else:
#     selected_demo = "Release Notes"

# Draw main page
if selected_demo in demo_pages:
    demo_pages[selected_demo]()
# else:
#     draw_main_page()