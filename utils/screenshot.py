# utils/screenshot.py
import os
import datetime
import streamlit as st # Import streamlit for messages

def take_pyautogui_screenshot(folder_path, filename_prefix="server_screenshot"):
    """
    Captures a screenshot of the server's screen using pyautogui and saves it.

    Args:
        folder_path (str): The directory where the image should be saved.
        filename_prefix (str): Prefix for the filename.
    Returns:
        str: The full path to the saved file, or None if saving failed.
    """
    try:
        import pyautogui # Import pyautogui for screenshots

        # Ensure the directory exists
        os.makedirs(folder_path, exist_ok=True)

        # Generate a unique filename with a timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{filename_prefix}-{timestamp}.png"
        file_path = os.path.join(folder_path, filename)

        # Take the screenshot
        screenshot = pyautogui.screenshot()
        screenshot.save(file_path)

        st.success(f"Screenshot saved on server to: {file_path}")
        return file_path
    except Exception as e:
        st.error(f"Error taking or saving screenshot on server: {e}")
        st.warning("PyAutoGUI requires a display environment. If running on a server without a GUI, "
                   "you might need to set up a virtual display (e.g., Xvfb on Linux).")
        return None