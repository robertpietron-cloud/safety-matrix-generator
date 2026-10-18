# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : tests/helpers.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - Shared paths and cached demo analysis for the tests.
# =============================================================================
"""Test helpers."""
import functools
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_L5K = os.path.join(ROOT, 'examples', 'demo', 'DemoCell.L5K')
DEMO_CFG = os.path.join(ROOT, 'examples', 'demo', 'config.yaml')
DEMO_L5X = os.path.join(ROOT, 'tests', 'data', 'DemoCell.L5X')
PORTALSAW_CFG = os.path.join(ROOT, 'examples', 'portalsaw', 'config.yaml')


@functools.lru_cache(maxsize=None)
def demo_project():
    from safety_matrix.parsers import load_project
    return load_project(DEMO_L5K)


@functools.lru_cache(maxsize=None)
def demo_analysis(info=True):
    from safety_matrix.analysis import Analysis, Options
    return Analysis(demo_project(), Options(info_effects=['Safety_ToStd[0].0'] if info else []))
