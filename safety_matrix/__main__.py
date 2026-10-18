# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/__main__.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: `python -m safety_matrix`.
# =============================================================================
"""Entry point for ``python -m safety_matrix``."""
import sys

from .cli import main

sys.exit(main())
