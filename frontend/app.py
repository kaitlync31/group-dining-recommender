import streamlit as st
import requests

# This frontend code was written with the help of ChatGPT.

# ----------------------------
# API endpoints
# ----------------------------
ENCODE_URL = "https://ebdfh3jo65.execute-api.us-east-2.amazonaws.com/prod/encode-restaurants"
GROUP_VECTOR_URL = "https://ebdfh3jo65.execute-api.us-east-2.amazonaws.com/prod/build-group-vector"
RECOMMEND_URL = "https://ebdfh3jo65.execute-api.us-east-2.amazonaws.com/prod/get-recommendations"

CUISINES = ["Italian", "Korean", "Mexican", "Japanese", "American"]

st.set_page_config(page_title="Group Dining Recommendation App", page_icon="🍽️")

# ----------------------------
# Session state setup
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = 1

if "recommendations" not in st.session_state:
    st.session_state.recommendations = []

if "encoded" not in st.session_state:
    st.session_state.encoded = False

# ----------------------------
# Page 1: Landing / Get Started
# ----------------------------
def page_1():

    st.markdown("""
        <style>
        .big-title {
            text-align: center;
            font-size: 60px;
            font-weight: 700;
        }

        .subtitle {
            text-align: center;
            font-size: 22px;
            margin-bottom: 40px;
        }

        .loading-text {
            text-align: center;
            font-size: 20px;
            color: #666666;
            margin-top: 20px;
            margin-bottom: 10px;
        }

        div.stButton > button {
            font-size: 22px;
            padding: 0.75em 2.5em;
            border-radius: 12px;
            background-color: #FF4B4B;
            color: white;
            border: none;
        }

        div.stButton > button:hover {
            background-color: #ff2e2e;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.write("")

    st.markdown('<div class="big-title">🍽️ GroupBite</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Find the perfect restaurant for your group based on shared preferences.</div>',
        unsafe_allow_html=True
    )

    _, center, _ = st.columns([1, 2, 1])

    with center:
        start = st.button("Get Started", use_container_width=True)
        loading_placeholder = st.empty()

    if start:
        payload = {
            "bucket": "group-dining-app",
            "key": "restaurants.json"
        }

        loading_placeholder.markdown(
            '<div class="loading-text">Preparing restaurant data...</div>',
            unsafe_allow_html=True
        )

        try:
            response = requests.post(ENCODE_URL, json=payload)
            result = response.json()

            loading_placeholder.empty()

            if response.status_code == 200:
                st.success("Restaurant data ready!")
                st.session_state.page = 2
                st.rerun()
            else:
                st.error(f"Error: {result.get("message", "Unknown error")}")

        except Exception as e:
            loading_placeholder.empty()
            st.error(f"Request failed: {e}")


# ----------------------------
# Page 2: Preferences input
# ----------------------------
def page_2():

    st.markdown("""
        <style>
        .section-title {
            text-align: center;
            font-size: 43px;
            font-weight: 700;
            color: #FF4B4B;
            margin-bottom: 6px;
        }

        .section-subtitle {
            text-align: center;
            font-size: 18px;
            color: #666666;
            margin-bottom: 30px;
        }

        .user-label {
            font-size: 22px;
            font-weight: 700;
            color: #FF4B4B;
            margin-bottom: 12px;
        }

        .summary-card {
            background-color: #FFF5F5;
            border: 1px solid #FFE3E3;
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            margin-top: 10px;
            margin-bottom: 25px;
        }

        .summary-title {
            font-size: 24px;
            font-weight: 700;
            color: #FF4B4B;
            margin-bottom: 10px;
        }

        .summary-text {
            font-size: 17px;
            line-height: 1.8;
            color: #333333;
        }

        div.stButton > button {
            font-size: 18px;
            padding: 0.7em 1.5em;
            border-radius: 12px;
            background-color: #FF4B4B;
            color: white;
            border: none;
        }

        div.stButton > button:hover {
            background-color: #ff2e2e;
            color: white;
        }

        div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            border: 1px solid #FFE3E3;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Enter Group Preferences</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Tell us what each person wants, and we’ll find the best match.</div>',
        unsafe_allow_html=True
    )

    num_users = st.number_input(
        "Number of users",
        min_value=1,
        max_value=10,
        value=2,
        step=1
    )

    group_preferences = []

    for i in range(num_users):
        with st.container(border=True):
            st.markdown(f'<div class="user-label">User {i+1}</div>', unsafe_allow_html=True)

            cuisines = st.multiselect(
                "Preferred cuisines",
                CUISINES,
                key=f"cuisines_{i}"
            )

            budget_range = st.slider(
                "Budget Range ($)",
                min_value=0,
                max_value=100,
                value=(15, 40),
                step=5,
                key=f"budget_range_{i}"
            )
            budget_min, budget_max = budget_range

            max_distance = st.slider(
                "Max Distance (miles)",
                min_value=0.0,
                max_value=5.0,
                value=2.0,
                step=0.1,
                key=f"distance_{i}"
            )

            group_preferences.append({
                "cuisines": cuisines,
                "budgetMin": budget_min,
                "budgetMax": budget_max,
                "maxDistance": max_distance
            })

        st.markdown("<div style='height:25px;'></div>", unsafe_allow_html=True)

    if group_preferences:
        avg_budget_min = sum(p["budgetMin"] for p in group_preferences) / len(group_preferences)
        avg_budget_max = sum(p["budgetMax"] for p in group_preferences) / len(group_preferences)
        avg_distance = sum(p["maxDistance"] for p in group_preferences) / len(group_preferences)

        cuisine_counts = {}
        for p in group_preferences:
            for cuisine in p["cuisines"]:
                cuisine_counts[cuisine] = cuisine_counts.get(cuisine, 0) + 1

        top_cuisines = sorted(cuisine_counts.items(), key=lambda x: x[1], reverse=True)
        top_cuisine_text = ", ".join(
            [f"{cuisine} ({count})" for cuisine, count in top_cuisines[:3]]
        ) if top_cuisines else "None selected"

        st.markdown(f"""
            <div class="summary-card">
                <div class="summary-title">Group Preference Summary</div>
                <div class="summary-text">
                    <strong>Users:</strong> {len(group_preferences)}<br>
                    <strong>Average Budget:</strong> ${avg_budget_min:.0f}–${avg_budget_max:.0f}<br>
                    <strong>Average Max Distance:</strong> {avg_distance:.1f} miles<br>
                    <strong>Top Cuisine Picks:</strong> {top_cuisine_text}
                </div>
            </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.page = 1
            st.rerun()

    with col2:
        if st.button("Get Recommendations", use_container_width=True):
            try:
                gv_response = requests.post(
                    GROUP_VECTOR_URL,
                    json={"groupPreferences": group_preferences}
                )
                gv_result = gv_response.json()

                if gv_response.status_code != 200:
                    st.error(
                        f"Error building group vector: {gv_result.get('message', 'Unknown error')}"
                    )
                else:
                    group_vector = gv_result["data"]["groupVector"]

                    rec_response = requests.post(
                        RECOMMEND_URL,
                        json={"groupVector": group_vector}
                    )
                    rec_result = rec_response.json()

                    if rec_response.status_code != 200:
                        st.error(
                            f"Error getting recommendations: {rec_result.get('message', 'Unknown error')}"
                        )
                    else:
                        st.session_state.recommendations = rec_result["data"]
                        st.session_state.page = 3
                        st.rerun()

            except Exception as e:
                st.error(f"Request failed: {e}")


# ----------------------------
# Page 3: Recommendations
# ----------------------------
def page_3():

    st.markdown("""
        <style>
        .section-title {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            color: #FF4B4B;
            margin-bottom: 8px;
        }

        .section-subtitle {
            text-align: center;
            font-size: 18px;
            color: #666666;
            margin-bottom: 30px;
        }

        .restaurant-card {
            background-color: #FFF5F5;
            border: 1px solid #FFE3E3;
            box-shadow: 0 4px 14px rgba(0,0,0,0.10);
            padding: 20px;
            border-radius: 16px;
            margin-top: 16px;
            margin-bottom: 14px;
        }

        .restaurant-rank {
            font-size: 18px;
            font-weight: 700;
            color: #C62828;
            margin-bottom: 6px;
        }

        .restaurant-name {
            font-size: 26px;
            font-weight: 700;
            color: #222222;
            margin-bottom: 10px;
        }

        .restaurant-details {
            font-size: 17px;
            color: #444444;
            line-height: 1.8;
            margin-bottom: 8px;
        }

        .restaurant-score {
            font-size: 18px;
            font-weight: 700;
            color: #FF4B4B;
            margin-top: 12px;
            padding-top: 10px;
            border-top: 2px dotted #FFD6D6;
        }

        div.stButton > button {
            font-size: 18px;
            padding: 0.7em 1.5em;
            border-radius: 12px;
            background-color: #FF4B4B;
            color: white;
            border: none;
        }

        div.stButton > button:hover {
            background-color: #ff2e2e;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-title">Your Restaurant Matches</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="section-subtitle">Based on your group’s preferences, here are the best places to eat.</div>',
        unsafe_allow_html=True
    )

    recommendations = st.session_state.recommendations

    if not recommendations:
        st.warning("No recommendations found yet.")
    else:
        badges = ["🥇 Best Match", "🥈 Second Pick", "🥉 Third Pick"]

        for idx, restaurant in enumerate(recommendations, start=1):
            badge = badges[idx - 1] if idx <= 3 else f"#{idx}"

            cuisine = restaurant.get("cuisine", "N/A")
            distance = restaurant.get("distance", "N/A")
            price_min = restaurant.get("priceMin", 0)
            price_max = restaurant.get("priceMax", 0)

            if isinstance(distance, (int, float)):
                distance_text = f"{distance:.1f} miles"
            else:
                distance_text = str(distance)

            price_text = f"${price_min:.0f}–${price_max:.0f}"

            st.markdown(f"""
                <div class="restaurant-card">
                    <div class="restaurant-rank">{badge}</div>
                    <div class="restaurant-name">{restaurant['name']}</div>
                    <div class="restaurant-details">
                        <strong>Cuisine:</strong> {cuisine}<br>
                        <strong>Distance:</strong> {distance_text}<br>
                        <strong>Price:</strong> {price_text}
                    </div>
                    <div class="restaurant-score">
                        Match Score: {restaurant['score']:.3f}
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("← Back to Preferences", use_container_width=True):
            st.session_state.page = 2
            st.rerun()

    with col2:
        if st.button("Start Over", use_container_width=True):
            st.session_state.page = 1
            st.session_state.recommendations = []
            st.rerun()

# ----------------------------
# Router
# ----------------------------
if st.session_state.page == 1:
    page_1()
elif st.session_state.page == 2:
    page_2()
elif st.session_state.page == 3:
    page_3()