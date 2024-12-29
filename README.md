Restify - Digital Fatigue Prediction and Recommendation System

About the Project

Restify is a Flask-based web application designed to predict digital fatigue levels and provide users with personalized recommendations accordingly. User inputs are analyzed using a machine learning model to calculate fatigue levels and deliver tailored suggestions.

Features

•User Input: Collects information such as screen time, break duration, sleep time, device type, and purpose of use.

•Fatigue Calculation: Predicts digital fatigue levels using the RandomForestClassifier algorithm.

•Recommendation System: Provides relaxing suggestions based on the user's fatigue level and current environment.

•Visualization: Generates insights into the user's digital usage habits through visualizations.

Technologies Used

•Backend: Python, Flask

•Frontend: HTML

•Data Processing and Modeling: Pandas, NumPy, Scikit-learn (RandomForestClassifier)

•Visualization: Matplotlib, Seaborn

Installation

Install the Required Dependencies:

pip install flask pandas numpy scikit-learn matplotlib seaborn

Run the Project:

python app.py

Launch the Application:
Open http://127.0.0.1:5000 in your web browser to view the application.

File Structure

Restify/
|— app.py           # Main Flask application
|— templates/       # Directory containing HTML files

Usage

•Users fill out the form with details (e.g., screen time, break duration, sleep time, device type).

•The Flask application processes user inputs and predicts fatigue levels using the model.

•Recommendations are displayed based on the fatigue level.

•Visualizations of digital usage habits are available for users to view.

Example Form Fields

•Daily screen time (in minutes)

•Daily break duration (in minutes)

•Sleep duration (in hours)

•User age

•Device type (phone, tablet, computer)

•Purpose of use (education, work, entertainment)

•Current environment (home, library, office)

•User gender

Recommendations

The recommendation system provides suggestions based on the user’s fatigue level and environment, such as:

•Home: "Apply the 20-20-20 rule: Every 20 minutes, focus on something 20 feet away for 20 seconds. 👀💪"

•Office: "Take a 10-minute break by closing your eyes and relaxing in a dark environment. 😌🛋"

•Library: "Practice deep breathing or step outside for fresh air. Maintain proper screen distance to reduce eye strain. 🌬📖"
