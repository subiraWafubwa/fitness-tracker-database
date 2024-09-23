from prettytable import PrettyTable
from config import get_session
from models import User, Target, Muscle, Exercise, BodySection, Session, Workout

# General commit function
def commit_session(instance):
    session = get_session()
    session.add(instance)
    session.commit()

# Create Methods
def create_user(username, email):
    new_user = User(username=username, email=email)
    commit_session(new_user)

def create_targets(username, month, back_and_shoulder_target, arms_target, core_target, legs_target, back_and_shoulder_progress = 0, arms_progress = 0, core_progress= 0 , legs_progress = 0):
    new_target = Target(username=username, month=month, back_and_shoulder_target=back_and_shoulder_target, arms_target=arms_target, core_target=core_target, legs_target=legs_target, back_and_shoulder_progress=back_and_shoulder_progress, arms_progress=arms_progress, core_progress=core_progress, legs_progress=legs_progress)
    commit_session(new_target)

def create_muscle(muscle_name, explanation, body_section_id):
    new_muscle = Muscle(muscle_name=muscle_name, explanation=explanation, body_section_id=body_section_id)
    commit_session(new_muscle)

def create_exercise(exercise_name, reps, sets, muscle_id, intensity_id):
    new_exercise = Exercise(exercise_name=exercise_name, reps=reps, sets=sets, muscle_id=muscle_id, intensity_id=intensity_id)
    commit_session(new_exercise)

def create_body_section(body_section_name):
    new_body_section = BodySection(body_section_name=body_section_name)
    commit_session(new_body_section)

def create_session(username, date, workout_id, target_id):
    new_session = Session(username=username, date=date, workout_id=workout_id, target_id=target_id)
    commit_session(new_session)

def create_workout(workout_name, intensity, body_section_id):
    new_workout = Workout(workout_name=workout_name, intensity=intensity, body_section_id=body_section_id)
    commit_session(new_workout)

# Check whether a user exists
def user_exists(value):
    session = get_session()
    try:
        if value:
            # Check for username or email
            user = (
                session.query(User)
                .filter((User.username == value) | (User.email == value))
                .first()
            )
        else:
            return False

        return user is not None
    finally:
        session.close()

# Check if target for current month exists, else creates new target
def get_target(username, month):
    session = get_session()
    # Query for an existing target for the given username and month
    target = session.query(Target).filter_by(username=username, month=month).first()
    
    if target:
        # If target exists, return its ID
        return target.id
    else:
        # If no target exists, create a new target for the current user
        return False
    
# Getting and validating data
def get_target_value(target_name):
    while True:
        try:
            value = int(input(f"Enter {target_name} target value: " + "\033[32m" + "Recommended (21):" + "\033[0m" + " "))
            if 0 <= value <= 30:
                return value
            else:
                print('\033[31m' + "(!) Invalid number added. Please enter a value between 0 and 30." + '\033[0m')
        except ValueError:
            print('\033[31m' + "(!) Invalid input. Please enter a numeric value." + '\033[0m')

# Function to map workout id to body section and update the progress accordingly
def update_workout_progress(username, workout_id):
    session = get_session()
    # Fetch the workout details based on the workout_id
    workout = session.query(Workout).filter_by(id=workout_id).first()

    if workout:
        intensity = workout.intensity
        body_section_id = workout.body_section_id

        # Get the current month (assuming you use the `datetime` module to get the current month)
        from datetime import datetime
        current_month = datetime.now().strftime("%B")
        
        # Fetch the user's target for the current month
        target = session.query(Target).filter_by(username=username, month=current_month).first()

        if target:
            # Adjust the progress for the respective body section
            if body_section_id == 1:  # Back and Shoulder
                target.back_and_shoulder_progress += intensity
            elif body_section_id == 2:  # Arms
                target.arms_progress += intensity
            elif body_section_id == 3:  # Core
                target.core_progress += intensity
            elif body_section_id == 4:  # Legs
                target.legs_progress += intensity
            
            # Commit the changes to the database
            session.commit()
            print(f"\nWorkout progress updated for {username} in {current_month}.")
        else:
            print("User target for the current month not found.")
    else:
        print("Workout not found.")
