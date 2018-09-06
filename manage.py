from application import app,manager
from flask_script import Server
import www                  #不知道为什么，但是必须要导入www
from jobs.launcher import runJob

##web server
manager.add_command("runserver",Server(host='127.0.0.1',port=app.config['SERVER_PORT'],
                                       use_debugger=True,use_reloader=True))
#job entrance
manager.add_command('runjob', runJob() )

def main():
    manager.run()

if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())    #sys.exit() 如果里面的方法出现异常并被捕获，则程序继续执行
    except Exception as e:
        import traceback
        traceback.print_exc()