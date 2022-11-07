import logging

import azure.functions as func
from FlaskApp import app
from Utils import export_comments

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """Each request is redirected to the WSGI handler.
    """
    response = func.WsgiMiddleware(app.wsgi_app).handle(req, context)
    export_comments(req.get_json().get("url"))
    return response

