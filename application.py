from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

import os

class Application(Flask):
    def __init__(self,import_name,template_folder=None,root_path=None):
        super(Application,self).__init__(import_name,template_folder=template_folder,root_path=root_path,static_folder=None)
        self.config.from_pyfile('config/base_setting.py')
        if "ops_config" in os.environ:  #dos中用 set ops_config=local更改环境配置，linux中用 export ops_config=local
            self.config.from_pyfile('config/%s_setting.py' % os.environ['ops_config'])

        db.init_app(self)

db=SQLAlchemy()
app=Application(__name__,template_folder=os.getcwd()+"/web/templates/",root_path=os.getcwd())     #getcwd获取当前目录


manager=Manager(app)

'''
函数模板
'''
from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildStaticUrl,'buildStaticUrl')     #将python中的方法注册到html中也可以使用
app.add_template_global(UrlManager.buildUrl,'buildUrl')
app.add_template_global(UrlManager.buildImageUrl,'buildImageUrl')
