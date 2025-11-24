"""
Student module for managing student information and their evaluations.

This module contains the Student class that represents a student in the system.
"""
from typing import List

# Support both direct execution and package imports
try:
    from .evaluation import Evaluation
except (ImportError, ValueError):
    from evaluation import Evaluation


class Student:
    """Represents a student in the CS-GradeCalculator system."""

    def __init__(self, student_id: str, name: str):
        """
        Initialize a Student.

        Args:
            student_id: Unique identifier for the student
            name: Full name of the student
        """
        self.student_id = student_id
        self.name = name
        self.evaluations: List[Evaluation] = []

    def add_evaluation(self, evaluation: Evaluation) -> None:
        """
        Add an evaluation for this student.

        Args:
            evaluation: The Evaluation object to add

        Raises:
            ValueError: If student_id doesn't match
        """
        if evaluation.student_id != self.student_id:
            raise ValueError(
                f"Evaluation student_id {evaluation.student_id} does not "
                f"match student {self.student_id}"
            )
        self.evaluations.append(evaluation)

    def get_evaluation_count(self) -> int:
        """
        Get the number of evaluations for this student.

        Returns:
            The count of evaluations
        """
        return len(self.evaluations)

    def get_evaluations(self) -> List[Evaluation]:
        """
        Get all evaluations for this student.

        Returns:
            List of Evaluation objects
        """
        return self.evaluations.copy()

    def __repr__(self) -> str:
        """Return a string representation of the Student."""
        return f"Student(id={self.student_id}, name={self.name})"
