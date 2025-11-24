"""
CS-GradeCalculator Package

A comprehensive grade calculation system for managing student evaluations,
attendance policies, and final grade calculations.

Author: UTEC Software Engineering
Course: CS3081 - Software Engineering
"""

from .evaluation import Evaluation
from .student import Student
from .teacher import Teacher
from .grade_calculator import GradeCalculator
from .attendance_policy import AttendancePolicy
from .extra_points_policy import ExtraPointsPolicy
from .main import GradeCalculatorApp

__version__ = "1.0.0"
__all__ = [
    "Evaluation",
    "Student",
    "Teacher",
    "GradeCalculator",
    "AttendancePolicy",
    "ExtraPointsPolicy",
    "GradeCalculatorApp"
]
