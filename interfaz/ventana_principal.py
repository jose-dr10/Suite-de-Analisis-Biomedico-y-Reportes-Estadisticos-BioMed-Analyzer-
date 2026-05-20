import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import matplotlib
matplotlib.use("TkAgg")  # Forzar el backend compatible con Tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches
# --- IMPORTES DE LÓGICA ---
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

        # Almacén de referencias de botones de la barra lateral para gestionar estados activos
        self.botones_menu = {}

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
                # Modificamos el comando para pasar por un gestor que controle el color activo del botón seleccionado
                btn = tk.Button(
                    self.sidebar,
                    text=texto,
                    command=lambda cmd=comando, txt=texto: self.ejecutar_y_resaltar(cmd, txt),
                    bg=self.color_primario,
                    fg="white",
                    bd=0,
                    font=self.fuente_ui,
                    cursor="hand2",
                    pady=4,
                    anchor="w",
                    padx=25,
                    activebackground=self.color_categoria,
                    activeforeground="white"
                )
                btn.pack(fill="x")
                self.botones_menu[texto] = btn

        self.contenedor = tk.Frame(self.root, bg=self.color_fondo)
        self.contenedor.pack(side="right", expand=True, fill="both", padx=30, pady=30)
        self.mostrar_bienvenida()

    # --- MÉTODOS DE APOYO UI ---
    def ejecutar_y_resaltar(self, comando, texto_boton):
        # Restablecemos todos los botones al fondo primario predeterminado
        for btn in self.botones_menu.values():
            btn.configure(bg=self.color_primario)
        # Resaltamos de forma fija el botón que el usuario ha seleccionado
        self.botones_menu[texto_boton].configure(bg=self.color_categoria)
        # Ejecutamos la llamada correspondiente de la interfaz
        comando()

    def limpiar_contenedor(self):
        # Restauramos los márgenes por defecto (30px) para que los módulos sigan viéndose perfectos
        self.contenedor.pack_configure(padx=30, pady=30)
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def crear_layout_dual(self, titulo_modulo):
        self.limpiar_contenedor()
        tk.Label(self.contenedor, text=titulo_modulo.upper(), bg=self.color_fondo,
                 font=self.fuente_titular, fg=self.color_primario).pack(anchor="w", pady=(0, 25))
        cuerpo = tk.Frame(self.contenedor, bg=self.color_fondo)
        cuerpo.pack(fill="both", expand=True)
        f_form = tk.Frame(cuerpo, bg=self.color_card, padx=25, pady=25, highlightthickness=1,
                          highlightbackground="#e0e0e0")
        f_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        f_res = tk.Frame(cuerpo, bg=self.color_card, padx=30, pady=30, highlightthickness=1,
                         highlightbackground="#e0e0e0", width=420)
        f_res.pack(side="right", fill="both", expand=False)
        f_res.pack_propagate(False)
        self.area_reporte = tk.Frame(f_res, bg=self.color_card)
        self.area_reporte.pack(fill="both", expand=True)

        # Mostramos por defecto el mensaje de espera de datos en la barra lateral de resultados
        self.mostrar_esperando_datos()
        return f_form

    def mostrar_esperando_datos(self):
        for widget in self.area_reporte.winfo_children():
            widget.destroy()

        f_espera = tk.Frame(self.area_reporte, bg=self.color_card)
        f_espera.pack(expand=True, fill="both")

        tk.Label(
            f_espera,
            text="⏳",
            font=("Helvetica", 24),
            fg=self.color_primario,
            bg=self.color_card
        ).pack(pady=(60, 10))

        tk.Label(
            f_espera,
            text="Esperando datos del usuario...",
            font=("Helvetica", 10, "bold"),
            fg="#9da1b0",
            bg=self.color_card,
            justify="center"
        ).pack()

        tk.Label(
            f_espera,
            text="",
            font=("Helvetica", 8),
            fg="#b0b4c3",
            bg=self.color_card,
            wraplength=280,
            justify="center"
        ).pack(pady=(10, 0))

    def mostrar_error_validacion(self, detalles_error):
        for widget in self.area_reporte.winfo_children():
            widget.destroy()

        f_error = tk.Frame(self.area_reporte, bg=self.color_card)
        f_error.pack(expand=True, fill="both")

        tk.Label(
            f_error,
            text="⚠️",
            font=("Helvetica", 24),
            fg=self.color_alerta,
            bg=self.color_card
        ).pack(pady=(60, 10))

        tk.Label(
            f_error,
            text="DATOS INCOHERENTES DETECTADOS",
            font=("Helvetica", 10, "bold"),
            fg=self.color_alerta,
            bg=self.color_card,
            justify="center"
        ).pack()

        tk.Label(
            f_error,
            text=detalles_error,
            font=("Helvetica", 9),
            fg=self.color_texto,
            bg=self.color_card,
            wraplength=280,
            justify="center"
        ).pack(pady=(10, 0))

    def actualizar_reporte(self, titulo, datos, color):
        for widget in self.area_reporte.winfo_children():
            widget.destroy()
        tk.Label(self.area_reporte, text=titulo.upper(), font=self.fuente_res_titulo, fg=color,
                 bg=self.color_card).pack(anchor="w", pady=(0, 15))
        for etiqueta, valor in datos.items():
            f_fila = tk.Frame(self.area_reporte, bg=self.color_card)
            f_fila.pack(fill="x", pady=2)
            tk.Label(f_fila, text=etiqueta, font=self.fuente_res_label, fg="#a0a0a0", bg=self.color_card).pack(
                anchor="w")
            tk.Label(f_fila, text=str(valor), font=self.fuente_res_info, fg=self.color_texto, bg=self.color_card,
                     wraplength=350, justify="left").pack(anchor="w", pady=(0, 5))

    def crear_label_entry(self, master, texto):
        tk.Label(master, text=texto, bg=self.color_card, font=self.fuente_ui, fg="#5f6368").pack(anchor="w",
                                                                                                 pady=(5, 0))
        ent = tk.Entry(master, bg=self.color_input, bd=0, font=self.fuente_ui, fg=self.color_texto)
        ent.pack(fill="x", pady=(2, 8), ipady=6)
        return ent

    def crear_selector_segmentado(self, master, etiqueta, opciones, variable_tk):
        tk.Label(master, text=etiqueta, bg=self.color_card, font=self.fuente_ui, fg="#5f6368").pack(anchor="w",
                                                                                                    pady=(5, 0))
        f_selector = tk.Frame(master, bg=self.color_card)
        f_selector.pack(fill="x", pady=(5, 10))
        botones_dict = {}

        def actualizar_colores(seleccionado):
            variable_tk.set(seleccionado)
            for opt, btn in botones_dict.items():
                if str(opt) == str(seleccionado):
                    btn.configure(bg=self.color_primario, fg="white")
                else:
                    btn.configure(bg=self.color_desactivado, fg=self.color_texto)

        for opcion in opciones:
            btn = tk.Button(f_selector, text=str(opcion).capitalize(), bd=0, font=self.fuente_ui, cursor="hand2",
                            pady=5)
            btn.configure(command=lambda o=opcion: actualizar_colores(o))
            btn.pack(side="left", expand=True, fill="x", padx=1)
            botones_dict[opcion] = btn
        actualizar_colores(variable_tk.get())

    # --- DE BIENVENIDA ACTUALIZADO - SIN MARCOS EXTERNOS ---
    def mostrar_bienvenida(self):
        self.limpiar_contenedor()

        # Al volver a la bienvenida, limpiamos el resaltado fijo de la barra lateral
        for btn in self.botones_menu.values():
            btn.configure(bg=self.color_primario)

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

    # --- MÉTODOS DE CÁLCULO CON LIMITACIONES DE SEGURIDAD ---

   #presion
    def mostrar_presion(self):
        f = self.crear_layout_dual("Presión Arterial")
        e_s = self.crear_label_entry(f, "Sistólica (mmHg):")
        e_d = self.crear_label_entry(f, "Diastólica (mmHg):")

        def calc():
            try:
                sis = int(e_s.get())
                dia = int(e_d.get())

                # Validación de rangos humanos posibles para presión arterial
                if not (40 <= sis <= 300) or not (20 <= dia <= 200) or (sis <= dia):
                    self.mostrar_error_validacion(
                        "Valores de presión imposibles o incoherentes.\n"
                        "Sistólica debe ser mayor a Diastólica.\n"
                        "Rangos: Sis (40-300), Dia (20-200)."
                    )
                    return

                r, s = evaluar_presion_arterial(sis, dia)
                detalles = {
                    "DIAGNÓSTICO": r.upper(),
                    "RIESGO": s,
                    "REFERENCIA": "Normal: <120/80 mmHg",
                    "RECOMENDACIÓN": "Reducir sodio y monitorear si hay cefalea o mareos."
                }

                # Pintamos primero el reporte de texto normal
                color_tema = self.color_alerta if "Hipertensión" in r or "Crisis" in r else self.color_primario
                self.actualizar_reporte("Informe Tensional", detalles, color_tema)

                # --- CONSTRUCCIÓN DEL GRÁFICO ESTADÍSTICO DE PRESIÓN ---
                fig, ax = plt.subplots(figsize=(4.2, 3.2), dpi=100)
                fig.patch.set_facecolor(self.color_card)  # Fondo blanco igual a la tarjeta
                ax.set_facecolor("#fcfcfc")

                # Dibujamos las zonas de riesgo (rectángulos de fondo sutiles)
                # 1. Normal (Verde)
                ax.add_patch(patches.Rectangle((40, 40), 40, 80, color="#e2fbeb", alpha=0.9, zorder=1))
                # 2. Elevada (Amarillo)
                ax.add_patch(patches.Rectangle((40, 120), 40, 10, color="#fff9db", alpha=0.9, zorder=1))
                # 3. Estadio 1 (Naranja claro)
                ax.add_patch(patches.Rectangle((80, 40), 10, 100, color="#ffe8cc", alpha=0.9, zorder=1))
                ax.add_patch(patches.Rectangle((40, 130), 50, 10, color="#ffe8cc", alpha=0.9, zorder=1))
                # 4. Estadio 2 (Rojo sutil)
                ax.add_patch(patches.Rectangle((90, 40), 30, 140, color="#ffdee2", alpha=0.9, zorder=1))
                ax.add_patch(patches.Rectangle((40, 140), 50, 40, color="#ffdee2", alpha=0.9, zorder=1))
                # 5. Crisis (Rojo fuerte)
                ax.add_patch(patches.Rectangle((40, 180), 160, 120, color="#fcc2cb", alpha=0.9, zorder=1))
                ax.add_patch(patches.Rectangle((120, 40), 80, 260, color="#fcc2cb", alpha=0.9, zorder=1))

                # Graficar el punto del paciente (resaltado)
                ax.scatter(dia, sis, color=self.color_primario, s=120, edgecolor="white", linewidth=2.5, zorder=5,
                           label="Paciente")

                # Configuración de límites y etiquetas estéticas
                ax.set_xlim(40, 140)
                ax.set_ylim(60, 220)
                ax.set_xlabel("Diastólica (mmHg)", fontsize=8, color="#5f6368", fontweight="bold")
                ax.set_ylabel("Sistólica (mmHg)", fontsize=8, color="#5f6368", fontweight="bold")
                ax.tick_params(colors="#5f6368", labelsize=7)

                # Ocultamos las líneas de los bordes para un acabado plano moderno
                for spine in ["top", "right"]:
                    ax.spines[spine].set_visible(False)
                for spine in ["left", "bottom"]:
                    ax.spines[spine].set_color("#e0e0e0")

                # Etiquetas de texto informativas dentro del gráfico
                ax.text(60, 95, "Normal", fontsize=7, color="#2b8a3e", fontweight="bold", alpha=0.7, zorder=2)
                ax.text(100, 155, "Estadio 2", fontsize=7, color="#c92a2a", fontweight="bold", alpha=0.7, zorder=2)
                ax.text(60, 195, "CRISIS", fontsize=7, color="#a61e4d", fontweight="bold", alpha=0.8, zorder=2)

                fig.tight_layout()

                # Añadir y dibujar el gráfico en Tkinter (debajo de los resultados de texto)
                canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_reporte)
                canvas_grafico.draw()
                canvas_grafico.get_tk_widget().pack(fill="both", expand=True, pady=(15, 0))

                # Liberamos memoria del gráfico cerrado para evitar sobrecarga en la app
                plt.close(fig)

            except ValueError:
                self.mostrar_error_validacion("Por favor, ingrese valores numéricos enteros válidos.")

        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)
    #presion
