from typing import Dict, List, Any, Optional
from jinja2 import Environment, PackageLoader
from models.app import App
from models.author import Author
from controllers.databasecontroller import DatabaseController
from controllers.currencycontroller import CurrencyController

class PagesController:
    """Контроллер для рендеринга страниц"""
    
    def __init__(self, 
                 db_controller: DatabaseController,
                 currency_controller: CurrencyController,
                 app: App,
                 author: Author):
        """
        Инициализация контроллера
        
        Args:
            db_controller: Экземпляр DatabaseController
            currency_controller: Экземпляр CurrencyController
            app: Объект приложения
            author: Объект автора
        """
        self.db = db_controller
        self.currency_ctrl = currency_controller
        self.app = app
        self.author = author
        
        self.env = Environment(
            loader=PackageLoader("myapp"),
            autoescape=True
        )
    
    def render_index(self) -> str:
        """
        Рендеринг главной страницы
        
        Returns:
            HTML страница
        """
        template = self.env.get_template("index.html")
        
        navigation = [
            {'href': '/users', 'caption': 'Пользователи'},
            {'href': '/currencies', 'caption': 'Валюты'},
            {'href': '/author', 'caption': 'Об авторе'},
            {'href': '/currency/sync', 'caption': 'Синхронизировать курсы'},
        ]
        
        return template.render(
            myapp=self.app.name,
            navigation=navigation,
            version=self.app.version
        )
    
    def render_users(self) -> str:
        """
        Рендеринг страницы со списком пользователей
        
        Returns:
            HTML страница
        """
        template = self.env.get_template("users.html")
        users = self.db.read_users()
        
        return template.render(
            myapp=self.app.name,
            users=users,
            author_name=self.author.name
        )
    
    def render_user_detail(self, user_id: int) -> str:
        """
        Рендеринг страницы детальной информации о пользователе
        
        Args:
            user_id: ID пользователя
            
        Returns:
            HTML страница
        """
        template = self.env.get_template("user_detail.html")
        
        user = self.db.read_user_by_id(user_id)
        if not user:
            return self.render_404(f"Пользователь с ID {user_id} не найден")
        
        currencies = self.db.read_user_currencies(user_id)
        
        return template.render(
            myapp=self.app.name,
            user=user,
            currencies=currencies,
            author_name=self.author.name
        )
    
    def render_currencies(self, 
                          message: str = "", 
                          message_type: str = "info") -> str:
        """
        Рендеринг страницы со списком валют
        
        Args:
            message: Сообщение для отображения
            message_type: Тип сообщения (info, success, warning, error)
            
        Returns:
            HTML страница
        """
        template = self.env.get_template("currencies.html")
        currencies = self.currency_ctrl.list_currencies()
        
        return template.render(
            myapp=self.app.name,
            currencies=currencies,
            author_name=self.author.name,
            message=message,
            message_type=message_type
        )
    
    def render_currencies_with_action_buttons(self) -> str:
        """
        Рендеринг страницы валют с кнопками действий (CRUD)
        
        Returns:
            HTML страница
        """
        template = self.env.get_template("currencies_crud.html")  
        currencies = self.currency_ctrl.list_currencies()
        
        return template.render(
            myapp=self.app.name,
            currencies=currencies,
            author_name=self.author.name
        )
    
    def render_author(self) -> str:
        """
        Рендеринг страницы об авторе
        
        Returns:
            HTML страница
        """
        template = self.env.get_template("author.html")
        
        return template.render(
            myapp=self.app.name,
            author=self.author
        )
    
    def render_404(self, message: str = "Страница не найдена") -> str:
        """
        Рендеринг страницы 404
        
        Args:
            message: Сообщение об ошибке
            
        Returns:
            HTML страница 404
        """
        template = self.env.get_template("404.html")
        
        return template.render(
            myapp=self.app.name,
            message=message,
            author_name=self.author.name
        )
    
    def render_success(self, title: str, message: str, redirect_url: str = "/") -> str:
        """
        Рендеринг страницы успешного выполнения операции
        
        Args:
            title: Заголовок
            message: Сообщение
            redirect_url: URL для перенаправления
            
        Returns:
            HTML страница
        """
        template = self.env.get_template("success.html")
        
        return template.render(
            myapp=self.app.name,
            title=title,
            message=message,
            redirect_url=redirect_url,
            author_name=self.author.name
        )