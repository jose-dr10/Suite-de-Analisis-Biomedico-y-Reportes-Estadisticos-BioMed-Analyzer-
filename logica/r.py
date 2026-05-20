import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk

# --- IMPORTES DE LÓGICA (Asegúrate de que estos archivos existan) ---
try:
    from logica.anemia import diagnosticar_anemia
    from logica.nutricion import calcular_imc
    from logica.presion import evaluar_presion_arterial
    from logica.cardio import evaluar_perfil_lipidico
    from logica.metabolismo import calcular_metabolismo_y_agua
    from logica.glucemia import evaluar_glucemia
    from logica.antropometria import evaluar_ica
    from logica.renal import calcular_tfg_avanzado
    from logica.ciclo import calcular_ovulacion
    from logica.conversor import convertir_glucosa, convertir_lipidos, convertir_trigliceridos
    from logica.framingham import evaluar_riesgo_framingham
    from logica.glasgow import evaluar_glasgow
    from logica.dolor import evaluar_dolor
    from logica.infusion import calcular_goteo
    from logica.respiratorio import calcular_kirby
    from logica.pediatria import calcular_dosis_pediatrica
    from logica.superficie import calcular_superficie_corporal
    from logica.hepatica import evaluar_bilirrubina
    from logica.electrolitos import calcular_anion_gap, calcular_deficit_agua
except ImportError as e:
    print(f"Error de importación: {e}. Asegúrate de que la carpeta 'logica' tenga los archivos .py")

class VentanaPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("BioAnalyst Pro")
        self.root.geometry("1200x850")
        self.root.configure(bg="#f5f7ff")

        # --- ESTILOS ---
        self.color_primario = "#5d5fef"
        self.color_categoria = "#4a4ccd"
        self.color_fondo = "#f5f7ff"
        self.color_card = "#ffffff"
        self.color_texto = "#2d2e5f"
        self.color_alerta = "#ff708b"
        self.color_input = "#f1f3f4"
        self.color_desactivado = "#e0e0e0"

        self.fuente_titular = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.fuente_ui = tkfont.Font(family="Helvetica", size=9)
        self.fuente_tags = tkfont.Font(family="Helvetica", size=8, weight="bold")
        self.fuente_res_titulo = tkfont.Font(family="Helvetica", size=16, weight="bold")
        self.fuente_res_label = tkfont.Font(family="Helvetica", size=9, weight="bold")
        self.fuente_res_info = tkfont.Font(family="Helvetica", size=11)

        # --- SIDEBAR ---
        self.sidebar = tk.Frame(self.root, bg=self.color_primario, width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        tk.Label(self.sidebar, text="BIOANALYST PRO", fg="white", bg=self.color_primario,
                 font=("Helvetica", 14, "bold")).pack(pady=(25, 15))

        menu_items = [
            ("SIGNOS Y NUTRICIÓN", None),
            ("Presión Arterial", self.mostrar_presion),
            ("Estado Nutricional (IMC)", self.mostrar_nutricion),
            ("Riesgo por Medidas (ICA)", self.mostrar_ica),
            ("Gasto Metabólico y Agua", self.mostrar_metabolismo),
            ("LABORATORIO", None),
            ("Detección de Anemia", self.mostrar_anemia),
            ("Niveles de Glucosa", self.mostrar_glucemia),
            ("Perfil de Lípidos", self.mostrar_cardio),
            ("Perfil de Bilirrubina", self.mostrar_bilirrubina),
            ("Función Renal (eTFG)", self.mostrar_renal),
            ("CLÍNICA Y CRÍTICOS", None),
            ("Escala de Glasgow", self.mostrar_glasgow),
            ("Escala de Dolor (EVA)", self.mostrar_dolor),
            ("Índice de Kirby (PAFI)", self.mostrar_respiratorio),
            ("Anión Gap", self.mostrar_anion_gap),
            ("Déficit de Agua (Na)", self.mostrar_deficit_agua),
            ("HERRAMIENTAS", None),
            ("Riesgo Cardiovascular", self.mostrar_framingham),
            ("Cálculo de Infusiones", self.mostrar_infusion),
            ("Dosis Pediátrica", self.mostrar_pediatria),
            ("Superficie Corporal", self.mostrar_superficie),
            ("Conversión de Unidades", self.mostrar_conversor),
            ("Calendario de Fertilidad", self.mostrar_ciclo),
        ]

        for texto, comando in menu_items:
            if comando is None:
                f_cat = tk.Frame(self.sidebar, bg=self.color_categoria, pady=3)
                f_cat.pack(fill="x", pady=(10, 2))
                tk.Label(f_cat, text=texto, fg="#b0b2ff", bg=self.color_categoria,
                         font=("Helvetica", 7, "bold"), padx=20).pack(anchor="w")
            else:
                btn = tk.Button(self.sidebar, text=texto, command=comando, bg=self.color_primario,
                                fg="white", bd=0, font=self.fuente_ui, cursor="hand2", pady=4,
                                anchor="w", padx=25, activebackground=self.color_categoria)
                btn.pack(fill="x")

        self.contenedor = tk.Frame(self.root, bg=self.color_fondo)
        self.contenedor.pack(side="right", expand=True, fill="both", padx=30, pady=30)
        self.mostrar_bienvenida()

    # --- MÉTODOS DE APOYO UI ---
    def limpiar_contenedor(self):
        for widget in self.contenedor.winfo_children(): widget.destroy()

    def crear_layout_dual(self, titulo_modulo):
        self.limpiar_contenedor()
        tk.Label(self.contenedor, text=titulo_modulo.upper(), bg=self.color_fondo,
                 font=self.fuente_titular, fg=self.color_primario).pack(anchor="w", pady=(0, 25))
        cuerpo = tk.Frame(self.contenedor, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        f_form = tk.Frame(cuerpo, bg=self.color_card, padx=25, pady=25, highlightthickness=1, highlightbackground="#e0e0e0")
        f_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        f_res = tk.Frame(cuerpo, bg=self.color_card, padx=30, pady=30, highlightthickness=1, highlightbackground="#e0e0e0", width=420)
        f_res.pack(side="right", fill="both", expand=False)
        f_res.pack_propagate(False)
        self.area_reporte = tk.Frame(f_res, bg=self.color_card)
        self.area_reporte.pack(fill="both", expand=True)
        return f_form

    def actualizar_reporte(self, titulo, datos, color):
        for widget in self.area_reporte.winfo_children(): widget.destroy()
        tk.Label(self.area_reporte, text=titulo.upper(), font=self.fuente_res_titulo, fg=color, bg=self.color_card).pack(anchor="w", pady=(0, 15))
        for etiqueta, valor in datos.items():
            f_fila = tk.Frame(self.area_reporte, bg=self.color_card)
            f_fila.pack(fill="x", pady=2)
            tk.Label(f_fila, text=etiqueta, font=self.fuente_res_label, fg="#a0a0a0", bg=self.color_card).pack(anchor="w")
            tk.Label(f_fila, text=str(valor), font=self.fuente_res_info, fg=self.color_texto, bg=self.color_card, wraplength=350, justify="left").pack(anchor="w", pady=(0, 5))

    def crear_label_entry(self, master, texto):
        tk.Label(master, text=texto, bg=self.color_card, font=self.fuente_ui, fg="#5f6368").pack(anchor="w", pady=(5, 0))
        ent = tk.Entry(master, bg=self.color_input, bd=0, font=self.fuente_ui, fg=self.color_texto)
        ent.pack(fill="x", pady=(2, 8), ipady=6)
        return ent

    def crear_selector_segmentado(self, master, etiqueta, opciones, variable_tk):
        tk.Label(master, text=etiqueta, bg=self.color_card, font=self.fuente_ui, fg="#5f6368").pack(anchor="w", pady=(5, 0))
        f_selector = tk.Frame(master, bg=self.color_card)
        f_selector.pack(fill="x", pady=(5, 10))
        botones_dict = {}
        def actualizar_colores(seleccionado):
            variable_tk.set(seleccionado)
            for opt, btn in botones_dict.items():
                if str(opt) == str(seleccionado): btn.configure(bg=self.color_primario, fg="white")
                else: btn.configure(bg=self.color_desactivado, fg=self.color_texto)
        for opcion in opciones:
            btn = tk.Button(f_selector, text=str(opcion).capitalize(), bd=0, font=self.fuente_ui, cursor="hand2", pady=5)
            btn.configure(command=lambda o=opcion: actualizar_colores(o))
            btn.pack(side="left", expand=True, fill="x", padx=1)
            botones_dict[opcion] = btn
        actualizar_colores(variable_tk.get())

    def limpiar_contenedor(self):
        # Restauramos los márgenes por defecto (30px) para que los módulos
        # de formularios y resultados sigan viéndose perfectos y ordenados
        self.contenedor.pack_configure(padx=30, pady=30)
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    # --- DE BIENVENIDA ACTUALIZADO - SIN MARCOS EXTERNOS ---
    def mostrar_bienvenida(self):
        self.limpiar_contenedor()

        # Ajustamos el contenedor al mínimo absoluto para que la portada ocupe todo el espacio
        self.contenedor.pack_configure(padx=5, pady=(5, 5))

        # Intentamos importar PIL localmente por seguridad
        try:
            from PIL import Image, ImageTk, ImageDraw
            use_pillow = True
        except ImportError:
            use_pillow = False

        nombre_imagen = "imagen_234.png"

        if use_pillow:
            try:
                # 1. Cabecera superior (Mantiene su espacio limpio para el texto)
                f_cabecera = tk.Frame(self.contenedor, bg=self.color_fondo)
                f_cabecera.pack(side="top", fill="x", pady=(15, 15))

                tk.Label(
                    f_cabecera,
                    text="BIOANALYST PRO",
                    bg=self.color_fondo,
                    fg=self.color_primario,
                    font=self.fuente_titular
                ).pack()

                tk.Label(
                    f_cabecera,
                    text="MONITORIZACIÓN Y ANÁLISIS DE INDICADORES BIOMÉDICOS",
                    bg=self.color_fondo,
                    fg=self.color_texto,
                    font=("Helvetica", 10, "bold")
                ).pack(pady=(5, 0))

                # 2. Cargar la imagen original
                self.img_original = Image.open(nombre_imagen)

                # 3. Canvas inferior totalmente pegado a los bordes
                canvas = tk.Canvas(self.contenedor, bg=self.color_fondo, bd=0, highlightthickness=0)
                canvas.pack(side="bottom", fill="both", expand=True, padx=0, pady=0)

                def redimensionar_y_redondear(event):
                    ancho_c = event.width
                    alto_c = event.height

                    if ancho_c > 10 and alto_c > 10:
                        # Redimensionar imagen base al tamaño total disponible
                        img_redimensionada = self.img_original.resize((ancho_c, alto_c), Image.Resampling.LANCZOS)

                        # Radio de curvatura sutil (16px) para acompañar la forma de la ventana
                        radio = 16
                        mascara = Image.new("L", (ancho_c, alto_c), 0)
                        dibujo = ImageDraw.Draw(mascara)
                        dibujo.rounded_rectangle([0, 0, ancho_c, alto_c], radius=radio, fill=255)

                        # Aplicar la máscara de bordes redondeados
                        img_final = Image.new("RGBA", (ancho_c, alto_c), (0, 0, 0, 0))
                        img_final.paste(img_redimensionada, (0, 0), mask=mascara)

                        # Convertir para Tkinter
                        self.img_tk = ImageTk.PhotoImage(img_final)

                        canvas.delete("all")
                        # Dibujar la imagen expandida
                        canvas.create_image(0, 0, image=self.img_tk, anchor="nw")

                canvas.bind("<Configure>", redimensionar_y_redondear)
                return

            except FileNotFoundError:
                print(f"Advertencia: No se encontró '{nombre_imagen}'. Cargando respaldo de texto.")

        # --- PLAN DE RESPALDO (Si no hay Pillow o no existe la imagen) ---
        f_respaldo = tk.Frame(self.contenedor, bg=self.color_fondo)
        f_respaldo.pack(expand=True)

        tk.Label(f_respaldo, text="SISTEMA DE ASISTENCIA Y DIAGNÓSTICO CLÍNICO", bg=self.color_fondo,
                 fg=self.color_primario, font=self.fuente_titular).pack()
        tk.Label(f_respaldo, text="MONITORIZACIÓN Y ANÁLISIS DE INDICADORES BIOMÉDICOS", bg=self.color_fondo,
                 fg=self.color_texto, font=("Helvetica", 10, "bold")).pack(pady=(10, 0))


    # --- MÉTODOS DE CÁLCULO ---

    def mostrar_presion(self):
        f = self.crear_layout_dual("Presión Arterial")
        e_s = self.crear_label_entry(f, "Sistólica (mmHg):"); e_d = self.crear_label_entry(f, "Diastólica (mmHg):")
        def calc():
            try:
                r, s = evaluar_presion_arterial(int(e_s.get()), int(e_d.get()))
                detalles = {"DIAGNÓSTICO": r.upper(), "RIESGO": s, "REFERENCIA": "Normal: <120/80 mmHg", "RECOMENDACIÓN": "Reducir sodio y monitorear si hay cefalea o mareos."}
                self.actualizar_reporte("Informe Tensional", detalles, self.color_alerta if "Hipertensión" in r else self.color_primario)
            except: pass
        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_nutricion(self):
        f = self.crear_layout_dual("Estado Nutricional")
        e_p = self.crear_label_entry(f, "Peso (kg):"); e_a = self.crear_label_entry(f, "Estatura (m):")
        def calc():
            try:
                v, cat, rec = calcular_imc(float(e_p.get()), float(e_a.get()))
                detalles = {"IMC": f"{v} kg/m²", "CATEGORÍA": cat.upper(), "PLAN": rec, "INFO": "El IMC no distingue entre masa muscular y grasa."}
                self.actualizar_reporte("Evaluación Nutricional", detalles, self.color_alerta if cat != "Peso normal" else self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR IMC", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_ica(self):
        f = self.crear_layout_dual("Riesgo por Medidas (ICA)")
        e_c = self.crear_label_entry(f, "Cintura (cm):"); e_a = self.crear_label_entry(f, "Altura (cm):")
        def calc():
            try:
                v, e, r = evaluar_ica(float(e_c.get()), float(e_a.get()))
                detalles = {"ICA": v, "ESTADO": e, "RIESGO CV": r, "NOTA": "El ICA es más preciso que el IMC para riesgo cardíaco."}
                self.actualizar_reporte("Índice Cintura-Altura", detalles, self.color_alerta if v > 0.5 else self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR ICA", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_metabolismo(self):
        f = self.crear_layout_dual("Gasto Metabólico")
        e_p = self.crear_label_entry(f, "Peso (kg):"); e_a = self.crear_label_entry(f, "Altura (m):"); e_e = self.crear_label_entry(f, "Edad:")
        v_s = tk.StringVar(value="mujer"); self.crear_selector_segmentado(f, "Sexo:", ["mujer", "hombre"], v_s)
        v_ac = tk.StringVar(value="sedentario"); self.crear_selector_segmentado(f, "Actividad:", ["sedentario", "moderado", "atleta"], v_ac)
        def calc():
            try:
                c, h = calcular_metabolismo_y_agua(float(e_p.get()), float(e_a.get()), int(e_e.get()), v_s.get(), v_ac.get())
                detalles = {"TMB": f"{c} kcal/día", "AGUA": f"{h} litros/día", "MÉTODO": "Harris-Benedict", "SUGERENCIA": "Mantener hidratación constante según actividad."}
                self.actualizar_reporte("Metabolismo", detalles, self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR TMB", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_anemia(self):
        f = self.crear_layout_dual("Anemia")
        e_ed = self.crear_label_entry(f, "Edad:"); v_u = tk.StringVar(value="años"); self.crear_selector_segmentado(f, "Unidad:", ["años", "meses"], v_u)
        v_s = tk.StringVar(value="mujer"); self.crear_selector_segmentado(f, "Sexo:", ["mujer", "hombre"], v_s); e_h = self.crear_label_entry(f, "Hb (g/dL):")
        def calc():
            try:
                pos, mi, ma = diagnosticar_anemia(float(e_ed.get()), v_u.get(), v_s.get(), float(e_h.get()))
                detalles = {"RESULTADO": "ANEMIA DETECTADA" if pos else "NIVELES NORMALES", "RANGO REF": f"{mi} - {ma} g/dL", "ACCION": "Consultar hemograma completo si hay fatiga crónica."}
                self.actualizar_reporte("Hemoglobina", detalles, self.color_alerta if pos else self.color_primario)
            except: pass
        tk.Button(f, text="EVALUAR Hb", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_glucemia(self):
        f = self.crear_layout_dual("Glucosa")
        e_g = self.crear_label_entry(f, "Glucosa (mg/dL):"); v_e = tk.StringVar(value="ayunas"); self.crear_selector_segmentado(f, "Estado:", ["ayunas", "postprandial"], v_e)
        def calc():
            try:
                r = evaluar_glucemia(float(e_g.get()), v_e.get())
                detalles = {"DIAGNÓSTICO": r, "ESTADO": v_e.get().upper(), "METAS": "Ayunas: <100 | Post: <140", "NOTA": "Valores >200 postprandial sugieren Diabetes."}
                self.actualizar_reporte("Glucemia", detalles, self.color_alerta if "NORMAL" not in r else self.color_primario)
            except: pass
        tk.Button(f, text="EVALUAR GLUCOSA", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_cardio(self):
        f = self.crear_layout_dual("Perfil Lipídico")
        e_c = self.crear_label_entry(f, "Col. Total:"); e_h = self.crear_label_entry(f, "HDL:"); e_l = self.crear_label_entry(f, "LDL:"); e_t = self.crear_label_entry(f, "Triglicéridos:")
        def calc():
            try:
                e, r, i = evaluar_perfil_lipidico(float(e_c.get()), float(e_h.get()), float(e_l.get()), float(e_t.get()))
                detalles = {"ESTADO": e, "RIESGO": r, "ÍNDICE CASTELLI": i, "RECOMENDACIÓN": "Dieta baja en grasas saturadas si el LDL es >130."}
                self.actualizar_reporte("Lípidos", detalles, self.color_alerta if r == "Alto" else self.color_primario)
            except: pass
        tk.Button(f, text="ANALIZAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_bilirrubina(self):
        f = self.crear_layout_dual("Bilirrubina")
        e_d = self.crear_label_entry(f, "Directa:"); e_i = self.crear_label_entry(f, "Indirecta:")
        def calc():
            try:
                t, est, col = evaluar_bilirrubina(float(e_d.get()), float(e_i.get()))
                detalles = {"TOTAL": f"{t} mg/dL", "ESTADO": est, "SÍNTOMAS": "Observar ictericia en conjuntivas si el valor es >2.0."}
                self.actualizar_reporte("Perfil Hepático", detalles, self.color_alerta if col == "rojo" else self.color_primario)
            except: pass
        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_renal(self):
        f = self.crear_layout_dual("Función Renal (eTFG)")
        e_c = self.crear_label_entry(f, "Creatinina:"); e_e = self.crear_label_entry(f, "Edad:"); v_s = tk.StringVar(value="mujer"); self.crear_selector_segmentado(f, "Sexo:", ["mujer", "hombre"], v_s)
        def calc():
            try:
                v, est = calcular_tfg_avanzado(float(e_c.get()), int(e_e.get()), v_s.get())
                detalles = {"TFG ESTIMADA": f"{v} ml/min", "ESTADIO": est, "NOTA": "Estadío 3 o superior requiere ajuste de dosis farmacológicas."}
                self.actualizar_reporte("Informe Renal", detalles, self.color_alerta if v < 60 else self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR TFG", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_glasgow(self):
        f = self.crear_layout_dual("Escala de Glasgow")
        v_o = tk.IntVar(value=4); self.crear_selector_segmentado(f, "Ocular:", [1,2,3,4], v_o)
        v_v = tk.IntVar(value=5); self.crear_selector_segmentado(f, "Verbal:", [1,2,3,4,5], v_v)
        v_m = tk.IntVar(value=6); self.crear_selector_segmentado(f, "Motor:", [1,2,3,4,5,6], v_m)
        def calc():
            t, e, g = evaluar_glasgow(v_o.get(), v_v.get(), v_m.get())
            detalles = {"PUNTAJE": f"{t}/15", "TRAUMA": e, "CONDUCTA": g}
            self.actualizar_reporte("GCS", detalles, self.color_alerta if t < 9 else self.color_primario)
        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_dolor(self):
        f = self.crear_layout_dual("Dolor EVA")
        v_d = tk.IntVar(value=0); self.crear_selector_segmentado(f, "Intensidad:", list(range(11)), v_d)
        def calc():
            v, n, s = evaluar_dolor(v_d.get())
            detalles = {"NIVEL": n, "SUGERENCIA": s, "TIPO": "Escala Visual Analógica (EVA)"}
            self.actualizar_reporte("Dolor", detalles, self.color_alerta if v > 6 else self.color_primario)
        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_respiratorio(self):
        f = self.crear_layout_dual("Kirby (PAFI)")
        e_p = self.crear_label_entry(f, "PaO2:"); e_f = self.crear_label_entry(f, "FiO2 (%):")
        def calc():
            try:
                i, e = calcular_kirby(float(e_p.get()), float(e_f.get()))
                detalles = {"ÍNDICE": i, "ESTADO": e, "ALERTA": "Valores <200 indican SDRA moderado-grave."}
                self.actualizar_reporte("Función Pulmonar", detalles, self.color_alerta if i < 300 else self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_anion_gap(self):
        f = self.crear_layout_dual("Anión Gap")
        e_n = self.crear_label_entry(f, "Sodio (Na):"); e_c = self.crear_label_entry(f, "Cloro (Cl):"); e_b = self.crear_label_entry(f, "Bicarbonato (HCO3):")
        def calc():
            try:
                g, i = calcular_anion_gap(float(e_n.get()), float(e_c.get()), float(e_b.get()))
                detalles = {"ANION GAP": g, "INTERPRETACIÓN": i, "REFERENCIA": "Normal: 8-12 mEq/L"}
                self.actualizar_reporte("Equilibrio Ácido-Base", detalles, self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR GAP", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_deficit_agua(self):
        f = self.crear_layout_dual("Déficit de Agua")
        e_p = self.crear_label_entry(f, "Peso (kg):"); e_n = self.crear_label_entry(f, "Sodio actual (mEq/L):"); v_s = tk.StringVar(value="hombre"); self.crear_selector_segmentado(f, "Sexo:", ["hombre", "mujer"], v_s)
        def calc():
            try:
                r = calcular_deficit_agua(float(e_p.get()), float(e_n.get()), v_s.get())
                detalles = {"DÉFICIT TOTAL": f"{r} Litros", "META": "Sodio deseado: 140 mEq/L", "AVISO": "Reponer lentamente para evitar daño neurológico."}
                self.actualizar_reporte("Reposición Hídrica", detalles, self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_framingham(self):
        f = self.crear_layout_dual("Riesgo Cardiovascular")
        e_e = self.crear_label_entry(f, "Edad:"); v_s = tk.StringVar(value="hombre"); self.crear_selector_segmentado(f, "Sexo:", ["hombre", "mujer"], v_s)
        e_c = self.crear_label_entry(f, "Col. Total:"); e_h = self.crear_label_entry(f, "HDL:"); e_si = self.crear_label_entry(f, "Sistólica:"); e_di = self.crear_label_entry(f, "Diastólica:")
        v_f = tk.StringVar(value="no"); self.crear_selector_segmentado(f, "¿Fuma?", ["si", "no"], v_f)
        def calc():
            try:
                p, pct, n = evaluar_riesgo_framingham(v_s.get(), int(e_e.get()), float(e_c.get()), float(e_h.get()), v_f.get()=="si", int(e_si.get()), int(e_di.get()))
                detalles = {"PUNTAJE": p, "PROBABILIDAD": pct, "RIESGO": n, "SUGERENCIA": "Control estricto de factores de riesgo si es >10%."}
                self.actualizar_reporte("Framingham 10 Años", detalles, self.color_alerta if n == "ALTO" else self.color_primario)
            except: pass
        tk.Button(f, text="ESTIMAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_infusion(self):
        f = self.crear_layout_dual("Cálculo de Infusiones")
        e_v = self.crear_label_entry(f, "Volumen (ml):"); e_t = self.crear_label_entry(f, "Tiempo (h):")
        def calc():
            try:
                res = calcular_goteo(float(e_v.get()), float(e_t.get()))
                self.actualizar_reporte("Plan de Goteo", res, self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_pediatria(self):
        f = self.crear_layout_dual("Dosis Pediátrica")
        e_p = self.crear_label_entry(f, "Peso (kg):"); e_d = self.crear_label_entry(f, "Dosis (mg/kg):"); e_c = self.crear_label_entry(f, "Presentación (mg):"); e_v = self.crear_label_entry(f, "En volumen (ml):")
        def calc():
            try:
                ml, mg = calcular_dosis_pediatrica(float(e_p.get()), float(e_d.get()), float(e_c.get()), float(e_v.get()))
                detalles = {"DOSIS ML": f"{ml} ml", "DOSIS MG": f"{mg} mg", "ALERTA": "Verificar siempre con doble chequeo en pediatría."}
                self.actualizar_reporte("Dosificación", detalles, self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR DOSIS", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_superficie(self):
        f = self.crear_layout_dual("Superficie Corporal")
        e_p = self.crear_label_entry(f, "Peso (kg):"); e_a = self.crear_label_entry(f, "Altura (cm):")
        def calc():
            try:
                res = calcular_superficie_corporal(float(e_p.get()), float(e_a.get()))
                detalles = {"RESULTADO": f"{res} m²", "MÉTODO": "Mosteller", "USO": "Necesario para ajuste de quimioterapia y fluidos."}
                self.actualizar_reporte("BSA", detalles, self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR BSA", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_conversor(self):
        f = self.crear_layout_dual("Conversor de Unidades")
        e_v = self.crear_label_entry(f, "Valor:"); v_t = tk.StringVar(value="glucosa"); self.crear_selector_segmentado(f, "Tipo:", ["glucosa", "colesterol", "triglicéridos"], v_t)
        v_d = tk.StringVar(value="mg_a_mmol"); self.crear_selector_segmentado(f, "Dirección:", ["mg/dL a mmol/L", "mmol/L a mg/dL"], v_d)
        def calc():
            try:
                val = float(e_v.get()); d = "mg_a_mmol" if "a mmol/L" in v_d.get() else "mmol_a_mg"
                if v_t.get() == "glucosa": r, u = convertir_glucosa(val, d)
                elif v_t.get() == "colesterol": r, u = convertir_lipidos(val, d)
                else: r, u = convertir_trigliceridos(val, d)
                self.actualizar_reporte("Conversión", {"RESULTADO": f"{r} {u}"}, self.color_primario)
            except: pass
        tk.Button(f, text="CONVERTIR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_ciclo(self):
        f = self.crear_layout_dual("Calendario de Fertilidad")
        e_d = self.crear_label_entry(f, "Días promedio del ciclo:")
        def calc():
            try:
                d, v = calcular_ovulacion(int(e_d.get()))
                detalles = {"DÍA OVULACIÓN": f"Día {d}", "VENTANA FÉRTIL": v, "INFO": "Cálculo basado en método de calendario estándar."}
                self.actualizar_reporte("Fertilidad", detalles, self.color_primario)
            except: pass
        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"), command=calc).pack(fill="x", pady=20, ipady=12)