#nutricion
    def mostrar_nutricion(self):
        f = self.crear_layout_dual("Estado Nutricional")
        e_p = self.crear_label_entry(f, "Peso (kg):")
        e_t = self.crear_label_entry(f, "Talla (m):")

        def calc():
            try:
                # 1. Recuperar datos de la interfaz
                peso = float(e_p.get())
                talla = float(e_t.get())

                # Validación de rangos biológicos realistas
                if not (10 <= peso <= 350) or not (0.5 <= talla <= 2.5):
                    self.mostrar_error_validacion(
                        "Valores de peso o talla fuera de rango.\n"
                        "Límites permitidos:\n"
                        "- Peso: 10 a 350 kg\n"
                        "- Talla: 0.5 a 2.5 metros (use punto para decimales)."
                    )
                    return

                # 2. CÁLCULO DIRECTO AQUÍ (Evita NameError de importación)
                imc = peso / (talla ** 2)

                # Clasificación estándar de la OMS
                if imc < 18.5:
                    r = "Bajo peso"
                    s = "Riesgo de deficiencias nutricionales. Se recomienda valoración médica."
                elif 18.5 <= imc < 25.0:
                    r = "Peso normal"
                    s = "¡Excelente! Estado nutricional óptimo y saludable."
                elif 25.0 <= imc < 30.0:
                    r = "Sobrepeso"
                    s = "Riesgo moderado de desarrollar problemas metabólicos."
                else:
                    r = "Obesidad"
                    s = "Riesgo alto de enfermedades cardiovasculares y metabólicas."

                detalles = {
                    "IMC CALCULADO": f"{imc:.1f} kg/m²",
                    "DIAGNÓSTICO": r.upper(),
                    "ESTADO": s,
                    "REFERENCIA": "Normal: 18.5 - 24.9 kg/m²",
                    "RECOMENDACIÓN": "Mantener una dieta balanceada y actividad física regular."
                }

                # Definir color del reporte según el riesgo
                color_tema = self.color_alerta if "Sobrepeso" in r or "Obesidad" in r else self.color_primario
                self.actualizar_reporte("Informe Nutricional", detalles, color_tema)

                # --- 3. CONSTRUCCIÓN DEL GRÁFICO ESTADÍSTICO DE RANGO (IMC) ---
                fig, ax = plt.subplots(figsize=(4.2, 2.0), dpi=100)
                fig.patch.set_facecolor(self.color_card)  # Fondo de la tarjeta
                ax.set_facecolor(self.color_card)

                # Dibujamos las franjas de color sutiles de fondo (Rango de IMC de 10 a 40)
                # Bajo peso (10 a 18.5) -> Azul sutil
                ax.barh(0, 8.5, left=10, height=0.35, color="#e6f2ff", edgecolor="none")
                # Normal (18.5 a 25) -> Verde sutil
                ax.barh(0, 6.5, left=18.5, height=0.35, color="#e2fbeb", edgecolor="none")
                # Sobrepeso (25 a 30) -> Amarillo sutil
                ax.barh(0, 5.0, left=25, height=0.35, color="#fff9db", edgecolor="none")
                # Obesidad (30 a 40) -> Rojo sutil
                ax.barh(0, 10.0, left=30, height=0.35, color="#ffdee2", edgecolor="none")

                # Acotamos el IMC gráficamente entre 10 y 40 para que el pin no se salga del dibujo
                imc_grafico = max(10, min(imc, 40))

                # Dibujamos el indicador del paciente (Línea vertical oscura con marcador de pin)
                ax.vlines(imc_grafico, -0.25, 0.25, colors="#202124", linewidth=2.5, zorder=5)
                ax.scatter(imc_grafico, 0.23, marker="v", color="#202124", s=80, zorder=5)

                # Agregamos los nombres de las zonas sobre cada barra
                ax.text(14.25, 0.25, "Bajo", fontsize=7, color="#1a73e8", ha="center", fontweight="bold")
                ax.text(21.75, 0.25, "Normal", fontsize=7, color="#2b8a3e", ha="center", fontweight="bold")
                ax.text(27.5, 0.25, "Sobrepeso", fontsize=7, color="#f59f00", ha="center", fontweight="bold")
                ax.text(35.0, 0.25, "Obesidad", fontsize=7, color="#c92a2a", ha="center", fontweight="bold")

                # Caja de texto flotante con el IMC numérico actual justo debajo de la línea indicador
                ax.text(imc_grafico, -0.32, f"{imc:.1f}", fontsize=8, color="#202124",
                        ha="center", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#e0e0e0", lw=0.8))

                # Ajustes de límites y estética minimalista (sin bordes toscos)
                ax.set_xlim(10, 40)
                ax.set_ylim(-0.45, 0.4)

                # Apagamos el eje Y y limpiamos los spines sobrantes
                ax.get_yaxis().set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["top"].set_visible(False)
                ax.spines["bottom"].set_color("#e0e0e0")
                ax.tick_params(colors="#5f6368", labelsize=7)
                ax.set_xlabel("Índice de Masa Corporal (kg/m²)", fontsize=8, color="#5f6368", fontweight="bold")

                fig.tight_layout()

                # 4. Acoplar y pintar el gráfico de Matplotlib dentro de self.area_reporte
                canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_reporte)
                canvas_grafico.draw()
                canvas_grafico.get_tk_widget().pack(fill="x", expand=True, pady=(15, 0))

                # Liberar memoria de la figura para no sobrecargar la RAM
                plt.close(fig)

            except ValueError:
                self.mostrar_error_validacion("Por favor, ingrese valores numéricos válidos.")

        # Botón de evaluar con los estilos del sistema
        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)
    #nutricion

