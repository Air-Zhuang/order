from flask import Blueprint,request,redirect,jsonify

from common.libs.Helper import ops_render,iPagination,getCurrentDate
from common.models.member.Member import Member
from common.libs.UrlManager import UrlManager
from application import app,db

route_member = Blueprint('member_page',__name__)

@route_member.route("/index")
def index():
    resp_data={}
    req=request.values
    page=int(req['p']) if ('p' in req and req['p']) else 1
    query=Member.query

    if 'mix_kw' in req:
        query=query.filter(Member.nickname.ilike("%{0}%".format(req['mix_kw'])))

    if 'status' in req and int(req['status'])>-1:                     #用于搜索框
        query=query.filter(Member.status==int(req['status']))

    page_params={
        'total':query.count(),
        'page_size':app.config['PAGE_SIZE'],
        'page':page,
        'display':app.config['PAGE_DISPLAY'],
        'url':request.full_path.replace("&p={}".format(page),"")
    }
    pages=iPagination(page_params)
    offset=(page-1)*app.config['PAGE_SIZE']         #offset偏移量

    list=query.order_by(Member.id.desc()).offset(offset).limit(app.config['PAGE_SIZE']).all()   #offset偏移量，limit每页显示的数量

    resp_data['list'] = list                                        #用于展示会员信息
    resp_data['pages'] = pages                                      #用于分页
    resp_data['search_con'] = req                                   #让 "请选择状态" 那里显示当前的搜索状态
    resp_data['status_mapping'] = app.config['STATUS_MAPPING']      #用于搜索框
    resp_data['current']='index'                                    #用于切换会员列表和会员评论
    return ops_render("member/index.html",resp_data)

@route_member.route("/info")
def info():
    resp_data={}
    req=request.args
    id=int(req.get('id',0))
    reback_url=UrlManager.buildUrl("/member/index")
    if id<1:
        return redirect(reback_url)
    info=Member.query.filter_by(id=id).first()
    if not info:
        return redirect(reback_url)

    resp_data['info']=info
    resp_data['current'] = 'index'
    return ops_render("member/info.html",resp_data)

@route_member.route("/set",methods=["GET","POST"])
def set():
    if request.method=="GET":
        resp_data={}
        req=request.args
        id=int(req.get("id",0))
        reback_url = UrlManager.buildUrl("/member/index")
        if id < 1:
            return redirect(reback_url)

        info = Member.query.filter_by(id=id).first()
        if not info:
            return redirect(reback_url)

        if info.status!=1:                  #防止手动输入url地址进入编辑页面
            return redirect(reback_url)

        resp_data['info'] = info
        resp_data['current'] = 'index'
        return ops_render("member/set.html",resp_data)
    resp={'code':200,'msg':'操作成功~~','data':{}}
    req=request.values
    id=req['id'] if 'id' in req else 0
    nickname=req['nickname'] if 'nickname' in req else ''
    if nickname is None or len(nickname)<1:
        resp['code']=-1
        resp['msg']="请输入符合规范的姓名~~"
        return jsonify(resp)

    member_info=Member.query.filter_by(id=id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定会员不存在~~"
        return jsonify(resp)

    member_info.nickname=nickname
    member_info.update_time=getCurrentDate()
    db.session.add(member_info)
    db.session.commit()
    return jsonify(resp)



@route_member.route("/comment")
def comment():
    return ops_render("member/comment.html",{'current':'index'})

@route_member.route("/ops",methods=["POST"])
def ops():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    id=req['id'] if 'id' in req else 0
    act=req['act'] if 'act' in req else ''

    if not id:
        resp['code'] = -1
        resp['msg'] = "请选择要操作的账号~~"
        return jsonify(resp)

    if act not in ['remove','recover']:
        resp['code'] = -1
        resp['msg'] = "操作有误，请重试~~"
        return jsonify(resp)

    member_info=Member.query.filter_by(id=id).first()
    if not member_info:
        resp['code'] = -1
        resp['msg'] = "指定的会员不存在~~"
        return jsonify(resp)

    if act=="remove":
        member_info.status = 0
    elif act=="recover":
        member_info.status = 1

    member_info.update_time=getCurrentDate()
    db.session.add(member_info)
    db.session.commit()

    return jsonify(resp)

@route_member.route("/member/share",methods=["POST"])
def memberShare():
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    req = request.values
    return jsonify(resp)