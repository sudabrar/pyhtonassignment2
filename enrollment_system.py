"""
EdTech Course Enrollment System
A command-line application using OOP to manage student enrollments
"""

import json
import os

# ============================================================================
# PART 1: The Course Class
# ============================================================================

class Course:
    """
    Represents a course in the educational platform
    """
    
    def __init__(self, course_id, course_name, instructor, max_capacity):
        """
        Initialize a Course object
        
        Args:
            course_id: Unique identifier for the course
            course_name: Name of the course
            instructor: Name of the instructor
            max_capacity: Maximum number of students allowed
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.max_capacity = max_capacity
        self.enrolled_students = []  # List to store student names
    
    def add_student(self, student_name):
        """
        Add a student to the course
        
        Args:
            student_name: Name of the student to add
            
        Returns:
            Success/error message
        """
        if len(self.enrolled_students) >= self.max_capacity:
            return f"❌ Course '{self.course_name}' is full! Maximum capacity ({self.max_capacity}) reached."
        
        if student_name in self.enrolled_students:
            return f"⚠️ {student_name} is already enrolled in '{self.course_name}'."
        
        self.enrolled_students.append(student_name)
        return f"✅ {student_name} has been enrolled in '{self.course_name}'."
    
    def remove_student(self, student_name):
        """
        Remove a student from the course
        
        Args:
            student_name: Name of the student to remove
            
        Returns:
            Success/error message
        """
        if student_name not in self.enrolled_students:
            return f"❌ {student_name} is not enrolled in '{self.course_name}'."
        
        self.enrolled_students.remove(student_name)
        return f"✅ {student_name} has been removed from '{self.course_name}'."
    
    def get_availability(self):
        """
        Get the number of available seats
        
        Returns:
            Number of available seats
        """
        return self.max_capacity - len(self.enrolled_students)
    
    def display_info(self):
        """Display course information"""
        print(f"\n{'='*50}")
        print(f"Course ID: {self.course_id}")
        print(f"Course Name: {self.course_name}")
        print(f"Instructor: {self.instructor}")
        print(f"Capacity: {len(self.enrolled_students)}/{self.max_capacity}")
        print(f"Available Seats: {self.get_availability()}")
        print(f"Enrolled Students: {', '.join(self.enrolled_students) if self.enrolled_students else 'None'}")
        print(f"{'='*50}")


# ============================================================================
# PART 2: The Student Class
# ============================================================================

class Student:
    """
    Represents a student in the educational platform
    """
    
    def __init__(self, student_id, name):
        """
        Initialize a Student object
        
        Args:
            student_id: Unique identifier for the student
            name: Name of the student
        """
        self.student_id = student_id
        self.name = name
        self.enrolled_courses = []  # List of Course objects
    
    def enroll(self, course_object):
        """
        Enroll the student in a course
        
        Args:
            course_object: Course object to enroll in
            
        Returns:
            Success/error message
        """
        # Check if already enrolled
        if course_object in self.enrolled_courses:
            return f"⚠️ {self.name} is already enrolled in '{course_object.course_name}'."
        
        # Try to add student to course
        result = course_object.add_student(self.name)
        
        # If successful, add course to student's list
        if "✅" in result:
            self.enrolled_courses.append(course_object)
        
        return result
    
    def drop_course(self, course_object):
        """
        Drop a course
        
        Args:
            course_object: Course object to drop
            
        Returns:
            Success/error message
        """
        # Try to remove student from course
        result = course_object.remove_student(self.name)
        
        # If successful, remove course from student's list
        if "✅" in result and course_object in self.enrolled_courses:
            self.enrolled_courses.remove(course_object)
        
        return result
    
    def view_courses(self):
        """Display all enrolled courses"""
        if not self.enrolled_courses:
            print(f"\n📚 {self.name} is not enrolled in any courses.")
            return
        
        print(f"\n{'='*50}")
        print(f"📚 {self.name}'s Enrolled Courses:")
        print(f"{'='*50}")
        for i, course in enumerate(self.enrolled_courses, 1):
            print(f"{i}. {course.course_name} (ID: {course.course_id}) - Instructor: {course.instructor}")
        print(f"{'='*50}")


# ============================================================================
# BONUS: PremiumStudent Class (Inheritance)
# ============================================================================

class PremiumStudent(Student):
    """
    Premium student that can bypass course capacity limits
    Inherits from Student class
    """
    
    def __init__(self, student_id, name, membership_level="Gold"):
        """
        Initialize a PremiumStudent object
        
        Args:
            student_id: Unique identifier for the student
            name: Name of the student
            membership_level: Premium membership level
        """
        super().__init__(student_id, name)
        self.membership_level = membership_level
        self.is_premium = True
    
    def enroll(self, course_object):
        """
        Override enroll method to bypass capacity limits
        
        Args:
            course_object: Course object to enroll in
            
        Returns:
            Success/error message
        """
        # Check if already enrolled
        if course_object in self.enrolled_courses:
            return f"⚠️ {self.name} is already enrolled in '{course_object.course_name}'."
        
        # Check if course is full
        if len(course_object.enrolled_students) >= course_object.max_capacity:
            # Premium students can bypass capacity
            if self.name not in course_object.enrolled_students:
                course_object.enrolled_students.append(self.name)
                self.enrolled_courses.append(course_object)
                return f"✅ PREMIUM: {self.name} has been enrolled in '{course_object.course_name}' (Bypassed capacity limit!)."
        else:
            # Normal enrollment
            result = course_object.add_student(self.name)
            if "✅" in result:
                self.enrolled_courses.append(course_object)
            return result


# ============================================================================
# PART 3: Main Application
# ============================================================================

class EnrollmentSystem:
    """
    Main enrollment system to manage courses and students
    """
    
    def __init__(self):
        """Initialize the enrollment system"""
        self.courses = {}  # Dictionary to store Course objects
        self.students = {}  # Dictionary to store Student objects
    
    def create_course(self):
        """Create a new course"""
        print("\n" + "="*50)
        print("📝 CREATE NEW COURSE")
        print("="*50)
        
        try:
            course_id = input("Enter Course ID: ").strip()
            
            # Check if course ID already exists
            if course_id in self.courses:
                print(f"❌ Course with ID '{course_id}' already exists!")
                return
            
            course_name = input("Enter Course Name: ").strip()
            instructor = input("Enter Instructor Name: ").strip()
            max_capacity = int(input("Enter Maximum Capacity: "))
            
            if max_capacity <= 0:
                print("❌ Capacity must be greater than 0!")
                return
            
            # Create and store course
            course = Course(course_id, course_name, instructor, max_capacity)
            self.courses[course_id] = course
            
            print(f"\n✅ Course '{course_name}' created successfully!")
            course.display_info()
            
        except ValueError:
            print("❌ Invalid input! Capacity must be a number.")
    
    def register_student(self):
        """Register a new student"""
        print("\n" + "="*50)
        print("👤 REGISTER NEW STUDENT")
        print("="*50)
        
        try:
            student_id = input("Enter Student ID: ").strip()
            
            # Check if student ID already exists
            if student_id in self.students:
                print(f"❌ Student with ID '{student_id}' already exists!")
                return
            
            name = input("Enter Student Name: ").strip()
            
            # Ask if premium student
            is_premium = input("Premium Student? (y/n): ").strip().lower()
            
            if is_premium == 'y':
                membership = input("Enter Membership Level (Gold/Silver/Platinum): ").strip()
                student = PremiumStudent(student_id, name, membership)
                print(f"\n✅ Premium Student '{name}' registered with {membership} membership!")
            else:
                student = Student(student_id, name)
                print(f"\n✅ Student '{name}' registered successfully!")
            
            self.students[student_id] = student
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def enroll_student_in_course(self):
        """Enroll a student in a course"""
        print("\n" + "="*50)
        print("📋 ENROLL STUDENT IN COURSE")
        print("="*50)
        
        # Check if there are students and courses
        if not self.students:
            print("❌ No students registered yet!")
            return
        
        if not self.courses:
            print("❌ No courses created yet!")
            return
        
        try:
            student_id = input("Enter Student ID: ").strip()
            
            if student_id not in self.students:
                print(f"❌ Student with ID '{student_id}' not found!")
                return
            
            course_id = input("Enter Course ID: ").strip()
            
            if course_id not in self.courses:
                print(f"❌ Course with ID '{course_id}' not found!")
                return
            
            student = self.students[student_id]
            course = self.courses[course_id]
            
            # Enroll student
            result = student.enroll(course)
            print(f"\n{result}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def view_student_courses(self):
        """View a student's enrolled courses"""
        print("\n" + "="*50)
        print("📚 VIEW STUDENT'S COURSES")
        print("="*50)
        
        if not self.students:
            print("❌ No students registered yet!")
            return
        
        try:
            student_id = input("Enter Student ID: ").strip()
            
            if student_id not in self.students:
                print(f"❌ Student with ID '{student_id}' not found!")
                return
            
            student = self.students[student_id]
            student.view_courses()
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def display_all_courses(self):
        """Display all available courses"""
        print("\n" + "="*50)
        print("📚 ALL AVAILABLE COURSES")
        print("="*50)
        
        if not self.courses:
            print("No courses available.")
            return
        
        for course in self.courses.values():
            course.display_info()
    
    def display_all_students(self):
        """Display all registered students"""
        print("\n" + "="*50)
        print("👥 ALL REGISTERED STUDENTS")
        print("="*50)
        
        if not self.students:
            print("No students registered.")
            return
        
        for student in self.students.values():
            print(f"\nID: {student.student_id}")
            print(f"Name: {student.name}")
            if hasattr(student, 'is_premium'):
                print(f"Type: Premium Student ({student.membership_level})")
            else:
                print("Type: Regular Student")
            print(f"Courses Enrolled: {len(student.enrolled_courses)}")
    
    def save_data(self):
        """Save courses and students to a JSON file"""
        data = {
            "courses": {},
            "students": {}
        }
        
        # Save courses
        for course_id, course in self.courses.items():
            data["courses"][course_id] = {
                "course_name": course.course_name,
                "instructor": course.instructor,
                "max_capacity": course.max_capacity,
                "enrolled_students": course.enrolled_students
            }
        
        # Save students
        for student_id, student in self.students.items():
            student_data = {
                "name": student.name,
                "enrolled_courses": [c.course_id for c in student.enrolled_courses]
            }
            
            if hasattr(student, 'is_premium'):
                student_data["is_premium"] = True
                student_data["membership_level"] = student.membership_level
            
            data["students"][student_id] = student_data
        
        try:
            with open("enrollment_data.json", "w") as file:
                json.dump(data, file, indent=4)
            print("✅ Data saved to 'enrollment_data.json'")
        except Exception as e:
            print(f"❌ Error saving data: {e}")
    
    def load_data(self):
        """Load courses and students from a JSON file"""
        if not os.path.exists("enrollment_data.json"):
            return
        
        try:
            with open("enrollment_data.json", "r") as file:
                data = json.load(file)
            
            # Load courses
            for course_id, course_data in data["courses"].items():
                course = Course(
                    course_id,
                    course_data["course_name"],
                    course_data["instructor"],
                    course_data["max_capacity"]
                )
                course.enrolled_students = course_data["enrolled_students"]
                self.courses[course_id] = course
            
            # Load students
            for student_id, student_data in data["students"].items():
                if student_data.get("is_premium"):
                    student = PremiumStudent(
                        student_id,
                        student_data["name"],
                        student_data.get("membership_level", "Gold")
                    )
                else:
                    student = Student(student_id, student_data["name"])
                
                # Re-enroll in courses
                for course_id in student_data["enrolled_courses"]:
                    if course_id in self.courses:
                        student.enrolled_courses.append(self.courses[course_id])
                
                self.students[student_id] = student
            
            print("✅ Data loaded from 'enrollment_data.json'")
        except Exception as e:
            print(f"⚠️ Could not load saved data: {e}")


