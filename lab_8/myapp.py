from jinja2 import Environment, PackageLoader, select_autoescape
from models.author import Author
from models.app import App
from models.user import User
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import datetime
import json
from utils .currencies_api import get_currencies
from models.user_currency import UserCurrency
from models.currency import Currency

# Инициализация Jinja2
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

main_author = Author('Роза Тихонова', 'P3122')


main_app = App(
    name="CurrenciesListApp", 
    version="1.0.0", 
    author = main_author
)

#delete
test_users = [
    User(1, "Бред Питт"),
    User(2, "Самовар Самоваров"),
    User(3, "Миллионер Миллиардерович"),
    User(4, "Роза Тихонова"),
    User(5, "Петр Скалкин"),
    User(6, "Тимофей Скакалкин"),
    User(7, "Катя Адушкина"),
    User(8, "Прасковья Изподмосковья"),
    User(9, "Редиска Огородовна"),
    User(10, "Ольга Любимка"),
]




# currency_dictionary = get_currencies()
currency_dictionary = {'USD': 76.9708, 'EUR': 89.9011, 'GBP': 102.6098, 'JPY': 49.585, 'CNY': 10.8487, 'KZT': 15.2753, 'CHF': 96.2496, 'CAD': 55.1802, 'AUD': 50.9085, 'SGD': 59.3865, 'HKD': 99.0615, 'NOK': 76.3819, 'SEK': 81.9804, 'TRY': 18.1499, 'PLN': 21.2503, 'DKK': 12.0244, 'HUF': 23.5522, 'CZK': 37.256, 'RON': 17.6373, 'BGN': 45.919, 'BRL': 14.4924, 'INR': 85.3463, 'UAH': 18.2381, 'BYN': 26.5811, 'AMD': 20.1949}


class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Обработка GET-запросов"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        # Устанавливаем общие заголовки
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Обработка разных маршрутов
        response_html = ""
        
        if path == "/" or path == "/index.html":
            # Главная страница
            template = env.get_template("index.html")
            response_html = template.render(
                myapp=main_app.name,
                author_name=main_author.name,
                group=main_author.group,
                navigation=[
                    {'caption': 'Основная страница', 'href': '/'},
                ],
            )
            
        elif path == "/users":
            # Загружаем users.html - отдельный файл
            template = env.get_template("users.html")
            response_html = template.render(
                myapp="CurrenciesListApp",
                users=test_users,
                author_name=main_author.name,
            )
            
        elif path == "/currencies":
            # Загружаем currencies.html - отдельный файл
            template = env.get_template("currencies.html")
            response_html = template.render(
                myapp="CurrenciesListApp",
                author_name=main_author.name,
                currencies_dict = currency_dictionary,
            )
            
        elif path == "/user":
            # Загружаем user_detail.html - отдельный файл
            user_id = int(query_params.get('id', [1])[0])
            user = next((u for u in test_users if u.id == user_id), None)
            
            template = env.get_template("user_detail.html")
            response_html = template.render(
                myapp="CurrenciesListApp",
                user=user,
                author_name=main_author.name,
            )
        
            
        elif path == "/author":
            template = env.get_template("author.html")
            response_html = template.render(
                myapp="CurrenciesListApp",
                author = main_author,
            )
                
        elif path == "/api/users":
            users_data = [
                {"id": user.id, "name": user.name}
                for user in test_users
            ]
            template = env.get_template('users.html')
            response_html = template.render(
                myapp="CurrenciesListApp",
                author=main_author,
                users=users_data 
            )
            
        else:
            # 404
            template = env.get_template("index.html")
            response_html = template.render(
                myapp=main_app.name,
                author_name=main_author.name,
                group=main_author.group,
                navigation=[
                    {'caption': 'На главную', 'href': '/'},
                    {'caption': 'Пользователи', 'href': '/users'}
                ],
                page_title="404 - Страница не найдена",
                message=f"Страница {path} не существует"
            )
        
        # Отправляем ответ
        self.wfile.write(response_html.encode('utf-8'))
    
def run_server(port=8080):
    server_address = ('localhost', port)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    
    print(f"""
    Сервер запущен на http://localhost:{port}
    Доступные маршруты:
    
    • /              - Главная страница
    • /users         - Список пользователей
    • /currencies    - Курсы валют
    • /author        - Информация об авторе
    • /api/users     - API пользователей (JSON)

    Для остановки нажмите Ctrl+C
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
        httpd.server_close()

if __name__ == "__main__":
    run_server(8080)