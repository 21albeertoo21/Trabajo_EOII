import tkinter as tk
from socket import *
import pickle 
import sys
import datetime 
import threading
import requests

#CONSTANTE DE tiempo hasta cerrar server windows in miliseconds
TIME_BEFORE_CLOSE_SERVER_WINDOWS = 10000
#Llave para poder utilizar la API de OpenWeatherMap para obtener la información del tiempo en valencia
API_KEY = "cbf557829a16f6572809313ff5b76dd0"
# Lista para almacenar clientes conectados (sockets) y sus direcciones (IP, puerto)
clientes_conectados = []
# Crear un evento de parada global
stop_event = threading.Event()
#Muxtex para evitar condiciones de carrera en clientes conectados
clientes_lock = threading.Lock()

#El proceso de las funciones es el siguiente: se ejecuta el main creando la ventana principal,
#Se vincula la función botón_click a cuando se pulsa el botón de crear servidor, esta función se encarga de crear un hilo vinculado a la función create_server
#Create_server se encarga de crear el servidor y se queda escuchando para nuevas conexiones, en el caso de que haya alguna creará un nuevo hilo vinculado a handle_client
#Handle_client se encarga de manejar la comunicación con el cliente recibiendo los mensajes correspondientes y checkeando que una vez acabe el hilo se haya cerrado la conexión con el cliente
#Además contamos con otras funciones como Close_all_connections que se encarga de usando la lista de clientes conectados cerrar todas estas conexiones



#Añade al cliente en la lista de clientes conectados y espera a recibir mensajes de este para imprimirlos por la ventana
#cuenta con un finally en el que si salido del bucle todavía no se ha eliminado la conexión con el cliente la cierra, y la elimina de la lista
def handle_client(connection, client_address):
    global clientes_conectados
    with clientes_lock:
        clientes_conectados.append((connection, client_address))
    print(f"conexion establecida con puerto: {client_address[1]}")
    print_list_clientes_conectados()
    #desactivar timeout de la conexion
    connection.settimeout(None)
    try:
        usuario_coded = connection.recv(1024)
        usuario = usuario_coded.decode()
        message=f"Conexion establecida con {usuario}"
        mensaje_por_ventana(message)
        while True:
            data = connection.recv(1024)
            data_decode = data.decode()
            if data:
                if data_decode == "FIN":
                    break
                elif data_decode == "HORA":
                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    message = f"{usuario}: {hora_actual}"
                    mensaje_por_ventana(message)
                elif data_decode == "TIEMPO":
                    tiempo_valencia_message = obtener_clima_valencia()
                    message = f"{usuario}: {tiempo_valencia_message}"
                    mensaje_por_ventana(message)
                else:
                    message = f"{usuario}: {data_decode}"
                    mensaje_por_ventana(message)
    #cuando se cierre el servidor mediante el boton al estar esperando recibir y cerrarse la conexión abrupta saltará una excepción que manejamos aquí
    except (ConnectionAbortedError, ConnectionResetError):
        print(f"Conexión finalizada debido a que el servidor se cierra con el cliente{client_address}")
    finally:
        # Verificar si la conexión sigue en la lista antes de intentar eliminarla
        with clientes_lock:
            if (connection, client_address) in clientes_conectados:
                clientes_conectados.remove((connection, client_address))
                # Verificamos si la conexión sigue abierta antes de enviar el mensaje de cierre
                if connection.fileno() != -1:
                        connection.send("CIERRE DE SERVIDOR".encode())
                        connection.close()
        print(f"Conexión cerrada con {client_address[1]}")
        mensaje_por_ventana(f"Conexión cerrada con {usuario}")


#Recorre la lista donde estan las conexiones y las cierra, una vez terminado limpia la lista.

def close_all_connections():
    global clientes_conectados
    # Cerrar conexiones de clientes y enviar mensaje de cierre
    print_list_clientes_conectados()
    with clientes_lock: 
        for connection, client_address in clientes_conectados:
            try:
                connection.send("CIERRE DE SERVIDOR".encode())
                connection.close()
            except Exception as e:
                print(f"Error al enviar mensaje de cierre a {client_address}: {e}")
        #despues de cerrar todas las conexiones vaciamos la lista
        clientes_conectados.clear()
    print_list_clientes_conectados()
    ventana.after(TIME_BEFORE_CLOSE_SERVER_WINDOWS, ventana.destroy) #destruir la ventana principal


#Print por la terminal de los clientes
def print_list_clientes_conectados():
    global clientes_conectados
    print("---------------------------")
    
    with clientes_lock:
        if(len(clientes_conectados) == 0):
            print("**Ningun cliente conectado al servidor** ")
            return
        print(f"tamaño de la lista: {len(clientes_conectados)}")
        for connection, client_address in clientes_conectados:
            print(f"cliente conectado: {client_address[1]}")
    print("---------------------------")       

#Hilo que crea el servidor en el puerto correspondiente y escucha a clientes creando un hilo por cada cliente
#Una vez la flag de que se ha tocado el boton se activa sale del bucle y realiza el cierre de todos las conexiones para finalizar 
def create_server(port):
    global clientes_conectados
    server = socket(AF_INET,SOCK_STREAM)
    server_address = ('127.0.0.1',port)
    server.bind(server_address)
    server.listen(1)
    print("Servidor escuchando en el puerto: ",port)
    message= f"Servidor escuchando en el puerto: {port}"
    mensaje_por_ventana(message)
    # Loop del  servidor mientras que no se le de al boton cerrar servidor
    while not stop_event.is_set(): 
        try:
            server.settimeout(1.0)  # Timeout para verificar el evento de parada cada segundo
            connection, client_address = server.accept()
            client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
            client_thread.start()
        except timeout:
            continue
    # Cerrar conexiones de clientes y enviar mensaje de cierre
    close_all_connections()
    #cerramos finalmente el servidor
    if(len(clientes_conectados) == 0):
        server.close()
        print("Servidor cerrado")
        mensaje_por_ventana("Se ha cerrado el servidor")

