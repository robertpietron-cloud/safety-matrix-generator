# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/__init__.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: package metadata and the
#                        high-level generate() API.
# =============================================================================
"""Safety Matrix Generator – Cause & Effect matrix from a GuardLogix SafetyTask (L5K / L5X)."""

__version__ = '1.0.0'
__author__ = 'Robert Pietroń'

__all__ = ['__version__', '__author__', 'generate']


def generate(input_path, output_path, config_path=None, languages=None, default_language=None, json_path=None):
    """Parse an export, analyse the SafetyTask and write the Safety Matrix workbook.

    Returns a dict with summary counts.
    """
    from .pipeline import run
    return run(input_path, output_path, config_path, languages, default_language, json_path)
