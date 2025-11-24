"""
Evaluation module for managing student evaluations and grades.

This module contains the Evaluation class that represents a student's
evaluation record for a course.
"""


class Evaluation:
    """Represents an evaluation record for a student."""

    MIN_GRADE = 0.0
    MAX_GRADE = 20.0
    DEFAULT_WEIGHT_PERCENTAGE = 100.0

    def __init__(self, student_id: str, evaluation_id: str, grade: float,
                 weight_percentage: float = DEFAULT_WEIGHT_PERCENTAGE):
        """
        Initialize an Evaluation.

        Args:
            student_id: Unique identifier for the student
            evaluation_id: Unique identifier for the evaluation
            grade: The grade obtained (0-20)
            weight_percentage: Weight percentage of this evaluation (default: 100%)

        Raises:
            ValueError: If grade is not in valid range
            ValueError: If weight_percentage is not in valid range
        """
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
        """
        Calculate the weighted grade.

        Returns:
            The weighted grade value
        """
        return self.grade * (self.weight_percentage / 100.0)

    def __repr__(self) -> str:
        """Return a string representation of the Evaluation."""
        return (
            f"Evaluation(student_id={self.student_id}, "
            f"evaluation_id={self.evaluation_id}, grade={self.grade}, "
            f"weight={self.weight_percentage}%)"
        )
