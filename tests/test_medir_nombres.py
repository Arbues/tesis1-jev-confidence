# -*- coding: utf-8 -*-
"""Nombres de modelo y de artefacto: regresión de una colisión real de archivos.

Los tres checkpoints de Laya comparten `model_id` (`convaiinnovations/laya`). Sin cualificar
con el subfolder, los tres escribían al mismo `.jsonl` y solo sobrevivía el último
(detectado el 08-oct-2026 al ver que faltaban 2 de los 3 checkpoints en los crudos).
"""
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
sys.path.insert(0, os.path.join(RAIZ, "src", "matriz"))

from medir import etiqueta_de, nombre_de_modelo  # noqa: E402


def test_laya_cualifica_con_el_subfolder():
    a = nombre_de_modelo({"model_id": "convaiinnovations/laya", "subfolder": "multilingual"})
    b = nombre_de_modelo({"model_id": "convaiinnovations/laya", "subfolder": "typed-decisions"})
    c = nombre_de_modelo({"model_id": "convaiinnovations/laya", "subfolder": None})
    assert len({a, b, c}) == 3, (a, b, c)
    assert a == "convaiinnovations/laya/multilingual"
    assert c == "convaiinnovations/laya"


def test_los_tres_checkpoints_no_colisionan_en_disco():
    etiquetas = {
        etiqueta_de(nombre_de_modelo({"model_id": "convaiinnovations/laya", "subfolder": s}),
                    "sst5")
        for s in ("none", "typed-decisions", "multilingual")
    }
    assert len(etiquetas) == 3, etiquetas


def test_kev_y_control_sin_subfolder():
    assert nombre_de_modelo({"model_id": "jaredpalmer/kev-0.8b"}) == "jaredpalmer/kev-0.8b"
    assert etiqueta_de("Qwen/Qwen3.5-0.8B-Base", "wanli") == "Qwen__Qwen3.5-0.8B-Base__wanli"
