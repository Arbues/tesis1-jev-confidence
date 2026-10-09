# -*- coding: utf-8 -*-
"""Deja el repo raíz en sys.path para que `src.jev_conf_metrics` sea importable en los tests."""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
