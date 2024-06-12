from hashlib import sha256
from typing import Annotated

import fastapi
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import cursor

app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

cursor.execute(
    "CREATE TABLE IF NOT EXISTS users\
        (username TEXT, hashedpassword TEXT, token TEXT)")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS feedback\
        (id int primary key, review_content TEXT, positive decimal(1,5), negative\
            decimal(1,5), neutral decimal(1,5), polarity decimal(1,5))")
cursor.execute(
    "CREATE TABLE IF NOT EXISTS postinformation\
        (id int, creation text, link text, source\
            text, FOREIGN KEY (id) REFERENCES feedback(id))")
cursor.connection.commit()


@app.get("/", response_class=HTMLResponse)
async def index(request: fastapi.Request):
    # check request cookies
    if request.cookies.get("token", None):
        res = cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            return templates.TemplateResponse("approval.html", {"request": request})
        else:
            # delete cookie
            response = RedirectResponse("/login")
            response.delete_cookie("token")
            return response
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def index_post(request: fastapi.Request):
    # check request cookies
    if request.cookies.get("token", None):
        res = cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            return templates.TemplateResponse("approval.html", {"request": request})
        else:
            # delete cookie
            response = RedirectResponse("/login")
            response.delete_cookie("token")
            return response
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=JSONResponse)
async def login(request: fastapi.Request, username: Annotated[str, fastapi.Form()], password: Annotated[str, fastapi.Form()]):
    res = cursor.execute("SELECT * FROM users WHERE username = ? AND hashedpassword = ?",
                         (username, sha256(password.encode()).hexdigest())).fetchone()
    if res:
        print(res)
        response = RedirectResponse("/")
        response.set_cookie("token", res[2])
        return response
    return JSONResponse({"message": "Login Failed"})


@app.get("/login", response_class=HTMLResponse)
async def login_get(request: fastapi.Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/logout", response_class=RedirectResponse)
async def logout(request: fastapi.Request):
    response = RedirectResponse("/")
    response.delete_cookie("token")
    return response


@app.get("/get-reviews", response_class=JSONResponse)
async def get_reviews(request: fastapi.Request):
    if request.cookies.get("token", None):
        res = cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            res = cursor.execute(
                "SELECT * FROM\
                    feedback WHERE positive = 0 AND negative = 0 AND neutral = 0"
                ).fetchmany(10)
            return JSONResponse({"data": res})
    else:
        return JSONResponse({"message": "Unauthorized"})

@app.get("/undo-review", response_class=JSONResponse)
async def undo_review(request: fastapi.Request, db_id: str, polarity: int):
    if request.cookies.get("token", None):
        res = cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            res = cursor.execute(
                "SELECT * FROM feedback WHERE id = ?", (db_id,)).fetchone()
            if res:
                factor = 0
                if polarity == 1:
                    cursor.execute(
                        "UPDATE feedback SET positive = ? WHERE id = ?", (res[2]-1, db_id))
                    factor = -1
                elif polarity == -1:
                    cursor.execute(
                        "UPDATE feedback SET negative = ? WHERE id = ?", (res[3]+1, db_id))
                    factor = 1
                elif polarity == 0:
                    cursor.execute(
                            "UPDATE feedback SET negative = ? WHERE id = ?", (res[4]-1, db_id))
                    factor = 0
                else:
                    return JSONResponse({"message": "Invalid polarity"})
                try:
                    polarity = (res[2] + res[3] + factor) / \
                        (res[2] - res[3] + res[4] - 1)
                except ZeroDivisionError:
                    polarity = 0
                cursor.execute(
                    "UPDATE feedback SET polarity = ? WHERE id = ?", (polarity, db_id))
                cursor.connection.commit()
                return JSONResponse({"message": "done"})
    return JSONResponse({"message": "Unauthorized"})
            

@app.get("/approve-review", response_class=JSONResponse)
async def approve_review(request: fastapi.Request, db_id: str, polarity: int):
    if request.cookies.get("token", None):
        res = cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            res = cursor.execute(
                "SELECT * FROM feedback WHERE id = ?", (db_id,)).fetchone()
            if res:
                factor = 0
                if polarity == 1:
                    cursor.execute(
                        "UPDATE feedback SET positive = ? WHERE id = ?", (res[2]+1, db_id))
                    factor = 1
                elif polarity == -1:
                    cursor.execute(
                        "UPDATE feedback SET negative = ? WHERE id = ?", (res[3]-1, db_id))
                    factor = -1
                elif polarity == 0:
                    cursor.execute(
                        "UPDATE feedback SET neutral = ? WHERE id = ?", (res[4]+1, db_id))
                    factor = 0
                else:
                    return JSONResponse({"message": "Invalid polarity"})
                # polarity = (positive - negative) / (positive + negative + neutral)
                polarity = (res[2] + res[3] + factor) / \
                    (res[2] - res[3] + res[4] + 1)
                cursor.execute(
                    "UPDATE feedback SET polarity = ? WHERE id = ?", (polarity, db_id))
                cursor.connection.commit()
                return JSONResponse({"message": "Approved"})
            else:
                return JSONResponse({"message": "Review not found"})
    return JSONResponse({"message": "Unauthorized"})