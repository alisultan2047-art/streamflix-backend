import streamlit as st
import requests
import urllib.parse

# 1. Page Configuration (Wide layout, Dark mode compatible)
st.set_page_config(page_title="StreamFlix", layout="wide")

# 2. Custom CSS for a streaming app look
st.markdown("""
    <style>
    /* Make the background dark and text white */
    .stApp {
        background-color: #0E0E0E;
        color: #FFFFFF;
    }
    /* Style the movie titles */
    .movie-title {
        font-size: 15px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        min-height: 45px;
    }
    /* Style the star ratings */
    .movie-rating {
        color: #E50914; /* Netflix Red */
        text-align: center;
        font-weight: bold;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🍿 StreamFlix")
st.write("Enter your User ID to unlock personalized recommendations.")

# 3. Clean Input Layout
col1, col2 = st.columns([1, 5])
with col1:
    user_id = st.number_input("User ID", min_value=1, max_value=600, value=1)
with col2:
    st.write("") # Spacing to align button with input
    st.write("")
    submit = st.button("Search", type="primary")

st.markdown("---")

if submit:
    # 4. Fetch data from your FastAPI backend
    response = requests.get(f"http://127.0.0.1:8000/recommend/{user_id}")
    
    if response.status_code == 200:
        data = response.json()
        st.subheader(f"Top Picks for You")
        
        # 5. Create a 5-column grid for the movie posters
        cols = st.columns(5)
        
        for index, movie in enumerate(data["top_picks"]):
            with cols[index]:
                # Generate a placeholder poster image (Later, replace this URL with TMDB API)
                safe_title = urllib.parse.quote(movie['title'][:15]) # Shorten title for the placeholder
                poster_url = f"https://placehold.co/300x450/222222/E50914/png?text={safe_title}"
                
                # Render the image and custom HTML text
                st.image(poster_url, use_container_width=True)
                st.markdown(f"<div class='movie-title'>{movie['title']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='movie-rating'>⭐ {movie['predicted_stars']}</div>", unsafe_allow_html=True)
    else:
        st.error("Backend offline. Ensure FastAPI is running on port 8000.")