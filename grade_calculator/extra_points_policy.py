"""
Extra points policy module for managing extra credit policies.

This module contains the ExtraPointsPolicy class that defines rules for
applying extra points to students' grades.
"""


class ExtraPointsPolicy:
    """Defines the policy for applying extra points to students' grades."""

    def __init__(self, extra_points_value: float = 1.0):
        """
        Initialize an ExtraPointsPolicy.

        Args:
            extra_points_value: The amount of points to add per extra point
                               (default: 1.0)

        Raises:
            ValueError: If extra_points_value is negative
        """
        if extra_points_value < 0:
            raise ValueError("Extra points value cannot be negative")
        self.extra_points_value = extra_points_value

    def apply_extra_points(self, grade: float,
                          extra_points_count: float) -> float:
        """
        Apply extra points to a grade, capped at maximum grade (20).

        Args:
            grade: The base grade
            extra_points_count: Number of extra points to apply

        Returns:
            The grade with extra points applied, capped at 20.0
        """
        MAX_GRADE = 20.0
        result = grade + (extra_points_count * self.extra_points_value)
        return min(result, MAX_GRADE)

    def __repr__(self) -> str:
        """Return a string representation of the ExtraPointsPolicy."""
        return f"ExtraPointsPolicy(value={self.extra_points_value})"
