import pyperclip
from tkinter import Text, Frame, Scrollbar, filedialog, messagebox, StringVar, END
from ttkbootstrap import Style
from ttkbootstrap.widgets import Button, Entry, Label, LabelFrame, Combobox
from .renderer import render_latex
from backend.fnd_converter import convertir_a_fnd_latex
from backend.storage import cargar_formulas_previas, guardar_formulas

class App:
    def __init__(self, root):
        self.root = root
        self.style = Style("darkly")
        self.root.title("Conversor FND con LaTeX")
        self.formulas = cargar_formulas_previas()
        self.canvas_entrada = self.canvas_salida = None

        entrada_frame = LabelFrame(root, text="Entrada")
        entrada_frame.pack(fill='x', padx=10, pady=5)
        self.input_text = Text(entrada_frame, height=3, wrap='word')
        self.input_text.pack(fill='x', padx=5, pady=5)
        Scrollbar(entrada_frame, command=self.input_text.yview).pack(side="right", fill="y")
        self.input_text.bind("<Control-l>", lambda e: self.limpiar())
        self.input_text.bind("<Return>", lambda e: self.convertir())

        btn_frame = Frame(root)
        btn_frame.pack(pady=5)
        Button(btn_frame, text="Convertir a FND", bootstyle="success", command=self.convertir).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Limpiar", command=self.limpiar).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Copiar LaTeX", command=self.copiar_latex).grid(row=0, column=2, padx=5)
        Button(btn_frame, text="Guardar Imagen", command=self.guardar_imagen).grid(row=0, column=3, padx=5)

        Label(root, text="Ejemplos rápidos:").pack()
        self.combo = Combobox(root, values=[r"(p \lor q \lor r) \land (\neg p \lor \neg q)", r"\neg (p \land q) \lor r", r"\neg (p \lor (q \land r))"], width=40)
        self.combo.pack()
        self.combo.bind("<<ComboboxSelected>>", self.insertar_ejemplo)

        salida_frame = LabelFrame(root, text="Resultado Renderizado")
        salida_frame.pack(fill='x', padx=10, pady=5)
        self.latex_container = Frame(salida_frame)
        self.latex_container.pack(pady=5)
        self.resultado_label = Label(root, text="", bootstyle="info")
        self.resultado_label.pack()

        hist_frame = LabelFrame(root, text="Historial reciente")
        hist_frame.pack(fill='x', padx=10, pady=5)
        self.historial_label = Label(hist_frame, text="", anchor='w', justify='left')
        self.historial_label.pack(fill='x', padx=5)

        self.actualizar_historial()

    def convertir(self):
        entrada = self.input_text.get("1.0", END).strip()
        if not entrada:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una fórmula.")
            return

        try:
            fnd_latex = convertir_a_fnd_latex(entrada)
        except Exception as e:
            self.resultado_label.config(text=f"Error: {e}", bootstyle="danger")
            return

        idx = str(len(self.formulas) + 1)
        self.formulas.append((idx, entrada, fnd_latex))
        guardar_formulas(self.formulas)

        self.canvas_entrada = render_latex(entrada, self.latex_container, self.canvas_entrada)
        self.canvas_salida = render_latex(fnd_latex.strip('$'), self.latex_container, self.canvas_salida)
        self.resultado_label.config(text=f"FND: {fnd_latex}", bootstyle="info")
        self.actualizar_historial()

    def limpiar(self):
        self.input_text.delete("1.0", END)
        self.resultado_label.config(text="")
        if self.canvas_entrada:
            self.canvas_entrada.get_tk_widget().destroy()
            self.canvas_entrada = None
        if self.canvas_salida:
            self.canvas_salida.get_tk_widget().destroy()
            self.canvas_salida = None

    def copiar_latex(self):
        contenido = self.resultado_label.cget("text")
        if contenido:
            pyperclip.copy(contenido.strip("FND: "))
            messagebox.showinfo("Copiado", "LaTeX copiado al portapapeles.")

    def guardar_imagen(self):
        if not self.canvas_salida:
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Imagen PNG", "*.png")])
        if filepath:
            self.canvas_salida.figure.savefig(filepath)
            messagebox.showinfo("Guardado", "Imagen guardada correctamente.")

    def insertar_ejemplo(self, event):
        self.input_text.delete("1.0", END)
        self.input_text.insert(END, self.combo.get())

    def actualizar_historial(self):
        ultimos = self.formulas[-5:]
        texto = "\n".join([f"{idx}. {entrada}" for idx, entrada, _ in ultimos])
        self.historial_label.config(text=texto)
