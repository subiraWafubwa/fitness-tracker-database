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
        option = int(input("Enter the workout number: "))  # Convert input to integer
        if 1 <= option <= 12:
            return option
        else:
            print("(!) This value is not accepted. Try again.")
            return None
    except ValueError:
        print("(!) Invalid input. Please enter a numeric value.")
        return None
