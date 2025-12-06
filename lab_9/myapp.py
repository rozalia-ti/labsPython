"""
Главное приложение - точка входа
"""

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
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        
        try:
            # Главная страница
            if path == "/":
                template = env.get_template("index.html")
                html = template.render(myapp=app.name, title="Главная")
            
            # Пользователи
            elif path == "/users":
                template = env.get_template("users.html")
                users = db.read_users()
                html = template.render(myapp=app.name, title="Пользователи", users=users)
            
            # Детали пользователя
            elif path == "/user":
                if 'id' in query:
                    user_id = int(query['id'][0])
                    user = db.read_user_by_id(user_id)
                    if user:
                        template = env.get_template("user_detail.html")
                        currencies = db.read_user_currencies(user_id)
                        html = template.render(
                            myapp=app.name, 
                            title=f"Пользователь {user.name}",
                            user=user, 
                            currencies=currencies
                        )
                    else:
                        html = self._render_404("Пользователь не найден")
                else:
                    html = self._render_404("Не указан ID пользователя")
            
            # Валюты (только просмотр)
            elif path == "/currencies":
                template = env.get_template("currencies.html")
                currencies = currency_controller.list_currencies()
                html = template.render(
                    myapp=app.name, 
                    title="Курсы валют", 
                    currencies=currencies
                )
            
            # Управление валютами (CRUD)
            elif path == "/currencies/crud":
                template = env.get_template("currencies_crud.html")
                currencies = currency_controller.list_currencies()
                message = query.get('message', [''])[0]
                message_type = query.get('message_type', ['info'])[0]
                html = template.render(
                    myapp=app.name,
                    title="Управление валютами",
                    currencies=currencies,
                    message=message,
                    message_type=message_type
                )
            
            # Синхронизация валют
            elif path == "/currency/sync":
                count = currency_controller.sync_currencies_from_api()
                if count > 0:
                    message = f"Добавлено {count} валют"
                    mtype = "success"
                else:
                    message = "Нет новых валют или ошибка"
                    mtype = "warning"
                
                self.send_response(302)
                self.send_header('Location', f'/currencies/crud?message={message}&message_type={mtype}')
                self.end_headers()
                return
            
            # Обновление валюты
            elif path == "/currency/update":
                if 'code' in query:
                    code = query['code'][0]
                    if currency_controller.update_currency_from_api(code):
                        message = f"Валюта {code} обновлена"
                        mtype = "success"
                    else:
                        message = f"Ошибка обновления {code}"
                        mtype = "error"
                    
                    self.send_response(302)
                    self.send_header('Location', f'/currencies/crud?message={message}&message_type={mtype}')
                    self.end_headers()
                    return
                else:
                    html = self._render_404("Не указан код валюты")
            
            # Удаление валюты
            elif path == "/currency/delete":
                if 'id' in query:
                    currency_id = query['id'][0]
                    if db.delete_currency(currency_id):
                        message = "Валюта удалена"
                        mtype = "success"
                    else:
                        message = "Ошибка удаления"
                        mtype = "error"
                    
                    self.send_response(302)
                    self.send_header('Location', f'/currencies/crud?message={message}&message_type={mtype}')
                    self.end_headers()
                    return
                else:
                    html = self._render_404("Не указан ID валюты")
            
            # Создание валюты
            elif path == "/currency/create":
                if all(k in query for k in ['id', 'num_code', 'char_code', 'name', 'value', 'nominal', 'rate']):
                    try:
                        currency = Currency(
                            id=query['id'][0],
                            num_code=query['num_code'][0],
                            char_code=query['char_code'][0],
                            nominal=query['nominal'][0],
                            name=query['name'][0],
                            value=query['value'][0],
                            rate=query['rate'][0]
                        )
                        
                        if db.create_currency(currency):
                            message = f"Валюта {currency.char_code} добавлена"
                            mtype = "success"
                        else:
                            message = f"Валюта {currency.char_code} уже существует"
                            mtype = "warning"
                    except Exception as e:
                        message = f"Ошибка: {str(e)}"
                        mtype = "error"
                    
                    self.send_response(302)
                    self.send_header('Location', f'/currencies/crud?message={message}&message_type={mtype}')
                    self.end_headers()
                    return
                else:
                    html = self._render_404("Не все параметры указаны")
            
            # Об авторе
            elif path == "/author":
                template = env.get_template("author.html")
                html = template.render(myapp=app.name, title="Автор", author=author)
            
            # 404
            else:
                html = self._render_404(f"Страница {path} не найдена")
        
        except Exception as e:
            print(f"Ошибка: {e}")
            html = self._render_error(str(e))
        
        self.wfile.write(html.encode('utf-8'))
    
    def _render_error(self, error_msg):
        template = env.get_template("currencies_crud.html")
        currencies = currency_controller.list_currencies()
        return template.render(
            myapp=app.name,
            title="Ошибка",
            currencies=currencies,
            message=f"Ошибка: {error_msg}",
            message_type="error"
        )
    
    def _render_404(self, msg):
        template = env.get_template("404.html")
        return template.render(myapp=app.name, title="Ошибка", message=msg)

def run_server(port=8088):
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