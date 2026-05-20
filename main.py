import tkinter as tk
from interfaz.ventana_principal import VentanaPrincipal


def iniciar_app():
    # 1. Creamos la instancia de Tkinter (la raíz)
    root = tk.Tk()

    # 2. Configuramos el icono o detalles globales si los hubiera
    # root.iconbitmap("assets/icon.ico") # Opcional si tienes un icono

    # 3. Llamamos a nuestra clase de interfaz
    app = VentanaPrincipal(root)

    # 4. Iniciamos el bucle del programa
    root.mainloop()


if __name__ == "__main__":
    iniciar_app()
