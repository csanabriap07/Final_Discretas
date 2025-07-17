# ---------------------- IMPORTS PRINCIPALES ----------------------
# Librerías principales:
# tkinter -> Para crear la interfaz gráfica
# matplotlib -> Para renderizar expresiones LaTeX en la GUI
# sympy -> Para manejar lógica proposicional y convertir a FND
# os -> Para manejo de archivos (guardar y cargar fórmulas)
from tkinter import Tk, Label, Entry, Button, Frame, messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols
from sympy.logic.boolalg import to_dnf, And, Or, Not
from sympy.parsing.sympy_parser import parse_expr
import os

# ---------------------- VARIABLES Y CONFIGURACIÓN ----------------------
# Declaración de símbolos lógicos p, q, r (se pueden extender si es necesario)
p, q, r = symbols('p q r')

# Archivo donde se almacenarán las fórmulas ingresadas y sus FND
nombre_archivo = 'formulas_guardadas.txt'

# ---------------------FUNCIONES PRINCIPALES --------------------

def latex_a_sympy(expr_latex):
    """
    Convierte una expresión en formato LaTeX a una expresión entendible por sympy.
    Reemplaza símbolos lógicos LaTeX por operadores de sympy:
    \neg -> ~, \land -> &, \lor -> |
    """
    reemplazos = {
        r'\neg': '~',
        r'\land': '&',
        r'\lor': '|',
    }
    for k, v in reemplazos.items():
        expr_latex = expr_latex.replace(k, v)
    return expr_latex.strip('$').strip().strip('\\[').strip('\\]')

def expr_a_latex(expr):
    """
    Convierte una expresión sympy en un string LaTeX para renderizar.
    Soporta And (∧), Or (∨) y Not (¬).
    """
    if isinstance(expr, And):
        partes = [expr_a_latex(arg) for arg in expr.args]
        return r' \wedge '.join(partes)
    elif isinstance(expr, Or):
        partes = [f'\\left({expr_a_latex(arg)}\\right)' for arg in expr.args]
        return r' \vee '.join(partes)
    elif isinstance(expr, Not):
        arg = expr.args[0]
        if isinstance(arg, (And, Or)):
            return r'\neg\left(' + expr_a_latex(arg) + r'\right)'
        else:
            return r'\neg ' + expr_a_latex(arg)
    else:
        return str(expr)

def convertir_a_fnd_latex(expr_latex):
    """
    Convierte una expresión lógica en LaTeX a su Forma Normal Disyuntiva (FND) en LaTeX.
    Si ocurre un error en la conversión, retorna un mensaje con el error.
    """
    try:
        expr_sympy = parse_expr(latex_a_sympy(expr_latex), local_dict={'p': p, 'q': q, 'r': r})
        fnd = to_dnf(expr_sympy, simplify=True)
        return f"${expr_a_latex(fnd)}$"
    except Exception as e:
        return f"Error: {e}"

def cargar_formulas_previas(nombre_archivo):
    """
    Carga las fórmulas previamente guardadas en un archivo de texto.
    Retorna una lista con (índice, entrada original, FND).
    """
    if not os.path.exists(nombre_archivo):
        return []
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        lineas = f.readlines()
    formulas = [linea.strip().split(' ||| ') for linea in lineas]
    return formulas

def guardar_formulas(nombre_archivo, formulas):
    """
    Guarda las fórmulas ingresadas y sus resultados en un archivo de texto.
    Formato: idx ||| entrada ||| FND
    """
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        for idx, entrada, fnd in formulas:
            f.write(f"{idx} ||| {entrada} ||| {fnd}\n")

def render_latex(latex_code, contenedor, old_canvas=None):
    """
    Renderiza una expresión LaTeX en la interfaz gráfica usando matplotlib.
    Si ya existe un canvas anterior, lo destruye para actualizar.
    """
    reemplazos = {
        r'\land': r'\wedge',
        r'\lor': r'\vee',
        r'\implies': r'\Rightarrow',
        r'\iff': r'\Leftrightarrow'
    }
    for k, v in reemplazos.items():
        latex_code = latex_code.replace(k, v)

    fig = plt.figure(figsize=(6, 1))
    plt.text(0.5, 0.5, f"${latex_code}$", fontsize=18, ha='center', va='center')
    plt.axis('off')

    if old_canvas:
        old_canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack()
    return canvas

# ---------------------- INTERFAZ GRÁFICA ----------------------
class App:
    """
    Clase principal que construye la interfaz y maneja los eventos.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor FND con Renderizado LaTeX")

        # Cargar fórmulas previas
        self.formulas = cargar_formulas_previas(nombre_archivo)

        # Entrada de texto
        Label(root, text="Ingrese fórmula lógica en LaTeX: sin $").pack(pady=5)
        self.entry = Entry(root, width=60)
        self.entry.pack(pady=5)

        # Botones
        Button(root, text="Convertir a FND", command=self.convertir).pack(pady=5)
        Button(root, text="Limpiar", command=self.limpiar).pack(pady=5)

        # Frame para render LaTeX
        self.frame_latex = Frame(root)
        self.frame_latex.pack(pady=10)

        # Salida de texto
        Label(root, text="Salida en texto:").pack(pady=5)
        self.salida_texto = Label(root, text="", fg="blue")
        self.salida_texto.pack(pady=5)

        self.canvas_entrada = None
        self.canvas_salida = None

    def convertir(self):
        """
        Toma la fórmula ingresada, la convierte a FND, la guarda y la muestra en pantalla.
        """
        entrada = self.entry.get().strip()
        if not entrada:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una fórmula.")
            return

        fnd_latex = convertir_a_fnd_latex(entrada)
        idx = str(len(self.formulas) + 1)
        self.formulas.append((idx, entrada, fnd_latex))
        guardar_formulas(nombre_archivo, self.formulas)

        # Mostrar render entrada y salida
        self.canvas_entrada = render_latex(entrada, self.frame_latex, self.canvas_entrada)
        self.canvas_salida = render_latex(fnd_latex.strip('$'), self.frame_latex, self.canvas_salida)

        # Mostrar salida en texto
        self.salida_texto.config(text=f"FND: {fnd_latex}")

    def limpiar(self):
        """
        Limpia la interfaz (entrada, salidas y canvas).
        """
        self.entry.delete(0, 'end')
        self.salida_texto.config(text="")
        if self.canvas_entrada:
            self.canvas_entrada.get_tk_widget().destroy()
            self.canvas_entrada = None
        if self.canvas_salida:
            self.canvas_salida.get_tk_widget().destroy()
            self.canvas_salida = None

# ---------------------- EJECUCIÓN PRINCIPAL ----------------------
if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()
