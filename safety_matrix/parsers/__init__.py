# =============================================================================
# Project : Safety Matrix Generator (GuardLogix SafetyTask -> Cause & Effect)
# File    : safety_matrix/parsers/__init__.py
# Author  : Robert Pietroń
# Revision: 1.0.0 (2026-10-18)
# Changes :
#   1.0.0 (2026-10-18) - First universal release: format detection and loading
#                        of .L5K, .L5X and exports pasted into .docx / .txt.
# =============================================================================
"""Load a Logix Designer export (L5K, L5X, or either pasted into a .docx/.txt)."""
from __future__ import annotations

import html
import os
import re
import zipfile

from ..model import Project
from .l5k import parse_l5k
from .l5x import parse_l5x

__all__ = ['load_project', 'parse_l5k', 'parse_l5x', 'docx_text']


def docx_text(path: str) -> str:
    """Plain text of a .docx (one paragraph per line) using only the standard library."""
    with zipfile.ZipFile(path) as z:
        xml = z.read('word/document.xml').decode('utf-8', errors='replace')
    paras = []
    for p in re.findall(r'<w:p[ >].*?</w:p>|<w:p/>', xml, re.S):
        p = re.sub(r'<w:tab/>', '\t', p)
        p = re.sub(r'<w:br/>', '\n', p)
        parts = re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>|(\t)|(\n)', p, re.S)
        paras.append(''.join(a or b or c for a, b, c in parts))
    return html.unescape('\n'.join(paras))


def _read_text(path: str) -> str:
    raw = open(path, 'rb').read()
    for enc in ('utf-8-sig', 'utf-16', 'cp1252', 'latin-1'):
        try:
            txt = raw.decode(enc)
            if enc == 'utf-16' and not raw[:2] in (b'\xff\xfe', b'\xfe\xff'):
                continue
            return txt
        except UnicodeDecodeError:
            continue
    return raw.decode('latin-1')


def load_project(path: str) -> Project:
    """Detect the format of `path` and parse it into a :class:`Project`."""
    name = os.path.basename(path)
    ext = os.path.splitext(path)[1].lower()
    text = docx_text(path) if ext == '.docx' else _read_text(path)
    head = text.lstrip()[:400]
    if ext == '.l5x' or head.startswith('<?xml') or '<RSLogix5000Content' in text[:2000]:
        return parse_l5x(text, name)
    if 'CONTROLLER ' in text or ext == '.l5k':
        return parse_l5k(text, name)
    raise ValueError(f'{name}: not recognised as an L5K or L5X export')
