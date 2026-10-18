# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/excel/__init__.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: Excel writer package.
# =============================================================================
"""Excel (.xlsx) output."""
from .builder import MatrixWorkbook

__all__ = ['MatrixWorkbook']
