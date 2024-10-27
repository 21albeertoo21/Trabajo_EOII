import tkinter as tk
from socket import *
import pickle 
import sys
import datetime 
import threading
import requests

#Llave para poder utilizar la API de OpenWeatherMap para obtener la información del tiempo en valencia
API_KEY = "cbf557829a16f6572809313ff5b76dd0"

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

def obtener_clima_valencia():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Valencia,ES&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        temperatura = data['main']['temp']
        return f"La temperatura en valencia hoy es de {temperatura}°C"
    else:
        mostrar_error_clima()

def handle_client(connection, client_address):
    print(f"conexion establecida con puerto {client_address[0]}")
    try:
        while True:
            data = connection.recv(1024)
            data_decode = data.decode()
            if data:
                if data_decode == "FIN":
                    break
                elif data_decode == "HORA":
                    hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
                    ventana.after(0, cuadro_texto_destino.insert, tk.END, f"Cliente en puerto {client_address[1]}: {hora_actual}\n")
                    ventana.after(0, cuadro_texto_destino.yview_moveto, 1.0)
                elif data_decode == "Tiempo en Valencia hoy":
                    data = obtener_clima_valencia()
                    ventana.after(0, cuadro_texto_destino.insert, tk.END, f"Cliente en puerto {client_address[1]}: {data}\n")
                    ventana.after(0, cuadro_texto_destino.yview_moveto, 1.0)
                else:
                    ventana.after(0, cuadro_texto_destino.insert, tk.END, f"Cliente en puerto {client_address[1]}: {data_decode}\n")
                    ventana.after(0, cuadro_texto_destino.yview_moveto, 1.0)
    finally:
        connection.close()
        print(f"Conexion cerrada con {client_address[1]}")
        ventana.after(0, cuadro_texto_destino.insert, tk.END, f"Conexion cerrada con {client_address[1]}\n")
        ventana.after(0, cuadro_texto_destino.yview_moveto, 1.0)

#Create server socket TCP
def create_server(port):
    server = socket(AF_INET,SOCK_STREAM)
    server_address = ('127.0.0.1',port)
    server.bind(server_address)
    server.listen(1)
    print("Servidor escuchando en el puerto",port)
    while True:
        connection,client_address = server.accept()
        client_thread=threading.Thread(target=handle_client,args=(connection,client_address))
        client_thread.start()
        

# Función que se ejecutará al pulsar el botón
def boton_click():
    texto = cuadro_texto_puerto.get()
    try:
        numero = int(texto)
        #cuadro_texto_destino.insert(tk.END, f"{numero}\n")
        #cuadro_texto_destino.yview_moveto(1.0)
        # desactivar cuadro de texto y boton despues de iniciar el servidor
        cuadro_texto_puerto.config(state='disabled')
        boton.config(state='disabled')
        #crear hilo del servidor
        server_thread = threading.Thread(target=create_server,args=(numero,))  
        server_thread.start() 
    except ValueError:
        mostrar_error_entero()




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
    # Visualizamos la ventana
    ventana.mainloop()
    

    
    
    