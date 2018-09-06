from flask import Flask,url_for

from flask_sqlalchemy import SQLAlchemy

from common.libs.UrlManager import UrlManager

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:123456@127.0.0.1/article_spider'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

@app.route('/')
def hello_world():
    url=url_for("index")
    url_1=UrlManager.buildUrl("/api")
    url_2 = UrlManager.buildStaticUrl("/css/bootstrap.css")
    msg="Hello World,url:%s,url_1:%s,url_2:%s" % (url,url_1,url_2)
    app.logger.error(msg)
    app.logger.info(msg)
    return msg
@app.route("/api")
def index():
    return "Index page"
@app.route("/api/hello")
def hello():
    from sqlalchemy import text
    sql=text("SELECT title FROM zhihu_question")
    result=db.engine.execute(sql)
    for row in result:
        app.logger.info(row)
    return "Hello World"
@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return 'This page does not exist',404

if __name__ == '__main__':
    app.run(debug=True)