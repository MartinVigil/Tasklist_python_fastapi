from fastapi import APIRouter, HTTPException, Request
from passlib.context import CryptContext
from jose import jwt
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta
from fastapi.responses import RedirectResponse
from db.models.models import User
from db.client import SessionLocal

# Configuración de la aplicación
router = APIRouter()

templates = Jinja2Templates(directory="templates")

templates.env.globals["url_for"] = router.url_path_for

# Configuración de encriptación y validación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de JWT (JSON Web Tokens)
SECRET_KEY = "019e0d9e8b8cd0c23f4698cbc7794d26586115b5fc6bb3a32d571473ddfffc006be20d7e"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Duración de los tokens de acceso en minutos

# Función para verificar y encriptar contraseñas
def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)

# Función para generar el hash de una contraseña
def get_password_hash(password):
    return pwd_context.hash(password)

# Función para autenticar y obtener información del usuario
def authenticate_user(username: str, password: str):
    db = SessionLocal()
    if db.query(User).filter(User.user == username).first():
        user = db.query(User).filter(User.user == username).first()
        if not verify_password(password, user.hashed_password):
            return None
        return user

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: int):
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=expires_delta)
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para obtener el token de acceso actual
def get_user_id_from_token(token: str, key : str):
    try:
        # Decodificar y validar el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        # Extraer el ID de usuario del payload
        user_id = payload.get("id")
        user_username = payload.get("sub")

        # Devolver el ID de usuario
        if key == 'id':
            return user_id
        if key == 'user':
            return user_username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

# Ruta para el registro de usuarios

@router.get('/register')
async def render_register(request : Request):
    return templates.TemplateResponse("register.html",{'request' : request})

@router.post('/register')
async def register(request : Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    db_user = User(user=username, hashed_password=get_password_hash(password), disabled=False)
    db = SessionLocal()
    if not db.query(User).filter(User.user == username).first():
        db.add(db_user)
        db.commit()
        db.close()
        response = RedirectResponse(url='/',status_code=302)
        return response
    db.close()
    raise HTTPException(status_code=400, detail="Username already registered")
    

# Ruta para el login y generación del token JWT

@router.get('/')
async def render_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post('/')
async def login(request : Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user,'id':user.id}, expires_delta=access_token_expires.total_seconds()
    )
    response = RedirectResponse(url='/tasks',status_code=302)
    response.set_cookie(key="access_token", value=access_token)
    return response


    


        


       



