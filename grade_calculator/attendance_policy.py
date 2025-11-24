"""
Attendance policy module for managing attendance requirements.

This module contains the AttendancePolicy class that defines minimum
attendance requirements based on academic policies.
"""


class AttendancePolicy:
    """Defines attendance requirements for students based on academic policies."""

    def __init__(self, minimum_attendance_percentage: float = 80.0):
        """
        Initialize an AttendancePolicy.

        Args:
            minimum_attendance_percentage: Minimum required attendance (default: 80%)

        Raises:
            ValueError: If percentage is not between 0 and 100
        """
        if not (0 <= minimum_attendance_percentage <= 100):
            raise ValueError("Attendance percentage must be between 0 and 100")
        self.minimum_attendance_percentage = minimum_attendance_percentage

    def is_attendance_sufficient(self, attendance_percentage: float) -> bool:
        """
        Check if the given attendance meets the policy requirement.

        Args:
            attendance_percentage: The actual attendance percentage

        Returns:
            True if attendance meets minimum requirement, False otherwise
        """
        return attendance_percentage >= self.minimum_attendance_percentage

    def __repr__(self) -> str:
        """Return a string representation of the AttendancePolicy."""
        return (
            f"AttendancePolicy(minimum={self.minimum_attendance_percentage}%)"
        )
