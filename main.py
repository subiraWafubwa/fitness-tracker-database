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
(5) Display tables
(6) Revoke membership
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

                        # new_user = create_user(username, email)
                        # new_targets = create_targets(username, month, back_and_shoulder_target, arms_target, core_target, legs_target, 0, 0, 0, 0)
                        print('\033[32m' + "\n(✓) New member has joined the gym\n" + '\033[0m')
                        
                        show_main_menu()
                    else:
                        print('\033[31m' + "(!) This email is already in use. Try again" + '\033[0m')
                else:
                    print('\033[31m' + "(!) Invalid email format. Try again." + '\033[0m')

# Add workout session
def add_workout_session():
    print("\nCreating a new workout session...")
    while True:
        username = input("Enter username: ")
        existing_user = user_exists(username)
        if not existing_user:
            print('\033[31m' + "(!) This user does not exist. Try again" + '\033[0m')
        else:
            while True:
                target_id = get_target(username, month)
                if get_target:
                    print(f"\nAdd new session for {username} on {date}:")
                    workout_id = get_workout_id()
                    print(f"{username}, {date}, {target_id}, {workout_id}")
                    # new_session = create_session(username, date, workout_id, target_id)

                    break
                else:
                    try:
                        print(f"No targets set found for {username} in {month}.")
                        print(f"\nSet workout targets for {month}...")
                        back_and_shoulder_target = get_target_value("back and shoulder")
                        arms_target = get_target_value("arms")
                        core_target = get_target_value("core")
                        legs_target = get_target_value("legs")

                        # new_targets = create_targets(username, month, back_and_shoulder_target, arms_target, core_target, legs_target, 0, 0, 0, 0)
                    finally:
                        print(f"\nAdd new session for {username} on {date}:")
                        target_id = get_target(username, month)
                        workout_id = get_workout_id()
                        # new_session = create_session(username, date, workout_id, target_id)

                        ## Update target table
                        
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
            print("Feature not implemented yet.")
        elif choice == "4":
            print("Feature not implemented yet.")
        elif choice == "5":
            print("Feature not implemented yet.")
        elif choice == "6":
            print("Feature not implemented yet.")
        elif choice == "7":
            print("Exiting. Have a great day!")
            break
        else:
            print('\033[31m' + "(!) Invalid choice. Please select the correct choice" + '\033[0m')

if __name__ == "__main__":
    main()
