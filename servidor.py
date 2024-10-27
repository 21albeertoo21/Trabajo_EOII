import tkinter as tk
from socket import *
import pickle 
import sys
from datetime import datetime
import threading
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
def mostrar_info_puerto():
    ventana_info = tk.Toplevel(ventana)
    ventana_info.title("Servidor en ejecución")
    ventana_info.geometry("300x100")
    ventana_info.transient(ventana)
    ventana_info.grab_set()
    ventana_info.update_idletasks()
    x = ventana.winfo_x() + (ventana.winfo_width() // 2) - (ventana_info.winfo_width() // 2)
    y = ventana.winfo_y() + (ventana.winfo_height() // 2) - (ventana_info.winfo_height() // 2)
    ventana_info.geometry(f"+{x}+{y}")

    # Mensaje de información
    tk.Label(ventana_info, text="Servidor ya está en ejecución en un puerto.").grid(row=0, column=0, padx=20, pady=20)
    tk.Label(ventana_info, text="Para cambiar el puerto, cierra el servidor.").grid(row=1, column=0, padx=20, pady=20)
    
    
def handle_client(connection, client_address):
    print(f"conexion establecida con puerto {client_address[0]}")
    try:
        while True:
            data = connection.recv(1024)
            data_decode = data.decode()
            if not data:
                print("no datos del cliente con puerto: ", client_address[1])
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
    ventana.after(0, mostrar_info_puerto)
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
    

    
    
    