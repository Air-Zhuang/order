from flask import request,jsonify,g

from web.controllers.api import route_api
from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.libs.Helper import selectFilterObj,getDictFilterField
from common.libs.UrlManager import UrlManager

import json

@route_api.route("/my/order",methods=["POST"])
def myOrderList():            #订单首页
    resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}
    member_info=g.member_info
    req=request.values

    status=int(req['status']) if 'status' in req else 0
    query=PayOrder.query.filter_by(member_id=member_info.id)               #先根据member_id过滤当前用户的订单

    if status==-8:          #等待付款的状态
        query.filter(PayOrder.status==-8)
    elif status==-7:        #待发货
        query.filter(PayOrder.status == 1,PayOrder.express_status==-7,PayOrder.comment_status==0)
    elif status==-6:        #待确认
        query.filter(PayOrder.status == 1, PayOrder.express_status == -6, PayOrder.comment_status == 0)
    elif status==-5:        #待评价
        query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 0)
    elif status==1:         #已完成
        query.filter(PayOrder.status == 1, PayOrder.express_status == 1, PayOrder.comment_status == 1)
    else:                   #已关闭状态
        query.filter(PayOrder.status == 0)

    pay_order_list=query.order_by(PayOrder.id.desc()).all()
    data_pay_order_list=[]
    if pay_order_list:
        pay_order_ids=selectFilterObj(pay_order_list,"id")                          #取id字段，保存在[]中
        pay_order_item_list=PayOrderItem.query.filter(PayOrderItem.pay_order_id.in_(pay_order_ids)).all()
        food_ids=selectFilterObj(pay_order_item_list,"food_id")                     #取PayOrderItem中food_id字段放在[]中
        food_map=getDictFilterField(Food,Food.id,"id",food_ids)

        pay_order_item_map={}
        if pay_order_item_list:
            for item in pay_order_item_list:
                if item.pay_order_id not in pay_order_item_map:
                    pay_order_item_map[item.pay_order_id]=[]

                tmp_food_info=food_map[item.food_id]
                pay_order_item_map[item.pay_order_id].append({
                    "id":item.id,
                    'food_id':item.food_id,
                    "quantity":item.quantity,
                    "pic_url":UrlManager.buildImageUrl(tmp_food_info.main_image),
                    "name":tmp_food_info.name
                })
        for item in pay_order_list:
            tmp_data={
                "status":item.pay_status,
                "status_desc":item.status_desc,
                "data":item.created_time.strftime("%Y-%m-%d %H:%M:%S"),
                "order_number":item.order_number,
                "order_sn":item.order_sn,
                "note":item.note,
                "total_price":str(item.total_price),
                "goods_list":pay_order_item_map[item.id]
            }
            data_pay_order_list.append(tmp_data)

    resp['data']['pay_order_list']=data_pay_order_list
    return jsonify(resp)