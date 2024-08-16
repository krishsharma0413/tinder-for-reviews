from hashlib import sha256
from typing import Annotated
from zipfile import ZipFile, ZIP_DEFLATED
from json import dump
import os
from shutil import rmtree

import fastapi
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import cursor, user_cursor
from user_config import *

app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.route("/", methods=["get", "post"])
async def index_post(request: fastapi.Request):
    # check request cookies
    if request.cookies.get("token"):
        res = user_cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            return templates.TemplateResponse(
                "approval.html",
                {
                    "request": request,
                    "left": left_swipe[1],
                    "right": right_swipe[1],
                    "up": up_swipe[1]
                }
            )
        else:
            # delete cookie
            response = RedirectResponse("/login")
            response.delete_cookie("token")
            return response
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=JSONResponse)
async def login(request: fastapi.Request, username: Annotated[str, fastapi.Form()], password: Annotated[str, fastapi.Form()]):
    res = user_cursor.execute("SELECT * FROM users WHERE username = ? AND hashedpassword = ?",
                         (username, sha256(password.encode()).hexdigest())).fetchone()
    if res:
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


@app.get("/json-export", response_class=FileResponse)
async def json_exp(request: fastapi.Request):
    if request.cookies.get("token"):
        res = user_cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            alldata = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
            with open(f"./exports/{res[2]}.zip", "w", encoding="utf-8") as _:
                zipf = ZipFile(f"./exports/{res[2]}.zip", "w", ZIP_DEFLATED)
                try:
                    os.mkdir(f"./{res[2]}/")
                except FileExistsError as _:
                    print("directory already created: cleaning directory")
                    rmtree(f"./{res[2]}/")
                    os.mkdir(f"./{res[2]}/")
                if len(alldata) > 15_000:
                    for x in range(0, len(alldata), 15_000):
                        with open(f"./{res[2]}/{x}-{x+15_000}.json", "w", encoding="utf-8") as filemanager:
                            dump({"data": [dict(zip(headers, y)) for y in alldata[x:x+15_000]]}, filemanager, indent=4)
                            filemanager.flush()
                        zipf.write(f"./{res[2]}/{x}-{x+15_000}.json")
                else:
                    with open(f"./{res[2]}/{0}-{len(alldata)}.json", "w", encoding="utf-8") as filemanager:
                        dump({"data": [dict(zip(headers, y)) for y in alldata]}, filemanager, indent=4)
                        zipf.write(f"./{res[2]}/{0}-{len(alldata)}.json")
                zipf.close()
                return FileResponse(f"./exports/{res[2]}.zip", filename=f"{res[2]}.zip")
    else:
        return JSONResponse({"message": "Unauthorized"})

@app.get("/get-reviews", response_class=JSONResponse)
async def get_reviews(request: fastapi.Request):
    if request.cookies.get("token"):
        res = user_cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            res = cursor.execute(
                f"SELECT {primary_key}, {column_for_review} FROM\
                    {table_name} WHERE {left_swipe[0]} = 0 AND {right_swipe[0]} = 0 AND {up_swipe[0]} = 0"
                ).fetchmany(10)
            return JSONResponse({"data": res})
    else:
        return JSONResponse({"message": "Unauthorized"})

@app.get("/undo-review", response_class=JSONResponse)
async def undo_review(request: fastapi.Request, db_id: str, polarity: int):
    if request.cookies.get("token"):
        res = user_cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            res = cursor.execute(
                f"SELECT {right_swipe[0]}, {left_swipe[0]}, {up_swipe[0]} FROM {table_name} WHERE id = ?", (db_id,)).fetchone()
            if res:
                factor = 0
                if polarity == 1:
                    cursor.execute(
                        f"UPDATE {table_name} SET {right_swipe[0]} = ? WHERE id = ?", (res[0]-1, db_id))
                    factor = -1
                elif polarity == -1:
                    cursor.execute(
                        f"UPDATE {table_name} SET {left_swipe[0]} = ? WHERE id = ?", (res[1]+1, db_id))
                    factor = 1
                elif polarity == 0:
                    cursor.execute(
                        f"UPDATE {table_name} SET {up_swipe[0]} = ? WHERE id = ?", (res[2]-1, db_id))
                    factor = 0
                else:
                    return JSONResponse({"message": "Invalid polarity"})
                try:
                    polarity = (res[0] + res[1] + factor) / \
                        (res[0] - res[1] + res[2] - 1)
                except ZeroDivisionError:
                    polarity = 0
                cursor.execute(
                    f"UPDATE {table_name} SET {polarity_column} = ? WHERE id = ?", (polarity, db_id))
                cursor.connection.commit()
                return JSONResponse({"message": "done"})
    return JSONResponse({"message": "Unauthorized"})
            

@app.get("/approve-review", response_class=JSONResponse)
async def approve_review(request: fastapi.Request, db_id: str, polarity: int):
    if request.cookies.get("token"):
        res = user_cursor.execute("SELECT * FROM users WHERE token = ?",
                             (request.cookies.get("token"),)).fetchone()
        if res:
            res = cursor.execute(
                f"SELECT {right_swipe[0]}, {left_swipe[0]}, {up_swipe[0]} FROM {table_name} WHERE id = ?", (db_id,)).fetchone()
            if res:
                factor = 0
                if polarity == 1:
                    cursor.execute(
                        f"UPDATE {table_name} SET {right_swipe[0]} = ? WHERE id = ?", (res[0]+1, db_id))
                    factor = 1
                elif polarity == -1:
                    cursor.execute(
                        f"UPDATE {table_name} SET {left_swipe[0]} = ? WHERE id = ?", (res[1]-1, db_id))
                    factor = -1
                elif polarity == 0:
                    cursor.execute(
                        f"UPDATE {table_name} SET {up_swipe[0]} = ? WHERE id = ?", (res[2]+1, db_id))
                    factor = 0
                else:
                    return JSONResponse({"message": "Invalid polarity"})
                # new polarity = (positive - negative + factor) / (positive + negative + neutral + 1)
                polarity = (res[0] + res[1] + factor) / \
                    (res[0] - res[1] + res[2] + 1)
                cursor.execute(
                    f"UPDATE {table_name} SET {polarity_column} = ? WHERE id = ?", (polarity, db_id))
                cursor.connection.commit()
                return JSONResponse({"message": "Approved"})
            else:
                return JSONResponse({"message": "Review not found"})
    return JSONResponse({"message": "Unauthorized"})