#ica
    def mostrar_ica(self):
        f = self.crear_layout_dual("Riesgo por Medidas (ICA)")
        e_c = self.crear_label_entry(f, "Cintura (cm):")
        e_a = self.crear_label_entry(f, "Altura (cm):")

        def calc():
            try:
                cintura = float(e_c.get())
                altura = float(e_a.get())

                # Validación de medidas físicas reales
                if not (20.0 <= cintura <= 250.0) or not (30.0 <= altura <= 280.0):
                    self.mostrar_error_validacion(
                        "Medidas antropométricas fuera de rango.\n"
                        "Rangos: Cintura (20-250 cm), Altura (30-280 cm)."
                    )
                    return

                # Lógica de cálculo integrada
                v = cintura / altura

                if v <= 0.42:
                    e = "Delgadez extrema / Subpeso"
                    r = "Bajo riesgo cardiovascular, pero evaluar posible desnutrición."
                elif 0.42 < v <= 0.50:
                    e = "Saludable / Peso Normal"
                    r = "Bajo riesgo cardiovascular y metabólico."
                elif 0.50 < v <= 0.60:
                    e = "Sobrepeso / Adiposidad elevada"
                    r = "Riesgo moderado de desarrollar diabetes e hipertensión."
                else:
                    e = "Obesidad abdominal / Riesgo elevado"
                    r = "Riesgo alto de eventos coronarios y síndrome metabólico."

                detalles = {
                    "ICA CALCULADO": f"{v:.2f}",
                    "ESTADO": e,
                    "RIESGO CV": r,
                    "REFERENCIA CLINICA": "Saludable: Menor o igual a 0.50",
                    "NOTA": "El ICA es más preciso que el IMC para estimar el riesgo cardíaco real."
                }

                color_tema = self.color_alerta if v > 0.50 else self.color_primario
                self.actualizar_reporte("Índice Cintura-Altura", detalles, color_tema)

                # --- GRÁFICO ESTADÍSTICO DE RANGO (ICA) ---
                fig, ax = plt.subplots(figsize=(4.2, 2.0), dpi=100)
                fig.patch.set_facecolor(self.color_card)
                ax.set_facecolor(self.color_card)

                # Franjas de color sutiles (Rango de ICA de 0.3 a 0.8)
                ax.barh(0, 0.12, left=0.3, height=0.35, color="#e6f2ff", edgecolor="none")
                ax.barh(0, 0.08, left=0.42, height=0.35, color="#e2fbeb", edgecolor="none")
                ax.barh(0, 0.10, left=0.50, height=0.35, color="#fff9db", edgecolor="none")
                ax.barh(0, 0.20, left=0.60, height=0.35, color="#ffdee2", edgecolor="none")

                ica_grafico = max(0.3, min(v, 0.8))

                ax.vlines(ica_grafico, -0.25, 0.25, colors="#202124", linewidth=2.5, zorder=5)
                ax.scatter(ica_grafico, 0.23, marker="v", color="#202124", s=80, zorder=5)

                ax.text(0.36, 0.25, "Bajo", fontsize=7, color="#1a73e8", ha="center", fontweight="bold")
                ax.text(0.46, 0.25, "Normal", fontsize=7, color="#2b8a3e", ha="center", fontweight="bold")
                ax.text(0.55, 0.25, "Moderado", fontsize=7, color="#f59f00", ha="center", fontweight="bold")
                ax.text(0.70, 0.25, "Riesgo Alto", fontsize=7, color="#c92a2a", ha="center", fontweight="bold")

                ax.text(ica_grafico, -0.32, f"{v:.2f}", fontsize=8, color="#202124",
                        ha="center", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#e0e0e0", lw=0.8))

                ax.set_xlim(0.3, 0.8)
                ax.set_ylim(-0.45, 0.4)

                ax.get_yaxis().set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["top"].set_visible(False)
                ax.spines["bottom"].set_color("#e0e0e0")
                ax.tick_params(colors="#5f6368", labelsize=7)
                ax.set_xlabel("Índice Cintura-Altura (Valor adimensional)", fontsize=8, color="#5f6368",
                              fontweight="bold")

                fig.tight_layout()

                canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_reporte)
                canvas_grafico.draw()
                canvas_grafico.get_tk_widget().pack(fill="x", expand=True, pady=(15, 0))

                plt.close(fig)

            except ValueError:
                self.mostrar_error_validacion("Por favor, ingrese valores numéricos de medida válidos.")

        tk.Button(f, text="CALCULAR ICA", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_metabolismo(self):
        f = self.crear_layout_dual("Gasto Metabólico")
        e_p = self.crear_label_entry(f, "Peso (kg):")
        e_a = self.crear_label_entry(f, "Altura (m):")
        e_e = self.crear_label_entry(f, "Edad:")

        v_s = tk.StringVar(value="mujer")
        self.crear_selector_segmentado(f, "Sexo:", ["mujer", "hombre"], v_s)

        v_ac = tk.StringVar(value="sedentario")
        self.crear_selector_segmentado(f, "Actividad:", ["sedentario", "moderado", "atleta"], v_ac)

        def calc():
            try:
                peso = float(e_p.get())
                altura = float(e_a.get())
                edad = int(e_e.get())
                sexo = v_s.get()
                actividad = v_ac.get()

                # Validación metabólica
                if not (2.0 <= peso <= 500.0) or not (0.3 <= altura <= 2.8) or not (0 <= edad <= 125):
                    self.mostrar_error_validacion(
                        "Valores fuera de los límites de cálculo.\n"
                        "Rangos: Peso (2-500 kg), Altura (0.3-2.8 m), Edad (0-125 años)."
                    )
                    return

                # --- LÓGICA DE CÁLCULO INTEGRADA (Ecuación de Harris-Benedict) ---
                # Convertimos altura a cm para la fórmula tradicional
                altura_cm = altura * 100.0

                if sexo == "hombre":
                    tmb = 88.362 + (13.397 * peso) + (4.799 * altura_cm) - (5.677 * edad)
                else:
                    tmb = 447.593 + (9.247 * peso) + (3.098 * altura_cm) - (4.330 * edad)

                # Factor de actividad
                factores = {
                    "sedentario": 1.2,
                    "moderado": 1.55,
                    "atleta": 1.9
                }
                factor = factores.get(actividad, 1.2)
                gasto_total = tmb * factor

                # Requerimiento de Agua aproximado (35ml por kg de peso)
                agua = (peso * 35) / 1000.0

                detalles = {
                    "METABOLISMO BASAL (TMB)": f"{int(tmb)} kcal/día",
                    "GASTO ENERGÉTICO TOTAL": f"{int(gasto_total)} kcal/día",
                    "REQUERIMIENTO DE AGUA": f"{agua:.2f} litros/día",
                    "MÉTODO APLICADO": "Harris-Benedict (Revisado)",
                    "SUGERENCIA": "Consuma la cantidad de calorías totales si desea mantener su peso actual."
                }

                self.actualizar_reporte("Metabolismo e Hidratación", detalles, self.color_primario)

                # --- GRÁFICO ESTADÍSTICO COMPARATIVO DE CALORÍAS ---
                fig, ax = plt.subplots(figsize=(4.2, 2.0), dpi=100)
                fig.patch.set_facecolor(self.color_card)
                ax.set_facecolor("#fcfcfc")

                # Barras comparativas
                categorias = ["Basal (TMB)", "Gasto Total"]
                valores = [tmb, gasto_total]
                colores = [self.color_primario, "#11caa0"]  # Azul tema y un verde clínico brillante

                bars = ax.barh(categorias, valores, color=colores, height=0.5, edgecolor="none")

                # Agregar etiquetas numéricas dentro/junto a las barras
                for bar in bars:
                    width = bar.get_width()
                    ax.text(width - (width * 0.15), bar.get_y() + bar.get_height() / 2,
                            f"{int(width)} kcal",
                            va="center", ha="right", color="white", fontsize=8, fontweight="bold")

                # Estética minimalista del gráfico de barras
                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["bottom"].set_color("#e0e0e0")
                ax.tick_params(colors="#5f6368", labelsize=8)
                ax.set_xlabel("Calorías diarias (kcal)", fontsize=8, color="#5f6368", fontweight="bold")

                fig.tight_layout()

                # Acoplar en Tkinter
                canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_reporte)
                canvas_grafico.draw()
                canvas_grafico.get_tk_widget().pack(fill="x", expand=True, pady=(15, 0))

                plt.close(fig)

            except ValueError:
                self.mostrar_error_validacion("Por favor, rellene todos los campos con números adecuados.")

        tk.Button(f, text="CALCULAR TMB", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)
    #ica

