import mysql.connector
from fastapi import FastAPI, HTTPException, Header, Depends
from starlette.requests import Request
from starlette.responses import PlainTextResponse

app = FastAPI()
students = ["Cosmin", "Edi", "Andrei", "Vlad", "Darius"]

# Hint: aveti functia checker in middleware cautati pe net ce face ea si ordinea apelarilor
# La final vreau sa vad ok printeat pe ecran

def string_checker():
    # Nu schimbi nimic aici decat ce e in if
    my_string = ("In wow you need a lot of alts, alts are characters that you don't play as a main, they are played "
                 "less frequently.")
    if my_string.split(",")[0].split()[1][::-1] != my_string.split(",")[0].split()[1][::]:
        return "ok"
    raise ValueError


def string_checker2():
    try:
        my_string = "In wow farming pets or items that drop in the open world is much harder then the pets or items from raids"
        my_string.split()[3][2] = my_string.split()[5][1]
    except BaseException:
        raise ValueError
    except:
        return "ok"


def db_connect():
    db = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="admins",
        passwd="admin",
    )
    return db


@app.middleware("http")
async def checker(request: Request, call_next):
    try:
        # string_checker2()
        response = await call_next(request)
        return response
    except ValueError as e:
        return PlainTextResponse(f"Custom error caught by middleware {str(e)}", status_code=400)
    except AttributeError as e:
        return PlainTextResponse(f"Custom error caught by middleware {str(e)}", status_code=400)


@app.get("/", summary="This is the home page",
         description="This is the home page of the server you need to fix the problems of this server",
         response_class=PlainTextResponse)
def home(result=Depends(string_checker)):
    # modifica =="u" trebuie pus sa fie correct
    if result == "ok":
        my_string = "Is best to have druid or mages in order to farm fast because of teleporting and shape-shifting"
        if my_string.split("fast")[1].split()[-1].split("-")[1][3] == "u":
            return "hello"
        raise ValueError


@app.get("/db", response_class=PlainTextResponse)
def data_base(db=Depends(db_connect)):
    # Aici toti sunteti picati adica aveti False vreau ca la finalul executiei acestui endpoint
    # Sa apara ok si apoi sa imi aratai in baza de date ca a-ti midifaicat si doar voi (numele tau)
    # A-ti trecut.

    cursor=db.cursor()
    cursor.execute("USE LAB")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS STUDENTI (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(2) NOT NULL,
        pass_not_pass BOOLEAN DEFAULT FALSE
    )
    """)

    for name in students:
        cursor.execute("INSERT INTO STUDENT (name) VALUES (%s)", (name,))

    db.commit()
    return "ok"
