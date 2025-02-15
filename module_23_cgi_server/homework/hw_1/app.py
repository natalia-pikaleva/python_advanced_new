import json

class SimpleWSGIApp:
    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')

        if path == '/hello':
            response_body = json.dumps({"response": "Hello, world!"}, indent=4)
            status = '200 OK'
            headers = [('Content-Type', 'application/json')]
        elif path.startswith('/hello/'):
            name = path.split('/')[-1]
            response_body = json.dumps({"response": f"Hello, {name}!"}, indent=4)
            status = '200 OK'
            headers = [('Content-Type', 'application/json')]
        else:
            response_body = json.dumps({"error": "404 Not Found"}, indent=4)
            status = '404 Not Found'
            headers = [('Content-Type', 'application/json')]


        start_response(status, headers)
        return [response_body.encode('utf-8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server

    app = SimpleWSGIApp()
    server = make_server('localhost', 8080, app)
    print("Запуск сервера на http://localhost:8080")
    server.serve_forever()
