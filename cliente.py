import tkinter as tk
import socket
import datetime
import threading

lista_usuarios = []

def comprobar_usuario(new_user, lista_usuarios):
    if new_user in lista_usuarios:
        return False
    else:
        lista_usuarios.append(new_user)
        return True

def crear_cliente_ventana(conexion,usuario):
    # Creamos la ventana
    ventana_client = tk.Tk()
    ventana_client.title(f"Enviar mensajes desde: {usuario}")
    # Creamos las etiquetas necesarias
    tk.Label(ventana_client, text='Mensaje a enviar:').grid(row=0, column=0)
    cuadro_texto_mensaje = tk.Entry(ventana_client)
    cuadro_texto_mensaje.grid(row=0, column=1)
    #Creamos un botón
    boton = tk.Button(ventana_client, text="Enviar mensaje", command=lambda: boton_click_client(cuadro_texto_mensaje.get(), cuadro_texto_destino_client,conexion,boton, usuario))
    boton.grid(row=1, column=1, columnspan=2)
    # Creamos un cuadro de texto que acepta varias líneas
    cuadro_texto_destino_client = tk.Text(ventana_client)
    cuadro_texto_destino_client.grid(row=2, column=0, columnspan=2)
    # Creamos el scrollbar y lo asociamos al cuadro de texto
    scrollbar_client = tk.Scrollbar(ventana_client)
    scrollbar_client.grid(row=2, column=2, sticky=tk.NS)
    cuadro_texto_destino_client.config(yscrollcommand=scrollbar_client.set)
    scrollbar_client.config(command=cuadro_texto_destino_client.yview)
    # Visualizamos la ventana
    ventana_client.mainloop()
    
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

"""""
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
"""
def boton_click_usuario():
    usuario = cuadro_texto_usuario.get()
    texto_IP = cuadro_texto_IP.get()
    texto_puerto = cuadro_texto_puerto.get()
    try:
        if comprobar_usuario(usuario, lista_usuarios) == False: #usuario ya registrado
            cuadro_texto_destino.insert(tk.END, f"Error: El usuario {usuario} ya está registrado. \n")
            cuadro_texto_destino.yview_moveto(1.0)
        else:
            #texto_puerto_numero = int(texto_puerto)
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            cuadro_texto_destino.insert(tk.END, f"Creado cliente con nombre: [{usuario}] a las {hora_actual}.\n")
            #Ajustar posición scrollbar para mostrar siempre el último texto
            cuadro_texto_destino.yview_moveto(1.0)
            #Creamos el nuevo usuario
            crear_cliente(texto_puerto, texto_IP, usuario)
    except:
        mostrar_error_entero()
    

def boton_click_client(mensaje,cuadro_texto_destino_client,conexion,boton,usuario):
    if mensaje.strip():
        if mensaje =="FIN":
            lista_usuarios.remove(usuario)
            cuadro_texto_destino_client.insert(tk.END, "Finaliza conexion con el servidor \n")
            cuadro_texto_destino_client.yview_moveto(1.0)
            enviar_mensaje(mensaje,conexion,boton)
            return
        try:
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
            cuadro_texto_destino_client.insert(tk.END, f"{hora_actual}: {mensaje}  \n")
            cuadro_texto_destino_client.yview_moveto(1.0)
            enviar_mensaje(mensaje,conexion,boton)
        except socket.timeout:
            cuadro_texto_destino_client.insert(tk.END, "Error: tiempo de espera excedido. \n")
            cuadro_texto_destino_client.yview_moveto(1.0)
            boton.config(state=tk.DISABLED)  # Deshabilitar el botón si hay timeout
        # mostrar_fin_conexion()
        except  Exception as e:
            cuadro_texto_destino_client.insert(tk.END, f"Error: {e} \n")
            cuadro_texto_destino_client.yview_moveto(1.0)
            boton.config(state=tk.DISABLED)  # Deshabilitar el botón si ocurre otro error
            #mostrar_fin_conexion()
    
def crear_cliente(texto_puerto, texto_IP, usuario):
    try:
        #conexion con el servidor
        conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        puerto = int(texto_puerto)
        direccion_IP = texto_IP
        conexion.connect((direccion_IP, puerto))
        #Establecer timeout para la recepción de datos
        conexion.settimeout(5)
        #Enviar usuario
        conexion.send(usuario.encode())
        #creamos un windows para cada cliente por lo que vamos a crear un hilo en cada caso
        client_thread = threading.Thread(target=crear_cliente_ventana,args=(conexion,usuario))  
        client_thread.start()
    except Exception as e:
        cuadro_texto_destino.insert(tk.END, f"Error al conectar con el servidor: {e}\n")
        cuadro_texto_destino.yview_moveto(1.0)
    

def enviar_mensaje(texto, conexion, boton):
    try:
        conexion.send(texto.encode())
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        boton.config(state=tk.DISABLED)  # Deshabilitar el botón si ocurre otro error
    # mostrar_fin_conexion()
    if texto == "FIN":
        boton.config(state=tk.DISABLED)  # Deshabilitar el botón al enviar "FIN"
        #mostrar_fin_conexion()

if __name__ == '__main__':
    # Creamos la ventana
    ventana = tk.Tk()
    ventana.title("Crear Clientes")
    # Creamos las etiquetas necesarias
    tk.Label(ventana, text='IP servidor:').grid(row=0, column=0)
    tk.Label(ventana, text='Puerto servidor:').grid(row=1, column=0)
    tk.Label(ventana, text='Usuario:').grid(row=2, column=0)
    # Creamos los cuadros de texto para las 3 etiquetas
    cuadro_texto_IP = tk.Entry(ventana)
    cuadro_texto_IP.grid(row=0, column=1)
    cuadro_texto_puerto = tk.Entry(ventana)
    cuadro_texto_puerto.grid(row=1, column=1)
    cuadro_texto_usuario = tk.Entry(ventana)
    cuadro_texto_usuario.grid(row=2, column=1)
    #Creamos un botón
    boton = tk.Button(ventana, text="Crear Usuario", command=boton_click_usuario)
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