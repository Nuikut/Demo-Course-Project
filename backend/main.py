import uvicorn
from fastapi import FastAPI, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.security import HTTPBearer
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from auth.utils import decode_jwt
from database import create_user, validate_user, validate_manager

app = FastAPI()


origins = {
    "http://localhost",
    "http://localhost:3000",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


templates = Jinja2Templates(directory="resourses")
httpbearer = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)


@app.get("/login")
async def load_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "action": "/login"})


@app.post("/login")
async def login(request: Request):
    form = await request.form()
    if token := validate_user(form.get("username"), form.get("password")):
        return token
    return templates.TemplateResponse("login.html", {"request": request, "action": "/login"})


@app.get("/register")
async def load_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_user(request: Request):
    form = await request.form()
    if create_user(form.get("username"), form.get("password")):
        return templates.TemplateResponse("register.html", {"request": request, "message": "Успех!"})
    return templates.TemplateResponse("register.html", {"request": request, "message": "Такой пользователь уже существует"})


@app.get("/manager")
async def load_manager_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "action": "/manager"})


@app.post("/manager")
async def login_manager(request: Request):
    form = await request.form()
    if token := validate_manager(form.get("username"), form.get("password")):
        return token
    return templates.TemplateResponse("login.html", {"request": request, "action": "/manager"})


@app.get("/me")
async def me(token: str = Depends(get_current_user)):
    pass


uvicorn.run(app)
