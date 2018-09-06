from flask import request,redirect,g,jsonify

from application import app
from common.models.member.Member import Member
from common.libs.member.MemberService import MemberService

import re

'''
认证微信请求头中的Authorization字段
'''

@app.before_request
def before_request():
    api_ignore_urls = app.config['API_IGNORE_URLS']
    path=request.path

    if "/api" not in path:
        return

    member_info=check_member_login()

    g.member_info=None
    if member_info:
        g.member_info=member_info

    pattern = re.compile('%s' % "|".join(api_ignore_urls))
    if pattern.match(path):
        return

    if not member_info:
        resp={'code':-1,'msg':'未登录~','data':{}}
        return jsonify(resp)
    return

'''验证，返回用户信息'''
def check_member_login():
    auth_cookie=request.headers.get("Authorization")        #获取请求头中的Authorization字段
    if auth_cookie is None:
        return False
    auth_info=auth_cookie.split("#")
    if len(auth_info)!=2:
        return False
    try:
        member_info=Member.query.filter_by(id=auth_info[1]).first()
    except Exception:
        return False

    if member_info is None:
        return False

    if auth_info[0]!=MemberService.geneAuthCode(member_info):
        return False

    if member_info.status!=1:     #账号设置为不可用时立刻退出
        return False

    return member_info