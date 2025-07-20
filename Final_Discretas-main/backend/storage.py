import os

NOMBRE_ARCHIVO = 'formulas_guardadas.txt'

def cargar_formulas_previas():
    if not os.path.exists(NOMBRE_ARCHIVO):
        return []
    with open(NOMBRE_ARCHIVO, 'r', encoding='utf-8') as f:
        return [linea.strip().split(' ||| ') for linea in f.readlines()]

def guardar_formulas(formulas):
    with open(NOMBRE_ARCHIVO, 'w', encoding='utf-8') as f:
        for idx, entrada, fnd in formulas:
            f.write(f"{idx} ||| {entrada} ||| {fnd}\n")
