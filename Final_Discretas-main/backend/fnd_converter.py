from sympy.logic.boolalg import to_dnf, And, Or, Not
from .parser import latex_a_sympy, parsear_expr

def expr_a_latex(expr) -> str:
    if isinstance(expr, And):
        return r' \wedge '.join([expr_a_latex(arg) for arg in expr.args])
    elif isinstance(expr, Or):
        return r' \vee '.join([f'\\left({expr_a_latex(arg)}\\right)' for arg in expr.args])
    elif isinstance(expr, Not):
        arg = expr.args[0]
        return r'\neg\left(' + expr_a_latex(arg) + r'\right)' if isinstance(arg, (And, Or)) else r'\neg ' + expr_a_latex(arg)
    else:
        return str(expr)

def convertir_a_fnd_latex(expr_latex: str) -> str:
    expr_str = latex_a_sympy(expr_latex)
    expr_sympy = parsear_expr(expr_str)
    fnd = to_dnf(expr_sympy, simplify=True)
    return f"${expr_a_latex(fnd)}$"
