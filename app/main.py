from contextlib import asynccontextmanager
import email
from operator import concat
from os import name
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.db.database import close_db, init_db
from app.api.v1.api_router_specialties import router as specialties_router
from app.api.v1.api_router_groups import router as groups_router
from app.api.v1.api_router_disciplines import router as disciplines_router
from app.api.v1.api_router_teachers import router as teachers_router
from app.api.v1.api_router_workload import router as workload_router
from app.api.v1.api_router_curriculums import router as curriculums_router
from app.api.v1.api_router_lesson_types import router as lesson_types_router
from app.api.v1.users_router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(
    title="Создание и тестирование АРМ учета нагрузки преподавателей колледжа ",  
    description="Сроки выполнения: 1. Разработка REST-сервиса с использованием фреймворка FastAPI : до 15.12.25г 2. Разработка web-приложения на Django: до 1.05.26г",
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Пашухин Андрей Викторович ИП-31",
        "email": "pashuhin@mail.ru"
        },
)

# Подключаем маршруты 
app.include_router(users_router, prefix="/api/v1")
app.include_router(specialties_router, prefix="/api/v1")
app.include_router(groups_router, prefix="/api/v1")
app.include_router(disciplines_router, prefix="/api/v1")
app.include_router(teachers_router, prefix="/api/v1")
app.include_router(workload_router, prefix="/api/v1")
app.include_router(curriculums_router, prefix="/api/v1")
app.include_router(lesson_types_router, prefix="/api/v1")

# Включаем пагинацию для всех маршрутов
add_pagination(app)
