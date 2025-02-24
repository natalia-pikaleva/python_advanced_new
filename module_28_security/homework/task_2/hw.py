from fastapi import FastAPI, Response

app = FastAPI()

@app.get("/")
def root(user_input: str = ""):
    HTML = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
      {user_input}
    </body>
    </html>
    """

    html = HTML.format(user_input=user_input)

    # Установка заголовка Content-Security-Policy для запрета инлайн-скриптов
    headers = {
        "Content-Security-Policy": "script-src 'self'; object-src 'self'; frame-src 'self';",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block"
    }

    return Response(content=html, media_type="text/html", headers=headers)
