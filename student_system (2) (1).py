"""
Student Result & Attendance Terminal System
PROG103 Assignment

This system demonstrates high-level structured programming by integrating
student attendance and subject scores to calculate a comprehensive CGPA.
"""

import sys

# Global nested dictionary to store student records
# Format: { "student_id": { "name": str, "attendance": float, "scores": list } }
students_db = {}


def calculate_attendance_points(attendance_percentage):
    """
    Converts attendance percentage into points (0 to 5).
    Supporting SDG 4 by emphasizing the importance of student attendance.
    """
    if attendance_percentage >= 90:
        return 5.0
    elif attendance_percentage >= 80:
        return 4.0
    elif attendance_percentage >= 70:
        return 3.0
    elif attendance_percentage >= 60:
        return 2.0
    elif attendance_percentage >= 50:
        return 1.0
    else:
        return 0.0


def calculate_gpa(scores):
    """
    Calculates the average of subject scores and converts it to a Grade Point (0 to 5).
    """
    if not scores:
        return 0.0
    
    average_score = sum(scores) / len(scores)
    
    if average_score >= 90:
        return 5.0
    elif average_score >= 80:
        return 4.0
    elif average_score >= 70:
        return 3.0
    elif average_score >= 60:
        return 2.0
    elif average_score >= 50:
        return 1.0
    else:
        return 0.0


def calculate_cgpa(gpa, attendance_points):
    """
    Calculates the final Cumulative Grade Point Average (CGPA).
    Formula: Average Subject Points + Attendance Points (Max 10.0)
    """
    return gpa + attendance_points


