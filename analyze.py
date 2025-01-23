import json
import datetime
from collections import Counter
import re

# Regex pattern for emojis
emoji_pattern = re.compile(
    r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
    r"\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
    r"\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
    r"\U00002702-\U000027B0\U000024C2-\U0001F251]"
)

def analyze_telegram_chat(file_path):
    # Load the JSON file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Initialize metrics
    messages_count = {}
    word_count = {}
    character_count = {}
    unique_words = {}
    emoji_usage = Counter()
    word_frequency = {}
    word_before_emoji = Counter()
    response_times = []
    conversation_starters = {}
    message_dates = {}
    peak_activity = Counter()
    emoji_count_per_person = Counter()
    total_emoji_count = 0
    emoji_usage_per_person = {}

    last_message_time = None
    last_sender = None

    # Process each message
    for message in data.get("messages", []):
        sender = message.get("from")
        text = message.get("text", "")
        date_str = message.get("date", "")

        if not sender or not date_str:
            continue

        # Handle text if it's a list
        if isinstance(text, list):
            text = ' '.join([str(item) for item in text])

        # Strip and clean text
        text = text.strip()

        try:
            message_date = datetime.datetime.fromisoformat(date_str)
        except ValueError:
            continue

        # Track messages by date
        message_dates.setdefault(message_date.date(), set()).add(sender)

        # Track peak activity by hour
        peak_activity[message_date.hour] += 1

        # Count messages
        messages_count[sender] = messages_count.get(sender, 0) + 1

        # Count words and characters
        if text:
            words = text.split()
            word_count[sender] = word_count.get(sender, 0) + len(words)
            character_count[sender] = character_count.get(sender, 0) + len(text)

            # Unique words
            unique_words.setdefault(sender, set()).update(words)

            # Word frequency
            word_frequency.setdefault(sender, Counter()).update(words)

            # Emojis
            emojis = emoji_pattern.findall(text)
            emoji_count = len(emojis)
            if emoji_count > 0:
                emoji_usage.update(emojis)  # Update the global emoji count
                emoji_count_per_person[sender] += emoji_count
                total_emoji_count += emoji_count

                # Track emoji counts per person (per sender)
                for emoji in emojis:
                    if sender not in emoji_usage_per_person:
                        emoji_usage_per_person[sender] = Counter()
                    emoji_usage_per_person[sender][emoji] += 1

                # Track words before emojis
                words_before_emoji = [
                    words[i - 1]
                    for i in range(1, len(words))
                    if emoji_pattern.match(words[i])
                ]
                word_before_emoji.update(words_before_emoji)

        # Response time calculation
        if last_sender and last_message_time and last_sender != sender:
            response_times.append((message_date - last_message_time).total_seconds())

        # Update last message details
        last_message_time = message_date
        last_sender = sender

        # Identify conversation starters (first message of the day)
        if message_date.time() < datetime.time(8, 0):
            conversation_starters[sender] = conversation_starters.get(sender, 0) + 1

    # Calculate metrics
    total_days = (
        (max(message_dates) - min(message_dates)).days + 1
        if message_dates else 0
    )
    no_activity_days = total_days - len(message_dates)

    days_one_person_sent = {
        sender: sum(1 for day_senders in message_dates.values() if {sender} == day_senders)
        for sender in messages_count
    }

    # Top 10 words (overall and individually)
    overall_word_frequency = sum((counter for counter in word_frequency.values()), Counter())
    top_10_words_overall = overall_word_frequency.most_common(10)
    top_10_words_per_person = {
        sender: freq.most_common(10) for sender, freq in word_frequency.items()
    }

    # Average message length (words)
    avg_message_length = {
        sender: word_count[sender] / messages_count[sender] for sender in messages_count
    }

    # Top 10 words preceding emojis
    top_words_before_emojis = word_before_emoji.most_common(10)

    # Overall emoji usage (using Counter's most_common)
    most_frequent_emoji_overall = emoji_usage.most_common(1)

    # Most frequent emoji for each person
    most_frequent_emoji_per_person = {}
    for sender, count in emoji_count_per_person.items():
        if count > 0:  # If this sender has used emojis
            most_frequent_emoji_per_person[sender] = emoji_usage_per_person[sender].most_common(1)[0]
        else:
            most_frequent_emoji_per_person[sender] = ("None", 0)

    return {
        "messages_count": messages_count,
        "word_count": word_count,
        "character_count": character_count,
        "unique_words": {sender: len(words) for sender, words in unique_words.items()},
        "days_with_no_messages": no_activity_days,
        "days_one_person_sent": days_one_person_sent,
        "peak_activity": sorted(peak_activity.items()),
        "top_10_words_overall": top_10_words_overall,
        "top_10_words_per_person": top_10_words_per_person,
        "avg_message_length": avg_message_length,
        "most_frequent_emoji_overall": most_frequent_emoji_overall,
        "most_frequent_emoji_per_person": most_frequent_emoji_per_person,
        "top_words_before_emojis": top_words_before_emojis,
        "total_emoji_count": total_emoji_count,
        "emoji_count_per_person": dict(emoji_count_per_person),
        "conversation_starters": conversation_starters,
    }

# Specify the path to your JSON file
file_path = 'result.json'


results = analyze_telegram_chat(file_path)


def display_results(results):
    print("\n===== Telegram Chat Analysis =====\n")

    print("Total Messages Sent by Each Person:")
    for person, count in results["messages_count"].items():
        print(f"  {person}: {count}")

    print("\nNumber of Words Sent by Each Person:")
    for person, count in results["word_count"].items():
        print(f"  {person}: {count}")

    print("\nTotal Characters Sent by Each Person:")
    for person, count in results["character_count"].items():
        print(f"  {person}: {count}")

    print("\nUnique Words Used by Each Person:")
    for person, count in results["unique_words"].items():
        print(f"  {person}: {count}")

    print("\nDays with No Messages Sent:")
    print(f"  {results['days_with_no_messages']}")

    print("\nDays Only One Person Sent Messages:")
    for person, days in results["days_one_person_sent"].items():
        print(f"  {person}: {days} days")

    print("\nPeak Activity by Hour:")
    for hour, count in results["peak_activity"]:
        print(f"  {hour}:00 - {count} messages")

    print("\nTop 10 Most Common Words Overall:")
    for word, count in results["top_10_words_overall"]:
        print(f"  {word}: {count}")

    print("\nTop 10 Most Common Words by Each Person:")
    for person, words in results["top_10_words_per_person"].items():
        print(f"  {person}:")
        for word, count in words:
            print(f"    {word}: {count}")

    print("\nAverage Message Length (words):")
    for person, avg_length in results["avg_message_length"].items():
        print(f"  {person}: {avg_length:.2f} words")

    print("\nMost Frequently Used Emoji Overall:")
    emoji, count = results["most_frequent_emoji_overall"][0]
    print(f"  {emoji} - {count} times")

    print("\nMost Frequently Used Emoji by Each Person:")
    for person, (emoji, count) in results["most_frequent_emoji_per_person"].items():
        print(f"  {person}: {emoji} ({count} times)")

    print("\nTop 10 Words Before Emojis:")
    for word, count in results["top_words_before_emojis"]:
        print(f"  {word}: {count}")

    print("\nTotal Emoji Count:")
    print(f"  {results['total_emoji_count']}")

    print("\nEmoji Count Per Person:")
    for person, count in results["emoji_count_per_person"].items():
        print(f"  {person}: {count}")

    print("\nConversations Started by Each Person:")
    for person, count in results["conversation_starters"].items():
        print(f"  {person}: {count} times")

display_results(results)
