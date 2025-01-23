import json
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from collections import defaultdict
import numpy as np
from PIL import Image
import matplotlib

import nltk
nltk.download('stopwords')

# Regex pattern for emojis
emoji_pattern = re.compile(
    r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
    r"\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
    r"\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
    r"\U00002702-\U000027B0\U000024C2-\U0001F251]"
)

def generate_word_cloud(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Stopwords list
    stop_words = set(stopwords.words('english'))

    user_messages = defaultdict(list)

    # Define a regex pattern to catch unwanted single characters
    unwanted_pattern = re.compile(r'\b[uU]\b')

    for message in data.get("messages", []):
        sender = message.get("from")
        text = message.get("text", "")

        # Only process messages that contain text
        if not sender or not text or isinstance(text, list):
            continue

        # Handle case when text might be a list
        if isinstance(text, list):
            text = ' '.join([str(item) for item in text])

        text = text.strip()

        # Skip non-text messages
        if re.match(r'^[^a-zA-Z0-9\s]*$', text):
            continue

        # Remove emojis and non-alphanumeric characters
        text = emoji_pattern.sub("", text)

        # Remove unwanted single characters like "u"
        text = unwanted_pattern.sub("", text)

        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)

        user_messages[sender].append(text)

    def color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        darker_medieval_colors = [
            '#9E2A2F',  # Crimson Red
            '#B8860B',  # Darker Golden Yellow
            '#3A5F2F',  # Dark Green
            '#1E3A5F',  # Darker Royal Blue
            '#6A4E23',  # Earthy Brown
            '#4B0082',  # Darker Plum Purple
            '#FF4500',  # Burnt Orange
        ]
        return np.random.choice(darker_medieval_colors)

    # Generate word clouds for each participant
    for sender, messages in user_messages.items():
        combined_text = " ".join(messages)

        wordcloud = WordCloud(
            stopwords=stop_words,
            background_color="white",
            width=800,
            height=600,
            colormap='Spectral',
            contour_width=3,
            contour_color='black',
            max_font_size=100,
            random_state=42,
            relative_scaling=0.5,
            color_func=color_func,
        ).generate(combined_text)

        wordcloud.to_file(f"{sender}_wordcloud.png")
        print(f"Word cloud saved for {sender}")

# Specify the path to your JSON file
file_path = 'result.json'

generate_word_cloud(file_path)
