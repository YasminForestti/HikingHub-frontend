import streamlit as st



class ActivityForm:

    def __init__(self) -> None:
        self.title = "Guiders Registration Form"
        self.description = "WELCOME TO BEYONDAURORA we are excited to have you on board, please register your activity here"

    def run(self):
        st.title(self.title)
        st.write(self.description)
        with st.form("Guiders Registration Form"):
            self.activity_name = st.text_input("Activity Name")
            self.activity_description = st.text_area("Activity Description")
            self.activity_date = st.date_input("When will the activity take place?")
            self.activity_time = st.time_input("How long will the activity take?")
            self.activity_location = st.text_input("Where is the activity taking place?")
            self.activity_capacity = st.number_input("How many people can participate in the activity?")
            self.activity_image = st.file_uploader("Any beautiful image you want to share of your activity?")
            self.activity_link = st.text_input("Any helpful links for the participants?")
            self.activity_tweet = st.text_input("Summarize your activity in a tweet")
            self.activity_age_group = st.selectbox("Which ages can participate in you activity?", ["Select Age Group", "0-3", "4-6", "7-9", "10-12", "13-15", "16-18", "19-21", "22-25", "26-30", "31-35", "36-40", "41-45", "46-50", "51-55", "56-60", "61-65", "66-70", "71-75", "76-80", "81-85", "86-90", "91+"])
            self.message4users = st.text_area("Anything you want to tell your future participants?")
            if st.form_submit_button("Upload activity"):
                self.send()
                st.write("Activity uploaded successfully!! Thank you for going beyond the aurora with us!")
            
                
    def send(self):
        # TODO: Save the data in an s3 bucket
        pass
if __name__ == "__main__":
    activity = ActivityForm()
    activity.run()

