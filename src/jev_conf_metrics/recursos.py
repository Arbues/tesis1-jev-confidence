# -*- coding: utf-8 -*-
"""Guard de recursos: aborta ANTES de cargar un modelo si no hay RAM/VRAM.

WSL2 no devuelve memoria a Windows con agresividad: cargar un modelo grande sin comprobar
puede colgar la VM y, con ella, Windows. Regla del autor (2026-10-08): **con 1 GB de RAM
disponible se para todo y se suspende.**
"""
from __future__ import annotations

import gc
import subprocess
import sys

RAM_MINIMA_GB = 1.0
__all__ = ["ram_disponible_gb", "vram_libre_mb", "exigir_recursos", "liberar", "RAM_MINIMA_GB"]


def ram_disponible_gb():
    """`MemAvailable` de /proc/meminfo, en GB."""
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) / 1024 / 1024
    except OSError:
        pass
    return float("inf")


def vram_libre_mb():
    """VRAM libre mínima entre las GPUs visibles, en MiB. `None` si no hay nvidia-smi."""
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=15, check=True).stdout.strip().splitlines()
        return min(int(x) for x in out) if out else None
    except Exception:
        return None


def exigir_recursos(vram_necesaria_mb=0, ram_necesaria_gb=RAM_MINIMA_GB, etiqueta=""):
    """Aborta el proceso si no hay recursos. Abortar es correcto: no se reintenta a lo bruto."""
    ram, vram = ram_disponible_gb(), vram_libre_mb()
    if ram < ram_necesaria_gb:
        sys.exit(f"[recursos] ABORTADO{etiqueta}: RAM libre {ram:.1f} GB < {ram_necesaria_gb} GB. "
                 f"PARAR TODO Y SUSPENDER (regla del autor).")
    if vram is not None and vram < vram_necesaria_mb:
        sys.exit(f"[recursos] ABORTADO{etiqueta}: VRAM libre {vram} MB < {vram_necesaria_mb} MB. "
                 f"¿Sigue vivo un servidor? Prueba: pkill -f 'ke[v].serve'")
    print(f"[recursos] ok{etiqueta}: RAM {ram:.1f} GB · VRAM {vram} MB", flush=True)


def liberar(*objetos):
    """Suelta referencias y vacía la caché de CUDA. Llamar SIEMPRE entre modelos."""
    for o in objetos:
        del o
    gc.collect()
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
    except Exception:
        pass
    print("[recursos] liberado", flush=True)
