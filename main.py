from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from bs4 import BeautifulSoup
import requests

# Definición del servidor Flask
app = Flask(__name__)

# Libreria Limiter para restringir solicitudes
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per minute"],
    storage_uri="memory://",
)

# Configurar la autenticación básica
app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin123'
basic_auth = BasicAuth(app)


# Ruta /search para el app
@app.route('/search', methods=['GET'])
@limiter.limit("20 per minute")  # 20 por minuto
@basic_auth.required  # Requiere autenticación
def search_entity():
    try:
        # Parámetro nombre
        entity_name = request.args.get('name')

        # Url de OFFSHORE LEAKS DATABASE
        url = f'https://offshoreleaks.icij.org/search?q={entity_name}&c=&j=&d='

        # Usar headers de ejemplo para evitar error 403 (solicitud bloqueada)
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/58.0.3029.110 Safari/537.3'}

        # Realizar solicitud HTTP
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Esto generará una excepción para códigos de estado HTTP no exitosos

        # Iniciar el parser html de BS
        soup = BeautifulSoup(response.text, 'html.parser')

        # Imprimir el contenido HTML para entender la estructura en la consola (debug only)
        # print(f'Status Code: {response.status_code}')
        # print(soup.prettify())

        # Extraer información de  Offshore Leaks Database
        table = soup.find('table', class_='search__results__table')
        result = []

        if table:
            rows = table.find_all('tr')  # Obtener todas las filas de la tabla

            for row in rows:
                entity_info = {}
                cells = row.find_all('td')  # Obtener todas las celdas de la fila

                # Extraer información de las celdas de una fila
                if len(cells) >= 4:
                    entity_info['ENTITY'] = cells[0].text.strip()
                    entity_info['JURISDICTION'] = cells[1].text.strip()
                    entity_info['LINKED TO'] = cells[2].text.strip()
                    entity_info['DATA FROM'] = cells[3].text.strip()
                    result.append(entity_info)

        hits = len(result)

        if hits == 0:
            return jsonify({'status': 'success', 'hits': hits, 'data': 'No se encontraron resultados'})
        else:
            return jsonify({'status': 'success', 'hits': hits, 'data': result})

    except requests.exceptions.HTTPError as http_err:
        return jsonify({'status': 'error', 'message': f'Error de HTTP: {http_err}'})

    except Exception as err:
        return jsonify({'status': 'error', 'message': f'Error general: {err}'})

    finally:
        pass


if __name__ == '__main__':
    app.run(debug=True)
