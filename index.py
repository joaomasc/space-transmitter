import socket
import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

host = "127.0.0.1"
port = 443

def send_file(filename):
    try:
        filesize = os.path.getsize(filename)
    except FileNotFoundError:
        print('Arquivo não encontrado!')
        return
    except Exception as e:
        print(f'Erro ao obter o tamanho do arquivo: {e}')
        return

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            print(f"Conectando com {host}:{port}")
            tcp_socket.connect((host, port))
            tcp_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

            progress = tqdm.tqdm(range(filesize), f"Enviando: {filename}", unit="B", unit_scale=True, unit_divisor=256)
            with open(filename, "rb") as file:
                while True:
                    bytes_read = file.read(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    tcp_socket.sendall(bytes_read)
                    progress.update(len(bytes_read))

            print(f"{filename} enviado com sucesso.")

    except Exception as e:
        print(f'Erro ao enviar o arquivo: {e}')

if __name__ == "__main__":
    file_to_send = input("Digite o caminho completo do arquivo para enviar: ")
    send_file(file_to_send)