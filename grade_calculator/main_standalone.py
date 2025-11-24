"""
Standalone main application - Direct imports version.
Can be executed directly with: python main_standalone.py
"""
import sys
from typing import List, Optional

# Import all modules directly
class Evaluation:
    """Represents an evaluation record for a student."""

    MIN_GRADE = 0.0
    MAX_GRADE = 20.0
    DEFAULT_WEIGHT_PERCENTAGE = 100.0

    def __init__(self, student_id: str, evaluation_id: str, grade: float,
                 weight_percentage: float = DEFAULT_WEIGHT_PERCENTAGE):
        if not (self.MIN_GRADE <= grade <= self.MAX_GRADE):
            raise ValueError(
                f"Grade must be between {self.MIN_GRADE} and {self.MAX_GRADE}"
            )
        if not (0 < weight_percentage <= 100):
            raise ValueError("Weight percentage must be between 0 and 100")

        self.student_id = student_id
        self.evaluation_id = evaluation_id
        self.grade = grade
        self.weight_percentage = weight_percentage

    def get_weighted_grade(self) -> float:
        return self.grade * (self.weight_percentage / 100.0)

    def __repr__(self) -> str:
        return (
            f"Evaluation(student_id={self.student_id}, "
            f"evaluation_id={self.evaluation_id}, grade={self.grade}, "
            f"weight={self.weight_percentage}%)"
        )


class Student:
    """Represents a student in the CS-GradeCalculator system."""

    def __init__(self, student_id: str, name: str):
        self.student_id = student_id
        self.name = name
        self.evaluations: List[Evaluation] = []

    def add_evaluation(self, evaluation: Evaluation) -> None:
        if evaluation.student_id != self.student_id:
            raise ValueError(
                f"Evaluation student_id {evaluation.student_id} does not "
                f"match student {self.student_id}"
            )
        self.evaluations.append(evaluation)

    def get_evaluation_count(self) -> int:
        return len(self.evaluations)

    def get_evaluations(self) -> List[Evaluation]:
        return self.evaluations.copy()

    def __repr__(self) -> str:
        return f"Student(id={self.student_id}, name={self.name})"


class Teacher:
    """Represents a teacher in the CS-GradeCalculator system."""

    def __init__(self, teacher_id: str, name: str, course: str):
        self.teacher_id = teacher_id
        self.name = name
        self.course = course

    def __repr__(self) -> str:
        return (
            f"Teacher(id={self.teacher_id}, name={self.name}, "
            f"course={self.course})"
        )


class AttendancePolicy:
    """Defines attendance requirements for students based on academic policies."""

    def __init__(self, minimum_attendance_percentage: float = 80.0):
        if not (0 <= minimum_attendance_percentage <= 100):
            raise ValueError("Attendance percentage must be between 0 and 100")
        self.minimum_attendance_percentage = minimum_attendance_percentage

    def is_attendance_sufficient(self, attendance_percentage: float) -> bool:
        return attendance_percentage >= self.minimum_attendance_percentage

    def __repr__(self) -> str:
        return (
            f"AttendancePolicy(minimum={self.minimum_attendance_percentage}%)"
        )


class ExtraPointsPolicy:
    """Defines the policy for applying extra points to students' grades."""

    def __init__(self, extra_points_value: float = 1.0):
        if extra_points_value < 0:
            raise ValueError("Extra points value cannot be negative")
        self.extra_points_value = extra_points_value

    def apply_extra_points(self, grade: float,
                          extra_points_count: float) -> float:
        MAX_GRADE = 20.0
        result = grade + (extra_points_count * self.extra_points_value)
        return min(result, MAX_GRADE)

    def __repr__(self) -> str:
        return f"ExtraPointsPolicy(value={self.extra_points_value})"


