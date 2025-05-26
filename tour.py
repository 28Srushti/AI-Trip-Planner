import streamlit as st
import pandas as pd
import os
from phi.agent import Agent
from phi.model.groq import Groq  # Assuming this is how you import Groq Llama
from phi.tools.serpapi_tools import SerpApiTools
from dotenv import load_dotenv
load_dotenv()


# Initialize page config
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_guide_data():
    return pd.read_csv("local_guide.csv")

guides_df = load_guide_data()

def safe_trim(text, max_chars=6000):
    if len(text) > max_chars:
        return text[:max_chars - 500] + "\n\n(Trimmed due to length...)"
    return text


# Enhanced Custom CSS for improved UI
st.markdown("""
    <style>
    :root {
        --primary-color: #2E86C1;
        --accent-color: #FF6B6B;
        --background-light: #F8F9FA;
        --text-color: #2C3E50;
        --hover-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .main {
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .stButton > button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: var(--accent-color) !important;
        color: white !important;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--hover-shadow);
        background-color: #FF4A4A !important;
    }

    .sidebar .element-container {
        background-color: var(--background-light);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .stExpander {
        background-color: #262730;
        border-radius: 10px;
        padding: 1rem;
        border: none;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .travel-summary {
        background-color: #262730;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }

    .travel-summary h4 {
        color: var(--primary-color);
        margin-bottom: 0.5rem;
    }

    .spinner-text {
        font-size: 1.2rem;
        font-weight: bold;
        color: var(--primary-color);
    }

    </style>
""", unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/airplane-take-off.png")
    st.title("Trip Settings")
    
    # User inputs for API keys
    #groq_api_key = st.text_input("🔑 Enter your Groq API Key", type="password")
    #serpapi_key = st.text_input("🔑 Enter your SerpAPI Key", type="password")
    
    destination = st.text_input("🌍 Where would you like to go?", "")
    duration = st.number_input("📅 How many days?", min_value=1, max_value=30)

    # Show summary only if both inputs are provided
    if destination and duration:
        st.markdown(f"🗓️ **Trip Summary:** {duration} days in **{destination.title()}**")
    
    budget = st.select_slider(
        "💰 What's your budget level?",
        options=["Budget", "Moderate", "Luxury"],
        value="Moderate"
    )
    
    travel_style = st.multiselect(
        "🎯 Travel Style",
        ["Culture", "Nature", "Adventure", "Relaxation", "Food", "Shopping"],
        ["Culture", "Nature"]
    )

    st.markdown("---")
    st.subheader("🧭 Tour Guide")

    hire_guide = st.checkbox("Do you want to hire a local guide?", value=True)

    guide_days = 0
    guide_transport = ""
    if hire_guide:
        guide_days = st.number_input("📆 Guide needed for how many days?", min_value=1, max_value=int(duration), value=duration)
        guide_transport = st.selectbox("🚗 Preferred transport with guide", ["Car", "Bike", "Bus", "Bicycle"])

# Initialize session state variables
if 'travel_plan' not in st.session_state:
    st.session_state.travel_plan = None
if 'qa_expanded' not in st.session_state:
    st.session_state.qa_expanded = False

# Add loading state container
loading_container = st.empty()

try:
    # Set API keys in environment variables
    groq_api_key = os.getenv("GROQ_API_KEY")
    serpapi_key = os.getenv("SERP_API_KEY")


    # Initialize travel agent with Groq Llama model and SerpAPI
    travel_agent = Agent(
        name="Travel Planner",
        model=Groq(id="llama-3.3-70b-versatile"),  # Adjust if necessary based on actual import
        tools=[SerpApiTools()],
        instructions=[
            "You are a travel planning assistant using Groq Llama.",
            "Help users plan their trips by researching destinations, finding attractions, suggesting accommodations, and providing transportation options.",
            "If user hires a local guide, include detailed sightseeing assistance and transport mode based on user preference.",
            "Give me relevant live Links of each places and hotels you provide by searching on internet (It's important)",
            "Always verify information is current before making recommendations."
        ],
        show_tool_calls=True,
        markdown=True
    )

    # Main UI
    st.title("🌎 AI Travel Planner")
    
    st.markdown(f"""
        <div class="travel-summary">
            <h4>Welcome to your personal AI Travel Assistant! 🌟</h4>
            <p>Let me help you create your perfect travel itinerary based on your preferences.</p>
            <p><strong>Destination:</strong> {destination}</p>
            <p><strong>Duration:</strong> {duration} days</p>
            <p><strong>Budget:</strong> {budget}</p>
            <p><strong>Travel Styles:</strong> {', '.join(travel_style)}</p>
            <p><strong>Guide:</strong> {"Yes" if hire_guide else "No"}</p>
            {f"<p><strong>Guide Days:</strong> {guide_days} days</p><p><strong>Transport:</strong> {guide_transport}</p>" if hire_guide else ""}
        </div>
    """, unsafe_allow_html=True)

    # Generate button
    if st.button("✨ Generate My Perfect Travel Plan", type="primary"):
        if destination:
            try:
                with st.spinner("🔍 Researching and planning your trip..."):
                    prompt = f"""Create a comprehensive travel plan for {destination} for {duration} days.

    Travel Preferences:
    - Budget Level: {budget}
    - Travel Styles: {', '.join(travel_style)}
    - Guide: {"Yes" if hire_guide else "No"}

    {"Include a local guide for sightseeing, hired for " + str(guide_days) + " days. Preferred transport: " + guide_transport + "." if hire_guide else "User does not want a local guide."}


    Please provide a detailed itinerary that includes:

    1. 🌞 Best Time to Visit
    - Seasonal highlights
    - Weather considerations

    2. 🏨 Accommodation Recommendations
    - {budget} range hotels/stays
    - Locations and proximity to attractions

    3. 🗺️ Day-by-Day Itinerary
    - Detailed daily activities
    - Must-visit attractions
    - Local experiences aligned with travel styles

    4. 🍽️ Culinary Experiences
    - Local cuisine highlights
    - Recommended restaurants
    - Food experiences matching travel style

    5. 💡 Practical Travel Tips
    - Local transportation options
    - Cultural etiquette
    - Safety recommendations
    - Estimated daily budget breakdown

    6. 💰 Estimated Total Trip Cost
    - Breakdown of expenses
    - Money-saving tips

    7. 🧭 Guide-based sightseeing details (if hired), including transport info

    8. 💡 Travel tips (transportation, safety, budget)

    Please provide source and relevant links without fail.

    Format the response in a clear, easy-to-read markdown format with headings and bullet points.
                    """
                    trimmed_prompt = safe_trim(prompt)
                    response = travel_agent.run(trimmed_prompt)
                    # response = travel_agent.run(prompt)

                    if hasattr(response, 'content'):
                        clean_response = response.content.replace('∣', '|').replace('\n\n\n', '\n\n')
                        st.session_state.travel_plan = clean_response
                        st.markdown(clean_response)

                        # Show local guides from CSV if user chose to hire a guide
                        if hire_guide and destination:
                            normalized_city = destination.strip().lower()
                            filtered_guides = guides_df[guides_df['city'].str.lower().str.contains(normalized_city)]

                        if not filtered_guides.empty:
                            st.markdown("### 🧭 Available Local Guides")
                            for _, guide in filtered_guides.iterrows():
                                phone_link = guide['phone'].replace(" ", "").replace("+", "")
                                whatsapp_link = f"https://wa.me/{phone_link}"
                                st.markdown(f"""
                                    <div style="background-color:#f8f9fa;padding:1rem;margin-bottom:1rem;border-radius:10px;color:#000;">
                                    <p><strong>👤 Name:</strong> {guide['name']}</p>
                                    <p><strong>📞 Phone:</strong> <a href="tel:{guide['phone']}" style="color:#0066cc;">{guide['phone']}</a></p>
                                    <p><strong>💬 WhatsApp:</strong> <a href="{whatsapp_link}" target="_blank" style="color:#0066cc;">Chat on WhatsApp</a></p>
                                    <p><strong>📧 Email:</strong> <a href="mailto:{guide['email']}" style="color:#0066cc;">{guide['email']}</a></p>
                                    <p><strong>🚗 Transport:</strong> {guide['transport']}</p>
                                </div>
                                """, unsafe_allow_html=True)

                        else:
                            st.info(f"No local guide records found for **{destination.title()}**.")

                    else:
                        st.session_state.travel_plan = str(response)
                        st.markdown(str(response))
            except Exception as e:
                st.error(f"Error generating travel plan: {str(e)}")
                st.info("Please try again in a few moments.")
        else:
            st.warning("Please enter a destination")

    # Q&A Section
    st.divider()
    
    # Use st.expander with a key to maintain state
    qa_expander = st.expander("🤔 Ask a specific question about your destination or travel plan", expanded=st.session_state.qa_expanded)
    
    with qa_expander:
        # Store the expanded state
        st.session_state.qa_expanded = True
        
        question = st.text_input("Your question:", placeholder="What would you like to know about your trip?")
        
        if st.button("Get Answer", key="qa_button"):
            if question and st.session_state.travel_plan:
                with st.spinner("🔍 Finding answer..."):
                    try:
                        # Combine the original travel plan with the new question for context
                        context_question = f"""
                        I have a travel plan for {destination}. Here's the existing plan:
                        {st.session_state.travel_plan}

                        Now, please answer this specific question: {question}
                        
                        Provide a focused, concise answer that relates to the existing travel plan if possible.
                        """

                        trimmed_context = safe_trim(context_question)
                        response = travel_agent.run(trimmed_context)

                        # response = travel_agent.run(context_question)
                        if hasattr(response, 'content'):
                            st.markdown(response.content)
                        else:
                            st.markdown(str(response))
                    except Exception as e:
                        st.error(f"Error getting answer: {str(e)}")
            elif not st.session_state.travel_plan:
                st.warning("Please generate a travel plan first before asking questions.")
            else:
                st.warning("Please enter a question")

except Exception as e:
    st.error(f"Application Error: {str(e)}")