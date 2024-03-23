import streamlit as st
import base64
import requests
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import boto3
import hashlib as hl
import json
import streamlit_authenticator as stauth


def main(): 
    title = "Guiders Registration Form"
    description = "Welcome to BeyondAurora we are excited to have you on board, please register your activity here"
    def send(jsonname, data_for_json):
        s3 = boto3.resource("s3")
        file = s3.Object("solvesdgs", "activityfiles/" + jsonname)
        file.put(Body=json.dumps(data_for_json))

    side_bg = "https://i.pinimg.com/originals/7f/1d/ec/7f1dec7a530d6bb94c849014f020d62e.jpg"
    side_bg_ext = "jpg"
    square_size_w = 1800
    square_size_h = 950

    # Fetch the image from the URL
    response = requests.get(side_bg)
    # Ensure the request was successful
    response.raise_for_status()

    # Encode the image content in Base64
    encoded_image = base64.b64encode(response.content).decode()

    # Use the encoded image in the CSS
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url(data:image/{side_bg_ext};base64,{encoded_image});
            background-size: {square_size_w}px {square_size_h}px;
            background-repeat: no-repeat;
            background-position: top center;
            
        }}
        .st-chat-message-user {{
            justify-content: flex-end;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title(title)
    st.write(description)
    allow_guest = False
    create_title = "Create Account"
    login_title = "Login"
    guest_title = "Guest"
    create_username_label = "Username"
    create_username_placeholder = "Enter your username"
    create_username_help = "Your username must be unique"
    create_password_label = "Password"
    create_password_placeholder = "Enter your password"
    create_password_help = "Your password must be at least 8 characters"
    create_submit_label = "Create Account"
    create_success_message = "Account created successfully"
    login_username_label = "Username"
    login_username_placeholder = "Enter your username"
    login_username_help = "Your username must be unique"
    login_password_label = "Password"
    login_password_placeholder = "Enter your password"
    login_password_help = "Your password must be at least 8 characters"
    login_submit_label = "Login"
    st.session_state["authenticated"] = False
    bucket = "solvesdgs"
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket=bucket, Key="config.yml")
    authenticator = stauth.Authenticate(response['credentials'])

    with st.expander(title, expanded=True):

        create_tab, login_tab = st.tabs(
            [
                create_title,
                login_title,
            ]
        )

        # Create new account
        with create_tab:
            with st.form(key="create"):
                username = st.text_input(
                    label=create_username_label,
                    placeholder=create_username_placeholder,
                    help=create_username_help,
                    disabled=st.session_state["authenticated"],
                )

                password = st.text_input(
                    label=create_password_label,
                    placeholder=create_password_placeholder,
                    help=create_password_help,
                    type="password",
                    disabled=st.session_state["authenticated"],
                )

                if st.form_submit_button(
                    label=create_submit_label,
                    type="primary",
                    disabled=st.session_state["authenticated"],
                ):
                    st.success(create_success_message)
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username

        # Login to existing account
        with login_tab:
            authenticator.login()
            # with st.form(key="login"):
            #     username = st.text_input(
            #         label=login_username_label,
            #         placeholder=login_username_placeholder,
            #         help=login_username_help,
            #         disabled= False,
            #     )

            #     password = st.text_input(
            #         label=login_password_label,
            #         placeholder=login_password_placeholder,
            #         help=login_password_help,
            #         type="password",
            #         disabled=st.session_state["authenticated"],
            #     )

            #     if st.form_submit_button(
            #         label=login_submit_label,
            #         disabled=st.session_state["authenticated"],
            #         type="primary",
            #     ):
            #         pass
                    

        

    

    
if __name__ == "__main__":
    main()

