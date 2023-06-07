import socket
import json
import time
import matplotlib.pyplot as plt

IP = '127.0.0.1'
PORT = 5000

SOCK_BUFFER = 1024

def ingresarDatos() -> dict:
    print("Ingrese datos del paciente")
    paciente_dict = {}
    paciente_dict['nombre'] = input("Nombre: ")
    paciente_dict['apellido'] = input("Apellido: ")
    paciente_dict['peso'] = float(input("Peso: "))
    paciente_dict['talla'] = int(input("Talla: "))
    paciente_dict['edad'] = int(input("Edad: ")) 
    opcion = input("¿Cuenta con seguro? (s/n): ")
    if opcion == "s":
        paciente_dict['seguro'] = True
    else:
        paciente_dict['seguro'] = False
    return paciente_dict

print("Seleccione la opcion")
print("1 - Añadir paciente")
print("2 - Descargar base de datos")
opcion = input()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP,PORT)

    s.connect(server_address)

    try:
        if opcion == "1":
            s.sendall(b'1')
            paciente_dict = ingresarDatos()
            #print(paciente_dict)
            msg_json = json.dumps(paciente_dict)#Convertimos un diccionario en un string
            s.sendall(msg_json.encode())
        elif opcion == "2":
            s.sendall(b'2')
            lVelocidades = []
            lNumPaquetes = [] 
            with open("descarga.csv", 'wb') as f:#Creando el archivo f
                while True:
                    inicio = time.perf_counter()
                    msg = s.recv(1024)
                    fin = time.perf_counter()
                    lVelocidades.append(1024/(fin-inicio))#Las velocidad lo medimos en bytes/segundo
                    if not msg:
                        break
                    f.write(msg)
                lNumPaquetes = [i for i in range(1,len(lVelocidades)+1)]
                plt.plot(lNumPaquetes, lVelocidades)
                plt.savefig("Descarga.png")

                lVelocidades.sort()
                medianaVelocidades = lVelocidades[len(lVelocidades)//2]
                print(f"La velocidad de descarga promedio es {medianaVelocidades}")
    finally:
        print("Cerrando la comunicación entre el cliente y el servidor")
        s.close()