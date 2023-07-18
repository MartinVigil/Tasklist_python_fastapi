from fastapi import FastAPI
from routers import jwt_auth,tasks
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(jwt_auth.router)
app.include_router(tasks.router)




