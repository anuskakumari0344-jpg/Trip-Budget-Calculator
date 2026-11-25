
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from datetime import date

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="TripWise",
    page_icon="✈️",
    layout="wide"
)

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "trips.json")

os.makedirs(DATA_FOLDER, exist_ok=True)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #f4f7fb;
}
.block-container {
    padding-top: 1.5rem;
}
[data-testid="stMetric"] {
    background: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5eaf0;
}
div.stButton > button {
    border-radius: 10px;
    height: 45px;
}
</style>
""", unsafe_allow_html=True)


# ---------------- STORAGE ----------------
def load_trips():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_trips(trips):
    with open(DATA_FILE, "w") as file:
        json.dump(trips, file, indent=4)


# ---------------- CALCULATIONS ----------------
def calculate_total(travel, accommodation, food, activities, other):
    return travel + accommodation + food + activities + other


def money(amount):
    return f"₹{amount:,.2f}"


# ---------------- VALIDATION ----------------
def valid_expense(value):
    return value >= 0


# ---------------- LOAD DATA ----------------
trips = load_trips()

# ---------------- SIDEBAR ----------------
st.sidebar.title("✈️ TripWise")
st.sidebar.caption("Smart Trip Budget Planner")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Plan a Trip",
        "My Trips",
        "Budget Analytics",
        "Reports"
    ]
)

st.sidebar.divider()
st.sidebar.info("Plan your trips. Track your budget. Travel smarter.")


# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("✈️ TripWise Dashboard")
    st.write("Plan your next adventure without exceeding your budget.")

    total_trips = len(trips)

    total_budget = sum(
        float(t.get("budget", 0)) for t in trips
    )

    total_cost = sum(
        float(t.get("total", 0)) for t in trips
    )

    avg_cost = total_cost / total_trips if total_trips else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Trips", total_trips)
    col2.metric("Planned Budget", money(total_budget))
    col3.metric("Estimated Expenses", money(total_cost))
    col4.metric("Average Trip Cost", money(avg_cost))

    st.divider()

    st.subheader("Recent Trips")

    if trips:
        df = pd.DataFrame(trips)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No trips yet. Start by planning your first trip!")

    st.subheader("Quick Start")

    if st.button("➕ Plan a New Trip"):
        st.switch_page("main.py")


# ---------------- PLAN A TRIP ----------------
elif page == "Plan a Trip":

    st.title("🧳 Plan Your Trip")
    st.write("Enter trip details and estimate your expenses.")

    with st.form("trip_form"):

        destination = st.text_input("Destination")
        start_location = st.text_input("Starting Location")

        col1, col2 = st.columns(2)

        with col1:
            travel_date = st.date_input(
                "Travel Date",
                value=date.today()
            )

        with col2:
            return_date = st.date_input(
                "Return Date",
                value=date.today()
        )

        travellers = st.number_input(
            "Number of Travellers",
            min_value=1,
            max_value=100,
            value=1,
            step=1
        )

        budget = st.number_input(
            "Your Budget (₹)",
            min_value=0.0,
            value=5000.0,
            step=500.0
        )

        st.subheader("Expense Details")

        col1, col2 = st.columns(2)

        with col1:
            travel = st.number_input(
                "Travel Expenses (₹)",
                min_value=0.0,
                value=0.0
            )

            accommodation = st.number_input(
                "Accommodation Expenses (₹)",
                min_value=0.0,
                value=0.0
            )

            food = st.number_input(
                "Food Expenses (₹)",
                min_value=0.0,
                value=0.0
            )

        with col2:
            activities = st.number_input(
                "Activities & Sightseeing (₹)",
                min_value=0.0,
                value=0.0
            )

            other = st.number_input(
                "Other Expenses (₹)",
                min_value=0.0,
                value=0.0
            )

        notes = st.text_area("Notes (optional)")

        submit = st.form_submit_button(
            "💾 Save Trip",
            use_container_width=True
        )

    if submit:

        if not destination.strip():
            st.error("Please enter a destination.")

        elif return_date < travel_date:
            st.error("Return date cannot be before travel date.")

        else:

            total = calculate_total(
                travel,
                accommodation,
                food,
                activities,
                other
            )

            new_trip = {
                "destination": destination.strip(),
                "start_location": start_location.strip(),
                "travel_date": str(travel_date),
                "return_date": str(return_date),
                "travellers": int(travellers),
                "budget": budget,
                "travel": travel,
                "accommodation": accommodation,
                "food": food,
                "activities": activities,
                "other": other,
                "total": total,
                "notes": notes
            }

            trips.append(new_trip)
            save_trips(trips)

            st.success("Trip saved successfully!")

            st.subheader("Trip Summary")

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Estimated Cost", money(total))
            col2.metric("Budget", money(budget))
            col3.metric("Cost Per Traveller", money(total / travellers))

            if total > budget:
                st.warning("Your trip estimate exceeds your budget!")
            else:
                st.success("Your trip is within your budget.")


# ---------------- MY TRIPS ----------------
elif page == "My Trips":

    st.title("🗺️ My Trips")

    if not trips:
        st.info("No trips have been saved yet.")

    else:

        search = st.text_input("Search destination")

        filtered = [
            t for t in trips
            if search.lower() in t["destination"].lower()
        ]

        st.write(f"Trips found: {len(filtered)}")

        for i, trip in enumerate(filtered):

            with st.expander(
                f"📍 {trip['destination']} - {money(trip['total'])}"
            ):

                st.write("Starting Location:", trip.get("start_location", ""))
                st.write("Travel Date:", trip.get("travel_date", ""))
                st.write("Return Date:", trip.get("return_date", ""))
                st.write("Travellers:", trip.get("travellers", 1))
                st.write("Budget:", money(trip.get("budget", 0)))

                st.write("Travel:", money(trip.get("travel", 0)))
                st.write("Accommodation:", money(trip.get("accommodation", 0)))
                st.write("Food:", money(trip.get("food", 0)))
                st.write("Activities:", money(trip.get("activities", 0)))
                st.write("Other:", money(trip.get("other", 0)))

                st.write("Notes:", trip.get("notes", ""))

                if trip["total"] > trip["budget"]:
                    st.warning("Budget exceeded")
                else:
                    st.success("Within budget")

                if st.button("Delete Trip", key=f"delete_{i}"):

                    trips.remove(trip)
                    save_trips(trips)

                    st.success("Trip deleted.")
                    st.rerun()


# ---------------- ANALYTICS ----------------
elif page == "Budget Analytics":

    st.title("📊 Budget Analytics")

    if not trips:
        st.info("Save some trips to view analytics.")

    else:

        df = pd.DataFrame(trips)

        total_spent = df["total"].sum()
        total_budget = df["budget"].sum()

        col1, col2 = st.columns(2)

        col1.metric("Total Estimated Expenses", money(total_spent))
        col2.metric("Combined Budget", money(total_budget))

        st.subheader("Expense Breakdown")

        categories = [
            "travel",
            "accommodation",
            "food",
            "activities",
            "other"
        ]

        expense_data = {
            category: df[category].sum()
            for category in categories
        }

        expense_df = pd.DataFrame(
            list(expense_data.items()),
            columns=["Category", "Amount"]
        )

        fig = px.pie(
            expense_df,
            names="Category",
            values="Amount",
            hole=0.45,
            title="Trip Expense Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Budget vs Estimated Cost")

        comparison = pd.DataFrame({
            "Destination": df["destination"],
            "Budget": df["budget"],
            "Estimated Cost": df["total"]
        })

        fig2 = px.bar(
            comparison,
            x="Destination",
            y=["Budget", "Estimated Cost"],
            barmode="group",
            title="Trip Budget Comparison"
        )

        st.plotly_chart(fig2, use_container_width=True)


# ---------------- REPORTS ----------------
elif page == "Reports":

    st.title("📄 Reports & Export")

    if not trips:
        st.info("No trip data available for export.")

    else:

        df = pd.DataFrame(trips)

        st.subheader("Trip Report")
        st.dataframe(df, use_container_width=True)

        csv_data = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download CSV Report",
            data=csv_data,
            file_name="trip_report.csv",
            mime="text/csv"
        )

        json_data = json.dumps(
            trips,
            indent=4
        ).encode("utf-8")

        st.download_button(
            "⬇️ Download JSON Report",
            data=json_data,
            file_name="trip_report.json",
            mime="application/json"
        )

        st.success("Your reports are ready to download.")
