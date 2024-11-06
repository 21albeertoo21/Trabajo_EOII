Ultimos cambios a hacer si dios quiere:

(HECHO)1. Poner boton cerrar servidor funcione siempre, aunque haya clientes. Otra manera es que si detecta client que se cierra la ventana cerrar el hilo de cliente

(HECHO)2. En el fichero servidor.py la variable global numero_clientes es de tipo diccionario, cambiarla de tipo 

3. Ha aparecido un bug de repente, lo que pasa es que cuando se empieza a toquitear que si abrir cerrar ventanas, como el cerrar ventanas no se hace desde el main, se ve que es posible que de fallos, y los da de vez en cuando. Solución: guardar desde el main en un vector todas las ventanas que se van creando y un booleano y que cada cierto tiempo compruebe desde el main el valor del booleano si estan a false significa que hay que eliminar la ventana y por tanto el main se encargara de eliminar la ventana exacta que toque, y eliminarla del vector, ademas valdria la pena utilizar un mutex para evitar problemas de concurrencia al añadir o eliminar ventanas.
4. Tambien se podria poner un evento cuando se de a la x de la ventana para cerrar tambien la conexion ("Enviar FIN")