from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from starlette_admin.contrib.sqlmodel import Admin, ModelView

from .auth import views as auth_views
from .core import views as main_views
from .admin import admin as admin_app
from .models import User, Essay, Topic
from .database import engine
from .admin.admin import AdminAuthProvider


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5173/api/login/",
    "http://localhost:5173/api/register/",
    "http://localhost:5173/api/main/user/me",
    "http://localhost:5173/api/main/user/storage",
    "http://localhost:5173/api/main/response",
    "http://localhost:5173/api/main/user/delete",
    "http://localhost:5173/api/main/user/info"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_views.router)
app.include_router(main_views.router)


####    For admin page  ####
# Create an empty admin interface
admin = Admin(engine, title="Tutorials: Basic", auth_provider=AdminAuthProvider())
app.add_middleware(SessionMiddleware, secret_key='jlkasdbjfgb234352')


# Add view
admin.add_view(ModelView(User, icon="fas fa-list"))
admin.add_view(ModelView(Topic, icon="fas fa-list"))
admin.add_view(ModelView(Essay, icon="fas fa-list"))


# Mount admin to your app
admin.mount_to(app)