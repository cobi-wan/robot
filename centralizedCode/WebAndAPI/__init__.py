# from flask import Flask, render_template, request, Response, Blueprint
# # from multiprocessing import Process
# from flask import _app_ctx_stack

# def getEnviron():
#     appContext = _app_ctx_stack.top
#     env = getattr(appContext, "Environ", None)
#     if env is None:
#         env = 

# def create_app(environ):
#     app = Flask(__name__)
#     app.config['Environ'] = environ 

#     from .api import api
#     app.register_blueprint(api, url_prefix='/')

#     return app

