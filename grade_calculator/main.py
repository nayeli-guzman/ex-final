"""
Main module for CS-GradeCalculator application.

This module provides the terminal-based interface for the grade calculator
system. Implements use case CU001: Calculate student's final grade.
"""
import sys
from typing import List, Optional

# Support both direct execution and package imports
try:
    from .student import Student
    from .teacher import Teacher
    from .evaluation import Evaluation
    from .grade_calculator import GradeCalculator
    from .attendance_policy import AttendancePolicy
    from .extra_points_policy import ExtraPointsPolicy
except (ImportError, ValueError):
    from student import Student
    from teacher import Teacher
    from evaluation import Evaluation
    from grade_calculator import GradeCalculator
    from attendance_policy import AttendancePolicy
    from extra_points_policy import ExtraPointsPolicy


class GradeCalculatorApp:
    """Main application class for CS-GradeCalculator."""

    # Class-level configuration for concurrent users (RNF02)
    MAX_CONCURRENT_USERS = 50

    def __init__(self, load_sample_data=True):
        """Initialize the Grade Calculator application.
        
        Args:
            load_sample_data: Whether to load sample data on initialization
        """
        self.students = {}
        self.teachers = {}
        self.grade_calculator = GradeCalculator()
        self.all_years_teachers = []
        
        # Load sample data if requested
        if load_sample_data:
            self._initialize_sample_data()

    def add_teacher(self, teacher_id: str, name: str, course: str) -> None:
        """
        Add a teacher to the system.

        Args:
            teacher_id: Unique identifier for the teacher
            name: Teacher's full name
            course: Course taught by the teacher
        """
        teacher = Teacher(teacher_id, name, course)
        self.teachers[teacher_id] = teacher
        if self.should_all_years_teacher(course):
            self.all_years_teachers.append(teacher)

    def add_student(self, student_id: str, name: str) -> None:
        """
        Add a student to the system.

        Args:
            student_id: Unique identifier for the student
            name: Student's full name
        """
        student = Student(student_id, name)
        self.students[student_id] = student

    def add_evaluation(self, student_id: str, evaluation_id: str,
                       grade: float, weight_percentage: float = 100.0) -> bool:
        """
        Add an evaluation for a student.

        Args:
            student_id: The student identifier
            evaluation_id: Unique identifier for the evaluation
            grade: Grade obtained (0-20)
            weight_percentage: Weight of the evaluation

        Returns:
            True if successful, False otherwise
        """
        try:
            if student_id not in self.students:
                print(f"Error: Student {student_id} not found")
                return False

            evaluation = Evaluation(student_id, evaluation_id, grade,
                                   weight_percentage)
            self.students[student_id].add_evaluation(evaluation)
            return True
        except ValueError as e:
            print(f"Error adding evaluation: {str(e)}")
            return False

    def should_all_years_teacher(self, course: str) -> bool:
        """
        Determine if a teacher teaches across all academic years.

        Args:
            course: The course name

        Returns:
            True if teacher is an all-years teacher
        """
        return "ALL YEARS" in course.upper()

    def _initialize_sample_data(self) -> None:
        """Initialize the application with sample data."""
        # Add sample teacher
        self.add_teacher("T001", "Dr. Juan Pérez", "Software Engineering "
                        "All Years")

        # Add sample students
        self.add_student("S001", "María García")
        self.add_student("S002", "Carlos López")
        self.add_student("S003", "Ana Martínez")

        # Add evaluations
        self.add_evaluation("S001", "E001", 15.5, 30.0)
        self.add_evaluation("S001", "E002", 17.0, 40.0)
        self.add_evaluation("S001", "E003", 16.0, 30.0)

        self.add_evaluation("S002", "E001", 18.0, 30.0)
        self.add_evaluation("S002", "E002", 19.0, 40.0)
        self.add_evaluation("S002", "E003", 17.5, 30.0)

        self.add_evaluation("S003", "E001", 12.0, 30.0)
        self.add_evaluation("S003", "E002", 11.5, 40.0)
        self.add_evaluation("S003", "E003", 13.0, 30.0)

    def get_student_final_grade(self, student_id: str,
                                attendance_percentage: float = 100.0,
                                extra_points: float = 0.0,
                                reached_minimum_attendance: bool = True
                                ) -> Optional[tuple]:
        """
        Calculate final grade for a student.

        Args:
            student_id: The student identifier
            attendance_percentage: Student's attendance percentage
            extra_points: Number of extra points earned
            reached_minimum_attendance: Whether student reached minimum
                                       attendance requirements

        Returns:
            Tuple of (final_grade, details) or None if student not found
        """
        if student_id not in self.students:
            print(f"Error: Student {student_id} not found")
            return None

        student = self.students[student_id]
        if not student.get_evaluations():
            print(f"Error: Student {student_id} has no evaluations")
            return None

        final_grade, details = self.grade_calculator.calculate_final_grade(
            student.get_evaluations(),
            attendance_percentage,
            extra_points,
            reached_minimum_attendance
        )
        return final_grade, details

    def display_grade_report(self, student_id: str,
                            attendance_percentage: float = 100.0,
                            extra_points: float = 0.0,
                            reached_minimum_attendance: bool = True) -> None:
        """
        Display grade report for a student in the terminal.

        Args:
            student_id: The student identifier
            attendance_percentage: Student's attendance percentage
            extra_points: Number of extra points earned
            reached_minimum_attendance: Whether student reached minimum
                                       attendance
        """
        if student_id not in self.students:
            print(f"Error: Student {student_id} not found")
            return

        student = self.students[student_id]
        if not student.get_evaluations():
            print(f"Error: Student {student_id} has no evaluations")
            return

        report = self.grade_calculator.generate_grade_report(
            student_id,
            student.name,
            student.get_evaluations(),
            attendance_percentage,
            extra_points,
            reached_minimum_attendance
        )
        print(report)

    def interactive_terminal_mode(self) -> None:
        """Run the application in interactive terminal mode."""
        print("\n" + "=" * 60)
        print("CS-GRADECALCULATOR - Use Case CU001")
        print("Calculate Student Final Grade")
        print("=" * 60 + "\n")

        # Step 1: Get student information
        student_id = input("Enter student ID/code: ").strip()

        if student_id not in self.students:
            print(f"Error: Student {student_id} not registered in system")
            return

        student = self.students[student_id]
        print(f"\nStudent found: {student.name}")

        # Step 2: Get student evaluations
        eval_count = student.get_evaluation_count()
        if eval_count == 0:
            print("Error: Student has no evaluations registered")
            return

        print(f"Total evaluations: {eval_count}")
        print("\nEvaluations:")
        for i, eval_obj in enumerate(student.get_evaluations(), 1):
            print(f"  {i}. {eval_obj.evaluation_id}: {eval_obj.grade}/20 "
                  f"({eval_obj.weight_percentage}%)")

        # Step 3: Get attendance information
        attendance_str = input(
            "\nEnter student attendance percentage (0-100): "
        ).strip()
        try:
            attendance = float(attendance_str)
            if not (0 <= attendance <= 100):
                raise ValueError("Attendance must be between 0 and 100")
        except ValueError as e:
            print(f"Error: Invalid attendance value - {str(e)}")
            return

        # Step 4: Check minimum attendance (RNF02)
        min_attendance = self.grade_calculator.attendance_policy.\
            minimum_attendance_percentage
        reached_minimum = attendance >= min_attendance
        print(f"Minimum attendance required: {min_attendance}%")
        print(f"Reached minimum: {'YES' if reached_minimum else 'NO'}")

        # Step 5: Get extra points
        extra_points_str = input(
            "\nEnter extra points earned (0 or more): "
        ).strip()
        try:
            extra_points = float(extra_points_str)
            if extra_points < 0:
                raise ValueError("Extra points cannot be negative")
        except ValueError as e:
            print(f"Error: Invalid extra points - {str(e)}")
            return

        # Step 6: Calculate and display final grade
        print("\n" + "-" * 60)
        self.display_grade_report(
            student_id,
            attendance,
            extra_points,
            reached_minimum
        )

    def print_menu(self) -> None:
        """Print the main menu options."""
        print("\n" + "=" * 60)
        print("CS-GRADECALCULATOR MAIN MENU")
        print("=" * 60)
        print("1. Use Case CU001: Calculate student final grade (interactive)")
        print("2. Add student")
        print("3. Add evaluation")
        print("4. View student information")
        print("5. Exit")
        print("-" * 60)

    def run(self) -> None:
        """Run the application main loop."""
        while True:
            self.print_menu()
            choice = input("Select an option (1-5): ").strip()

            if choice == "1":
                self.interactive_terminal_mode()
            elif choice == "2":
                self.menu_add_student()
            elif choice == "3":
                self.menu_add_evaluation()
            elif choice == "4":
                self.menu_view_student()
            elif choice == "5":
                print("\nGoodbye!")
                break
            else:
                print("Error: Invalid option. Please select 1-5.")

    def menu_add_student(self) -> None:
        """Menu option to add a student."""
        student_id = input("Enter student ID: ").strip()
        student_name = input("Enter student name: ").strip()

        if not student_id or not student_name:
            print("Error: Student ID and name cannot be empty")
            return

        if student_id in self.students:
            print(f"Error: Student {student_id} already exists")
            return

        self.add_student(student_id, student_name)
        print(f"Student {student_name} ({student_id}) added successfully")

    def menu_add_evaluation(self) -> None:
        """Menu option to add an evaluation."""
        student_id = input("Enter student ID: ").strip()

        if student_id not in self.students:
            print(f"Error: Student {student_id} not found")
            return

        eval_id = input("Enter evaluation ID: ").strip()

        try:
            grade_str = input("Enter grade (0-20): ").strip()
            grade = float(grade_str)

            weight_str = input("Enter weight percentage (default 100): ")\
                .strip() or "100"
            weight = float(weight_str)

            if self.add_evaluation(student_id, eval_id, grade, weight):
                print("Evaluation added successfully")
            else:
                print("Failed to add evaluation")
        except ValueError as e:
            print(f"Error: Invalid input - {str(e)}")

    def menu_view_student(self) -> None:
        """Menu option to view student information."""
        student_id = input("Enter student ID: ").strip()

        if student_id not in self.students:
            print(f"Error: Student {student_id} not found")
            return

        student = self.students[student_id]
        print(f"\nStudent: {student.name} (ID: {student_id})")
        print(f"Evaluations: {student.get_evaluation_count()}")

        if student.get_evaluations():
            print("\nEvaluation details:")
            for eval_obj in student.get_evaluations():
                print(f"  - {eval_obj.evaluation_id}: {eval_obj.grade}/20 "
                      f"(Weight: {eval_obj.weight_percentage}%)")


def main():
    """Main entry point for the application."""
    app = GradeCalculatorApp(load_sample_data=True)

    print("Sample data loaded successfully!\n")

    # Run the application
    app.run()


if __name__ == "__main__":
    main()
