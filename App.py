import json
from typing import Any
from http import HTTPStatus
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from var import Data_type as dt
from consulta import DB_query

try: from json import dumps as json_dumps
except ImportError:
    try: from simplejson import dumps as json_dumps
    except ImportError:
        try: from django.utils.simplejson import dumps as json_dumps
        except ImportError:
            def json_dumps(data):
                raise ImportError("JSON support requires Python 2.6 or simplejson.")
            json_lds = json_dumps

class WSGIServer(object):
    adapter : dt.Adapter
    quiet = False
    def __init__(self, adapter:dt.Adapter, **options) -> None:
        self.options = options
        self.host = adapter['host']
        self.port = adapter['port']
        
    def run(self, app : any, count : int = 1) -> None:
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server
        import socket

        class FixedHandler(WSGIRequestHandler):
            def address_string(self): # Evite las búsquedas de DNS inversas, por favor.
                return self.client_address[0]
            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls  = self.options.get('server_class', WSGIServer)

        if ':' in self.host: # Arregle wsgiref para direcciones IPv6.
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        if count is None:
            srv.serve_forever()
        else:
            for _ in range(count):
                srv.handle_request()

def application(environ : Any, start_response : Any) -> json:
    status = "{status.value} {status.phrase}".format(status=HTTPStatus.OK)
    headers = [ ('Content-type', 'application/json;charset=utf-8') ]
    params = parse_qs(environ['QUERY_STRING'])
    start_response(status, headers)
    
    db = DB_query() #se inicia la base donde se haran las consultas
    db.run_con("localhost", "root", "unicornio003", "habi")
    response = db.query( dt.Query(params) )

    if response is None:
        response = {"resultado" : "No se encontraron resultados"}
    
    return [ json_dumps(response, indent=2).encode('utf-8') ]

if __name__ == "__main__":
    WSGIServer(dt.Adapter(host = 'localhost', port = 8000)).run(application, None)
