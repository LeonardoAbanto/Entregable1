REST API para realizar la búsqueda de una empresa en la base de Offshore Leaks Database.

Código fuente: main.py

Instrucciones de despliegue:
1. Instalar Python 3.10
2. (Recomendado) Configurar entorno virtual
3. Instalar las dependencias (Flask, beautifulsoup4, requests, Flask-BasicAuth, Flask-Limiter)
4. Ejecutar main.py
5. El servidor se estará ejecutando en http://127.0.0.1:5000/
6. Para realizar la búsqueda de una empresa, realizar la solicitud a http://127.0.0.1:5000/search?name={nombre-de-la-empresa}

Ejemplo de solicitud: http://127.0.0.1:5000/search?name=odebrecht
Resultado: ejemplo.json

Colección en Postman: https://www.postman.com/leonardoabanto/workspace/entrega1/collection/17383080-9c97a634-e879-4d00-a22b-2f1fc052d86c?action=share&creator=17383080

