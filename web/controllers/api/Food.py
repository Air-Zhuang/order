from flask import request,jsonify,g

from web.controllers.api import route_api
from application import app,db
from common.libs.Helper import getCurrentDate
from common.libs.UrlManager import UrlManager
from common.models.food.FoodCat import FoodCat
from common.models.food.Food import Food
from common.models.member.MemberCart import MemberCart
from sqlalchemy import or_

import requests,json

@route_api.route("/food/index")
def foodIndex():        #返回首页barner图和分类信息
    resp={'code':200,'msg':'操作成功~','data':{}}

    # 取出所有的可展分类
    cat_list=FoodCat.query.filter_by(status=1).order_by(FoodCat.weight.desc()).all()
    data_cat_list=[]
    data_cat_list.append({
        'id':0,
        'name':'全部'
    })
    if cat_list:
        for item in cat_list:
            tmp_data={                  #拼index.js中的categories
                "id":item.id,
                'name': item.name
            }
            data_cat_list.append(tmp_data)
    resp['data']['cat_list'] = data_cat_list

    # 取销售额最多的三条记录
    food_list=Food.query.filter_by(status=1).order_by(Food.total_count.desc(),Food.id.desc()).limit(3).all()
    data_food_list = []
    if food_list:
        for item in food_list:
            tmp_data={                  #拼index.js中的banners
                "id": item.id,
                "pic_url": UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)

    resp['data']['banner_list'] = data_food_list

    return jsonify(resp)

@route_api.route("/food/search")
def foodSearch():       #返回搜索信息
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req=request.values
    cat_id=int(req['cat_id']) if 'cat_id' in req else 0
    mix_kw=str(req['mix_kw']) if 'mix_kw' in req else ''
    p = int(req['p']) if 'p' in req else 1          #获取分页值
    if p<1:
        p=1
    query = Food.query.filter_by(status=1)

    page_size=4
    offset=(p-1)*page_size
    if cat_id> 0:
        query = query.filter(Food.cat_id == cat_id)
    if mix_kw:
        rule = or_(Food.name.ilike("%{0}%".format(mix_kw)), Food.tags.ilike("%{0}%".format(mix_kw)))
        query = query.filter(rule)

    food_list=query.order_by(Food.total_count.desc(),Food.id.desc()).offset(offset).limit(page_size).all()
    data_food_list=[]
    if food_list:
        for item in food_list:
            tmp_data={
                'id':item.id,
                'name':item.name,
                'price':str(item.price),
                'min_price':str(item.price),
                'pic_url':UrlManager.buildImageUrl(item.main_image)
            }
            data_food_list.append(tmp_data)
    resp['data']['list']=data_food_list
    resp['data']['has_more']=0 if len(data_food_list)<page_size else 1          #判断查询数据库是否还有数据，给前端判断是否还可以上拉刷新
    return jsonify(resp)

@route_api.route("/food/info")
def foodInfo():      #小程序详情页
    resp = {'code': 200, 'msg': '操作成功~', 'data': {}}
    req = request.values
    id=int(req['id']) if 'id' in req else 0
    food_info=Food.query.filter_by(id=id).first()
    if not food_info or not food_info.status:
        resp['code']=-1
        resp['msg']="已下架~~"
        return jsonify(resp)

    member_info=g.member_info       #为了显示购物车右上角的角标
    cart_number=0
    if member_info:
        cart_number=MemberCart.query.filter_by(member_id=member_info.id).count()


    resp['data']['info']={
        "id":food_info.id,
        "name":food_info.name,
        "summary":food_info.summary,
        "total_count":food_info.total_count,
        "comment_count":food_info.comment_count,
        "main_image":UrlManager.buildImageUrl(food_info.main_image),
        "price":str(food_info.price),
        "stock":food_info.stock,
        "pics":[UrlManager.buildImageUrl(food_info.main_image)]
    }
    resp['data']['cart_number']=cart_number

    return jsonify(resp)