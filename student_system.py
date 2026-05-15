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
    student_id = input("Enter Student ID (e.g., S001): ").strip().upper()
    
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
    """Adds multiple subject scores to a specific student."""
    print("\n--- Input Subject Scores ---")
    student_id = input("Enter Student ID: ").strip().upper()
    
    if student_id not in students_db:
        print("  [!] Error: Student not found in the database.")
        return
        
    print(f"Adding scores for {students_db[student_id]['name']}. Type '-1' to stop adding scores.")
    
    while True:
        score = get_valid_number("Enter subject score (0-100) or -1 to finish: ", float, -1, 100)
        if score == -1:
            break
        students_db[student_id]["scores"].append(score)
        print("  [+] Score recorded.")
        

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
        
        # Determine Status (Pass if CGPA >= 5.0 out of 10.0)
        status = "PASS" if cgpa >= 5.0 else "FAIL"
        
        # Limit name length for display purposes
        display_name = name[:17] + "..." if len(name) > 20 else name
        
        print(f"{sid:<10} | {display_name:<20} | {attendance:<8.1f} | {gpa:<5.1f} | {cgpa:<5.1f} | {status:<10}")
        
    print("="*70)
    print("  * GPA is based on Subject Scores (Max: 5.0)")
    print("  * CGPA = GPA + Attendance Points (Max: 10.0)")
    print("  * Pass requires a CGPA of 5.0 or higher")


def main():
    """Main application loop."""
    # Pre-populate some demo data to show off the system immediately
    students_db["S001"] = {"name": "Aminata Sesay", "attendance": 95.0, "scores": [88, 92, 85]}
    students_db["S002"] = {"name": "Ibrahim Kamara", "attendance": 65.0, "scores": [55, 60, 45]}
    
    while True:
        print("\n" + "*"*50)
        print(f"{'STUDENT RESULT & ATTENDANCE SYSTEM':^50}")
        print("*"*50)
        print("1. Add New Student")
        print("2. Input Subject Scores")
        print("3. Update or Delete Student")
        print("4. Show Student Analytics")
        print("5. Exit System")
        print("*"*50)
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            add_student()
        elif choice == '2':
            input_scores()
        elif choice == '3':
            delete_update_student()
        elif choice == '4':
            show_analytics()
        elif choice == '5':
            print("\nShutting down system. Have a great day!")
            sys.exit(0)
        else:
            print("\n  [!] Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