class GradeCalculator:
    """Calculates final grades based on evaluations and policies."""

    MAX_EVALUATIONS_PER_STUDENT = 10
    MAX_GRADE = 20.0
    MIN_GRADE = 0.0
    ATTENDANCE_PENALTY_PERCENTAGE = 0.1
    MAX_CALCULATION_TIME_MS = 300

    def __init__(self, attendance_policy: AttendancePolicy = None,
                 extra_points_policy: ExtraPointsPolicy = None):
        self.attendance_policy = attendance_policy or AttendancePolicy()
        self.extra_points_policy = extra_points_policy or ExtraPointsPolicy()

    def calculate_weighted_average(self,
                                    evaluations: List[Evaluation]) -> float:
        if not evaluations:
            raise ValueError("No evaluations provided")

        if len(evaluations) > self.MAX_EVALUATIONS_PER_STUDENT:
            raise ValueError(
                f"Maximum {self.MAX_EVALUATIONS_PER_STUDENT} evaluations "
                f"allowed per student"
            )

        total_weighted = sum(e.get_weighted_grade() for e in evaluations)
        total_weight = sum(e.weight_percentage for e in evaluations)

        if total_weight == 0:
            raise ValueError("Total weight cannot be zero")

        return total_weighted / (total_weight / 100.0)

    def calculate_attendance_penalty(self, attendance_percentage: float) -> float:
        if attendance_percentage < 0 or attendance_percentage > 100:
            return 0.0

        missing_percentage = (100 - attendance_percentage) / 100.0
        penalty = missing_percentage * self.MAX_GRADE * \
                  self.ATTENDANCE_PENALTY_PERCENTAGE
        return min(penalty, self.MAX_GRADE)

    def calculate_final_grade(
        self,
        evaluations: List[Evaluation],
        attendance_percentage: float = 100.0,
        extra_points: float = 0.0,
        reached_minimum_attendance: bool = True
    ):
        weighted_avg = self.calculate_weighted_average(evaluations)
        penalty = self.calculate_attendance_penalty(attendance_percentage)

        grade_after_penalty = max(
            self.MIN_GRADE,
            weighted_avg - penalty
        )

        extra_points_applied = 0.0
        if reached_minimum_attendance:
            extra_points_applied = \
                self.extra_points_policy.apply_extra_points(
                    grade_after_penalty,
                    extra_points
                ) - grade_after_penalty

        final_grade = min(
            self.MAX_GRADE,
            grade_after_penalty + extra_points_applied
        )

        details = {
            'weighted_average': round(weighted_avg, 2),
            'attendance_percentage': attendance_percentage,
            'attendance_penalty': round(penalty, 2),
            'grade_before_extra': round(grade_after_penalty, 2),
            'extra_points_applied': round(extra_points_applied, 2),
            'final_grade': round(final_grade, 2)
        }

        return final_grade, details

    def generate_grade_report(
        self,
        student_id: str,
        student_name: str,
        evaluations: List[Evaluation],
        attendance_percentage: float = 100.0,
        extra_points: float = 0.0,
        reached_minimum_attendance: bool = True
    ) -> str:
        try:
            final_grade, details = self.calculate_final_grade(
                evaluations,
                attendance_percentage,
                extra_points,
                reached_minimum_attendance
            )

            report = [
                "=" * 60,
                "GRADE REPORT",
                "=" * 60,
                f"Student ID: {student_id}",
                f"Student Name: {student_name}",
                f"Total Evaluations: {len(evaluations)}",
                "",
                "GRADE CALCULATION BREAKDOWN:",
                f"  Weighted Average: {details['weighted_average']}",
                f"  Attendance: {details['attendance_percentage']}%",
                f"  Attendance Penalty: -{details['attendance_penalty']}",
                f"  Grade Before Extra Points: "
                f"{details['grade_before_extra']}",
                f"  Extra Points Applied: "
                f"+{details['extra_points_applied']}",
                "",
                f"FINAL GRADE: {details['final_grade']}/20",
                "=" * 60
            ]
            return "\n".join(report)
        except ValueError as e:
            return f"Error generating report: {str(e)}"


class GradeCalculatorApp:
    """Main application class for CS-GradeCalculator."""

    MAX_CONCURRENT_USERS = 50

    def __init__(self, load_sample_data=True):
        self.students = {}
        self.teachers = {}
        self.grade_calculator = GradeCalculator()
        self.all_years_teachers = []
        
        # Load sample data if requested
        if load_sample_data:
            self._initialize_sample_data()

    def add_teacher(self, teacher_id: str, name: str, course: str) -> None:
        teacher = Teacher(teacher_id, name, course)
        self.teachers[teacher_id] = teacher
        if self.should_all_years_teacher(course):
            self.all_years_teachers.append(teacher)

    def add_student(self, student_id: str, name: str) -> None:
        student = Student(student_id, name)
        self.students[student_id] = student

    def add_evaluation(self, student_id: str, evaluation_id: str,
                       grade: float, weight_percentage: float = 100.0) -> bool:
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

        student_id = input("Enter student ID/code: ").strip()

        if student_id not in self.students:
            print(f"Error: Student {student_id} not registered in system")
            return

        student = self.students[student_id]
        print(f"\nStudent found: {student.name}")

        eval_count = student.get_evaluation_count()
        if eval_count == 0:
            print("Error: Student has no evaluations registered")
            return

        print(f"Total evaluations: {eval_count}")
        print("\nEvaluations:")
        for i, eval_obj in enumerate(student.get_evaluations(), 1):
            print(f"  {i}. {eval_obj.evaluation_id}: {eval_obj.grade}/20 "
                  f"({eval_obj.weight_percentage}%)")

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

        min_attendance = self.grade_calculator.attendance_policy.\
            minimum_attendance_percentage
        reached_minimum = attendance >= min_attendance
        print(f"Minimum attendance required: {min_attendance}%")
        print(f"Reached minimum: {'YES' if reached_minimum else 'NO'}")

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

    app.run()


if __name__ == "__main__":
    main()
