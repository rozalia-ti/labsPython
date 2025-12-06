# Лабораторная работа №9 - CRUD приложение для управления курсами валют
### Выполнила Тихонова Роза P3122

## Архитектура проекта
Проект реализован по принципу MVC (Model-View-Controller):
- **models/** - модели данных (Author, App, User, Currency, UserCurrency)
- **controllers/** - контроллеры бизнес-логики (DatabaseController, CurrencyController)
- **templates/** - HTML шаблоны для представления (Jinja2)
- **api.py** - абстракция для работы с внешними API (ЦБ РФ)
- **myapp.py** - точка входа, HTTP сервер и маршрутизация

## Основные файлы

### myapp.py
Главный файл приложения, содержащий HTTP сервер на базе стандартной библиотеки Python.

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import os
from jinja2 import Environment, FileSystemLoader
from models.author import Author
from models.app import App
from models.currency import Currency
from controllers.databasecontroller import DatabaseController
from controllers.currencycontroller import CurrencyController
from api import MockApi

# Инициализация основных объектов
author = Author('Роза Тихонова', 'P3122')
app = App('CurrenciesApp', '1.0', author)

# Инициализация БД и контроллеров
db = DatabaseController()
currency_controller = CurrencyController(db)

# Заполнение начальными данными
db.populate_initial_data(MockApi())

# Инициализация Jinja2
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
env = Environment(loader=FileSystemLoader(template_dir))

class RequestHandler(BaseHTTPRequestHandler):
    """
    Обработчик HTTP запросов. Наследуется от BaseHTTPRequestHandler.
    
    Механизм работы:
    1. Парсит URL и query-параметры с помощью urllib.parse
    2. Определяет маршрут по path
    3. Выполняет соответствующую бизнес-логику через контроллеры
    4. Рендерит HTML шаблоны с данными
    5. Отправляет ответ клиенту
    """
    
    def do_GET(self):
        """
        Обрабатывает все GET-запросы к серверу.
        
        Поддерживаемые маршруты:
        • / - Главная страница (index.html)
        • /users - Список пользователей (users.html)
        • /user?id=N - Детали пользователя (user_detail.html)
        • /currencies - Просмотр валют (currencies.html)
        • /currencies/crud - Управление валютами (currencies_crud.html)
        • /currency/sync - Синхронизация с API ЦБ РФ
        • /currency/update?code=USD - Обновление курса валюты
        • /currency/delete?id=R01235 - Удаление валюты
        • /currency/create - Добавление новой валюты
        • /author - Информация об авторе (author.html)
        
        Возвращает:
        HTTP ответ с HTML страницей или перенаправлением (302)
        """
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        try:
            if path == "/":
                template = env.get_template("index.html")
                html = template.render(myapp=app.name, title="Главная")
            elif path == "/users":
                template = env.get_template("users.html")
                users = db.read_users()
                html = template.render(myapp=app.name, title="Пользователи", users=users)
            # ... остальные маршруты
        except Exception as e:
            html = self._render_error(str(e))
        
        self.wfile.write(html.encode('utf-8'))
    
    def _render_error(self, error_msg):
        """Рендерит страницу с ошибкой"""
        template = env.get_template("currencies_crud.html")
        currencies = currency_controller.list_currencies()
        return template.render(
            myapp=app.name,
            title="Ошибка",
            currencies=currencies,
            message=f"Ошибка: {error_msg}",
            message_type="error"
        )

def run_server(port=8088):
    """
    Запускает HTTP сервер на указанном порту.
    
    Args:
        port: Порт для запуска сервера (по умолчанию 8088)
    
    Возвращает:
        None
    """
    server = HTTPServer(('localhost', port), RequestHandler)
    
    print(f"""
    Сервер запущен: http://localhost:{port}
    
    Маршруты:
    • /                - Главная страница
    • /users           - Пользователи
    • /user?id=N       - Детали пользователя
    • /currencies      - Курсы валют (просмотр)
    • /currencies/crud - Управление валютами (CRUD)
    • /author          - Об авторе
    
    CRUD операции:
    • /currency/sync      - Синхронизировать с API
    • /currency/update?code=USD - Обновить курс
    • /currency/delete?id=1     - Удалить валюту
    • /currency/create     - Форма добавления
    
    Ctrl+C для остановки
    """)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nСервер остановлен")
        db.close()
        server.server_close()

if __name__ == "__main__":
    run_server()