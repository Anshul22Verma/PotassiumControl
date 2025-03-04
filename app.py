import streamlit as st
import pandas as pd
import json
import re

st.set_page_config(
    page_title="LLM Qualitative",  # The name of the app (shown in the browser tab)
    page_icon="📟",  # The path to the icon image (or a URL to an image)
)

# Load the prompt data
try:
    df = pd.read_csv("assets/all_recommendations.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "diet_history", "dietician_recommendation", "haiku_one_shot_recommendation", 
        "gpt4_one_shot_recommendation", "generated_recommendations"])

# Title for the Streamlit app
st.title("LLM Generation Comparison")

def submit_feedback():
    # Get the current row
    current_row = st.session_state.current_row
    row = df.iloc[current_row]

    # Retrieve the generations from the current row
    generation1 = row["dietician_recommendation"]
    generation1 = re.sub(r'(\d+\.)', r'\n\1', generation1)
    generation2 = row["haiku_one_shot_recommendation"]
    generation3 = row["gpt4_one_shot_recommendation"]
    generation4 = row["generated_recommendations"].replace("<｜end▁of▁sentence｜>", "").replace("<think>", "").replace("</think>", "\n")
    generation4 = re.sub(r'(\d+\.)', r'\n\1', generation4)

    # Collect ratings and comments
    ratings = {}
    comments = {}

    for i in range(4):
        for aspect in ["correctness", "completeness", "relevance"]:
            key = f"llm{i+1}_{aspect}"
            ratings[key] = st.session_state.get(key, "Excellent")  # Default value "Excellent"

        comments[f"llm{i+1}_comment"] = st.session_state.get(f"llm{i+1}_comment", "No comments provided")

    # Collect the preferred generation
    preferred_generation = st.session_state.get("preferred_generation", "LLM 1")
    print(ratings)
    print(comments)

    # Create the new entry
    feedback_json = {
        "input_text": row["diet_history"],
        "llm1_generation": generation1,
        "llm2_generation": generation2,
        "llm3_generation": generation3,
        "llm4_generation": generation4,
        "preferred_generation": preferred_generation,
        **ratings,
        **comments
    }

    # Append the new entry to df_response
    
    with open(f"assets/row_{current_row}_feedback.json", "w") as json_file:
        json.dump(feedback_json, json_file, indent=4)

    # Update session state to move to the next row
    st.session_state.current_row += 1  # Move to the next row
    st.success("Feedback submitted successfully!")
    


# Add CSS to style the columns (make them fixed width and height, with scrollable content)
st.markdown("""
    <style>
        .scrollable-column {
            height: 300px; /* Fixed height */
            overflow-y: scroll; /* Enable vertical scrolling */
            width: 175px; /* Fixed width */
            padding: 10px;
            border: 1.5px solid #ddd; /* Optional border */
            border-radius: 8px; /* Optional rounded corners */
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for keeping track of which row is being displayed
if "current_row" not in st.session_state:
    st.session_state.current_row = 0

# Get the current row from the DataFrame
current_row = st.session_state.current_row

if current_row < len(df):
    row = df.iloc[current_row]
    input_text = row["diet_history"]  # Assuming the prompt is in "diet_history"
    st.subheader(f"Prompt: {input_text}")

    # Show the button after the prompt
    show_button = st.button(f"Generate Response")

    if show_button:
        # Retrieve the generations
        generation1 = row["dietician_recommendation"]
        generation1 = re.sub(r'(\d+\.)', r'\n\1', generation1)
        generation2 = row["haiku_one_shot_recommendation"]
        generation3 = row["gpt4_one_shot_recommendation"]
        generation4 = row["generated_recommendations"].replace("<｜end▁of▁sentence｜>", "").replace("<think>", "").replace("</think>", "\n")
        generation4 = re.sub(r'(\d+\.)', r'\n\1', generation4)
        

        st.subheader("LLM Generations:")
        cols = st.columns(4)

        generations = [generation1, generation2, generation3, generation4]

        # Collect user ratings and comments
        ratings = {}
        comments = {}

        for i, col in enumerate(cols):
            with col:
                st.write(f"**LLM {i+1}:**")
                
                # Use a scrollable column with fixed height and width
                st.markdown(f'<div class="scrollable-column">{generations[i]}</div>', unsafe_allow_html=True)

                # Collect user ratings for correctness, completeness, and relevance
                for aspect in ["correctness", "completeness", "relevance"]:
                    key = f"llm{i+1}_{aspect}"
                    ratings[key] = st.selectbox(
                        f"{aspect.capitalize()} (LLM {i+1}):",
                        ["Excellent", "Good", "Fair", "Poor", "Very Poor"],
                        index=["Excellent", "Good", "Fair", "Poor", "Very Poor"].index("Fair")
                    )

                # Collect comments for each LLM generation
                comments[f"llm{i+1}_comment"] = st.text_area(
                    f"Comments (LLM {i+1}):",
                    "No comments provided"
                )

        # Collect feedback for preferred generation
        preferred_generation = st.radio(
            "Select your preferred generation:",
            [f"LLM {i+1}" for i in range(4)],
            index=0  # default index for LLM 1
        )

        st.button("Submit Feedback", on_click=submit_feedback)

else:
    st.write("You have completed all evaluations.")