#anemia
    def mostrar_anemia(self):
        f = self.crear_layout_dual("Evaluación de Anemia")
        e_h = self.crear_label_entry(f, "Hemoglobina (g/dL):")

        v_s = tk.StringVar(value="mujer")
        self.crear_selector_segmentado(f, "Sexo:", ["mujer", "hombre"], v_s)

        def calc():
            try:
                hb = float(e_h.get())
                sexo = v_s.get()

                # Validación de rangos biológicos lógicos para hemoglobina
                if not (2.0 <= hb <= 25.0):
                    self.mostrar_error_validacion(
                        "Valor de hemoglobina fuera de rango biológico viable.\n"
                        "Rango aceptado: 2.0 a 25.0 g/dL."
                    )
                    return

                # --- LÓGICA DE CÁLCULO INTEGRADA ---
                if sexo == "hombre":
                    limite_anemia = 13.0
                    limite_severa = 8.0
                    if hb < 8.0:
                        r = "Anemia Severa"
                        s = "Riesgo crítico. Requiere evaluación médica urgente."
                    elif 8.0 <= hb < 11.0:
                        r = "Anemia Moderada"
                        s = "Requiere investigación etiológica y tratamiento."
                    elif 11.0 <= hb < 13.0:
                        r = "Anemia Leve"
                        s = "Evaluar depósitos de hierro (Ferritina) y dieta."
                    else:
                        r = "Normal"
                        s = "Nivel de hemoglobina adecuado para hombres."
                else:  # mujer
                    limite_anemia = 12.0
                    limite_severa = 8.0
                    if hb < 8.0:
                        r = "Anemia Severa"
                        s = "Riesgo crítico. Requiere evaluación médica urgente."
                    elif 8.0 <= hb < 11.0:
                        r = "Anemia Moderada"
                        s = "Requiere investigación clínica y suplementación."
                    elif 11.0 <= hb < 12.0:
                        r = "Anemia Leve"
                        s = "Monitorear pérdidas y optimizar ingesta de hierro."
                    else:
                        r = "Normal"
                        s = "Nivel de hemoglobina adecuado para mujeres."

                detalles = {
                    "HEMOGLOBINA": f"{hb:.1f} g/dL",
                    "DIAGNÓSTICO": r.upper(),
                    "ESTADO CLÍNICO": s,
                    "REFERENCIA OMS": f"Normal: >= {limite_anemia:.1f} g/dL ({sexo.capitalize()})",
                    "RECOMENDACIÓN": "La interpretación debe correlacionarse con volumen corpuscular medio (VCM)."
                }

                # Pintar el reporte (Rojo si hay anemia, azul si está normal)
                color_tema = self.color_alerta if "Anemia" in r else self.color_primario
                self.actualizar_reporte("Informe de Serie Roja", detalles, color_tema)

                # --- CONSTRUCCIÓN DEL GRÁFICO DINÁMICO ---
                fig, ax = plt.subplots(figsize=(4.2, 2.0), dpi=100)
                fig.patch.set_facecolor(self.color_card)
                ax.set_facecolor(self.color_card)

                # Ajustar dinámicamente las barras según el sexo
                if sexo == "hombre":
                    # Severa (2 a 8) -> Rojo
                    ax.barh(0, 6.0, left=2.0, height=0.35, color="#fcc2cb", edgecolor="none")
                    # Moderada/Leve (8 a 13) -> Amarillo/Naranja sutil
                    ax.barh(0, 5.0, left=8.0, height=0.35, color="#fff9db", edgecolor="none")
                    # Normal (13 a 18) -> Verde sutil
                    ax.barh(0, 5.0, left=13.0, height=0.35, color="#e2fbeb", edgecolor="none")

                    # Etiquetas de texto de rangos
                    ax.text(5.0, 0.25, "Severa", fontsize=7, color="#c92a2a", ha="center", fontweight="bold")
                    ax.text(10.5, 0.25, "Anemia", fontsize=7, color="#f59f00", ha="center", fontweight="bold")
                    ax.text(15.5, 0.25, "Normal", fontsize=7, color="#2b8a3e", ha="center", fontweight="bold")
                else:
                    # Severa (2 a 8) -> Rojo
                    ax.barh(0, 6.0, left=2.0, height=0.35, color="#fcc2cb", edgecolor="none")
                    # Moderada/Leve (8 a 12) -> Amarillo/Naranja sutil
                    ax.barh(0, 4.0, left=8.0, height=0.35, color="#fff9db", edgecolor="none")
                    # Normal (12 a 18) -> Verde sutil
                    ax.barh(0, 6.0, left=12.0, height=0.35, color="#e2fbeb", edgecolor="none")

                    # Etiquetas de texto de rangos
                    ax.text(5.0, 0.25, "Severa", fontsize=7, color="#c92a2a", ha="center", fontweight="bold")
                    ax.text(10.0, 0.25, "Anemia", fontsize=7, color="#f59f00", ha="center", fontweight="bold")
                    ax.text(15.0, 0.25, "Normal", fontsize=7, color="#2b8a3e", ha="center", fontweight="bold")

                # Acotar valor para que no se desborde el pin en hemoglobinas extremadamente altas/bajas
                hb_grafico = max(2.0, min(hb, 18.0))

                # Dibujar pin indicador del paciente
                ax.vlines(hb_grafico, -0.25, 0.25, colors="#202124", linewidth=2.5, zorder=5)
                ax.scatter(hb_grafico, 0.23, marker="v", color="#202124", s=80, zorder=5)

                # Caja flotante con el valor actual de Hb
                ax.text(hb_grafico, -0.32, f"{hb:.1f}", fontsize=8, color="#202124",
                        ha="center", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#e0e0e0", lw=0.8))

                # Configuración estética minimalista
                ax.set_xlim(2.0, 18.0)
                ax.set_ylim(-0.45, 0.4)

                ax.get_yaxis().set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["top"].set_visible(False)
                ax.spines["bottom"].set_color("#e0e0e0")
                ax.tick_params(colors="#5f6368", labelsize=7)
                ax.set_xlabel("Nivel de Hemoglobina (g/dL)", fontsize=8, color="#5f6368", fontweight="bold")

                fig.tight_layout()

                # Acoplar el gráfico en el panel derecho de la interfaz
                canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_reporte)
                canvas_grafico.draw()
                canvas_grafico.get_tk_widget().pack(fill="x", expand=True, pady=(15, 0))

                plt.close(fig)

            except ValueError:
                self.mostrar_error_validacion("Por favor, ingrese un valor numérico válido para hemoglobina.")

        tk.Button(f, text="EVALUAR HEMOGLOBINA", bg=self.color_primario, fg="white", bd=0,
                  font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_glucemia(self):
        f = self.crear_layout_dual("Niveles de Glucosa")
        e_g = self.crear_label_entry(f, "Glucosa (mg/dL):")

        v_e = tk.StringVar(value="ayunas")
        self.crear_selector_segmentado(f, "Estado:", ["ayunas", "postprandial"], v_e)

        def calc():
            try:
                glucosa = float(e_g.get())
                estado = v_e.get()

                # Validación de rangos biológicos lógicos para glucosa en sangre
                if not (10.0 <= glucosa <= 1000.0):
                    self.mostrar_error_validacion(
                        "Valor de glucosa fuera de rango biológico viable.\n"
                        "Rango aceptado: 10 a 1000 mg/dL."
                    )
                    return

                # --- LÓGICA DE CÁLCULO INTEGRADA (Criterios ADA) ---
                if estado == "ayunas":
                    if glucosa < 70:
                        r = "Hipoglucemia"
                        s = "Nivel críticamente bajo. Consuma carbohidratos de absorción rápida de inmediato."
                        color_tema = self.color_alerta
                    elif 70 <= glucosa < 100:
                        r = "Normal"
                        s = "¡Excelente! Nivel de glucosa en ayunas óptimo."
                        color_tema = self.color_primario
                    elif 100 <= glucosa < 126:
                        r = "Prediabetes (Glucosa alterada en ayunas)"
                        s = "Riesgo moderado. Se recomienda mejorar hábitos alimenticios y consultar al médico."
                        color_tema = self.color_alerta
                    else:
                        r = "Diabetes Mellitus (Sospecha clínica)"
                        s = "Riesgo alto. Requiere confirmación diagnóstica con prueba HbA1c o curva de tolerancia."
                        color_tema = self.color_alerta
                else:  # postprandial (2 horas después de comer)
                    if glucosa < 70:
                        r = "Hipoglucemia"
                        s = "Nivel críticamente bajo para estado postprandial."
                        color_tema = self.color_alerta
                    elif 70 <= glucosa < 140:
                        r = "Normal"
                        s = "Nivel de glucosa postprandial dentro del rango esperado."
                        color_tema = self.color_primario
                    elif 140 <= glucosa < 200:
                        r = "Prediabetes (Tolerancia alterada a la glucosa)"
                        s = "Riesgo moderado. Monitoree de cerca la ingesta de carbohidratos simples."
                        color_tema = self.color_alerta
                    else:
                        r = "Diabetes Mellitus (Sospecha clínica)"
                        s = "Riesgo alto de complicaciones micro y macrovasculares. Consulte a su médico."
                        color_tema = self.color_alerta

                detalles = {
                    "GLUCOSA DETECTADA": f"{glucosa:.1f} mg/dL",
                    "DIAGNÓSTICO": r.upper(),
                    "ESTADO CLÍNICO": s,
                    "TIPO DE PRUEBA": f"Medición en {estado.capitalize()}",
                    "REFERENCIA ADA": "Normal en ayunas: < 100 mg/dL | Postprandial: < 140 mg/dL"
                }

                self.actualizar_reporte("Informe Metabólico de Glucosa", detalles, color_tema)

                # --- CONSTRUCCIÓN DEL GRÁFICO DINÁMICO (GLUCEMIA) ---
                fig, ax = plt.subplots(figsize=(4.2, 2.0), dpi=100)
                fig.patch.set_facecolor(self.color_card)
                ax.set_facecolor(self.color_card)

                # Ajustamos dinámicamente las barras y límites según el estado de la medición
                if estado == "ayunas":
                    # Rangos en ayunas: Hipoglucemia (10-70), Normal (70-100), Prediabetes (100-126), Diabetes (126-200+)
                    ax.barh(0, 60.0, left=10.0, height=0.35, color="#e6f2ff", edgecolor="none")  # Azul sutil
                    ax.barh(0, 30.0, left=70.0, height=0.35, color="#e2fbeb", edgecolor="none")  # Verde sutil
                    ax.barh(0, 26.0, left=100.0, height=0.35, color="#fff9db", edgecolor="none")  # Amarillo sutil
                    ax.barh(0, 124.0, left=126.0, height=0.35, color="#ffdee2", edgecolor="none")  # Rojo sutil

                    ax.text(40.0, 0.25, "Bajo", fontsize=7, color="#1a73e8", ha="center", fontweight="bold")
                    ax.text(85.0, 0.25, "Normal", fontsize=7, color="#2b8a3e", ha="center", fontweight="bold")
                    ax.text(113.0, 0.25, "Pre", fontsize=7, color="#f59f00", ha="center", fontweight="bold")
                    ax.text(188.0, 0.25, "Elevado", fontsize=7, color="#c92a2a", ha="center", fontweight="bold")
                else:
                    # Rangos postprandial: Hipoglucemia (10-70), Normal (70-140), Prediabetes (140-200), Diabetes (200-250+)
                    ax.barh(0, 60.0, left=10.0, height=0.35, color="#e6f2ff", edgecolor="none")
                    ax.barh(0, 70.0, left=70.0, height=0.35, color="#e2fbeb", edgecolor="none")
                    ax.barh(0, 60.0, left=140.0, height=0.35, color="#fff9db", edgecolor="none")
                    ax.barh(0, 110.0, left=200.0, height=0.35, color="#ffdee2", edgecolor="none")

                    ax.text(40.0, 0.25, "Bajo", fontsize=7, color="#1a73e8", ha="center", fontweight="bold")
                    ax.text(105.0, 0.25, "Normal", fontsize=7, color="#2b8a3e", ha="center", fontweight="bold")
                    ax.text(170.0, 0.25, "Pre", fontsize=7, color="#f59f00", ha="center", fontweight="bold")
                    ax.text(255.0, 0.25, "Elevado", fontsize=7, color="#c92a2a", ha="center", fontweight="bold")

                # Acotar el valor para el renderizado del indicador
                glucosa_grafica = max(10.0, min(glucosa, 240.0))

                # Dibujamos pin indicador
                ax.vlines(glucosa_grafica, -0.25, 0.25, colors="#202124", linewidth=2.5, zorder=5)
                ax.scatter(glucosa_grafica, 0.23, marker="v", color="#202124", s=80, zorder=5)

                # Caja flotante con valor de glucosa actual
                ax.text(glucosa_grafica, -0.32, f"{glucosa:.0f}", fontsize=8, color="#202124",
                        ha="center", fontweight="bold",
                        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#e0e0e0", lw=0.8))

                # Configuración estética minimalista
                ax.set_xlim(10.0, 250.0)
                ax.set_ylim(-0.45, 0.4)

                ax.get_yaxis().set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["top"].set_visible(False)
                ax.spines["bottom"].set_color("#e0e0e0")
                ax.tick_params(colors="#5f6368", labelsize=7)
                ax.set_xlabel("Glucosa Sérica (mg/dL)", fontsize=8, color="#5f6368", fontweight="bold")

                fig.tight_layout()

                # Pintar gráfico en el canvas derecho
                canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_reporte)
                canvas_grafico.draw()
                canvas_grafico.get_tk_widget().pack(fill="x", expand=True, pady=(15, 0))

                plt.close(fig)

            except ValueError:
                self.mostrar_error_validacion("Por favor, ingrese un valor numérico válido para la glucosa.")

        tk.Button(f, text="EVALUAR GLUCOSA", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)
    #anemia
#cardio
    def mostrar_cardio(self):
        f = self.crear_layout_dual("Perfil Lipídico")
        e_c = self.crear_label_entry(f, "Col. Total:")
        e_h = self.crear_label_entry(f, "HDL:")
        e_l = self.crear_label_entry(f, "LDL:")
        e_t = self.crear_label_entry(f, "Triglicéridos:")

        def calc():
            try:
                col = float(e_c.get())
                hdl = float(e_h.get())
                ldl = float(e_l.get())
                tri = float(e_t.get())

                # Validación de límites para lípidos
                if not (20.0 <= col <= 1000.0) or not (5.0 <= hdl <= 200.0) or not (5.0 <= ldl <= 800.0) or not (
                        10.0 <= tri <= 3000.0):
                    self.mostrar_error_validacion("Valores lipídicos inconsistentes con la fisiología humana.")
                    return

                # --- LÓGICA DE CÁLCULO INTEGRADA (Evita NameError de importación) ---
                # Cálculo del Índice de Castelli (Colesterol Total / HDL)
                i = col / hdl

                # Evaluación de niveles individuales para construir diagnóstico clínico
                alertas = []
                if col >= 200: alertas.append("Hipercolesterolemia")
                if ldl >= 130: alertas.append("LDL Elevado")
                if hdl < 40: alertas.append("HDL Bajo (Protección débil)")
                if tri >= 150: alertas.append("Hipertrigliceridemia")

                if len(alertas) == 0:
                    e = "Perfil Lipídico Óptimo"
                    r = "Bajo"
                    rec = "Mantener el estilo de vida actual y chequeo anual."
                elif len(alertas) <= 2:
                    e = f"Dislipidemia Leve-Moderada ({', '.join(alertas[:1])})"
                    r = "Moderado"
                    rec = "Reducir grasas saturadas, realizar ejercicio aeróbico regular y reevaluar en 3 meses."
                else:
                    e = "Dislipidemia Mixta / Severa"
                    r = "Alto"
                    rec = "Considerar intervención farmacológica (estatinas) bajo estricta supervisión médica."

                detalles = {
                    "ÍNDICE CASTELLI": f"{i:.2f} (Deseable < 5.0)",
                    "ESTADO GENERAL": e,
                    "RIESGO CARDIOVASCULAR": r.upper(),
                    "RECOMENDACIÓN": rec,
                    "NOTA": "El LDL (colesterol malo) óptimo es < 100 mg/dL. El HDL (colesterol bueno) óptimo es > 40 mg/dL."
                }

                color_tema = self.color_alerta if r == "Alto" or r == "Moderado" else self.color_primario
                self.actualizar_reporte("Lípidos y Riesgo Cardiovascular", detalles, color_tema)

                # --- CONSTRUCCIÓN DEL GRÁFICO DE FRACCIONES LIPÍDICAS ---
                fig, ax = plt.subplots(figsize=(4.2, 2.3), dpi=100)
                fig.patch.set_facecolor(self.color_card)
                ax.set_facecolor("#fcfcfc")

                # Parámetros y valores del paciente
                fracciones = ["Col. Total", "LDL", "HDL", "Triglicéridos"]
                valores = [col, ldl, hdl, tri]

                # Valores de referencia máximos deseables para cada uno (HDL es mínimo, se maneja diferente)
                valores_referencia = [200, 100, 40, 150]

                # Colores adaptados al estado de cada fracción del paciente
                colores_barras = []
                colores_barras.append("#ef4444" if col >= 200 else "#11caa0")  # Col Total
                colores_barras.append("#ef4444" if ldl >= 130 else "#11caa0")  # LDL
                colores_barras.append(
                    "#11caa0" if hdl >= 40 else "#fbbf24")  # HDL (Verde si es alto, amarillo si es bajo)
                colores_barras.append("#ef4444" if tri >= 150 else "#11caa0")  # Triglicéridos

                # Dibujamos las barras horizontales
                y_pos = range(len(fracciones))
                bars = ax.barh(y_pos, valores, color=colores_barras, height=0.5, edgecolor="none")

                # Añadimos etiquetas numéricas de los valores del paciente sobre o junto a las barras
                for idx, bar in enumerate(bars):
                    width = bar.get_width()
                    # Si los triglicéridos son muy altos, los acotamos visualmente en el gráfico para no arruinar la escala
                    if idx == 3 and width > 400:
                        ax.text(380, bar.get_y() + bar.get_height() / 2, f"{int(width)}*",
                                va="center", ha="right", color="white", fontsize=8, fontweight="bold")
                    else:
                        ax.text(width + 5, bar.get_y() + bar.get_height() / 2, f"{int(width)}",
                                va="center", ha="left", color="#475569", fontsize=8, fontweight="bold")

                # Dibujamos líneas verticales de puntos grises indicando el valor de referencia clínica sugerido
                for idx, ref in enumerate(valores_referencia):
                    if idx != 3:  # Para Col, LDL, HDL dibujamos marcas sutiles de referencia
                        ax.plot([ref, ref], [idx - 0.3, idx + 0.3], color="#94a3b8", linestyle="--", linewidth=1)

                # Ajustes estéticos y límites del gráfico
                ax.set_yticks(y_pos)
                ax.set_yticklabels(fracciones, fontsize=8, fontweight="bold", color="#475569")

                # Escalamos de forma inteligente para que entren bien Colesterol (normalmente ~200) y Triglicéridos
                limite_x = max(col + 50, ldl + 50, hdl + 20, min(tri + 50, 400))
                ax.set_xlim(0, limite_x)

                ax.spines["top"].set_visible(False)
                ax.spines["right"].set_visible(False)
                ax.spines["left"].set_visible(False)
                ax.spines["bottom"].set_color("#e0e0e0")
                ax.tick_params(colors="#5f6368", labelsize=7)
                ax.set_xlabel("Concentración Sérica (mg/dL)", fontsize=8, color="#5f6368", fontweight="bold")

                fig.tight_layout()

                # Acoplar el gráfico en el panel derecho de Tkinter
                canvas_grafico = FigureCanvasTkAgg(fig, master=self.area_reporte)
                canvas_grafico.draw()
                canvas_grafico.get_tk_widget().pack(fill="x", expand=True, pady=(15, 0))

                plt.close(fig)

            except ValueError:
                self.mostrar_error_validacion("Rellene todas las fracciones lipídicas con valores numéricos.")

        tk.Button(f, text="ANALIZAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)
    #cardio


    def mostrar_bilirrubina(self):
        f = self.crear_layout_dual("Bilirrubina")
        e_d = self.crear_label_entry(f, "Directa:");
        e_i = self.crear_label_entry(f, "Indirecta:")

        def calc():
            try:
                bd = float(e_d.get())
                bi = float(e_i.get())

                if not (0.0 <= bd <= 50.0) or not (0.0 <= bi <= 50.0):
                    self.mostrar_error_validacion("Los valores de bilirrubina deben estar entre 0.0 y 50.0 mg/dL.")
                    return

                t, est, col = evaluar_bilirrubina(bd, bi)
                detalles = {"TOTAL": f"{t} mg/dL", "ESTADO": est,
                            "SÍNTOMAS": "Observar ictericia en conjuntivas si el valor es >2.0."}
                self.actualizar_reporte("Perfil Hepático", detalles,
                                        self.color_alerta if col == "rojo" else self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Ingrese valores de bilirrubina directa e indirecta.")

        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_renal(self):
        f = self.crear_layout_dual("Función Renal (eTFG)")
        e_c = self.crear_label_entry(f, "Creatinina:");
        e_e = self.crear_label_entry(f, "Edad:");
        v_s = tk.StringVar(value="mujer");
        self.crear_selector_segmentado(f, "Sexo:", ["mujer", "hombre"], v_s)

        def calc():
            try:
                crea = float(e_c.get())
                edad = int(e_e.get())

                # Validación renal
                if not (0.1 <= crea <= 35.0) or not (18 <= edad <= 120):
                    self.mostrar_error_validacion(
                        "Fórmula CKD-EPI válida únicamente para adultos (18-120 años).\nRango de creatinina aceptado: 0.1 - 35.0 mg/dL.")
                    return

                v, est = calcular_tfg_avanzado(crea, edad, v_s.get())
                detalles = {"TFG ESTIMADA": f"{v} ml/min", "ESTADIO": est,
                            "NOTA": "Estadío 3 o superior requiere ajuste de dosis farmacológicas."}
                self.actualizar_reporte("Informe Renal", detalles, self.color_alerta if v < 60 else self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Por favor, ingrese valores válidos de creatinina y edad.")

        tk.Button(f, text="CALCULAR TFG", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_glasgow(self):
        f = self.crear_layout_dual("Escala de Glasgow")
        v_o = tk.IntVar(value=4);
        self.crear_selector_segmentado(f, "Ocular:", [1, 2, 3, 4], v_o)
        v_v = tk.IntVar(value=5);
        self.crear_selector_segmentado(f, "Verbal:", [1, 2, 3, 4, 5], v_v)
        v_m = tk.IntVar(value=6);
        self.crear_selector_segmentado(f, "Motor:", [1, 2, 3, 4, 5, 6], v_m)

        def calc():
            # Glasgow usa variables de selección directa controladas (sin error de digitación externa posible)
            t, e, g = evaluar_glasgow(v_o.get(), v_v.get(), v_m.get())
            detalles = {"PUNTAJE": f"{t}/15", "TRAUMA": e, "CONDUCTA": g}
            self.actualizar_reporte("GCS", detalles, self.color_alerta if t < 9 else self.color_primario)

        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_dolor(self):
        f = self.crear_layout_dual("Dolor EVA")
        v_d = tk.IntVar(value=0);
        self.crear_selector_segmentado(f, "Intensidad:", list(range(11)), v_d)

        def calc():
            v, n, s = evaluar_dolor(v_d.get())
            detalles = {"NIVEL": n, "SUGERENCIA": s, "TIPO": "Escala Visual Analógica (EVA)"}
            self.actualizar_reporte("Dolor", detalles, self.color_alerta if v > 6 else self.color_primario)

        tk.Button(f, text="EVALUAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_respiratorio(self):
        f = self.crear_layout_dual("Kirby (PAFI)")
        e_p = self.crear_label_entry(f, "PaO2:");
        e_f = self.crear_label_entry(f, "FiO2 (%):")

        def calc():
            try:
                pao2 = float(e_p.get())
                fio2 = float(e_f.get())

                # Validación respiratoria
                if not (20.0 <= pao2 <= 700.0) or not (21.0 <= fio2 <= 100.0):
                    self.mostrar_error_validacion(
                        "Valores gasométricos fuera de la realidad de ventilación.\nPaO2: 20-700 mmHg. FiO2: 21% a 100%.")
                    return

                i, e = calcular_kirby(pao2, fio2)
                detalles = {"ÍNDICE": i, "ESTADO": e, "ALERTA": "Valores <200 indican SDRA moderado-grave."}
                self.actualizar_reporte("Función Pulmonar", detalles,
                                        self.color_alerta if i < 300 else self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Ingrese PaO2 y FiO2 como valores numéricos.")

        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_anion_gap(self):
        f = self.crear_layout_dual("Anión Gap")
        e_n = self.crear_label_entry(f, "Sodio (Na):");
        e_c = self.crear_label_entry(f, "Cloro (Cl):");
        e_b = self.crear_label_entry(f, "Bicarbonato (HCO3):")

        def calc():
            try:
                na = float(e_n.get())
                cl = float(e_c.get())
                hco3 = float(e_b.get())

                # Validación de electrolitos
                if not (80.0 <= na <= 200.0) or not (50.0 <= cl <= 180.0) or not (2.0 <= hco3 <= 60.0):
                    self.mostrar_error_validacion(
                        "Concentración de electrolitos séricos fuera de límites fisiológicos posibles.")
                    return

                g, i = calcular_anion_gap(na, cl, hco3)
                detalles = {"ANION GAP": g, "INTERPRETACIÓN": i, "REFERENCIA": "Normal: 8-12 mEq/L"}
                self.actualizar_reporte("Equilibrio Ácido-Base", detalles, self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Ingrese valores de electrolitos en todos los casilleros.")

        tk.Button(f, text="CALCULAR GAP", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_deficit_agua(self):
        f = self.crear_layout_dual("Déficit de Agua")
        e_p = self.crear_label_entry(f, "Peso (kg):");
        e_n = self.crear_label_entry(f, "Sodio actual (mEq/L):");
        v_s = tk.StringVar(value="hombre");
        self.crear_selector_segmentado(f, "Sexo:", ["hombre", "mujer"], v_s)

        def calc():
            try:
                peso = float(e_p.get())
                na = float(e_n.get())

                # Validación de sodio
                if not (5.0 <= peso <= 400.0) or not (120.0 <= na <= 200.0):
                    self.mostrar_error_validacion(
                        "Sodio sérico fuera de límites metabólicos de vida o peso inválido.\nNa aceptable: 120-200 mEq/L.")
                    return

                r = calcular_deficit_agua(peso, na, v_s.get())
                detalles = {"DÉFICIT TOTAL": f"{r} Litros", "META": "Sodio deseado: 140 mEq/L",
                            "AVISO": "Reponer lentamente para evitar daño neurológico."}
                self.actualizar_reporte("Reposición Hídrica", detalles, self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Introduzca peso y nivel de sodio sérico reales.")

        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_framingham(self):
        f = self.crear_layout_dual("Riesgo Cardiovascular")
        e_e = self.crear_label_entry(f, "Edad:");
        v_s = tk.StringVar(value="hombre");
        self.crear_selector_segmentado(f, "Sexo:", ["hombre", "mujer"], v_s)
        e_c = self.crear_label_entry(f, "Col. Total:");
        e_h = self.crear_label_entry(f, "HDL:");
        e_si = self.crear_label_entry(f, "Sistólica:");
        e_di = self.crear_label_entry(f, "Diastólica:")
        v_f = tk.StringVar(value="no");
        self.crear_selector_segmentado(f, "¿Fuma?", ["si", "no"], v_f)

        def calc():
            try:
                edad = int(e_e.get())
                col = float(e_c.get())
                hdl = float(e_h.get())
                sis = int(e_si.get())
                dia = int(e_di.get())

                # Validación Framingham (Restricciones del modelo)
                if not (20 <= edad <= 79):
                    self.mostrar_error_validacion(
                        "La escala de Framingham se encuentra validada para personas entre 20 y 79 años.")
                    return
                if not (100 <= col <= 450) or not (10 <= hdl <= 150) or not (90 <= sis <= 220) or not (
                        50 <= dia <= 150):
                    self.mostrar_error_validacion(
                        "Los parámetros analíticos exceden los rangos de la tabla Framingham.")
                    return

                p, pct, n = evaluar_riesgo_framingham(v_s.get(), edad, col, hdl, v_f.get() == "si", sis, dia)
                detalles = {"PUNTAJE": p, "PROBABILIDAD": pct, "RIESGO": n,
                            "SUGERENCIA": "Control estricto de factores de riesgo si es >10%."}
                self.actualizar_reporte("Framingham 10 Años", detalles,
                                        self.color_alerta if n == "ALTO" else self.color_primario)
            except ValueError:
                self.mostrar_error_validacion(
                    "Por favor complete todos los datos requeridos con valores numéricos correctos.")

        tk.Button(f, text="ESTIMAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_infusion(self):
        f = self.crear_layout_dual("Cálculo de Infusiones")
        e_v = self.crear_label_entry(f, "Volumen (ml):");
        e_t = self.crear_label_entry(f, "Tiempo (h):")

        def calc():
            try:
                vol = float(e_v.get())
                tie = float(e_t.get())

                if not (1.0 <= vol <= 10000.0) or not (0.1 <= tie <= 168.0):
                    self.mostrar_error_validacion(
                        "Límites de infusión inválidos.\nVolumen: 1-10,000 ml. Tiempo: 0.1-168 horas.")
                    return

                res = calcular_goteo(vol, tie)
                self.actualizar_reporte("Plan de Goteo", res, self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Introduzca volumen en ml y tiempo en horas.")

        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_pediatria(self):
        f = self.crear_layout_dual("Dosis Pediátrica")
        e_p = self.crear_label_entry(f, "Peso (kg):");
        e_d = self.crear_label_entry(f, "Dosis (mg/kg):");
        e_c = self.crear_label_entry(f, "Presentación (mg):");
        e_v = self.crear_label_entry(f, "En volumen (ml):")

        def calc():
            try:
                peso = float(e_p.get())
                dosis = float(e_d.get())
                conc = float(e_c.get())
                vol = float(e_v.get())

                # Validación pediátrica estricta (Evita accidentes por error de coma o dígito)
                if not (0.5 <= peso <= 60.0) or not (0.01 <= dosis <= 500.0) or not (0.1 <= conc <= 5000.0) or not (
                        0.1 <= vol <= 1000.0):
                    self.mostrar_error_validacion(
                        "Parámetros de dosificación fuera de márgenes terapéuticos estándar pediátricos.")
                    return

                ml, mg = calcular_dosis_pediatrica(peso, dosis, conc, vol)
                detalles = {"DOSIS ML": f"{ml} ml", "DOSIS MG": f"{mg} mg",
                            "ALERTA": "Verificar siempre con doble chequeo en pediatría."}
                self.actualizar_reporte("Dosificación", detalles, self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Todos los campos de dosificación deben ser numéricos.")

        tk.Button(f, text="CALCULAR DOSIS", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_superficie(self):
        f = self.crear_layout_dual("Superficie Corporal")
        e_p = self.crear_label_entry(f, "Peso (kg):");
        e_a = self.crear_label_entry(f, "Altura (cm):")

        def calc():
            try:
                peso = float(e_p.get())
                altura = float(e_a.get())

                if not (1.0 <= peso <= 450.0) or not (20.0 <= altura <= 250.0):
                    self.mostrar_error_validacion("Datos antropométricos incompatibles con la fórmula de Mosteller.")
                    return

                res = calcular_superficie_corporal(peso, altura)
                detalles = {"RESULTADO": f"{res} m²", "MÉTODO": "Mosteller",
                            "USO": "Necesario para ajuste de quimioterapia y fluidos."}
                self.actualizar_reporte("BSA", detalles, self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Ingrese valores válidos de peso (kg) y altura (cm).")

        tk.Button(f, text="CALCULAR BSA", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_conversor(self):
        f = self.crear_layout_dual("Conversor de Unidades")
        e_v = self.crear_label_entry(f, "Valor:");
        v_t = tk.StringVar(value="glucosa");
        self.crear_selector_segmentado(f, "Tipo:", ["glucosa", "colesterol", "triglicéridos"], v_t)
        v_d = tk.StringVar(value="mg_a_mmol");
        self.crear_selector_segmentado(f, "Dirección:", ["mg/dL a mmol/L", "mmol/L a mg/dL"], v_d)

        def calc():
            try:
                val = float(e_v.get())
                if not (0.001 <= val <= 10000.0):
                    self.mostrar_error_validacion(
                        "Por favor, ingrese un valor de analito clínico realista para convertir.")
                    return

                d = "mg_a_mmol" if "a mmol/L" in v_d.get() else "mmol_a_mg"
                if v_t.get() == "glucosa":
                    r, u = convertir_glucosa(val, d)
                elif v_t.get() == "colesterol":
                    r, u = convertir_lipidos(val, d)
                else:
                    r, u = convertir_trigliceridos(val, d)
                self.actualizar_reporte("Conversión", {"RESULTADO": f"{r} {u}"}, self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Ingrese un valor numérico para iniciar la conversión de unidades.")

        tk.Button(f, text="CONVERTIR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)

    def mostrar_ciclo(self):
        f = self.crear_layout_dual("Calendario de Fertilidad")
        e_d = self.crear_label_entry(f, "Días promedio del ciclo:")

        def calc():
            try:
                ciclo = int(e_d.get())

                # Validación de ciclo menstrual biológicamente viable
                if not (20 <= ciclo <= 45):
                    self.mostrar_error_validacion(
                        "Los ciclos menstruales regulares saludables típicamente duran entre 20 y 45 días.")
                    return

                d, v = calcular_ovulacion(ciclo)
                detalles = {"DÍA OVULACIÓN": f"Día {d}", "VENTANA FÉRTIL": v,
                            "INFO": "Cálculo basado en método de calendario estándar."}
                self.actualizar_reporte("Fertilidad", detalles, self.color_primario)
            except ValueError:
                self.mostrar_error_validacion("Ingrese el número de días promedio de duración de su ciclo como entero.")

        tk.Button(f, text="CALCULAR", bg=self.color_primario, fg="white", bd=0, font=("Helvetica", 10, "bold"),
                  command=calc).pack(fill="x", pady=20, ipady=12)