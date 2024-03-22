import streamlit as st



def main(): 
    title = "Guiders Registration Form"
    description = "WELCOME TO BEYONDAURORA we are excited to have you on board, please register your activity here"
    def send():
        pass

    st.title(title)
    st.write(description)
    with st.form("Guiders Registration Form"):
        activity_name = st.text_input("Activity Name")
        activity_description = st.text_area("Activity Description")
        activity_date = st.date_input("When will the activity take place?")
        activity_time = st.time_input("How long will the activity take?")
        activity_location = st.text_input("Where is the activity taking place?")
        activity_capacity = st.number_input("How many people can participate in the activity?")
        activity_image = st.file_uploader("Any beautiful image you want to share of your activity?")
        activity_link = st.text_input("Any helpful links for the participants?")
        activity_tweet = st.text_input("Summarize your activity in a tweet")
        activity_age_group = st.selectbox("Which ages can participate in you activity?", ["Select Age Group", "0-3", "4-6", "7-9", "10-12", "13-15", "16-18", "19-21", "22-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-60", "61-65", "66-70", "71-75", "76-80", "81-85", "86-90", "91+"])
        message4users = st.text_area("Anything you want to tell your future participants?")
        if st.form_submit_button("Upload activity"):
            send()
            st.write("Activity uploaded successfully!! Thank you for going beyond the aurora with us!")

if __name__ == "__main__":
    main()