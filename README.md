🌍 AI Travel Planner
An intelligent travel planning assistant that combines LLM-based reasoning, real-time web search, and local guide integration to build complete travel itineraries based on user preferences. Powered by Groq-hosted LLaMA 3.3 70B and built in Streamlit, this app delivers practical, day-wise travel plans with live links, tips, and Q&A features — all in one interactive interface.

✨ Highlights
    Personalized Travel Itineraries – Plan trips based on destination, days, budget, and travel style.
    LLM-Powered Planning – Uses phi.agent + Groq’s LLaMA 3.3 70B for detailed itinerary generation.
    Live Web Integration – Fetches real-time hotel and sightseeing info via SerpAPI.
    Local Guide Matching – Matches user-selected destination with guide info from CSV.
    Interactive Q&A – Ask custom questions about your travel plan.
    Elegant UI – Custom-styled Streamlit interface with summary views and collapsible sections.

🔧 Tech Stack
| Component     | Tech Used                            |
| ------------- | ------------------------------------ |
| UI Framework  | Streamlit                            |
| AI Backend    | Groq LLaMA 3.3 70B (via `phi.agent`) |
| Data Handling | pandas, CSV                          |
| Live Search   | SerpAPI                              |
| State Mgmt    | Streamlit session state              |
| Styling       | HTML + custom CSS                    |
| Deployment    | Localhost / Streamlit Cloud          |

🚀 Features
    ✈️ Personalized Itinerary Generation using LLaMA 3.3 70B via phi.agent.
    🔍 Real-Time Web Search powered by SerpAPI for hotels, places, and food.
    📅 Day-by-Day Trip Plans with weather, cost, and experience recommendations.
    🧭 Optional Local Guide Integration from city-filtered CSV data.
    🤖 Interactive Q&A: Ask follow-up questions about your travel plan.
    🧠 Markdown-formatted, structured, and responsive output.
    🎨 Custom UI enhancements with HTML + CSS in Streamlit.

📦 Installation
    git clone https://github.com/yourusername/ai-travel-planner.git
    cd ai-travel-planner
    pip install -r requirements.txt

  Create a .env file in the root folder with your API keys:
    GROQ_API_KEY=your_groq_api_key
    SERP_API_KEY=your_serpapi_key
    
  Run the app
  streamlit run app.py
Make sure local_guide.csv is present in the same directory.

📂 File Structure
    ├── tour.py                # Streamlit application
    ├── local_guide.csv       # CSV with guide info by city
    ├── .env                  # API credentials
    ├── requirements.txt      # Project dependencies
    └── README.md             # Project overview

🙏 Credits
    Groq – For lightning-fast LLaMA model hosting
    Streamlit – For clean UI and interactive app framework
    SerpAPI – For real-time Google Search integration
    OpenAI Phi – For agent-based prompt handling
