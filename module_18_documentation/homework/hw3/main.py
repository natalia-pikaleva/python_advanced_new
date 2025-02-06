import operator
from flask import Flask, jsonify
from flask_jsonrpc import JSONRPC
from flasgger import Swagger
from flask_jsonrpc.exceptions import JSONRPCError
import json

app = Flask(__name__)

swagger = Swagger(app, template_file='swagger.json')


class MyJSONRPCError(JSONRPCError):
    def __init__(self, code: int, message: str) -> None:
        super().__init__(code, message)

    def to_dict(self) -> dict:
        return {"error": {"code": self.code, "message": self.message}}


class DivisionByZeroError(MyJSONRPCError):
    def __init__(self) -> None:
        code = -32000  # Код ошибки для деления на ноль
        message = "Деление на ноль"
        super().__init__(code=code, message=message)


class InvalidParamsError(MyJSONRPCError):
    def __init__(self) -> None:
        code = -32602
        message = "Некорректный формат данных"
        super().__init__(code=code, message=message)


class MethodNotFoundError(MyJSONRPCError):
    def __init__(self) -> None:
        code = -32601
        message = "Метод не найден"
        super().__init__(code=code, message=message)


class ParseError(MyJSONRPCError):
    def __init__(self) -> None:
        code = -32700
        message = "Ошибка парсинга"
        super().__init__(code=code, message=message)


class MyOtherError(MyJSONRPCError):
    def __init__(self) -> None:
        code = -32600
        message = "Ошибка, невозможно выполнить запрос"
        super().__init__(code=code, message=message)


jsonrpc = JSONRPC(app, '/api', enable_web_browsable_api=True)


@app.after_request
def modify_json_rpc_response(response):
    if response.content_type == 'application/json':
        try:
            data = json.loads(response.get_data(as_text=True))
            if 'error' in data:
                if data['error']['name'] == 'DivisionByZeroError':
                    error = DivisionByZeroError()
                    data = error.to_dict()
                    response.set_data(json.dumps(data))
                elif data['error']['name'] == 'InvalidParamsError':
                    error = InvalidParamsError()
                    data = error.to_dict()
                    response.set_data(json.dumps(data))
                elif data['error']['name'] == 'MethodNotFoundError':
                    error = MethodNotFoundError()
                    data = error.to_dict()
                    response.set_data(json.dumps(data))
                elif data['error']['name'] == 'ParseError':
                    error = ParseError()
                    data = error.to_dict()
                    response.set_data(json.dumps(data))
                else:
                    error = MyOtherError()
                    data = error.to_dict()
                    response.set_data(json.dumps(data))
        except json.JSONDecodeError:
            pass  # Если JSON невалиден, ничего не делаем
    return response


@jsonrpc.method('calc.add')
def add(a: float, b: float) -> float:
    return operator.add(a, b)


@jsonrpc.method('calc.subtract')
def subtract(a: float, b: float) -> float:
    return operator.sub(a, b)


@jsonrpc.method('calc.multiply')
def multiply(a: float, b: float) -> float:
    return operator.mul(a, b)


@jsonrpc.method('calc.divide')
def divide(a: float, b: float) -> float:
    if b == 0:
        raise DivisionByZeroError()
    return operator.truediv(a, b)


#
# @app.errorhandler(Exception)
# def handle_exception(e):
#     if isinstance(e, DivisionByZeroError):
#         return jsonify({
#             "jsonrpc": "2.0",
#             "error": {
#                 "code": e.code,
#                 "message": e.message
#             },
#             "id": None
#         }), 400
#
#     return jsonify({
#         "jsonrpc": "2.0",
#         "error": {
#             "code": -32000,
#             "message": str(e)
#         },
#         "id": None
#     }), 500


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
