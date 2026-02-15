"""Validation layer: SELECT-only, injection protection, forbidden columns, structural checks."""

from .validator import QueryValidator, ValidationResult

__all__ = ["QueryValidator", "ValidationResult"]
