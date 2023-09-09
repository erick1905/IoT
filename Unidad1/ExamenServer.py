import http.server
import socketserver
import json
#definicion de puerto
port = 8040
#Contador en ceros
contador=0

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        global contador
        if self.path == '/contador':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str(contador).encode())
        else:
            # Si la ruta no es "/contador", responder con 404 Not Found
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        global contador
        # verifica si la ruta de la solicitud POST es "/actualizar_contador"
        if self.path == '/actualizar_contador':
            #se obtiene la longitud del cuerpo del mensaje POST
            content_length = int(self.headers['Content-Length'])
            # lee el contenido del cuerpo de la solicitud POST
            post_data = self.rfile.read(content_length)
            #contenido JSON se decodifica y se convierte en un objeto Python
            data = json.loads(post_data.decode('utf-8'))
            #extraen las claves 'action' y 'quantity' del objeto JSON para determinar la acción a realizar en el contador
            action = data.get('action')
            quantity = data.get('quantity')
            
            if action == 'asc':
                contador += quantity
            elif action == 'desc':
                contador -= quantity

            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Contador actualizado')
        else:
            # Si la ruta no es "/actualizar_contador", responder con 404 Not Found
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')
            
#Se configura el server para recibir el puerto especificado.
with socketserver.TCPServer(("", port), MyRequestHandler) as httpd:
    print(f"Servidor HTTP activo en el puerto {port}")
    try:
        # Inicia el servidor y mantenlo en ejecución.
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Detén el servidor si se presiona Ctrl+C.
        print("Servidor detenido.")
