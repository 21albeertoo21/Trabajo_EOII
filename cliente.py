import tkinter as tk
import socket
import datetime
import threading

dic_users_and_ports = {} #creamos un diccionario vacío
mutex = threading.Lock() #mutex para evitar concurrencia
def insertar_user(dic_users_and_ports, new_user, puerto):
    with mutex:
        if puerto not in dic_users_and_ports:
            dic_users_and_ports[puerto] = [] #Si el puerto no está en el diccionario creamos una lista vacía en la clave puerto
        #insertamos el usuario en la clave puerto correcta
        dic_users_and_ports[puerto].append(new_user)

def eliminar_user(dic_users_and_ports, new_user, puerto):
    with mutex:
        if puerto in dic_users_and_ports and new_user in dic_users_and_ports[puerto]:
            dic_users_and_ports[puerto].remove(new_user)
            if not dic_users_and_ports[puerto]:  # Si la lista está vacía, elimina la clave del diccionario
                del dic_users_and_ports[puerto]

def comprobar_usuario(dic_users_and_ports, new_user, puerto):
    with mutex:
        if puerto in dic_users_and_ports and new_user in dic_users_and_ports[puerto]:
            return False
        return True
    
    
#Escucha mensajes del servidor en un hilo separado.
def escuchar_mensajes(conexion, cuadro_texto_destino_client, ventana_client,usuario,puerto):
    
    #desactivar timeout de la conexion
    conexion.settimeout(None)
    while True:
        try:
            data = conexion.recv(1024)
            if not data:
                break
            mensaje = data.decode()
            print(f"{usuario}: ha recibido cerrar la conexion")
            if mensaje == "CIERRE DE SERVIDOR":
                cuadro_texto_destino_client.insert(tk.END, "Servidor cerrado. Cerrando cliente...\n")
                cuadro_texto_destino_client.yview_moveto(1.0)
                eliminar_user(dic_users_and_ports, usuario, puerto)
                ventana_client.after(2000, ventana_client.destroy)  # Cierra la ventana después de 2 segundos
                break
            else:
                break
        except socket.error as e:
            print(f"Error al recibir datos: {e}")
            break
def crear_cliente_ventana(conexion,usuario,puerto):
    # Creamos la ventana
    ventana_client = tk.Tk()
    ventana_client.title(f"Enviar mensajes desde: {usuario} al servidor de puerto: {puerto}")
    # Creamos las etiquetas necesarias
    tk.Label(ventana_client, text='Mensaje a enviar:').grid(row=0, column=0)
    cuadro_texto_mensaje = tk.Entry(ventana_client)
    cuadro_texto_mensaje.grid(row=0, column=1)
    #Creamos un botón
    boton = tk.Button(ventana_client, text="Enviar mensaje", command=lambda: boton_click_client(cuadro_texto_mensaje.get(), cuadro_texto_destino_client,conexion,boton, usuario, ventana_client,puerto))
    boton.grid(row=1, column=1, columnspan=2)
    # Creamos un cuadro de texto que acepta varias líneas
    cuadro_texto_destino_client = tk.Text(ventana_client)
    cuadro_texto_destino_client.grid(row=2, column=0, columnspan=2)
    # Creamos el scrollbar y lo asociamos al cuadro de texto
    scrollbar_client = tk.Scrollbar(ventana_client)
    scrollbar_client.grid(row=2, column=2, sticky=tk.NS)
    cuadro_texto_destino_client.config(yscrollcommand=scrollbar_client.set)
    scrollbar_client.config(command=cuadro_texto_destino_client.yview)
    
     # Inicia un hilo para escuchar mensajes del servidor
    threading.Thread(target=escuchar_mensajes, args=(conexion, cuadro_texto_destino_client, ventana_client,usuario,puerto), daemon=True).start()
    
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

def boton_click_usuario():
    usuario = cuadro_texto_usuario.get()
    texto_IP = cuadro_texto_IP.get()
    texto_puerto = cuadro_texto_puerto.get()
    puerto = int(texto_puerto)
    try:
        if comprobar_usuario(dic_users_and_ports, usuario, puerto) == False: #usuario ya registrado
            cuadro_texto_destino.insert(tk.END, f"Error: El usuario {usuario} ya está registrado. \n")
            cuadro_texto_destino.yview_moveto(1.0)
        else:
           #Creamos el nuevo usuario
            if crear_cliente(texto_puerto, texto_IP, usuario) == True:
                hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                cuadro_texto_destino.insert(tk.END, f"Creado cliente con nombre: [{usuario}] a las {hora_actual}.\n")
                #Ajustar posición scrollbar para mostrar siempre el último texto
                cuadro_texto_destino.yview_moveto(1.0)
    except:
        mostrar_error_entero()
    

def boton_click_client(mensaje,cuadro_texto_destino_client,conexion,boton,usuario,ventana_client,puerto):
    if mensaje.strip():
        if mensaje =="FIN":
            eliminar_user(dic_users_and_ports, usuario, puerto)
            print(f"{usuario}: Finalizó conexión con el servidor\n")
            cuadro_texto_destino_client.insert(tk.END, "Finaliza conexión con el servidor \n")
            cuadro_texto_destino_client.yview_moveto(1.0)
            enviar_mensaje(mensaje,conexion,boton)
            ventana_client.after(5000, ventana_client.destroy)
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
        client_thread = threading.Thread(target=crear_cliente_ventana,args=(conexion,usuario,puerto))  
        client_thread.start()
        #agregamos el usuario a la lista de usuarios con clave = puerto
        insertar_user(dic_users_and_ports, usuario, puerto)
    except Exception as e:
        cuadro_texto_destino.insert(tk.END, f"Error al conectar con el servidor: {e}\n")
        cuadro_texto_destino.yview_moveto(1.0)
        return False
    
    return True

def enviar_mensaje(texto, conexion, boton):
    try:
        conexion.send(texto.encode())
    except Exception as e:
        print(f"Error al enviar mensaje: {e}")
        boton.config(state=tk.DISABLED)  # Deshabilitar el botón si ocurre otro error
    if texto == "FIN":
        boton.config(state=tk.DISABLED)  # Deshabilitar el botón al enviar "FIN"

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