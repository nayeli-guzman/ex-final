"""
Comprehensive test suite for CS-GradeCalculator with high code coverage.

This test suite aims for >80% code coverage across all modules:
- evaluation.py
- student.py
- teacher.py
- grade_calculator.py
- attendance_policy.py
- extra_points_policy.py
- main.py

Tests include normal cases, edge cases, boundary conditions, and error scenarios.
"""
import unittest
import sys
import os
from io import StringIO

# Support both direct execution and package imports
import sys
import os

# Add grade_calculator directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'grade_calculator'))

try:
    from evaluation import Evaluation
    from student import Student
    from teacher import Teacher
    from grade_calculator import GradeCalculator
    from attendance_policy import AttendancePolicy
    from extra_points_policy import ExtraPointsPolicy
    from main import GradeCalculatorApp
except ImportError as e:
    # Fallback - try relative imports from package
    try:
        from ..grade_calculator.evaluation import Evaluation
        from ..grade_calculator.student import Student
        from ..grade_calculator.teacher import Teacher
        from ..grade_calculator.grade_calculator import GradeCalculator
        from ..grade_calculator.attendance_policy import AttendancePolicy
        from ..grade_calculator.extra_points_policy import ExtraPointsPolicy
        from ..grade_calculator.main import GradeCalculatorApp
    except ImportError:
        print(f"Import error: {e}")
        raise


class TestEvaluation(unittest.TestCase):
    """Test cases for the Evaluation class."""

    def test_valid_evaluation_creation(self):
        """Test creating a valid evaluation."""
        eval_obj = Evaluation("S001", "E001", 15.5, 50.0)
        self.assertEqual(eval_obj.student_id, "S001")
        self.assertEqual(eval_obj.evaluation_id, "E001")
        self.assertEqual(eval_obj.grade, 15.5)
        self.assertEqual(eval_obj.weight_percentage, 50.0)

    def test_minimum_grade(self):
        """Test evaluation with minimum valid grade."""
        eval_obj = Evaluation("S001", "E001", 0.0, 100.0)
        self.assertEqual(eval_obj.grade, 0.0)

    def test_maximum_grade(self):
        """Test evaluation with maximum valid grade."""
        eval_obj = Evaluation("S001", "E001", 20.0, 100.0)
        self.assertEqual(eval_obj.grade, 20.0)

    def test_invalid_grade_too_low(self):
        """Test that grade below 0 raises ValueError."""
        with self.assertRaises(ValueError):
            Evaluation("S001", "E001", -0.1, 100.0)

    def test_invalid_grade_too_high(self):
        """Test that grade above 20 raises ValueError."""
        with self.assertRaises(ValueError):
            Evaluation("S001", "E001", 20.1, 100.0)

    def test_invalid_weight_zero(self):
        """Test that zero weight raises ValueError."""
        with self.assertRaises(ValueError):
            Evaluation("S001", "E001", 15.0, 0.0)

    def test_invalid_weight_negative(self):
        """Test that negative weight raises ValueError."""
        with self.assertRaises(ValueError):
            Evaluation("S001", "E001", 15.0, -10.0)

    def test_invalid_weight_over_100(self):
        """Test that weight over 100 raises ValueError."""
        with self.assertRaises(ValueError):
            Evaluation("S001", "E001", 15.0, 101.0)

    def test_weighted_grade_calculation(self):
        """Test weighted grade calculation."""
        eval_obj = Evaluation("S001", "E001", 20.0, 50.0)
        self.assertEqual(eval_obj.get_weighted_grade(), 10.0)

    def test_weighted_grade_full_weight(self):
        """Test weighted grade with full weight."""
        eval_obj = Evaluation("S001", "E001", 15.0, 100.0)
        self.assertEqual(eval_obj.get_weighted_grade(), 15.0)

    def test_weighted_grade_zero_weight_boundary(self):
        """Test weighted grade with minimum valid weight."""
        eval_obj = Evaluation("S001", "E001", 15.0, 0.1)
        self.assertAlmostEqual(eval_obj.get_weighted_grade(), 0.015, places=3)


