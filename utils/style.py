# import base64
# import os
# import streamlit as st

# def set_bg_from_local(image_file):
#     ext = image_file.split('.')[-1]
#     abs_path = os.path.abspath(image_file)

#     if not os.path.exists(abs_path):
#         st.warning(f"⚠️ Background image not found at: {abs_path}")
#         return

#     with open(abs_path, "rb") as f:
#         data = f.read()
#     encoded = base64.b64encode(data).decode()

#     css = f"""
#     <style>
#     [data-testid="stAppViewContainer"]::before {{
#         content: "";
#         position: fixed;
#         top: 0;
#         left: 0;
#         width: 100%;
#         height: 100%;
#         background-image: url("data:image/{ext};base64,{encoded}");
#         background-size: cover;
#         background-position: center;
#         z-index: -1;
#         opacity: 1.0;
#     }}

#     /* Hide sidebar completely */
#     [data-testid="stSidebar"], [data-testid="stSidebarNav"], [data-testid="collapsedControl"] {{
#         display: none !important;
#     }}

#     /* Adjust main container to full width */
#     .main {{
#         margin-left: 0 !important;
#     }}
#     </style>
#     """
#     st.markdown(css, unsafe_allow_html=True)

import base64
import os
import streamlit as st

def set_bg_from_local(image_file):
    ext = image_file.split('.')[-1]
    abs_path = os.path.abspath(image_file)

    if not os.path.exists(abs_path):
        st.warning(f"⚠️ Background image not found at: {abs_path}")
        return

    with open(abs_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    css = f"""
    <style>
    /* Set background on main container */
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/{ext};base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    
/* Overlay to darken background slightly */
[data-testid="stAppViewContainer"]::after {{
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);  /* semi-transparent black */
    z-index: -1;
}}

    /* Hide sidebar and navigation */
    [data-testid="stSidebar"], 
    [data-testid="stSidebarNav"], 
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    /* Ensure main content uses full width */
    .main {{
        margin-left: 0 !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
