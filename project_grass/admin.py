from re import U
from flask import redirect, url_for
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField, Select2Widget
from flask_admin.menu import MenuLink
from flask_login import current_user
from wtforms_sqlalchemy.fields import QuerySelectField
#from app import university
def get_university():
    from app import university
    return university

from config import Config
from models import User, db
from models import University


# Кастомна головна сторінка адмінки
class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("login"))
        return super().index()


# Обмежений доступ до адмінки
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))


class UserAdmin(AdminModelView):
    column_list = ["id", "username"]
    column_labels = {"username": "Логін"}
    can_edit = False  # Вимикаємо можливість редагування
    can_create = False  # Вимикаємо можливість створення нових користувачів
    can_view_details = True  # Дозволяємо перегляд користувача


class CategoryAdmin(AdminModelView):
    column_labels = {"name": "Назва"}


# Обираємо категорію для товару
class ProductAdmin(AdminModelView):
    column_list = ("category", "name", "price")
    column_labels = {
        "category": "Категорія",
        "name": "Назва",
        "price": "Ціна",
        "description": "Опис товару",
    }
    form_columns = ["category", "name", "price", "picture", "description"]
    form_overrides = {"category": QuerySelectField, "picture": FileUploadField}
    form_args = {
        "category": {
            "query_factory": lambda: university.query.all(),
            "get_label": "name",
            "allow_blank": False,
            "widget": Select2Widget(),
        },
        "picture": {
            "label": "Зображення",
            "base_path": Config.UPLOAD_FOLDER,
            "allowed_extensions": {"png", "jpg", "jpeg", "gif"},
        },
    }


# Створюємо об'єкт адмінки
admin = Admin(
    name="Адмінка Unifinder",
    template_mode="bootstrap4",
    index_view=MyAdminIndexView(),
)

admin.add_link(MenuLink(name=" Перейти до переліку унівеситетів", url="/"))
admin.add_link(MenuLink(name=" Вийти", url="/logout"))
# Додаємо моделі в адмінку
admin.add_view(CategoryAdmin(University, db.session, name="Категорії"))
admin.add_view(UserAdmin(User, db.session, name="Користувачі"))
