import re
from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr

def latex_a_sympy(expr_latex: str) -> str:
    expr_latex = expr_latex.strip('$').strip().strip('\[').strip('\]')
    reemplazos = {
        r'\\neg': '~', r'\\land': '&', r'\\lor': '|',
        r'\\rightarrow': '>>', r'\\leftrightarrow': '=='
    }
    for k, v in reemplazos.items():
        expr_latex = re.sub(k, v, expr_latex)
    return re.sub(r'\s+', '', expr_latex)

def obtener_variables(expr_str: str) -> list[str]:
    return sorted(set(re.findall(r'[a-zA-Z]\w*', expr_str)))

def parsear_expr(expr_str: str):
    contexto = {v: symbols(v) for v in obtener_variables(expr_str)}
    return parse_expr(expr_str, local_dict=contexto)
