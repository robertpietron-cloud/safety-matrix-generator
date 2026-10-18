# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : tools/check_headers.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - Checker of the mandatory file header (project, file
#                        name, author, revision with date, list of changes).
# =============================================================================
"""Verify that every file of the repository starts with the mandatory header.

Usage:  python tools/check_headers.py [repo_root]      (exit code 1 when a file lacks it)
"""
import os
import re
import subprocess
import sys

SKIP_DIRS = {'.git', '__pycache__', '.pytest_cache', 'build', 'dist', '.venv', 'venv', 'output', 'private'}
SKIP_EXT = {'.xlsx', '.xlsm', '.pdf', '.png', '.jpg', '.pyc', '.docx'}
REQUIRED = [r'Project\s*:', r'File\s*:', r'Author\s*:\s*Robert Pietroń', r'Revision\s*:\s*\d+\.\d+\.\d+ \(\d{4}-\d{2}-\d{2}\)',
            r'Changes\s*:']


def repo_files(root):
    try:
        out = subprocess.run(['git', 'ls-files'], cwd=root, capture_output=True, text=True, check=True).stdout.split('\n')
        files = [f for f in out if f]
        if files:
            return files
    except (OSError, subprocess.CalledProcessError):
        pass
    files = []
    for d, dirs, fs in os.walk(root):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS and not x.endswith('.egg-info')]
        for f in fs:
            files.append(os.path.relpath(os.path.join(d, f), root))
    return files


def has_header(path, rel):
    head = open(path, encoding='utf-8', errors='replace').read(3000)
    if not all(re.search(p, head) for p in REQUIRED):
        return False
    m = re.search(r'File\s*:\s*(\S+)', head)
    return bool(m) and m.group(1).replace('\\', '/') == rel.replace('\\', '/')


def missing(root):
    bad = []
    for rel in sorted(repo_files(root)):
        if os.path.splitext(rel)[1].lower() in SKIP_EXT or any(p in SKIP_DIRS for p in rel.split(os.sep)):
            continue
        path = os.path.join(root, rel)
        if os.path.isfile(path) and not has_header(path, rel):
            bad.append(rel)
    return bad


if __name__ == '__main__':
    root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad = missing(root)
    for b in bad:
        print('missing/invalid header:', b)
    print(f'{len(bad)} file(s) without a valid header')
    sys.exit(1 if bad else 0)
