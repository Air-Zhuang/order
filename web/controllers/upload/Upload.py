from flask import Blueprint, request, jsonify

from application import app
from common.libs.UploadService import UploadService
from common.libs.UrlManager import UrlManager
from common.models.Image import Image

import json, re

route_upload = Blueprint('upload_page', __name__)


@route_upload.route("/ueditor", methods=["GET", "POST"])
def ueditor():
    req = request.values
    action = req['action'] if 'action' in req else ''

    if action == "config":              #初始化
        root_path = app.root_path

        config_path = "{0}/web/static/plugins/ueditor/upload_config.json".format(root_path)
        with open(config_path, encoding="utf-8") as fp:  # window平台需要写utf-8!!!!
            try:
                config_data = json.loads(re.sub(r'\/\*.*\*/', '', fp.read()))
            except Exception as e:
                config_data = {}
        return jsonify(config_data)

    if action == "uploadimage":                                             #上传图片
        return uploadImage()

    if action == "listimage":                                             #上传图片里面的在线管理
        return listImage()

    return "upload"

@route_upload.route("/pic", methods=["GET", "POST"])
def uploadPic():       #上传封面图
    file_target = request.files
    upfile = file_target['pic'] if 'pic' in file_target else None           #input标签的name属性
    callback_target='window.parent.upload'                                  #让iframe页面可以调用父页面的js方法
    if upfile is None:
        return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target,"上传失败")

    ret = UploadService.uploadByFile(upfile)

    if ret['code'] != 200:
        return "<script type='text/javascript'>{0}.error('{1}')</script>".format(callback_target, "上传失败"+ret['msg'])

    return "<script type='text/javascript'>{0}.success('{1}')</script>".format(callback_target,ret['data']['file_key'])



def uploadImage():
    resp = {'state': 'SUCCESS', 'url': '', 'title': '', 'original': ''}     #官方返回格式
    file_target = request.files                                             #flask获取文件方式
    upfile = file_target['upfile'] if 'upfile' in file_target else None
    if upfile is None:
        resp['state'] = "上传失败"
        return jsonify(resp)

    ret = UploadService.uploadByFile(upfile)

    if ret['code'] != 200:
        resp['state'] = "上传失败：" + ret['msg']
        return jsonify(resp)

    resp['url']=ret['data']['file_key']
    resp['url'] = UrlManager.buildImageUrl(ret['data']['file_key'])
    return jsonify(resp)

def listImage():
    resp = {'state': 'SUCCESS', 'list': [], 'start': 0, 'total': 0}          #官方返回格式
    req=request.values

    start=int(req['start']) if 'start' in req else 0
    page_size=int(req['size']) if 'size' in req else 20

    query=Image.query

    #以下三行为图片管理分页逻辑
    if start>0:
        query=query.filter(Image.id<start)
    list=query.order_by(Image.id.desc()).limit(page_size).all()

    images=[]
    if list:
        for item in list:
            images.append({'url':UrlManager.buildImageUrl(item.file_key)})      #'list': []返回的是字典列表
            start=item.id                                                       #处理图片管理分页问题
    resp['list'] = images
    resp['start']=start
    resp['total']=len(images)
    return jsonify(resp)