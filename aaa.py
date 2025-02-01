import tkinter as tk
from datetime import datetime, timedelta
import random
import json
import os

# File to store user data
DATA_FILE = "user_data.json"

# Load user data from file (if it exists)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

# Save user data to file
def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump(user_data, file)

# Dictionary to store data for each member
user_data = load_data()  # Load previous data at startup

# Health tips categorized by issue
health_tips = {
    "back pain": [
        "Apply a heating pad to your lower back to relieve pain.",
        "Practice gentle yoga stretches for back pain relief.",
        "Take a warm bath to relax your back muscles.",
    ],
    "cramps": [
        "Use a heating pad on your abdomen to ease cramps.",
        "Drink herbal teas like chamomile or ginger tea.",
        "Take over-the-counter pain relievers like ibuprofen.",
    ],
    "bloating": [
        "Avoid salty foods to reduce water retention.",
        "Drink plenty of water to flush out excess fluids.",
        "Eat small, frequent meals to avoid bloating.",
    ],
    "mood swings": [
        "Practice deep breathing or meditation to calm your mind.",
        "Engage in regular physical activity to boost your mood.",
        "Get enough sleep to regulate your emotions.",
    ],
    "fatigue": [
        "Eat iron-rich foods like spinach and beans to combat fatigue.",
        "Take short naps to recharge your energy.",
        "Stay hydrated to avoid feeling tired.",
    ],
}

# Global variable to track the current user
current_user = None

# Function to predict next period and ovulation
def predict_cycle(username):
    if username not in user_data or not user_data[username]["last_period_start"]:
        return "Please provide the start date of your last period (YYYY-MM-DD)."

    last_period = datetime.strptime(user_data[username]["last_period_start"], "%Y-%m-%d")
    next_period = last_period + timedelta(days=user_data[username]["cycle_length"])
    ovulation_date = last_period + timedelta(days=user_data[username]["cycle_length"] - 14)

    return (
        f"Last Period Start: {last_period.strftime('%Y-%m-%d')}\n"
        f"Next Period Predicted: {next_period.strftime('%Y-%m-%d')}\n"
        f"Ovulation Predicted: {ovulation_date.strftime('%Y-%m-%d')}\n"
    )

# Function to provide reminders
def provide_reminders(username):
    if username not in user_data or not user_data[username]["last_period_start"]:
        return "Please provide your last period date first."

    last_period = datetime.strptime(user_data[username]["last_period_start"], "%Y-%m-%d")
    next_period = last_period + timedelta(days=user_data[username]["cycle_length"])
    ovulation_date = last_period + timedelta(days=user_data[username]["cycle_length"] - 14)

    return (
        f"Reminder:\n"
        f"- Your next period is on {next_period.strftime('%Y-%m-%d')}.\n"
        f"- Your ovulation date is on {ovulation_date.strftime('%Y-%m-%d')}.\n"
    )

