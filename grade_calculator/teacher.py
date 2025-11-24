"""
Teacher module for managing teacher information.

This module contains the Teacher class that represents a teacher in the system.
"""


class Teacher:
    """Represents a teacher in the CS-GradeCalculator system."""

    def __init__(self, teacher_id: str, name: str, course: str):
        """
        Initialize a Teacher.

        Args:
            teacher_id: Unique identifier for the teacher
            name: Full name of the teacher
            course: Name of the course taught
        """
        self.teacher_id = teacher_id
        self.name = name
        self.course = course

    def __repr__(self) -> str:
        """Return a string representation of the Teacher."""
        return (
            f"Teacher(id={self.teacher_id}, name={self.name}, "
            f"course={self.course})"
        )