# Función que se ejecutará al pulsar el botón de crear el servidor crea el hilo create_server
def boton_click():
    texto = cuadro_texto_puerto.get()
    try:
        numero = int(texto)
        if numero < 0 or numero > 65535 :
            print("El puerto tiene que estar en el rango de [0,65535]")
            return
        # desactivar cuadro de texto y boton despues de iniciar el servidor
        cuadro_texto_puerto.config(state='disabled')
        boton.config(state='disabled')
        #activar boton para cerrar el servidor
        boton_cerrar.config(state='normal')
        #crear hilo del servidor
        server_thread = threading.Thread(target=create_server,args=(numero,))  
        server_thread.start() 
    except ValueError:
        mostrar_error_entero()

#funcion que se activa una vez se toca el botón cerrar servidor, activa flag para cerrar servidor y inhabilita el boton 
def cerrar_servidor():
    stop_event.set()
    boton_cerrar.config(state='disabled')
    
#Comprueba si el puerto escrito por la ventana es un entero
def mostrar_error_entero():
    ventana_no_entero = tk.Toplevel(ventana)
    ventana_no_entero.title("Error")
    ventana_no_entero.geometry("300x100")  # Ajusta el tamaño de la ventana de error

    # Centrar la ventana de error respecto a la ventana principal
    ventana_no_entero.transient(ventana)
    ventana_no_entero.grab_set()
    ventana_no_entero.update_idletasks()
    x = ventana.winfo_x() + (ventana.winfo_width() // 2) - (ventana_no_entero.winfo_width() // 2)
    y = ventana.winfo_y() + (ventana.winfo_height() // 2) - (ventana_no_entero.winfo_height() // 2)
    ventana_no_entero.geometry(f"+{x}+{y}")

    tk.Label(ventana_no_entero, text="Por favor introduce un valor entero").grid(row=0, column=0, padx=20, pady=20)
    ventana_no_entero.mainloop()

#comprueba si ha habido algún problema al encontrar el tiempo en la página web
def mostrar_error_clima():
    ventana_no_clima = tk.Toplevel(ventana)
    ventana_no_clima.title("Error")
    ventana_no_clima.geometry("300x100")  

    # Centrar la ventana de error respecto a la ventana principal
    ventana_no_clima.transient(ventana)
    ventana_no_clima.grab_set()
    ventana_no_clima.update_idletasks()
    x = ventana.winfo_x() + (ventana.winfo_width() // 2) - (ventana_no_clima.winfo_width() // 2)
    y = ventana.winfo_y() + (ventana.winfo_height() // 2) - (ventana_no_clima.winfo_height() // 2)
    ventana_no_clima.geometry(f"+{x}+{y}")

    tk.Label(ventana_no_clima, text="No se pudo obtener el clima").grid(row=0, column=0, padx=20, pady=20)
    ventana_no_clima.mainloop()

#obtener la temperatura en valencia desde la página web una vez un cliente envie el mensaje: "TIEMPO"
def obtener_clima_valencia():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Valencia,ES&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperatura = data['main']['temp']
        return f"La temperatura en valencia hoy es de {temperatura}°C"
    else:
        mostrar_error_clima()

#Funcion encarga de imprimir por la ventana principal los mensajes
def mensaje_por_ventana(message):
    ventana.after(0, cuadro_texto_destino.insert, tk.END, f"{message}\n")
    ventana.after(0, cuadro_texto_destino.yview_moveto, 1.0)    
    
    
if __name__ == '__main__':
    # Creamos la ventana
    ventana = tk.Tk()
    ventana.title("Recibir mensajes")
    # Creamos una etiqueta
    tk.Label(ventana, text='Puerto servidor:').grid(row=0, column=0)
    # Creamos un cuadro de texto que acepta una sola línea
    cuadro_texto_puerto = tk.Entry(ventana)
    cuadro_texto_puerto.grid(row=0, column=1)
    #Creamos un botón
    boton = tk.Button(ventana, text="Iniciar servidor en un nuevo hilo", command=boton_click)
    boton.grid(row=1, column=1, columnspan=2)
    # Creamos un cuadro de texto que acepta varias líneas
    cuadro_texto_destino = tk.Text(ventana)
    cuadro_texto_destino.grid(row=2, column=0, columnspan=2)
    # Creamos el scrollbar y lo asociamos al cuadro de texto
    scrollbar = tk.Scrollbar(ventana)
    scrollbar.grid(row=2, column=2, sticky=tk.NS)
    cuadro_texto_destino.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=cuadro_texto_destino.yview)
    #Boton para cerrar el servidor
    # Creamos el botón "Cerrar servidor" y lo colocamos debajo del cuadro de texto
    boton_cerrar = tk.Button(ventana, text="Cerrar servidor", command=cerrar_servidor, font=("Arial", 12, "bold"))
    boton_cerrar.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    #Hasta que no se cree el servidor el boton estara desactivado
    boton_cerrar.config(state='disabled')
    # Visualizamos la ventana
    ventana.mainloop()
    
