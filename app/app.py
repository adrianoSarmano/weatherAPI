import os
import requests
import psycopg2
from datetime import datetime
from flask import Flask, jsonify, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Constantes e Parametros de configuração do .env 
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DEFAULT_CITY = 'Florianopolis'

# Conecta ao banco de dados e retorna a conexão
def get_db_connection():
    try:
        connection = psycopg2.connect(host='postgres', database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        return connection
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        raise

# Criar a tabela caso não exista
def create_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(100) NOT NULL,
            temperature FLOAT NOT NULL,
            humidity FLOAT NOT NULL,
            pressure FLOAT NOT NULL,
            wind_speed FLOAT NOT NULL,
            description TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL
        )
    """)
    connection.commit()
    cursor.close()
    connection.close()

# Salvar dados da cidade no banco de dados
def save_weather_data(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO weather_data 
        (city, temperature, humidity, pressure, wind_speed, description, timestamp) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data['city'], 
        data['temperature'], 
        data['humidity'], 
        data['pressure'], 
        data['wind_speed'], 
        data['description'], 
        data['timestamp']
    ))
    connection.commit()
    cursor.close()
    connection.close()

# Busca dados da API OpenWeather e salva no banco de dados
def get_weather_data(city=DEFAULT_CITY):
    
    URL = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'units': 'metric',
        'appid': OPENWEATHER_API_KEY
    }
    response = requests.get(URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'city': city,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'timestamp': datetime.now()
        }
        save_weather_data(weather_data)
        return weather_data
    else:
        return None

# Endpoint para obter dados atuais
@app.route('/api/now', methods=['GET'])
def get_weather_now():
    city = request.args.get('city', DEFAULT_CITY)
    data = get_weather_data(city)
    if data:
        return jsonify(data)
    return jsonify({"error": "Não foi possível obter os dados climáticos"}), 404

# Endpoint para obter histórico
@app.route('/api/history', methods=['GET'])
def get_weather_history():
    city = request.args.get('city', DEFAULT_CITY)
    limit = request.args.get('limit', 10, type=int)
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT city, temperature, humidity, pressure, wind_speed, description, timestamp 
        FROM weather_data 
        WHERE city = %s 
        ORDER BY timestamp DESC 
        LIMIT %s
    """, (city, limit))
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    
    result = []
    for row in rows:
        result.append({
            'city': row[0],
            'temperature': row[1],
            'humidity': row[2],
            'pressure': row[3],
            'wind_speed': row[4],
            'description': row[5],
            'timestamp': row[6].isoformat()
        })
    
    return jsonify(result)


# Cria a tabela no banco caso ainda não exista
create_table()

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)