# Getting workout id for sessions
def get_workout_id():
    print('''
Choose the workout you have completed:
            
(1) Advanced Back and Shoulder
(2) Intermediate Back and Shoulder
(3) Beginner Back and Shoulder
(4) Advanced Arms
(5) Intermediate Arms
(6) Beginner Arms
(7) Advanced Core
(8) Intermediate Core
(9) Beginner Core
(10) Advanced Legs
(11) Intermediate Legs
(12) Beginner Legs   
''')
    
    try:
        option = int(input("Enter the workout number: "))
        if 1 <= option <= 12:
            return option
        else:
            print("(!) This value is not accepted. Try again.")
            return None
    except ValueError:
        print("(!) Invalid input. Please enter a numeric value.")
        return None

# Getting the progress data for a user
def get_progress_data(username):
    session = get_session()

    try:
        result = session.query(
            Target.month,
            Target.back_and_shoulder_progress,
            Target.back_and_shoulder_target,
            Target.arms_progress,
            Target.arms_target,
            Target.core_progress,
            Target.core_target,
            Target.legs_progress,
            Target.legs_target
        ).filter(Target.username == username).all()

        if result:
            # Create a PrettyTable instance
            table = PrettyTable()
            table.field_names = ["Month", "Back & Shoulder Progress", "Arms Progress", "Core Progress", "Legs Progress"]

            # Add rows to the table with formatted progress/target
            for row in result:
                month = row[0]
                back_and_shoulder = f"{row[1]}/{row[2]}"
                arms = f"{row[3]}/{row[4]}"
                core = f"{row[5]}/{row[6]}"
                legs = f"{row[7]}/{row[8]}"
                
                table.add_row([month, back_and_shoulder, arms, core, legs])

            # Print the table
            print('\033[32m' + f"\nDisplaying progress data for {username}..." + '\033[0m')
            print(table)

            return "Progress data logged successfully."
        else:
            return f"No progress data found for {username}."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        session.close()

# Displaying all sessions for a user
def display_sessions_data(username):
    session = get_session()

    try:
        # Query to retrieve session data for the given username
        result = session.query(
            Session.username,
            Session.date,
            Session.workout_id,
            Session.target_id
        ).filter(Session.username == username).all()

        if result:
            # Create a PrettyTable instance
            table = PrettyTable()
            table.field_names = ["Username", "Date", "Workout ID", "Target ID"]

            # Add rows to the table
            for row in result:
                table.add_row([row.username, row.date, row.workout_id, row.target_id])

            # Print the table
            print('\033[32m' + f"\nDisplaying all sessions for {username}..." + '\033[0m')
            print(table)
            return "Session data displayed successfully."
        else:
            return f"No session data found for {username}."
    except Exception as e:
        return f"An error occurred: {e}"
    finally:
        session.close()


def get_workout_details(workout_id):
    session = get_session()
    
    try:
        # Query to get the workout based on the provided workout_id
        workout = session.query(Workout).filter(Workout.id == workout_id).first()
        
        if workout:
            # Return the body_section_id and intensity of the workout
            return workout.body_section_id, workout.intensity
        else:
            print("(!) Workout not found.")
            return None, None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

    finally:
        session.close()

