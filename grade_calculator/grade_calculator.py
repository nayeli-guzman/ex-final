"""
Grade calculator module for computing final grades.

This module contains the GradeCalculator class that computes weighted
averages, applies penalties and extra points, and generates grade reports.
"""
from typing import List, Tuple, Dict

# Support both direct execution and package imports
try:
    from .evaluation import Evaluation
    from .attendance_policy import AttendancePolicy
    from .extra_points_policy import ExtraPointsPolicy
except (ImportError, ValueError):
    from evaluation import Evaluation
    from attendance_policy import AttendancePolicy
    from extra_points_policy import ExtraPointsPolicy


class GradeCalculator:
    """Calculates final grades based on evaluations and policies."""

    MAX_EVALUATIONS_PER_STUDENT = 10
    MAX_GRADE = 20.0
    MIN_GRADE = 0.0
    ATTENDANCE_PENALTY_PERCENTAGE = 0.1  # 10% penalty per missed class
    MAX_CALCULATION_TIME_MS = 300  # milliseconds

    def __init__(self, attendance_policy: AttendancePolicy = None,
                 extra_points_policy: ExtraPointsPolicy = None):
        """
        Initialize a GradeCalculator.

        Args:
            attendance_policy: Policy for attendance requirements
            extra_points_policy: Policy for extra points application
        """
        self.attendance_policy = attendance_policy or AttendancePolicy()
        self.extra_points_policy = extra_points_policy or ExtraPointsPolicy()

    def calculate_weighted_average(self,
                                    evaluations: List[Evaluation]) -> float:
        """
        Calculate the weighted average of evaluations.

        Args:
            evaluations: List of Evaluation objects

        Returns:
            The weighted average grade

        Raises:
            ValueError: If evaluations list is empty
            ValueError: If exceeds maximum evaluations per student
        """
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
        """
        Calculate attendance penalty based on missing classes.

        Args:
            attendance_percentage: The attendance percentage

        Returns:
            The penalty value to subtract from the grade
        """
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
    ) -> Tuple[float, Dict[str, float]]:
        """
        Calculate the final grade with all adjustments.

        Args:
            evaluations: List of Evaluation objects
            attendance_percentage: Student's attendance percentage
            extra_points: Number of extra points earned
            reached_minimum_attendance: Whether student reached minimum
                                       attendance (RNF02 requirement)

        Returns:
            Tuple of (final_grade, details_dict) where details_dict contains
            'weighted_average', 'attendance_penalty', 'final_grade_before_extra',
            'extra_points_applied', and 'final_grade'

        Raises:
            ValueError: If inputs are invalid
        """
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
        """
        Generate a detailed grade report for a student.

        Args:
            student_id: The student identifier
            student_name: The student name
            evaluations: List of Evaluation objects
            attendance_percentage: Student's attendance percentage
            extra_points: Number of extra points earned
            reached_minimum_attendance: Whether student reached minimum
                                       attendance

        Returns:
            A formatted grade report string
        """
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