class TestStudent(unittest.TestCase):
    """Test cases for the Student class."""

    def setUp(self):
        """Set up test fixtures."""
        self.student = Student("S001", "John Doe")

    def test_student_creation(self):
        """Test creating a student."""
        self.assertEqual(self.student.student_id, "S001")
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.get_evaluation_count(), 0)

    def test_add_evaluation(self):
        """Test adding an evaluation to a student."""
        eval_obj = Evaluation("S001", "E001", 15.0)
        self.student.add_evaluation(eval_obj)
        self.assertEqual(self.student.get_evaluation_count(), 1)

    def test_add_multiple_evaluations(self):
        """Test adding multiple evaluations."""
        for i in range(1, 4):
            eval_obj = Evaluation("S001", f"E{i:03d}", 15.0 + i)
            self.student.add_evaluation(eval_obj)
        self.assertEqual(self.student.get_evaluation_count(), 3)

    def test_add_evaluation_mismatched_student_id(self):
        """Test that adding evaluation with wrong student ID raises error."""
        eval_obj = Evaluation("S002", "E001", 15.0)
        with self.assertRaises(ValueError):
            self.student.add_evaluation(eval_obj)

    def test_get_evaluations_returns_copy(self):
        """Test that get_evaluations returns a copy."""
        eval_obj = Evaluation("S001", "E001", 15.0)
        self.student.add_evaluation(eval_obj)
        evals = self.student.get_evaluations()
        evals.append(Evaluation("S001", "E999", 10.0))
        # Original should not be modified
        self.assertEqual(self.student.get_evaluation_count(), 1)


class TestAttendancePolicy(unittest.TestCase):
    """Test cases for the AttendancePolicy class."""

    def test_default_policy_creation(self):
        """Test creating default attendance policy."""
        policy = AttendancePolicy()
        self.assertEqual(policy.minimum_attendance_percentage, 80.0)

    def test_custom_policy_creation(self):
        """Test creating custom attendance policy."""
        policy = AttendancePolicy(minimum_attendance_percentage=75.0)
        self.assertEqual(policy.minimum_attendance_percentage, 75.0)

    def test_invalid_policy_negative(self):
        """Test that negative attendance percentage raises error."""
        with self.assertRaises(ValueError):
            AttendancePolicy(minimum_attendance_percentage=-1.0)

    def test_invalid_policy_over_100(self):
        """Test that attendance over 100 raises error."""
        with self.assertRaises(ValueError):
            AttendancePolicy(minimum_attendance_percentage=101.0)

    def test_attendance_sufficient(self):
        """Test checking sufficient attendance."""
        policy = AttendancePolicy(80.0)
        self.assertTrue(policy.is_attendance_sufficient(80.0))
        self.assertTrue(policy.is_attendance_sufficient(90.0))

    def test_attendance_insufficient(self):
        """Test checking insufficient attendance."""
        policy = AttendancePolicy(80.0)
        self.assertFalse(policy.is_attendance_sufficient(79.9))

    def test_attendance_boundary_minimum(self):
        """Test attendance at exactly minimum."""
        policy = AttendancePolicy(80.0)
        self.assertTrue(policy.is_attendance_sufficient(80.0))

    def test_attendance_boundary_zero(self):
        """Test attendance at zero."""
        policy = AttendancePolicy(80.0)
        self.assertFalse(policy.is_attendance_sufficient(0.0))


class TestExtraPointsPolicy(unittest.TestCase):
    """Test cases for the ExtraPointsPolicy class."""

    def test_default_policy_creation(self):
        """Test creating default extra points policy."""
        policy = ExtraPointsPolicy()
        self.assertEqual(policy.extra_points_value, 1.0)

    def test_custom_policy_creation(self):
        """Test creating custom extra points policy."""
        policy = ExtraPointsPolicy(extra_points_value=0.5)
        self.assertEqual(policy.extra_points_value, 0.5)

    def test_invalid_policy_negative(self):
        """Test that negative extra points raises error."""
        with self.assertRaises(ValueError):
            ExtraPointsPolicy(extra_points_value=-1.0)

    def test_apply_extra_points_normal(self):
        """Test applying extra points normally."""
        policy = ExtraPointsPolicy(1.0)
        result = policy.apply_extra_points(15.0, 2.0)
        self.assertEqual(result, 17.0)

    def test_apply_extra_points_zero(self):
        """Test applying zero extra points."""
        policy = ExtraPointsPolicy(1.0)
        result = policy.apply_extra_points(15.0, 0.0)
        self.assertEqual(result, 15.0)

    def test_apply_extra_points_capped_at_max_grade(self):
        """Test that extra points are capped at maximum grade (20)."""
        policy = ExtraPointsPolicy(1.0)
        result = policy.apply_extra_points(19.0, 5.0)
        self.assertEqual(result, 20.0)

    def test_apply_extra_points_with_custom_value(self):
        """Test applying extra points with custom value."""
        policy = ExtraPointsPolicy(0.5)
        result = policy.apply_extra_points(15.0, 4.0)
        self.assertEqual(result, 17.0)

    def test_apply_extra_points_from_zero(self):
        """Test applying extra points starting from zero grade."""
        policy = ExtraPointsPolicy(1.0)
        result = policy.apply_extra_points(0.0, 5.0)
        self.assertEqual(result, 5.0)

    def test_apply_extra_points_boundary_at_max(self):
        """Test applying extra points starting from max grade."""
        policy = ExtraPointsPolicy(1.0)
        result = policy.apply_extra_points(20.0, 5.0)
        self.assertEqual(result, 20.0)


