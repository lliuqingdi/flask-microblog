from flask import Flask#从flask包中导入Flask类

app = Flask(__name__)

print('等会谁（哪个包或模块）在使用我：',__name__)


#从app包中导入模块routes
from app import routes