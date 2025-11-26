import mysql.connector
from fastapi import FastAPI, HTTPException, Header, Depends
from starlette.requests import Request
from starlette.responses import PlainTextResponse

app = FastAPI()
students = ["Cosmin", "Edi", "Andrei", "Vlad", "Darius", "Rares"]

# Hint: aveti functia checker in middleware cautati pe net ce face ea si ordinea apelarilor
# La final vreau sa vad ok printeat pe ecran

def string_checker():
    # Nu schimbi nimic aici decat ce e in if
    my_string = ("In wow you need a lot of alts, alts are characters that you don't play as a main, they are played "
                 "less frequently.")
    # my_string.split(",")[0] => "In wow you need a lot of alts"
    # .split()[1] => "wow"
    # [::-1] => "wow" reversed is "wow"
    if my_string.split(",")[0].split()[1][::-1] == my_string.split(",")[0].split()[1][::]:
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
        host="mysql_server", #change to container name
        port=3306,
        user="admin",
        passwd="admin",
    )
    return db


@app.middleware("http")
async def checker(request: Request, call_next):
    try:
        string_checker()
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
        # split on "fast" breaks the string in two parts, index 1 is the second part
        # split on nothing breaks the string into words, -1 is the last word
        # split on - breaks shape-shifting into shape and shifting, [1] is shifting
        # index 3 of shifting is the letter f
        if my_string.split("fast")[1].split()[-1].split("-")[1][3] == "f":
            return "hello"
        raise ValueError


@app.get("/db", response_class=PlainTextResponse)
def data_base(db=Depends(db_connect)):
    # Aici toti sunteti picati adica aveti False vreau ca la finalul executiei acestui endpoint
    # Sa apara ok si apoi sa imi aratai in baza de date ca a-ti midifaicat si doar voi (numele tau)
    # A-ti trecut.

    cursor=db.cursor()
    cursor.execute("USE LAB")
#change varchar to 20 so names fit in
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS STUDENTI (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        pass_not_pass BOOLEAN DEFAULT FALSE
    )
    """)

#typo in the table name fixed
    for name in students:
        cursor.execute("INSERT INTO STUDENTI (name) VALUES (%s)", (name,))
#update column name only for 1 student
    cursor.execute("""
                    update STUDENTI 
                    set pass_not_pass = TRUE 
                    where name = %s
                   """, ("Rares",))

    db.commit()
    return "ok"