def get_exercises_by_workout():
    print('''
Choose the workout you have completed:
            
(1) Advanced Back and Shoulder
(2) Intermediate Back and Shoulder
(3) Beginner Back and Shoulder
(4) Advanced Arms
(5) Intermediate Arms
(6) Beginner Arms
(7) Advanced Core
(8) Intermediate Core
(9) Beginner Core
(10) Advanced Legs
(11) Intermediate Legs
(12) Beginner Legs   
''')
    
    try:
        option = int(input("Enter the workout number: "))
        if 1 <= option <= 12:
            # Retrieve body_section_id and intensity using the workout ID
            body_section_id, intensity = get_workout_details(option)
            
            if body_section_id is None or intensity is None:
                print("Workout details not found. Cannot retrieve exercises.")
                return  # Handle the case where the workout is not found

            session = get_session()
            
            try:
                # Define the allowed muscle names based on the body_section_id
                body_section_muscles = {
                    1: ["Trapezius", "Shoulder", "Latissimus Dorsi"],
                    2: ["Biceps", "Triceps", "Forearms"],
                    3: ["Rectus Abdominis (Abs)", "External Abdominal Oblique (Side Abs)"],
                    4: ["Front Thigh (Quadriceps)", "Back Thigh (Hamstrings)", "Calves (Gastrocnemius and Soleus)"]
                }

                allowed_muscles = body_section_muscles.get(body_section_id, [])

                # Query to get muscles matching the allowed names
                muscles = session.query(Muscle).filter(Muscle.muscle_name.in_(allowed_muscles)).all()
                
                if not muscles:
                    print(f"No muscles found for body section ID {body_section_id}")
                    return

                # Gather all exercise IDs for the retrieved muscles
                muscle_ids = [muscle.id for muscle in muscles]
                
                # Get exercises that match both muscle_ids and intensity
                exercises = session.query(Exercise).filter(
                    Exercise.muscle_id.in_(muscle_ids),
                    Exercise.intensity_id == intensity  # Filter by intensity
                ).all()

                if not exercises:
                    print(f"No exercises found for body section ID {body_section_id} and intensity {intensity}")
                    return

                # Create a PrettyTable instance
                table = PrettyTable()
                table.field_names = ["Exercise ID", "Exercise Name", "Reps", "Sets", "Muscle ID"]

                # Populate the table with exercise data
                for exercise in exercises:
                    table.add_row([exercise.id, exercise.exercise_name, exercise.reps, exercise.sets, exercise.muscle_id])

                # Print the table
                print(f"Exercises for workout {option} (Body Section ID: {body_section_id}, Intensity: {intensity}):")
                print(table)
            
            except Exception as e:
                print(f"An error occurred while retrieving exercises: {e}")
            
            finally:
                session.close()
        else:
            print("(!) This value is not accepted. Try again.")
            return None
    except ValueError:
        print("(!) Invalid input. Please enter a numeric value.")
        return None

def display_tables():
    print('''\
Which table do you want to display: 
          
(1) Workouts
(2) Exercises
(3) Muscles
(4) Sessions
(5) Targets
(6) Users
(7) Body Sections
''')
    choice = input("Enter your choice (1-7): ")
    session = get_session()

    if choice == '1':
        records = session.query(Workout).all()
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Intensity"]
        for record in records:
            table.add_row([record.id, record.workout_name, record.intensity])
        print(str(table))
    
    elif choice == '2':
        records = session.query(Exercise).all()
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Reps", "Sets"]
        for record in records:
            table.add_row([record.id, record.exercise_name, record.reps, record.sets])
        print(str(table))
    
    elif choice == '3':
        records = session.query(Muscle).all()
        table = PrettyTable()
        table.field_names = ["ID", "Name", "Explanation"]
        for record in records:
            table.add_row([record.id, record.muscle_name, record.explanation])
        print(str(table))
    
    elif choice == '4':
        records = session.query(Session).all()
        table = PrettyTable()
        table.field_names = ["ID", "Date", "User", "Workout ID"]
        for record in records:
            table.add_row([record.id, record.date, record.user.username, record.workout_id])
        print(str(table))
    
    elif choice == '5':
        records = session.query(Target).all()
        table = PrettyTable()
        table.field_names = ["ID", "User", "Month", "Core Target"]
        for record in records:
            table.add_row([record.id, record.user.username, record.month, record.core_target])
        print(str(table))
    
    elif choice == '6':
        records = session.query(User).all()
        table = PrettyTable()
        table.field_names = ["ID", "Username", "Email"]
        for record in records:
            table.add_row([record.id, record.username, record.email])
        print(str(table))
    
    elif choice == '7':
        records = session.query(BodySection).all()
        table = PrettyTable()
        table.field_names = ["ID", "Body Section Name"]
        for record in records:
            table.add_row([record.id, record.body_section_name])
        print(str(table))

    else:
        return "Invalid choice. Please select a number between 1 and 7."