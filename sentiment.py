import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import json
import matplotlib.pyplot as plt

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def perform_sentiment_analysis(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    sentiment_counts = {'positive': 0, 'neutral': 0, 'negative': 0}

    for message in data.get("messages", []):
        text = message.get("text", "")

        if not text:
            continue

        # If the text is a list, join it into a single string
        if isinstance(text, list):
            text = ' '.join(str(item) for item in text)

        sentiment_score = sia.polarity_scores(text)
        compound_score = sentiment_score['compound']

        # Categorize the sentiment
        if compound_score >= 0.05:
            sentiment_counts['positive'] += 1
        elif compound_score <= -0.05:
            sentiment_counts['negative'] += 1
        else:
            sentiment_counts['neutral'] += 1

    return sentiment_counts

# Specify the path to your JSON file
file_path = 'result.json'

sentiment_counts = perform_sentiment_analysis(file_path)

labels = ['Positive', 'Neutral', 'Negative']
sizes = [sentiment_counts['positive'], sentiment_counts['neutral'], sentiment_counts['negative']]
colors = ['#4CAF50', '#9E9E9E', '#F44336']  # Green for Positive, Gray for Neutral, Red for Negative

plt.figure(figsize=(7, 7))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
plt.axis('equal')

output_file = 'sentiment_pie_chart.png'
plt.savefig(output_file, format='png', dpi=300)

plt.close()

print(f"Sentiment pie chart saved as {output_file}")
