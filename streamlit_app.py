import streamlit as st

# Create the Streamlit form
st.title("Health Appointment Booking")

with st.form("appointment_form"):
    name = st.text_input("Name")
    birthdate = st.date_input("Birthdate")
    phone = st.text_input("Phone Number")
    ic = st.text_input("IC")
    clinic = st.selectbox("Clinic", ["Clinic A", "Clinic B", "Clinic C"])
    date = st.date_input("Appointment Date")
    time = st.time_input("Appointment Time")
    
    submitted = st.form_submit_button("Submit")

if submitted:
    # Display appointment details as receipt
    st.success("Appointment booked successfully!")
    st.write("### Appointment Receipt")
    st.write(f"*Name:* {name}")
    st.write(f"*Birthdate:* {birthdate}")
    st.write(f"*Phone Number:* {phone}")
    st.write(f"*IC:* {ic}")
    st.write(f"*Clinic:* {clinic}")
    st.write(f"*Date:* {date}")
    st.write(f"*Time:* {time}")
