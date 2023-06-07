import socket
import json

IP = '127.0.0.1'
PORT = 5000

SOCK_BUFFER = 1024

def guardaEnArchivo(paciente_dic:dict,nomArch:str):
    with open(nomArch,"a+") as arch:# 'a+' indica que vamos a abrir el archivo para añadir info al final
        list_str = [str(valor) for valor in paciente_dic.values()]
        arch.write(','.join(list_str))
        arch.write('\n')


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (IP,PORT)

    s.bind(server_address)
    s.listen(5)

    while True:
        try:
            conn,client_address = s.accept()
            try:
                opcion = conn.recv(SOCK_BUFFER).decode('utf8')
                if opcion == '1':
                    msg_raw = conn.recv(SOCK_BUFFER).decode('utf8')
                    paciente_dic = json.loads(msg_raw)#Convertimos de string a diccionario
                    #print(alumno_dict)
                    guardaEnArchivo(paciente_dic,"pacientes.csv")
                elif opcion == '2':
                    with open("pacientes.csv","rb") as f:
                        while True:
                            msg = f.read(1024)
                            if not msg:
                                break
                            conn.sendall(msg)#El archivo se va a estar enviando en paquetes de 1024 bytes
            except ConnectionResetError:
                print("El cliente la conexión de manera abrupta")
            finally:
                print("Cerrando conexión con el cliente")
                conn.close()
        except KeyboardInterrupt:
            print("Se cerro el servidor")
