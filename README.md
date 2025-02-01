# tinkerhack
Documentation for Periods Tracker Chatbot
Overview
The Periods Tracker Chatbot is a desktop application built using the Tkinter library in Python. It allows users to track their menstrual cycles, receive health tips, and set reminders about their periods. The application stores user data in a JSON file, allowing for data persistence across sessions.

File Structure
user_data.json: A JSON file to store user data including last period start date and cycle length.
Dependencies
tkinter: For creating the graphical user interface.
datetime: For handling date and time operations.
random: For selecting random health tips.
json: For reading and writing JSON data.
os: For checking file existence.
Global Variables
DATA_FILE: A string that stores the path to the JSON file for user data.
user_data: A dictionary that stores user data loaded from the JSON file at startup.
health_tips: A dictionary containing health tips categorized by specific issues.
current_user: A global variable to track the currently active user.
Functions
1. load_data()
This function loads user data from the user_data.json file if it exists. It returns a dictionary containing user data2. save_data()
This function saves the current user_data dictionary to the user_data.json file.
3. predict_cycle(username)
This function predicts the user's next period and ovulation date based on the last period start date and cycle length. It returns a formatted string with the results.4. provide_reminders(username)
This function provides reminders for the user's next period and ovulation date. It checks if the required data is available and returns a formatted reminder string.
Conclusion
The Periods Tracker Chatbot is a useful tool for users to manage their menstrual health. By combining date predictions, health tips, and reminders in an interactive chat format, it aims to provide a personalized experience for tracking menstrual cycles.

Users can easily extend its functionality or modify the health tips as needed, making it a flexible solution for menstrual health management.



