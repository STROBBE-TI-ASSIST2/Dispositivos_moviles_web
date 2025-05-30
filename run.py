from app import create_app
import socket

app = create_app()

if __name__ == '__main__':
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"Servidor corriendo en: http://{local_ip}:5000/")

    app.run(host='0.0.0.0', port=5000, debug=True)