# Function to handle chatbot conversation
def chat():
    global current_user
    user_input = entry.get().strip().lower()
    chat_history.insert(tk.END, f"You: {user_input}\n")

    # Check if the user is providing a username
    if user_input.startswith("my username is "):
        username = user_input.replace("my username is ", "").strip()
        if username not in user_data:
            user_data[username] = {"last_period_start": None, "cycle_length": 28}
            chat_history.insert(tk.END, f"Chatbot: Welcome, {username}! Your account has been created.\n")
        else:
            chat_history.insert(tk.END, f"Chatbot: Welcome back, {username}!\n")
            # Retrieve and display previous data
            if user_data[username]["last_period_start"]:
                chat_history.insert(tk.END, f"Chatbot: Your last period was on {user_data[username]['last_period_start']}.\n")
            if user_data[username]["cycle_length"]:
                chat_history.insert(tk.END, f"Chatbot: Your cycle length is {user_data[username]['cycle_length']} days.\n")
        current_user = username
        chat_history.insert(tk.END, f"Chatbot: You can now provide your last period date or cycle length.\n")
        save_data()  # Save data after updating

    # Check if the user is providing a date (last period)
    elif any(word in user_input for word in ["last period", "period was", "started on"]):
        if not current_user:
            chat_history.insert(tk.END, "Chatbot: Please provide your username first (e.g., 'My username is Alice').\n")
        else:
            try:
                # Extract date from input
                date_str = user_input.split(" ")[-1]  # Assumes date is the last word
                input_date = datetime.strptime(date_str, "%Y-%m-%d")
                if input_date > datetime.now():
                    chat_history.insert(tk.END, "Chatbot: Date cannot be in the future. Please enter a valid date.\n")
                else:
                    user_data[current_user]["last_period_start"] = date_str
                    chat_history.insert(tk.END, f"Chatbot: Last period date saved as {date_str}.\n")
                    # Automatically provide predictions and reminders
                    prediction = predict_cycle(current_user)
                    chat_history.insert(tk.END, f"Chatbot: {prediction}\n")
                    reminders = provide_reminders(current_user)
                    chat_history.insert(tk.END, f"Chatbot: {reminders}\n")
                    save_data()  # Save data after updating
            except ValueError:
                chat_history.insert(tk.END, "Chatbot: Invalid date format. Please use YYYY-MM-DD.\n")

    # Check if the user is providing cycle length
    elif any(word in user_input for word in ["cycle length", "length is"]):
        if not current_user:
            chat_history.insert(tk.END, "Chatbot: Please provide your username first (e.g., 'My username is Alice').\n")
        else:
            try:
                # Extract cycle length from input
                length = int(user_input.split(" ")[-1])  # Assumes length is the last word
                if 21 <= length <= 35:
                    user_data[current_user]["cycle_length"] = length
                    chat_history.insert(tk.END, f"Chatbot: Cycle length updated to {length} days.\n")
                    # Automatically provide predictions and reminders if last period date is available
                    if user_data[current_user]["last_period_start"]:
                        prediction = predict_cycle(current_user)
                        chat_history.insert(tk.END, f"Chatbot: {prediction}\n")
                        reminders = provide_reminders(current_user)
                        chat_history.insert(tk.END, f"Chatbot: {reminders}\n")
                    save_data()  # Save data after updating
                else:
                    chat_history.insert(tk.END, "Chatbot: Cycle length should be between 21 and 35 days.\n")
            except ValueError:
                chat_history.insert(tk.END, "Chatbot: Invalid input. Please enter a number.\n")

    # Check if the user is asking for health tips
    elif any(word in user_input for word in ["health tips", "tips", "advice"]):
        chat_history.insert(tk.END, "Chatbot: What issue are you facing? (e.g., back pain, cramps, bloating, mood swings, fatigue)\n")

    # Check if the user mentions a specific issue
    elif any(issue in user_input for issue in health_tips.keys()):
        issue = next((issue for issue in health_tips.keys() if issue in user_input), None)
        if issue:
            tips = random.sample(health_tips[issue], min(3, len(health_tips[issue])))  # Show up to 3 random tips
            chat_history.insert(tk.END, f"Chatbot: Here are some tips for {issue}:\n")
            for tip in tips:
                chat_history.insert(tk.END, f"- {tip}\n")

    # Check if the user is asking for reminders
    elif any(word in user_input for word in ["reminder", "remind me"]):
        if not current_user:
            chat_history.insert(tk.END, "Chatbot: Please provide your username first (e.g., 'My username is Alice').\n")
        else:
            reminders = provide_reminders(current_user)
            chat_history.insert(tk.END, f"Chatbot: {reminders}\n")

    # Check if the user is asking for help
    elif any(word in user_input for word in ["help", "what can you do"]):
        chat_history.insert(tk.END, "Chatbot: I can help you track your menstrual cycle. Here's what you can do:\n")
        chat_history.insert(tk.END, "- Provide your username (e.g., 'My username is Alice').\n")
        chat_history.insert(tk.END, "- Tell me your last period date (e.g., 'My last period was 2023-10-01').\n")
        chat_history.insert(tk.END, "- Tell me your cycle length (e.g., 'My cycle length is 28').\n")
        chat_history.insert(tk.END, "- Ask for health tips (e.g., 'Give me some health tips').\n")
        chat_history.insert(tk.END, "- Mention an issue (e.g., 'I have back pain').\n")
        chat_history.insert(tk.END, "- Ask for reminders (e.g., 'Remind me of my next period').\n")

    # Default response for unrecognized input
    else:
        chat_history.insert(tk.END, "Chatbot: I didn't understand that. Type 'help' for a list of commands.\n")

    # Clear the input box
    entry.delete(0, tk.END)

# Set up the main window
root = tk.Tk()
root.title("Periods Tracker Chatbot")

# Create and place the widgets
chat_history = tk.Text(root, width=60, height=20, wrap=tk.WORD)
chat_history.pack(pady=10)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_history.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=chat_history.yview)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

send_button = tk.Button(root, text="Send", command=chat)
send_button.pack(pady=5)

# Add an initial message from the chatbot
chat_history.insert(tk.END, "Chatbot: Hi! I'm your Periods Tracker Chatbot. How can I help you today?\n")
chat_history.insert(tk.END, "Please provide your username (e.g., 'My username is Alice').\n\n")

# Start the GUI event loop
root.mainloop()