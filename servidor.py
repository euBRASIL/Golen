import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# AF_INET

# O “AF_INET” representa o tipo de socket, existem dois para internet, o IPV4 e IPV6 que basicamente, fazendo um # paralelo, é como se fosse um sistema de endereços de casas, onde para você saber qual máquina vai se comunicar com # qual é necessário saber o endereço IP da outra máquina, o IPV4 é mais antigo, ele tem a capacidade de criar # endereços para bilhões de máquinas, porém, com o crescimento da internet, se fez necessário a criação de um novo # sistema com maior capacidade que é o IPV6.

# SOCK_STREAM E SOCK_DGRAM

# Já o “SOCK_STREAM” representa o tipo do protocolo, que nesse caso é o TCP (Transmission Control Protocol ou # Protocolo de controle de transmissão), mas também existe o “SOCK_DGRAM” que seria para o protocolo UDP (User # Datagram Protocol). A diferença entre os dois basicamente é que no TCP existe um sistema para garantir que todos os # pacotes de dados sejam enviados, uma conexão é estabelecida antes da transmissão e depois fechada. Enquanto no UDP, # não existe um sistema que garanta que todos os dados serão recebidos, o que torna esse tipo de conexão mais leve e # rápida. Geralmente utiliza-se o UDP para, por exemplo, chats em tempo real com câmera e compartilhamento de tela # como o google meet, o zoom ou o skype (por isso, que às vezes a imagem da outra pessoa “congela”), já um exemplo com # o TCP seria um chat por texto, onde é uma prioridade maior que a mensagem chegue completa ao destino do que o tempo # de resposta.


HOST = '127.0.0.1'
PORT = 14532

server.bind((HOST, PORT))
server.listen()
print(f"Server escutando na porta: {PORT}")


clients = []
usernames = []

def sendMessage(message):
    for client in clients:
        client.send(message)



def handle(client, username):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            sendMessage(f"[{username}] {message}".encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            usernames.remove(username)
            sendMessage(f"{username} desconectou do servidor.".encode('utf-8'))
            break


def receive():
    while True:
        client, address = server.accept()
        client.send("USERNAME".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
 
        print(f"O usuário {username} se conectou no servidor! endereço: {address}")
        sendMessage(f"{username} entrou no chat.".encode('utf-8'))
        clients.append(client)
        client.send('Conectado ao servidor!'.encode('utf-8'))
                    	
        thread = threading.Thread(target=handle, args=(client, username, ))
        thread.start()

receive()