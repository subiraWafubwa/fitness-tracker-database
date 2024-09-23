import re
from methods import *
from datetime import datetime

# Constant objects
month = datetime.now().strftime("%B")
date = datetime.now().date()

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
    
# Create membership and set targets
def create_user():
    print("\nCreating a new memmbership...")
    while True:
        username = input("Enter username: ")
        exists = user_exists(username)
        
        if exists:
            print('\033[31m' + "(!) This username is already in use. Try again" + '\033[0m')
        else:
            while True:
                email = input("Enter email: ")
                regex = r"^\S+@\S+\.\S+$"
                email_matches = re.match(regex, email)
                
                if email_matches:
                    exists = user_exists(email)
                    if not exists:
                        print(f"\nSet workout targets for {month}")
                        back_and_shoulder_target = get_target_value("back and shoulder")
                        arms_target = get_target_value("arms")
                        core_target = get_target_value("core")
                        legs_target = get_target_value("legs")

                        create_user(username, email)
                        create_targets(username, month, back_and_shoulder_target, arms_target, core_target, legs_target, 0, 0, 0, 0)
                        print('\033[32m' + "\n(✓) New member has joined the gym\n" + '\033[0m')
                        
                        show_main_menu()
                    else:
                        print('\033[31m' + "(!) This email is already in use. Try again" + '\033[0m')
                else:
                    print('\033[31m' + "(!) Invalid email format. Try again." + '\033[0m')

# Add workout session
def add_workout_session():
    print("\nCreating a new workout session...")
    
    # Get user input and ensure user exists
    while True:
        username = input("Enter username: ")
        existing_user = user_exists(username)
        
        if not existing_user:
            print('\033[31m' + "(!) This user does not exist. Try again" + '\033[0m')
        else:            
            while True:
                # Get the user's target for the month
                target_id = get_target(username, month)
                
                if target_id:
                    print(f"\nAdd new session for {username} on {date}:")
                    
                    # Get the workout ID from user input
                    workout_id = get_workout_id()
                    
                    if workout_id:                        
                        # Update the user's target progress based on the workout completed
                        update_workout_progress(username, workout_id)
                        
                        # Create session
                        create_session(username, date, workout_id, target_id)
                    
                    # After completing the session, go back to the main menu and break out of the loop
                    show_main_menu()
                    break  # Exit the loop after returning to the main menu
                
                else:
                    try:
                        # If no target for the current month, prompt user to set new targets
                        print(f"No targets set found for {username} in {month}.")
                        print(f"\nSet workout targets for {month}...")

                        back_and_shoulder_target = get_target_value("back and shoulder")
                        arms_target = get_target_value("arms")
                        core_target = get_target_value("core")
                        legs_target = get_target_value("legs")

                        # Create new targets for the user in the current month
                        create_targets(
                            username, month, back_and_shoulder_target, arms_target, core_target, legs_target, 
                            back_and_shoulder_progress=0, arms_progress=0, core_progress=0, legs_progress=0
                        )
                        
                    finally:
                        # Once targets are created, ask for the workout session again
                        print(f"\nAdd new session for {username} on {date}:")
                        
                        # Get the target ID again after creating the target
                        target_id = get_target(username, month)
                        
                        if target_id:
                            workout_id = get_workout_id()
                            
                            if workout_id:
                                # Log the session info
                                print(f"{username}, {date}, {target_id}, {workout_id}")
                                
                                # Update the user's workout progress
                                update_workout_progress(username, workout_id)
                                
                                # Create a new session record
                                create_session(username, date, workout_id, target_id)

                        # After completing the session, go back to the main menu and break
                        show_main_menu()
                        break  # Exit the loop after returning to the main menu

# Generate user progress
def get_progress():
    while True:
        username = input("Enter username: ")
        print('\n')
        existing_user = user_exists(username)
        
        if not existing_user:
            print('\033[31m' + "(!) This user does not exist. Try again" + '\033[0m')
        else:
            get_progress_data(username)
        break

def get_user_sessions():
    while True:
        username = input("Enter username: ")
        print('\n')
        existing_user = user_exists(username)
        
        if not existing_user:
            print('\033[31m' + "(!) This user does not exist. Try again" + '\033[0m')
        else:
            display_sessions_data(username)
        break


def main():
    while True:
        show_main_menu()
        choice = input("Enter choice: ")

        if choice == "1":
            create_user()
        elif choice == "2":
            add_workout_session()
        elif choice == "3":
            get_progress()
        elif choice == "4":
            get_user_sessions()
        elif choice == "5":
            get_exercises_by_workout()
        elif choice == "6":
            display_tables()
        elif choice == "7":
            print("Exiting. Have a great day!")
            break
        else:
            print('\033[31m' + "(!) Invalid choice. Please select the correct choice" + '\033[0m')

if __name__ == "__main__":
    main()
