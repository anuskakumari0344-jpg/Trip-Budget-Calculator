import streamlit as st

st.title("Plan a Trip")
st.write("Enter your trip details below.")

destination = st.text_input("Destination")
travelers = st.number_input("Number of Travelers", min_value=1, value=1)

transport = st.number_input("Transport Expenses (₹)", min_value=0)
accommodation = st.number_input("Accommodation Expenses (₹)", min_value=0)
food = st.number_input("Food Expenses (₹)", min_value=0)
activities = st.number_input("Activity Expenses (₹)", min_value=0)

total = transport + accommodation + food + activities

st.subheader("Estimated Trip Budget")
st.write(f"₹{total}")

if st.button("Save Trip"):
    st.success("Trip budget calculated successfully!")
    st.write("Destination:", destination)
    st.write("Travelers:", travelers)
    st.write("Total Budget:", f"₹{total}")