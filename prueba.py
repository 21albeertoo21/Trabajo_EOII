def insertar_dic(new_dic, new_user, port):
    if port not in new_dic:
        new_dic[port] = []
    if new_user not in new_dic[port]:
        new_dic[port].append(new_user)

def remover_dic(new_dic, new_user, port):
    if port in new_dic and new_user in new_dic[port]:
        new_dic[port].remove(new_user)
        if not new_dic[port]:  # Si la lista está vacía, elimina la clave del diccionario
            del new_dic[port]

def print_dic(new_dic):
    print(new_dic)

def comprobar_usuario(new_user, new_dic, port):
    return port in new_dic and new_user in new_dic[port]

if __name__ == "__main__":
    new_dic = {}
    insertar_dic(new_dic, "pepe", 1234)
    insertar_dic(new_dic, "juan", 1234)
    insertar_dic(new_dic, "luis", 1234)
    insertar_dic(new_dic, "pepe", 5678)
    print_dic(new_dic)
    if comprobar_usuario("pepe", new_dic, 1234):
        print("Usuario ya existe en el puerto 1234")
    else:
        print("Usuario no existe en el puerto 1234")
    remover_dic(new_dic, "pepe", 1234)
    print_dic(new_dic)