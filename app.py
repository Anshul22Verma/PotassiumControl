import json
import os
import pandas as pd
import random
import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

st.set_page_config(
    page_title="LLM Qualitative",
    page_icon="📟",
)

# Initialize session state variables
if "generate_response" not in st.session_state:
    st.session_state["generate_response"] = False
if "compare_feedback" not in st.session_state:
    st.session_state["compare_feedback"] = False
if "submit_feedback" not in st.session_state:
    st.session_state["submit_feedback"] = False
if "ratings" not in st.session_state:
    st.session_state["ratings"] = {}
if "comments" not in st.session_state:
    st.session_state["comments"] = {}
if "current_row" not in st.session_state:
    st.session_state.current_row = 0

with open('utils/auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
)

try:
    df = pd.read_csv("assets/all_recommendations.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "diet_history", "dietician_recommendation", "haiku_one_shot_recommendation", 
        "gpt4_one_shot_recommendation", "generated_recommendations"])

output = authenticator.login(location='main', key='Login')

def form_submitted():
    st.session_state["form_submitted"] = True
    #Retrieve form data from session state.
    st.session_state["preferred_generation"] = st.session_state.get("preferred_generation")
    st.session_state["rated_generated_recommendations"] = st.session_state.get("rated_generated_recommendations")
    st.session_state["expert_comments"] = st.session_state.get("expert_comments")
    st.session_state["expert_recommendation"] = st.session_state.get("expert_recommendation")
    
    # putting ratings in ratings dictionary
    for k in st.session_state["ratings"]:
        if k in st.session_state:
            st.session_state["ratings"][k] = st.session_state[k]
            del st.session_state[k]

    for k in st.session_state["comments"]:
        if k in st.session_state:
            st.session_state["comments"][k] = st.session_state[k]
            del st.session_state[k]

    print(st.session_state)
    submit_feedback()

def show_recommendations():
    if st.session_state["generate_response"]:
        current_row = st.session_state.current_row
        row = df.iloc[current_row]

        generations = [
            ("dietician_recommendation", row["dietician_recommendation"]),
            ("haiku_one_shot_recommendation", row["haiku_one_shot_recommendation"]),
            ("gpt4_one_shot_recommendation", row["gpt4_one_shot_recommendation"].replace("**", "")),
            ("generated_recommendations", row["generated_recommendations"].replace("<|end▁of▁sentence|>", "").replace("<think>", "").replace("</think>", "\n")),
        ]
        random.shuffle(generations)

        # Create a form for ratings, comments, and comparison feedback
        with st.form(key="user_form"):
            for i, (label, text) in enumerate(generations):
                with st.expander(f"Recommendation {i + 1}", expanded=True):
                    st.text(text)

                    # Ratings and comments
                    for aspect in ["correctness", "completeness", "relevance"]:
                        key = f"{label}_{aspect}"
                        if key not in st.session_state.ratings:
                            st.session_state.ratings[key] = "Fair"  # Default value

                        rating = st.selectbox(
                            f"{aspect.capitalize()} ({label}):",
                            ["Excellent", "Good", "Fair", "Poor", "Very Poor"],
                            index=["Excellent", "Good", "Fair", "Poor", "Very Poor"].index(st.session_state.ratings[key]),
                            key=key
                        )
                        st.session_state.ratings[key] = rating #save rating to session state immidiately.

                    # Store comments in a temporary variable
                    comment_key = f"{label}_comment"
                    comment = st.text_area(
                        f"Comments ({label}):",
                        st.session_state.comments.get(comment_key, "No comments provided"),
                        key=comment_key
                    )
                    st.session_state.comments[comment_key] = comment #save comment to session state immidiately.

            # Comparison feedback
            st.subheader("Comparison Feedback")
            preferred_generation = st.radio(
                "Select your preferred recommendation:",
                [f"Recommendation {i + 1}" for i in range(len(generations))],
                key="preferred_generation"
            )

            rated_generated_recommendations = st.multiselect(
                "Which of the recommendations do you think are generated:",
                [f"Recommendation {i + 1}" for i in range(len(generations))],
                key="rated_generated_recommendations"
            )

            expert_comments = st.text_area("Overall Comments:", "", key="expert_comments")

            form_data = st.session_state.get("user_form", {}) #this gets the form data.
            st.form_submit_button(label="Submit Feedback", on_click=form_submitted)

def submit_feedback():
    # Handle the feedback submission logic (e.g., save to a database or file)
    preferred_generation = st.session_state["preferred_generation"]
    rated_generated_recommendations = st.session_state["rated_generated_recommendations"]
    expert_comments = st.session_state["expert_comments"]
    expert_recommendation = st.session_state["expert_recommendation"]

    # Here you can save the ratings and comments to a JSON or any other format
    feedback_data = {
        "ratings": st.session_state["ratings"],
        "comments": st.session_state["comments"],
        "preferred_generation": preferred_generation,
        "rated_generated_recommendations": rated_generated_recommendations,
        "expert_comments": expert_comments,
        "expert_recommendation": expert_recommendation
    }

    # Example: Print feedback data (you can replace this with your saving logic)
    st.write("Feedback submitted successfully!")
    # st.json(feedback_data)

    current_row = st.session_state.current_row
    with open(f"assets/row_{current_row}_feedback_{st.session_state['name']}.json", "w") as json_file:
        json.dump(feedback_data, json_file, indent=4)
    
    st.session_state["generate_response"] = False
    st.session_state["ratings"] = {}
    st.session_state["comments"] = {}
    check_and_skip_existing_feedback()

def check_and_skip_existing_feedback():
    # Check if the feedback JSON file for the current row exists
    while True:
        current_row = st.session_state.current_row
        feedback_file_path = f"assets/row_{current_row}_feedback_{st.session_state['name']}.json"
        
        if os.path.exists(feedback_file_path):
            # If feedback exists, skip to the next row
            st.session_state.current_row += 1
        else:
            # If feedback doesn't exist, break out of the loop and continue
            break


if st.session_state['authentication_status']:
    authenticator.logout(button_name='Logout', location='main')
    st.text(f"User: {st.session_state['name']}")
    st.title("LLM Generation Comparison")

    check_and_skip_existing_feedback()
    current_row = st.session_state.current_row

    if current_row < len(df):
        row = df.iloc[current_row]
        input_text = row["diet_history"]
        st.subheader("User Meal Log:")
        st.text(input_text)

        expert_recommendation = st.text_area(
                "Your Recommendations:",
                value=st.session_state.get("expert_recommendation", ""),
                help="Provide any expert recommendations for the user.",
                key="expert_recommendation_key"
            )

        if st.button("Generate Response"):
            # Save expert recommendation to session state
            if expert_recommendation:
                st.session_state["expert_recommendation"] = expert_recommendation
            else:
                st.session_state["expert_recommendation"] = ""
            st.session_state["generate_response"] = True
            show_recommendations()
    else:
        st.write("You have completed all evaluations.")
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning("Please enter your username and password")