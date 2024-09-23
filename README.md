# Mr. Muscles Gym Management System

This code is a gym management system that allows users to create memberships, log workout sessions, track progress, and manage various exercises and workouts. Below is a detailed breakdown of the main components and functions.

## Imports

```python
import re
from methods import *
from datetime import datetime
from prettytable import PrettyTable
from config import get_session
from models import User, Target, Muscle, Exercise, BodySection, Session, Workout
```

`Libraries`: The code imports libraries for regular expressions, date handling, pretty table formatting, and models for database interaction.

`Constants`

```python
month = datetime.now().strftime("%B")
date = datetime.now().date()
```

Current Month and Date: Retrieves the current month and date for use in various functions.

`Main Menu`

```python
def show_main_menu():
    print('''
    Welcome to Mr. Muscles Gym
    (1) Create membership
    (2) Add workout session
    (3) Generate user progress
    (4) View user's sessions
    (5) View workouts
    (6) Display tables
    (7) Exit
    ''')
```

`Menu Function`: Displays the main menu for user interaction.

## User Membership Creation

`create_user()`: This function handles the creation of a new gym membership:

- Prompts for a username and checks if it exists.
- Validates email format and checks for duplicates.
- Collects workout targets for different body sections and saves the user.

## Adding Workout Sessions

`add_workout_session()`: Prompts for a username to log a workout session.
Checks if the user exists and retrieves their workout targets for the month.
Allows the user to select a workout and updates their progress.

## User Progress

`get_progress()`: Prompts for a username and displays their progress data using the get_progress_data() function.

## User Sessions

`get_user_sessions()`: Prompts for a username and displays all workout sessions associated with that user using display_sessions_data().

## Main Loop

`main()`: This function continuously displays the main menu and executes the appropriate function based on user choice.

## Database Interaction

```python
def commit_session(instance):
    session = get_session()
    session.add(instance)
    session.commit()
```

- Handles database session management for creating and updating records.
- User and Target Management

## User Functions

`create_user(username, email)`: Adds a new user to the database.
`user_exists(value)`: Checks if a user (by username or email) exists in the database.
`get_target(username, month)`: Checks for an existing target for the user and month.

## Target Functions

`create_targets(...)`: Creates targets for the user based on their workout goals.

## Workout Management

`create_session(...)`: Records a new workout session.
`update_workout_progress(username, workout_id)`: Updates the progress for the user's workout based on the intensity of the workout completed.

## Data Retrieval

`get_progress_data(username)`: Retrieves and displays the user's progress data in a formatted table.
`display_sessions_data(username)`: Retrieves and displays all workout sessions for a user.

## Exercise Management

`get_workout_id()`: Prompts the user to select a completed workout.
`get_exercises_by_workout()`: Retrieves exercises associated with the chosen workout based on intensity and muscle group.

## Error Handling

The code includes exception handling in various functions to manage and report errors gracefully.

## Conclusion

This gym management system is structured to allow easy interaction for creating memberships, logging workouts, and tracking progress, all while ensuring data integrity through database interactions.
