import uvicorn
from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer
from auth.utils import decode_jwt
from database import validate_user, create_user

app = FastAPI()


templates = Jinja2Templates(directory="resourses")
httpbearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/login")
async def load_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request):
    form = await request.form()
    if validate_user(form):
        return validate_user(form)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register")
async def load_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_user(request: Request):
    form = await request.form()
    if create_user(form):
        return templates.TemplateResponse("register.html", {"request": request, "message": "Успех!"})
    return templates.TemplateResponse("register.html", {"request": request, "message": "Такой пользователь уже существует"})


@app.get("/me")
async def me(token: str = Depends(get_current_user)):
    pass

uvicorn.run(app)