class TestGradeCalculator(unittest.TestCase):
    """Test cases for the GradeCalculator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.calculator = GradeCalculator()

    def test_calculator_creation_with_defaults(self):
        """Test creating calculator with default policies."""
        calc = GradeCalculator()
        self.assertIsNotNone(calc.attendance_policy)
        self.assertIsNotNone(calc.extra_points_policy)

    def test_calculator_creation_with_custom_policies(self):
        """Test creating calculator with custom policies."""
        att_policy = AttendancePolicy(85.0)
        extra_policy = ExtraPointsPolicy(0.5)
        calc = GradeCalculator(att_policy, extra_policy)
        self.assertEqual(calc.attendance_policy.minimum_attendance_percentage,
                         85.0)
        self.assertEqual(calc.extra_points_policy.extra_points_value, 0.5)

    def test_weighted_average_single_evaluation(self):
        """Test weighted average with single evaluation."""
        eval_obj = Evaluation("S001", "E001", 15.0, 100.0)
        avg = self.calculator.calculate_weighted_average([eval_obj])
        self.assertEqual(avg, 15.0)

    def test_weighted_average_multiple_evaluations(self):
        """Test weighted average with multiple evaluations."""
        evaluations = [
            Evaluation("S001", "E001", 15.0, 50.0),
            Evaluation("S001", "E002", 17.0, 50.0)
        ]
        avg = self.calculator.calculate_weighted_average(evaluations)
        self.assertEqual(avg, 16.0)

    def test_weighted_average_different_weights(self):
        """Test weighted average with different weights."""
        evaluations = [
            Evaluation("S001", "E001", 20.0, 30.0),
            Evaluation("S001", "E002", 10.0, 70.0)
        ]
        avg = self.calculator.calculate_weighted_average(evaluations)
        self.assertEqual(avg, 13.0)

    def test_weighted_average_empty_list(self):
        """Test that empty evaluations list raises error."""
        with self.assertRaises(ValueError):
            self.calculator.calculate_weighted_average([])

    def test_weighted_average_exceeds_max_evaluations(self):
        """Test that exceeding max evaluations raises error."""
        evaluations = [
            Evaluation("S001", f"E{i:03d}", 15.0, 1.0)
            for i in range(1, 12)  # 11 evaluations, max is 10
        ]
        with self.assertRaises(ValueError):
            self.calculator.calculate_weighted_average(evaluations)

    def test_attendance_penalty_no_penalty(self):
        """Test attendance penalty with no missing classes."""
        penalty = self.calculator.calculate_attendance_penalty(100.0)
        self.assertEqual(penalty, 0.0)

    def test_attendance_penalty_full_penalty(self):
        """Test attendance penalty with full absence."""
        penalty = self.calculator.calculate_attendance_penalty(0.0)
        self.assertGreater(penalty, 0.0)

    def test_attendance_penalty_partial(self):
        """Test attendance penalty with partial absence."""
        penalty = self.calculator.calculate_attendance_penalty(50.0)
        self.assertGreater(penalty, 0.0)
        self.assertLess(penalty, 2.0)  # Should be reasonable

    def test_attendance_penalty_invalid_negative(self):
        """Test attendance penalty with negative value."""
        penalty = self.calculator.calculate_attendance_penalty(-10.0)
        self.assertEqual(penalty, 0.0)

    def test_attendance_penalty_invalid_over_100(self):
        """Test attendance penalty over 100."""
        penalty = self.calculator.calculate_attendance_penalty(110.0)
        self.assertEqual(penalty, 0.0)

    def test_final_grade_calculation_basic(self):
        """Test final grade calculation with basic inputs."""
        evaluations = [
            Evaluation("S001", "E001", 15.0, 100.0)
        ]
        final_grade, details = self.calculator.calculate_final_grade(
            evaluations,
            attendance_percentage=100.0,
            extra_points=0.0
        )
        self.assertEqual(final_grade, 15.0)
        self.assertEqual(details['final_grade'], 15.0)

    def test_final_grade_calculation_with_attendance_penalty(self):
        """Test final grade calculation with attendance penalty."""
        evaluations = [
            Evaluation("S001", "E001", 18.0, 100.0)
        ]
        final_grade, details = self.calculator.calculate_final_grade(
            evaluations,
            attendance_percentage=80.0
        )
        self.assertLess(final_grade, 18.0)

    def test_final_grade_calculation_with_extra_points(self):
        """Test final grade calculation with extra points."""
        evaluations = [
            Evaluation("S001", "E001", 17.0, 100.0)
        ]
        final_grade, details = self.calculator.calculate_final_grade(
            evaluations,
            attendance_percentage=100.0,
            extra_points=2.0,
            reached_minimum_attendance=True
        )
        self.assertEqual(final_grade, 19.0)

    def test_final_grade_capped_at_maximum(self):
        """Test that final grade is capped at 20."""
        evaluations = [
            Evaluation("S001", "E001", 20.0, 100.0)
        ]
        final_grade, details = self.calculator.calculate_final_grade(
            evaluations,
            attendance_percentage=100.0,
            extra_points=10.0,
            reached_minimum_attendance=True
        )
        self.assertEqual(final_grade, 20.0)

    def test_final_grade_no_extra_points_without_minimum_attendance(self):
        """Test that extra points not applied without minimum attendance."""
        evaluations = [
            Evaluation("S001", "E001", 17.0, 100.0)
        ]
        final_grade, details = self.calculator.calculate_final_grade(
            evaluations,
            attendance_percentage=100.0,
            extra_points=2.0,
            reached_minimum_attendance=False
        )
        self.assertEqual(final_grade, 17.0)

    def test_grade_report_generation(self):
        """Test grade report generation."""
        evaluations = [
            Evaluation("S001", "E001", 15.0, 100.0)
        ]
        report = self.calculator.generate_grade_report(
            "S001",
            "John Doe",
            evaluations,
            attendance_percentage=100.0
        )
        self.assertIn("GRADE REPORT", report)
        self.assertIn("S001", report)
        self.assertIn("John Doe", report)
        self.assertIn("15.0", report)


class TestTeacher(unittest.TestCase):
    """Test cases for the Teacher class."""

    def test_teacher_creation(self):
        """Test creating a teacher."""
        teacher = Teacher("T001", "Dr. Smith", "Mathematics")
        self.assertEqual(teacher.teacher_id, "T001")
        self.assertEqual(teacher.name, "Dr. Smith")
        self.assertEqual(teacher.course, "Mathematics")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""

    def test_complete_workflow(self):
        """Test a complete workflow from student to grade calculation."""
        # Create student
        student = Student("S001", "Jane Doe")

        # Add evaluations
        eval1 = Evaluation("S001", "E001", 16.0, 40.0)
        eval2 = Evaluation("S001", "E002", 18.0, 30.0)
        eval3 = Evaluation("S001", "E003", 14.0, 30.0)

        student.add_evaluation(eval1)
        student.add_evaluation(eval2)
        student.add_evaluation(eval3)

        # Calculate grade
        calculator = GradeCalculator()
        final_grade, details = calculator.calculate_final_grade(
            student.get_evaluations(),
            attendance_percentage=95.0,
            extra_points=1.0,
            reached_minimum_attendance=True
        )

        # Verify results
        self.assertGreater(final_grade, 0)
        self.assertLessEqual(final_grade, 20.0)
        self.assertEqual(details['final_grade'], final_grade)

    def test_multiple_students_independent(self):
        """Test that multiple students' grades are independent."""
        student1 = Student("S001", "Student A")
        student2 = Student("S002", "Student B")

        # Student 1 has high grades
        student1.add_evaluation(Evaluation("S001", "E001", 19.0, 100.0))

        # Student 2 has low grades
        student2.add_evaluation(Evaluation("S002", "E001", 8.0, 100.0))

        calculator = GradeCalculator()
        grade1, _ = calculator.calculate_final_grade(
            student1.get_evaluations()
        )
        grade2, _ = calculator.calculate_final_grade(
            student2.get_evaluations()
        )

        self.assertGreater(grade1, grade2)


if __name__ == "__main__":
    unittest.main()
