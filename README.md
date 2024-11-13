Ultimos cambios a hacer si dios quiere:

(HECHO)1. Poner boton cerrar servidor funcione siempre, aunque haya clientes. Otra manera es que si detecta client que se cierra la ventana cerrar el hilo de cliente

(HECHO)2. En el fichero servidor.py la variable global numero_clientes es de tipo diccionario, cambiarla de tipo 

(HECHO)3. Ha aparecido un bug de repente, lo que pasa es que cuando se empieza a toquitear que si abrir cerrar ventanas, como el cerrar ventanas no se hace desde el main, se ve que es posible que de fallos, y los da de vez en cuando. Solución: guardar desde el main en un vector todas las ventanas que se van creando y un booleano y que cada cierto tiempo compruebe desde el main el valor del booleano si estan a false significa que hay que eliminar la ventana y por tanto el main se encargara de eliminar la ventana exacta que toque, y eliminarla del vector, ademas valdria la pena utilizar un mutex para evitar problemas de concurrencia al añadir o eliminar ventanas.
(HECHO)4. Tambien se podria poner un evento cuando se de a la x de la ventana para cerrar tambien la conexion ("Enviar FIN")
(HECHO) 5. NUevo problema: cuando le das al boton de cerrar servidor saltan muchos errores
6. Testear un poco más aunq yo lo veo GOD
7. Crear mini doc explicando un poco todo/ limpiar y hacer código más clean con comentarios que expliquen las funciones y un comentario al principio explicando un poco el funcionamiento de la clase

El objetivo de este proyecto ha sido crear una comunicación cliente servidor que permita al usuario crear todos los clientes que quiera dentro de un servidor, además de permitir que haya varios servidores con distintos clientes. Para hacerlo más friendly para el usuario, este tendrá un nombre de usuario que dentro de un servidor no podrá ser duplicado.
Además hemos buscado la robustez dentro de la aplicación con el fin de que no se den casos extraordinarios durante la ejecución de la aplicación
Modo de funcionamiento:
1. Ejecuta el script del servidor y elige un puerto.
2. Ejecuta el script del cliente, al crear el usuario necesitaras poner la ip, en este caso usamos la local_ip (127.0.0.1), el puerto del servidor activo y el nombre del usuario.
3. Una vez creado el usuario se te abrirá una nueva ventana en la que de titulo saldrá tu usuario y podrás enviar mensajes directos al usuario.
    los mensajes saldrán en el servidor con el usuario que los ha enviado.
    Las palabras claves son:
    FIN-> Finaliza la conexion con el servidor
    HORA-> El servidor devuelve la hora actual
    TIEMPO -> El servidor guiandose de una web de tiempo, devuelve el tiempo actual en Valencia (temperatura)
4. Como ultimo puedas clickar el botón cerrar servidor de la ventana servidor, este se encargará de cerrar todas las conexiones con los     
     clientes,   y de eliminar la ventana del servidor terminando la ejecución del programa

     Además la aplicación permite que te crees más de un servidor y que puedas asignar los usuarios a distintos servidores.

    Por último aunque usemos el usuario y no el puerto, desde la terminal se va siguiendo el proceso mediante mensajes para que se pueda
    saber cada usuario a que puerto están asociados. 