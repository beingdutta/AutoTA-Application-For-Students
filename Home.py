import streamlit as st
from pathlib import Path
import json
import urllib.parse as ul

st.set_page_config(page_title="AutoTA | Pause. Ask. Progress.",
                   page_icon="🎓",
                   layout="centered",
                   initial_sidebar_state="collapsed",
                   )

# --------------  Dummy catalogue  --------------
# Replace with your DB / API
videos = [
    {
        "id": "intro_algo",
        "title": "Introduction to Algorithms and Analysis – Lec 1: Insertion Sort",
        "summary": "An introduction to the Insertion Sort algorithm and its complexity.",
        "url": "https://www.youtube.com/watch?v=oZgbwa8lvDE", # Corrected YouTube URL
        "thumbnail": "https://i.ytimg.com/vi/oZgbwa8lvDE/hqdefault.jpg",
        "video_file": "videos/oZgbwa8lvDE.mp4",
        "transcript_file": "transcripts/oZgbwa8lvDE.csv"
    },
    {
        "id": "dl_basics",
        "title": "Deep Learning(CS7015): Lec 2.5 Perceptron Learning Algorithm",
        "summary": "An introduction to the perceptron learning algorithm with an example.",
        "url": "https://www.youtube.com/watch?v=VRcixOuG-TU", # Corrected YouTube URL
        "thumbnail": "https://i.ytimg.com/vi/VRcixOuG-TU/hqdefault.jpg",
        "video_file": "videos/VRcixOuG-TU.mp4",
        "transcript_file": "transcripts/VRcixOuG-TU.csv"
    },
    {
        "id": "python_intro",
        "title": "Unit testing | Intro to CS - Python | Khan Academy",
        "summary": "How do teams of programmers continuously write and revise code without breaking things? Unit tests define a function's expected behavior and then enforce that those requirements are met.",
        "url": "https://www.youtube.com/watch?v=3OmfTIf-SOU", # Corrected YouTube URL
        "thumbnail": "https://i.ytimg.com/vi/3OmfTIf-SOU/hqdefault.jpg",
        "video_file": "videos/3OmfTIf-SOU.mp4",
        "transcript_file": "transcripts/3OmfTIf-SOU.csv"
    },
]
# Persists last timestamp per-user per-video
progress_store = Path(".progress.json")
if progress_store.exists():
    last_pos = json.loads(progress_store.read_text())
else:
    last_pos = {}

st.markdown(
    """
    <style>
    .autota-style {
        font-family: 'Montserrat', sans-serif; /* Define Montserrat */
        text-align: center; /* Centers the text horizontally */
        font-size: 100px;    /* Adjust the font size as desired */
        font-weight: bold;  /* Optional: make it bold */
        color: white;        /* Optional: change text color */
        padding: 10px;      /* Optional: Add some padding around the text */
    }
    </style>
    <div class="autota-style">AutoTA</div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <style>
    .center-desc {
        font-family: 'Montserrat', sans-serif; /* Define Montserrat */
        text-align: center; /* Centers the text horizontally */
        font-size: 30px;    /* Adjust the font size as desired */
        font-weight: bold;  /* Optional: make it bold */
        color: #555;        /* Optional: change text color */
        padding: 10px;      /* Optional: Add some padding around the text */
    }
    </style>
    <div class="center-desc">A Virtual TA to interact with lecture videos</div>
    """,
    unsafe_allow_html=True
)
st.divider()

st.title("Video Gallery")

st.markdown("---") # Separator

for video in videos:
    with st.container(border=True):
        col1, col2 = st.columns([1, 3]) # Column for thumbnail, column for text

        with col1:
            # Use Streamlit's markdown to embed HTML for a clickable image link.
            # The 'href' should point to the page name (from the 'pages' folder, without '.py').
            # Query parameters are used to pass data (like video_id).
            st.markdown(
                f"""
                <a href="/VideoViewer?video_id={video['id']}" target="_self">
                    <img src="{video['thumbnail']}" width="160" style="border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: block; margin: auto;">
                </a>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.subheader(video['title'])
            st.write(video['summary'])
            # You can also add a direct Streamlit link button for clarity
            # This is an alternative or supplementary way to navigate

    st.markdown("---") # Separator between video entries
            