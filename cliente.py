import tkinter as tk
import socket
import datetime

def mostrar_error_entero():
    ventana_no_entero = tk.Toplevel(ventana)
    ventana_no_entero.title("Error")
    ventana_no_entero.geometry("300x100")  

    # Centrar la ventana de error respecto a la ventana principal
    ventana_no_entero.transient(ventana)
    ventana_no_entero.grab_set()
    ventana_no_entero.update_idletasks()
    x = ventana.winfo_x() + (ventana.winfo_width() // 2) - (ventana_no_entero.winfo_width() // 2)
    y = ventana.winfo_y() + (ventana.winfo_height() // 2) - (ventana_no_entero.winfo_height() // 2)
    ventana_no_entero.geometry(f"+{x}+{y}")

    tk.Label(ventana_no_entero, text="Por favor introduce un valor entero").grid(row=0, column=0, padx=20, pady=20)
    ventana_no_entero.mainloop()

def mostrar_fin_conexion():
    ventana_fin_conexion = tk.Toplevel(ventana)
    ventana_fin_conexion.title("Conexión finalizada")
    ventana_fin_conexion.geometry("300x100")  

    # Centrar la ventana de error respecto a la ventana principal
    ventana_fin_conexion.transient(ventana)
    ventana_fin_conexion.grab_set()
    ventana_fin_conexion.update_idletasks()
    x = ventana.winfo_x() + (ventana.winfo_width() // 2) - (ventana_fin_conexion.winfo_width() // 2)
    y = ventana.winfo_y() + (ventana.winfo_height() // 2) - (ventana_fin_conexion.winfo_height() // 2)
    ventana_fin_conexion.geometry(f"+{x}+{y}")

    tk.Label(ventana_fin_conexion, text="Conexión finalizada").grid(row=0, column=0, padx=20, pady=20)
    ventana_fin_conexion.mainloop()

def boton_click():
    texto = cuadro_texto_mensaje.get()
    texto_IP = cuadro_texto_IP.get()
    texto_puerto = cuadro_texto_puerto.get()
    try:
        texto_puerto_numero = int(texto_puerto)
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        cuadro_texto_destino.insert(tk.END, f"mensaje({texto}) enviado por el cliente a las {hora_actual}"+'\n')
        #Ajustar posición scrollbar para mostrar siempre el último texto
        cuadro_texto_destino.yview_moveto(1.0)
    except:
        mostrar_error_entero()
    
    conexion = crear_cliente(texto_puerto, texto_IP)
    enviar_mensaje(texto, conexion)
    #cerrar el cliente y la ventana
    if texto == "FIN":
        conexion.close()
        mostrar_fin_conexion()
        ventana.destroy()

def crear_cliente(texto_puerto, texto_IP):
    #conexion con el servidor
    conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    puerto = int(texto_puerto)
    direccion_IP = texto_IP
    conexion.connect(direccion_IP, puerto)
    #Establecer timeout para la recepción de datos
    conexion.settimeout(5)

    return conexion

def enviar_mensaje(texto, conexion):
    conexion.send(texto.encode())

if __name__ == '__main__':
    # Creamos la ventana
    ventana = tk.Tk()
    ventana.title("Enviar mensajes")
    # Creamos las etiquetas necesarias
    tk.Label(ventana, text='IP servidor:').grid(row=0, column=0)
    tk.Label(ventana, text='Puerto servidor:').grid(row=1, column=0)
    tk.Label(ventana, text='Mensaje:').grid(row=2, column=0)
    # Creamos los cuadros de texto para las 3 etiquetas
    cuadro_texto_IP = tk.Entry(ventana)
    cuadro_texto_IP.grid(row=0, column=1)
    cuadro_texto_puerto = tk.Entry(ventana)
    cuadro_texto_puerto.grid(row=1, column=1)
    cuadro_texto_mensaje = tk.Entry(ventana)
    cuadro_texto_mensaje.grid(row=2, column=1)
    #Creamos un botón
    boton = tk.Button(ventana, text="Enviar mensaje", command=boton_click)
    boton.grid(row=3, column=1, columnspan=2)
    # Creamos un cuadro de texto que acepta varias líneas
    cuadro_texto_destino = tk.Text(ventana)
    cuadro_texto_destino.grid(row=4, column=0, columnspan=2)
    # Creamos el scrollbar y lo asociamos al cuadro de texto
    scrollbar = tk.Scrollbar(ventana)
    scrollbar.grid(row=4, column=2, sticky=tk.NS)
    cuadro_texto_destino.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=cuadro_texto_destino.yview)
    # Visualizamos la ventana
    ventana.mainloop()