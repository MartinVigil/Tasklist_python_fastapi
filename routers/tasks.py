from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from db.models.models import Task
from db.client import SessionLocal
from routers.jwt_auth import get_user_id_from_token

router = APIRouter()

templates = Jinja2Templates(directory="templates")

templates.env.globals["url_for"] = router.url_path_for

@router.post('/tasks')
async def add_task(request : Request):
    token = request.cookies.get("access_token")
    id = get_user_id_from_token(token,'id')
    form_data = await request.form()
    task = form_data.get("task")
    db = SessionLocal()
    db_task = Task(task=task,fk_user=id)
    db.add(db_task)
    db.commit()
    db.close()   
    response = RedirectResponse(url='/tasks',status_code=302)
    return response

@router.get("/tasks")
async def get_task_list(request: Request):
    token = request.cookies.get("access_token")
    user = get_user_id_from_token(token,'user')
    id = get_user_id_from_token(token,'id')
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.fk_user == id).all()
    task_list = [{"id": task.id, "task": task.task} for task in tasks]
    return templates.TemplateResponse("index.html", {"request": request, "tasks": task_list, "user":user})

@router.post('/tasks/{task_id}/delete')
async def delete_task(task_id: int):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        response = RedirectResponse(url='/tasks',status_code=302)
        return response
    
@router.post('/tasks/{task_id}/update')
async def update_task(task_id : int, request:Request):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        form_data = await request.form()
        new_task = form_data.get('new_task')
        task.task = new_task
        db.commit()
        response = RedirectResponse(url='/tasks',status_code=302)
        return response
    else:
        return {"message": "Tarea no encontrada"}    
    