def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("🎓 EDTECH COURSE ENROLLMENT SYSTEM")
    print("="*50)
    print("1. 📝 Create a New Course")
    print("2. 👤 Register a New Student")
    print("3. 📋 Enroll a Student in a Course")
    print("4. 📚 View Student's Enrolled Courses")
    print("5. 📖 View All Courses")
    print("6. 👥 View All Students")
    print("7. 💾 Save Data to File")
    print("8. 🚪 Exit")
    print("="*50)


def main():
    """Main program loop"""
    system = EnrollmentSystem()
    
    # Load saved data if available
    system.load_data()
    
    while True:
        display_menu()
        
        try:
            choice = int(input("\nEnter your choice (1-8): "))
            
            if choice == 1:
                system.create_course()
            elif choice == 2:
                system.register_student()
            elif choice == 3:
                system.enroll_student_in_course()
            elif choice == 4:
                system.view_student_courses()
            elif choice == 5:
                system.display_all_courses()
            elif choice == 6:
                system.display_all_students()
            elif choice == 7:
                system.save_data()
            elif choice == 8:
                # Auto-save before exiting
                print("\n💾 Saving data before exit...")
                system.save_data()
                print("\n👋 Thank you for using the EdTech Enrollment System!")
                print("Goodbye!\n")
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1 and 8.")
            
            input("\nPress Enter to continue...")
            
        except ValueError:
            print("❌ Invalid input! Please enter a number.")
            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n\n👋 Program interrupted. Goodbye!\n")
            break
        except Exception as e:
            print(f"❌ An error occurred: {e}")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
