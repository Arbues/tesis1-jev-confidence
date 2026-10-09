# -*- coding: utf-8 -*-
"""jev-conf-metrics — metrología del campo `confidence` en modelos de decisión tipo Jev.

Librería del entregable 2 de la Tesis 1 (Ruta 1):
  · `definiciones`  — DEF-1..DEF-5 (Jev, entropía, pmax, margen, noul) y DEF-7 (AnyJev L0/L1).
  · `metricas`      — ECE (ancho/masa), el binning exacto de Laya, AUROC, Brier, NLL, RPS.
  · `transferencia` — umbrales, celdas de la matriz, cross-fitting, bootstrap y FDR.
  · `recursos`      — guard de RAM/VRAM para WSL2.

Uso:
    from jev_conf_metrics import all_confidences, celda, umbral_para_cobertura
"""
from .definiciones import (  # noqa: F401
    CONFIDENCES, all_confidences, aplicar_l0, aplicar_l1, conf_ent, conf_jev,
    conf_margin, conf_noul, conf_pmax, order_equiv_affine_jev_pmax,
    phi_inv, prior_por_desplazamiento_ciclico,
)
from .metricas import auroc, brier_multi, ece, ece_laya, nll, rps  # noqa: F401
from .recursos import exigir_recursos, liberar, ram_disponible_gb, vram_libre_mb  # noqa: F401
from .transferencia import (  # noqa: F401
    bh_fdr, bootstrap_delta, celda, cobertura, fold_de, precision,
    umbral_para_cobertura,
)

__version__ = "0.1.0"
