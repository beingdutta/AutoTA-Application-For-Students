# autota/pages/VideoViewer.py
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.screenshot as utils  # Import the new screenshot utility functions
import chatbot.llm_answer as llm_answer

# Set page configuration for the detail page
st.set_page_config(page_title="Video Details", page_icon="🎥", layout="wide")

# --- CSS to hide the sidebar ---
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sample video data
videos = [
    {
        "id": "intro_algo",
        "title": "Introduction to Algorithms and Analysis – Lec 1: Insertion Sort",
        "summary": "An introduction to the Insertion Sort algorithm and its complexity.",
        "url": "https://www.youtube.com/watch?v=oZgbwa8lvDE",
        "thumbnail": "https://i.ytimg.com/vi/oZgbwa8lvDE/hqdefault.jpg",
        "video_file": "videos/oZgbwa8lvDE.mp4",
        "transcript_file": "transcripts/oZgbwa8lvDE.csv"
    },
    {
        "id": "dl_basics",
        "title": "Deep Learning(CS7015): Lec 2.5 Perceptron Learning Algorithm",
        "summary": "An introduction to the perceptron learning algorithm with an example.",
        "url": "https://www.youtube.com/watch?v=VRcixOuG-TU",
        "thumbnail": "https://i.ytimg.com/vi/VRcixOuG-TU/hqdefault.jpg",
        "video_file": "videos/VRcixOuG-TU.mp4",
        "transcript_file": "transcripts/VRcixOuG-TU.csv"
    },
    {
        "id": "python_intro",
        "title": "Unit testing | Intro to CS - Python | Khan Academy",
        "summary": "How do teams of programmers continuously write and revise code without breaking things? Unit tests define a function's expected behavior and then enforce that those requirements are met.",
        "url": "https://www.youtube.com/watch?v=3OmfTIf-SOU",
        "thumbnail": "https://i.ytimg.com/vi/3OmfTIf-SOU/hqdefault.jpg",
        "video_file": "videos/3OmfTIf-SOU.mp4",
        "transcript_file": "transcripts/3OmfTIf-SOU.csv"
    },
]

# --- Retrieve Video Details ---
query_params = st.query_params
video_id = query_params.get("video_id")

selected_video = None
if video_id:
    selected_video = next((v for v in videos if v["id"] == video_id), None)

# --- Layout: Video on Left, Chat on Right ---
if selected_video:
    st.title(selected_video['title'])
    st.markdown(f"**Summary:** {selected_video['summary']}")
    st.write("---")

    st.markdown("If you're new around here, please check the instructions at the bottom of the page on how to ask questions with timestamps!")
    st.write("---")

    col_video, col_chat = st.columns([3, 1])

    with col_video:
        st.video(selected_video['url'])
        st.caption(f"Source: {selected_video['url']}")

    with col_chat:
        if "messages" not in st.session_state:
            st.session_state.messages = []

        chat_history_container = st.container(height=500, border=True)

        st.components.v1.html(
            """
            <script>
                const allVerticalBlocks = document.querySelectorAll('[data-testid="stVerticalBlock"]');
                let chatContainerElement = null;
                for (let i = allVerticalBlocks.length - 1; i >= 0; i--) {
                    if (allVerticalBlocks[i].querySelector('[data-testid="stChatMessage"]')) {
                        chatContainerElement = allVerticalBlocks[i];
                        break;
                    }
                }
                if (chatContainerElement) {
                    chatContainerElement.id = 'chat-container';
                    console.log("Assigned ID 'chat-container' to:", chatContainerElement);
                } else {
                    console.warn("Could not find the chat history container to assign 'chat-container' ID.");
                }
            </script>
            """,
            height=0, width=0,
        )

        with chat_history_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

        prompt = st.chat_input("Ask a question with a timestamp", key="chat_input_field")
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_history_container:
                with st.chat_message("user"):
                    st.markdown(prompt)

            with chat_history_container:
                with st.chat_message("assistant"):
                    thinking_placeholder = st.empty()
                    thinking_placeholder.markdown("Thinking...")

            # Generate the response
            response = llm_answer.answer_question(
                prompt,
                selected_video['video_file'],
                selected_video['transcript_file']
            )

            # Replace "Thinking..." with the actual response
            thinking_placeholder.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

else:
    st.error("No video selected or video not found. Please go back to the main gallery.")

st.markdown("---")

st.markdown(
    """
    #### 🕒 How to Ask Timestamp-Based Questions for AutoTA
    To get a valid answer, for all questions, include a **timestamp** from the video in your question. Start with typing the timestamp in the format `mm:ss` or `hh:mm:ss`, add a space, followed by your question. This helps AutoTA understand exactly which part of the video you're referring to.

    **✅ Good Examples:**
    - *02:15 what does the professor mean by stability of insertion sort?*
    - *10:45 Can you explain the concept where he mentions activation function?*

    **❌ Avoid:**
    - *What does he mean by that?*
    - *01:00Explain the thing mentioned earlier.*

    **Tip:** Use the `hh:mm:ss` or `mm:ss` format for timestamps.
    """
)

st.markdown("---")
st.page_link("Home.py", label="🔙 Back to Video List", icon="🏠")
