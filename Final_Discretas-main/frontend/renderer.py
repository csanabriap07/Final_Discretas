from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def render_latex(latex_code, contenedor, old_canvas=None):
    latex_code = latex_code.replace('\\land', r'\wedge').replace('\\lor', r'\vee')
    fig = plt.figure(figsize=(6, 1.2))
    plt.text(0.5, 0.5, f"${latex_code}$", fontsize=18, ha='center', va='center')
    plt.axis('off')
    if old_canvas:
        old_canvas.get_tk_widget().destroy()
    canvas = FigureCanvasTkAgg(fig, master=contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack()
    return canvas
