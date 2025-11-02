import pandas as pd
import cv2
import os
import base64
import requests
import json

import re
from typing import Tuple, Optional

# OpenAI API Key
api_key = "your-api-key"  

# Replace with your actual OpenAI API key
headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}


timestamp_pattern = re.compile(
    r"""^                       # start of string
        \s*                     # optional leading whitespace
        (?P<ts>                 # --- TIMESTAMP ---
            (?:\d{1,2}:)?       # optional hours (hh:)
            \d{1,2}:\d{2}       # minutes and seconds  (mm:ss)
        )
        \s+                     # at least one space after the timestamp
        (?P<q>.+?)              # --- QUESTION ---
        \s*$                    # optional trailing whitespace to end of string
    """,
    re.VERBOSE,
)

# Function to encode a cv2 image
def encode_image(cv2_image):
    _, buffer = cv2.imencode('.jpg', cv2_image)
    return base64.b64encode(buffer).decode('utf-8')


def split_timestamp_question(line: str) -> Tuple[Optional[str], str]:
    """
    Split a string of the form '<timestamp> <question>'.

    Parameters
    ----------
    line : str
        Input string such as '01:23:45 How does quicksort work?'
        or '12:34 What is a heap?'

    Returns
    -------
    (timestamp, question) : Tuple[Optional[str], str]
        - timestamp : str or None if the pattern is not matched.
        - question  : str (always returned, stripped of extra spaces).
    """
    match = timestamp_pattern.match(line)
    if match:
        return match.group("ts"), match.group("q").strip()
    # fall-back: no timestamp found
    return None, line.strip()


def process_video(video_path, timestamp):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None

    # Get the frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    # Calculate the total duration of the video
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    #print(f"Total Duration: {duration} seconds")
    
    # Calculate the frame number corresponding to the given timestamp
    frame_number = int(timestamp * fps)
    
    # Set the frame position
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the frame at the specified timestamp
    ret, frame = cap.read()
    
    # Check if the frame was successfully read
    if not ret:
        print("Error: Could not read the frame at the given timestamp.")
        return None 
    
    # Release the video capture object
    cap.release()
    return (duration, frame)


def build_transcript(transcript, timestamp, vid_length):
    start_time = transcript['start'].tolist()
    texts = transcript['text'].tolist()
    text = ''
    start = max(0, timestamp - 120)
    end = min(vid_length-1, timestamp + 120)
    for i in range(len(start_time)):
        if start_time[i]>=start and start_time[i]<=end:
            text += (texts[i] + " ")
    return text

def get_timestamps_in_seconds(time):
    t_list = str(time).split(":")
    t = 0
    if len(t_list) == 2:
        t = (int(t_list[0])*60) + (int(t_list[1]))
    elif len(t_list) == 3:
        t = (int(t_list[0])*60*60)  + (int(t_list[1])*60) + (int(t_list[2]))
    return t


def find_video_file(id):

    for filename in os.listdir(videos_directory):
        file_id = filename.split(".")[0]
        if file_id == id:
            return filename
        

def answer_question(prompt, video_file, transcript_file):
    timestamp, question = split_timestamp_question(prompt)
    if timestamp is None:
        return "Please provide a valid timestamp in the format 'mm:ss' or 'hh:mm:ss'."
    else:
        try:
            video_path = video_file#change to mkv if required
            transcript_path = transcript_file
            timestamp = get_timestamps_in_seconds(timestamp)
            vid_length, frame = process_video(video_path, timestamp)
            vid_length = int(vid_length)

            #print(vid_length)

            transcript = pd.read_csv(transcript_path)
            text = build_transcript(transcript, timestamp, vid_length)
            #print("Relevant transcript: ", text)

            SYSTEM_PROMPT = "You are an expert educator. You have to answer a question that a student has asked from a video. For context, we have provided you with the transcript around the relevant timestamp, and the frame from the video corresponding to the relevant timestamp."

            QUESTION_PROMPT = "Use the context from the transcript to answer the following question in a single short paragraph. Use a conversational tone, as if you are a teaching assistant answering a student's question. If the question is not related to the video, politely inform the user that you cannot answer it."

            final_prompt = "System Prompt: " + SYSTEM_PROMPT + '\n' + " Relevant transcript: " + text + '\n' + "Question Prompt: " + QUESTION_PROMPT + "Question: " + '\n' + question

            #print(final_prompt)
            base64_image = encode_image(frame)

            payload = {
            "model": "gpt-4o",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": final_prompt,
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 300
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

            #print(response.json())
            response_json  = response.json()
            #data = json.loads(response_json)
            if 'error' in response_json:
                return f"Error: {response_json['error']['message']} --- Please try again after a few seconds."
            response = str(response_json['choices'][0]['message']['content'])
            return response
        except:
            return "An error occurred while processing your request. Please try again."
