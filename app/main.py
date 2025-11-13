from fastapi import FastAPI
from app.db.database import init_db
from app.api.v1.api_router_specialties import router as specialties_router
from app.api.v1.api_router_groups import router as groups_router
from app.api.v1.api_router_disciplines import router as disciplines_router
from app.api.v1.api_router_teachers import router as teachers_router
from app.api.v1.api_router_workload import router as workload_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    print("Запуск приложения...")  
    init_db()

app.include_router(specialties_router)
app.include_router(groups_router)
app.include_router(disciplines_router)
app.include_router(teachers_router)
app.include_router(workload_router)