def get_valid_number(prompt, num_type=float, min_val=None, max_val=None):
    """
    Utility function with robust try/except blocks to ensure safe user input.
    Prevents the system from crashing if a user enters a letter instead of a number.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            value = num_type(user_input)
            if min_val is not None and value < min_val:
                print(f"  [!] Error: Value must be at least {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"  [!] Error: Value must not exceed {max_val}.")
                continue
            return value
        except ValueError:
            print("  [!] Error: Invalid input. Please enter a valid number, not text/letters.")


def add_student():
    """Adds a new student to the database."""
    print("\n--- Add New Student ---")
    student_id = input("Enter Student ID (e.g., 900000001): ").strip().upper()
    
    if not student_id:
        print("  [!] Error: Student ID cannot be empty.")
        return
        
    if student_id in students_db:
        print(f"  [!] Error: Student ID '{student_id}' already exists!")
        return
    
    name = input("Enter Student Name: ").strip()
    if not name:
        print("  [!] Error: Name cannot be empty.")
        return

    attendance = get_valid_number("Enter Attendance Percentage (0-100): ", float, 0, 100)
    
    # Adding to the nested dictionary
    students_db[student_id] = {
        "name": name,
        "attendance": attendance,
        "scores": []
    }
    print(f"  [+] Success: Student '{name}' added to the system.")


def input_scores():
    """Adds scores for the 6 specific subjects to a specific student."""
    print("\n--- Input Subject Scores ---")
    student_id = input("Enter Student ID: ").strip().upper()
    
    if student_id not in students_db:
        print("  [!] Error: Student not found in the database.")
        return
        
    print(f"Adding scores for {students_db[student_id]['name']}.")
    
    subjects = [
        "Introduction to Computer Hardware (COMP 109)",
        "Principles of Software Engineering (PROG 102)",
        "Introduction to Databases (COMP 102)",
        "Introduction to Data Communication (DIT 1203)",
        "Computerized Mathematics (Math 108)",
        "Principles of Structured Programming (PROG 103)"
    ]
    
    # Clear existing scores if any
    students_db[student_id]["scores"] = []
    
    for subject in subjects:
        score = get_valid_number(f"Enter score for {subject} (0-100): ", float, 0, 100)
        students_db[student_id]["scores"].append(score)
        print("  [+] Score recorded.")
        
    print("  [+] All 6 subject scores recorded successfully.")
        

def delete_update_student():
    """Allows updating or removing a student record."""
    print("\n--- Delete or Update Student ---")
    student_id = input("Enter Student ID to modify/delete: ").strip().upper()
    
    if student_id not in students_db:
        print("  [!] Error: Student not found in the database.")
        return
        
    print(f"\nTarget Student: {students_db[student_id]['name']}")
    print("1. Update Name")
    print("2. Update Attendance")
    print("3. Delete Student entirely")
    print("4. Cancel")
    
    choice = input("Select an option (1-4): ").strip()
    
    if choice == '1':
        new_name = input("Enter new name: ").strip()
        if new_name:
            students_db[student_id]["name"] = new_name
            print("  [+] Success: Name updated.")
        else:
            print("  [!] Error: Name cannot be empty.")
    elif choice == '2':
        new_attendance = get_valid_number("Enter new Attendance (0-100): ", float, 0, 100)
        students_db[student_id]["attendance"] = new_attendance
        print("  [+] Success: Attendance updated.")
    elif choice == '3':
        confirm = input(f"Are you sure you want to delete {students_db[student_id]['name']}? (y/n): ").strip().lower()
        if confirm == 'y':
            del students_db[student_id]
            print("  [+] Success: Student record deleted.")
        else:
            print("  [-] Deletion cancelled.")
    elif choice == '4':
        print("  [-] Operation cancelled.")
    else:
        print("  [!] Error: Invalid selection.")


def show_analytics():
    """Displays a formatted analytical report of all students."""
    print("\n" + "="*70)
    print(f"{'STUDENT ANALYTICS DASHBOARD':^70}")
    print("="*70)
    
    if not students_db:
        print(f"{'No student records found in the system.':^70}")
        print("="*70)
        return
        
    print(f"{'ID':<10} | {'Name':<20} | {'Att.(%)':<8} | {'GPA':<5} | {'CGPA':<5} | {'Status':<10}")
    print("-" * 70)
    
    for sid, data in students_db.items():
        name = data["name"]
        attendance = data["attendance"]
        scores = data["scores"]
        
        # Data Processing Logic
        att_points = calculate_attendance_points(attendance)
        gpa = calculate_gpa(scores)
        cgpa = calculate_cgpa(gpa, att_points)
        
        # Determine Status (Pass if GPA >= 2.6)
        status = "PASS" if gpa >= 2.6 else "FAIL"
        
        # Limit name length for display purposes
        display_name = name[:17] + "..." if len(name) > 20 else name
        
        print(f"{sid:<10} | {display_name:<20} | {attendance:<8.1f} | {gpa:<5.1f} | {cgpa:<5.1f} | {status:<10}")
        
    print("="*70)
    print("  * GPA is based on Subject Scores (Max: 5.0)")
    print("  * CGPA = GPA + Attendance Points (Max: 10.0)")
    print("  * Pass requires a GPA of 2.6 or higher")


def view_transcript():
    """Displays a student transcript formatted like the official Limkokwing document."""
    print("\n--- View Student Transcript ---")
    student_id = input("Enter Student ID: ").strip().upper()
    
    if student_id not in students_db:
        print("  [!] Error: Student not found in the database.")
        return
        
    student = students_db[student_id]
    scores = student["scores"]
    
    if len(scores) < 6:
        print("  [!] Error: Student does not have all 6 subject scores recorded yet.")
        return
        
    att_points = calculate_attendance_points(student["attendance"])
    gpa = calculate_gpa(scores)
    cgpa = calculate_cgpa(gpa, att_points)
    
    modules = [
        ("COMP 109", "Introduction to Computer Hardware", 3),
        ("PROG 102", "Principles of Software Engineering", 4),
        ("COMP 102", "Introduction to Databases", 4),
        ("DIT 1203", "Introduction to Data Communication", 3),
        ("Math 108", "Computerized Mathematics", 3),
        ("PROG 103", "Principles of Structured Programming", 3)
    ]
    
    def get_letter_grade(score):
        if score >= 90: return "A+"
        elif score >= 80: return "A"
        elif score >= 75: return "B+"
        elif score >= 70: return "B"
        elif score >= 65: return "B-"
        elif score >= 60: return "C+"
        elif score >= 55: return "C"
        elif score >= 50: return "C-"
        else: return "F"
        
    total_credits = sum(m[2] for m in modules)
    
    print("\n" + "="*80)
    print(f"{'Student Name':<19}: {student['name']}")
    print(f"{'Student ID':<19}: {student_id}")
    print(f"{'IC / Passport No.':<19}: -")
    print(f"{'Gender':<19}: -")
    print(f"{'Nationality':<19}: Sierra Leonean")
    print("\n" + f"{'Date of Admission':<19}: August 2024")
    print(f"{'Date of Completion':<19}: -")
    print(f"{'Programme':<19}: Diploma in Information Technology")
    print(f"{'Faculty':<19}: Faculty Of Information & Communication Technology")
    print(f"{'Issued Date':<19}: 02 April 2026")
    print("-" * 80)
    print(f"{'Code':<12} {'Module Name':<45} {'Credit':<8} {'Grade'}")
    print("-" * 80)
    print("Semester 03 (September 2025)")
    
    for i, mod in enumerate(modules):
        code, name, credit = mod
        grade = get_letter_grade(scores[i])
        print(f"{code:<12} {name:<45} {credit:<8} {grade}")
        
    print("\n" + f"GPA  : {gpa:<20.2f} Credits Earned     : {total_credits}")
    print(f"CGPA : {cgpa:<20.2f} Cumulative Credits : {total_credits}")
    print("\n" + f"{'Total MPU Credits':<27} : -")
    print(f"{'Total Credit Transferred':<27} : -")
    print(f"{'Total Credits Earned':<27} : {total_credits}")
    print(f"{'Total Cummulative Credits':<27} : {total_credits}")
    print("="*80)


def main():
    """Main application loop."""
    # Pre-populate demo data with 15 students
    students_db["900000001"] = {"name": "Aminata Sesay", "attendance": 95.0, "scores": [88, 92, 85, 90, 89, 94]}
    students_db["900000002"] = {"name": "Ibrahim Kamara", "attendance": 65.0, "scores": [55, 60, 45, 50, 65, 58]}
    students_db["900000003"] = {"name": "Fatmata Koroma", "attendance": 88.0, "scores": [75, 80, 82, 79, 85, 77]}
    students_db["900000004"] = {"name": "Mohamed Bangura", "attendance": 72.0, "scores": [60, 65, 70, 55, 62, 58]}
    students_db["900000005"] = {"name": "Isatu Turay", "attendance": 90.0, "scores": [95, 90, 88, 92, 89, 96]}
    students_db["900000006"] = {"name": "Abu Bakarr Mansaray", "attendance": 85.0, "scores": [78, 82, 80, 85, 79, 81]}
    students_db["900000007"] = {"name": "Kadiatu Conteh", "attendance": 92.0, "scores": [88, 85, 90, 92, 87, 89]}
    students_db["900000008"] = {"name": "Hassan Jalloh", "attendance": 50.0, "scores": [45, 50, 40, 55, 48, 52]}
    students_db["900000009"] = {"name": "Zainab Kargbo", "attendance": 80.0, "scores": [70, 75, 72, 68, 74, 71]}
    students_db["900000010"] = {"name": "Samuel Cole", "attendance": 68.0, "scores": [58, 62, 60, 55, 59, 64]}
    students_db["900000011"] = {"name": "Mariatu Kanu", "attendance": 96.0, "scores": [98, 95, 96, 92, 94, 97]}
    students_db["900000012"] = {"name": "Emmanuel Davies", "attendance": 75.0, "scores": [65, 68, 70, 62, 66, 69]}
    students_db["900000013"] = {"name": "Hawa Barrie", "attendance": 82.0, "scores": [76, 79, 81, 75, 78, 80]}
    students_db["900000014"] = {"name": "Alpha Bah", "attendance": 60.0, "scores": [50, 55, 48, 52, 50, 54]}
    students_db["900000015"] = {"name": "Fatu Sankoh", "attendance": 89.0, "scores": [85, 88, 86, 82, 84, 87]}
    
    while True:
        print("\n" + "*"*50)
        print(f"{'STUDENT RESULT & ATTENDANCE SYSTEM':^50}")
        print("*"*50)
        print("1. Add New Student")
        print("2. Input Subject Scores")
        print("3. Update or Delete Student")
        print("4. Show Student Analytics")
        print("5. View Student Transcript")
        print("6. Exit System")
        print("*"*50)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            input_scores()
        elif choice == '3':
            delete_update_student()
        elif choice == '4':
            show_analytics()
        elif choice == '5':
            view_transcript()
        elif choice == '6':
            print("\nShutting down system. Have a great day!")
            sys.exit(0)
        else:
            print("\n  [!] Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
