from application import db

from common.models.food.Food import Food
from common.models.pay.PayOrder import PayOrder
from common.models.pay.PayOrderItem import PayOrderItem
from common.models.pay.PayOrderCallbackData import PayOrderCallbackData
from common.libs.Helper import getCurrentDate
from common.libs.food.FoodService import FoodService
from common.models.food.FoodSaleChangeLog import FoodSaleChangeLog
from common.libs.queue import QueueService

import decimal,hashlib,time,random

class PayService():
    def __init__(self):
        pass

    def createOrder(self,member_id,items=None,params=None):
        resp = {'code': 200, 'msg': '操作成功~~', 'data': {}}

        pay_price=decimal.Decimal(0.00)
        coutinue_cnt=0
        foods_id=[]                                 #商品id列表
        for item in items:
            if decimal.Decimal(item['price'])<0:
                coutinue_cnt+=1
                continue
            pay_price=pay_price+decimal.Decimal(item['price'])*int(item['number'])
            foods_id.append(item['id'])

        if coutinue_cnt>=len(items):
            resp['code']=-1
            resp['msg']="商品items为空"
            return resp

        yun_price=params['yun_price'] if params and 'yun_price' in params else 0
        note=params['note'] if params and 'note' in params else ''

        yun_price=decimal.Decimal(yun_price)        #运费
        total_price=pay_price+yun_price             #总价

        try:                                        #并发处理：悲观锁        取Food表信息，更新PayOrder和PayOrderItem信息，更新Food表库存，之后统一提交
            tmp_food_list=db.session.query(Food).filter(Food.id.in_(foods_id))\
                                        .with_for_update().all()            #with_for_update()悲观锁 这条进行了行级别的锁

            tmp_food_stock_mapping={}                                       #商品id和商品库存组成的dict
            for tmp_item in tmp_food_list:
                tmp_food_stock_mapping[tmp_item.id]=tmp_item.stock

            model_pay_order=PayOrder()                                      #主表，存放订单信息
            model_pay_order.order_sn=self.geneOrderSn()                     #随机订单号
            model_pay_order.member_id=member_id
            model_pay_order.total_price=total_price
            model_pay_order.yun_price=yun_price
            model_pay_order.pay_price=pay_price
            model_pay_order.note=note
            model_pay_order.status=-8                                       #支付状态，-8为待支付
            model_pay_order.express_status=-8                               #快递状态，-8为待支付
            model_pay_order.updated_time=model_pay_order.created_time=getCurrentDate()
            db.session.add(model_pay_order)

            for item in items:
                tmp_left_stock=tmp_food_stock_mapping[item['id']]
                if decimal.Decimal(item['price'])<0:
                    continue
                if int(item['number'])>int(tmp_left_stock):
                    raise Exception("您购买的商品太火爆了,剩余:%s,您购买:%s" % (tmp_left_stock,item['number']))

                tmp_ret=Food.query.filter_by(id=item['id']).update({         #更新库存
                    "stock":int(tmp_left_stock)-int(item['number'])
                })
                if not tmp_ret:
                    raise Exception("下单失败请重新下单-1~~")
                tmp_pay_item=PayOrderItem()                                 #从表，存放订单商品信息
                tmp_pay_item.pay_order_id=model_pay_order.id
                tmp_pay_item.member_id=member_id
                tmp_pay_item.quantity=item['number']
                tmp_pay_item.price=item['price']
                tmp_pay_item.food_id=item['id']
                tmp_pay_item.note=note
                tmp_pay_item.updated_time=tmp_pay_item.created_time=getCurrentDate()
                db.session.add(tmp_pay_item)
                FoodService.setStockChangeLog(item['id'],-item['number'],"在线购买")        #操作库存信息表FoodStockChangeLog

            db.session.commit()
            resp['data']={
                'id':model_pay_order.id,
                'order_sn':model_pay_order.order_sn,
                'total_price':str(total_price)
            }
        except Exception as e:
            db.session.rollback()           #数据库会话也可回滚。调用 db.session.rollback() 后,添加到数据库会话中、还未提交的所有对象都会还原到它们在数据库中的版本。
            print(e)
            resp['code']=-1
            resp['msg']="下单失败请重新下单-2~~"
            resp['msg']=str(e)
            return resp
        return resp
    def orderSuccess(self,pay_order_id = 0,params = None):
        try:
            pay_order_info = PayOrder.query.filter_by( id = pay_order_id ).first()
            if not pay_order_info or pay_order_info.status not in [ -8,-7 ]:
                return True

            pay_order_info.pay_sn = params['pay_sn'] if params and 'pay_sn' in params else ''
            pay_order_info.status = 1
            pay_order_info.express_status = -7
            pay_order_info.updated_time = getCurrentDate()
            db.session.add( pay_order_info  )


            pay_order_items = PayOrderItem.query.filter_by( pay_order_id = pay_order_id ).all()
            for order_item in pay_order_items:
                tmp_model_sale_log = FoodSaleChangeLog()
                tmp_model_sale_log.food_id = order_item.food_id
                tmp_model_sale_log.quantity = order_item.quantity
                tmp_model_sale_log.price = order_item.price
                tmp_model_sale_log.member_id = order_item.member_id
                tmp_model_sale_log.created_time = getCurrentDate()
                db.session.add( tmp_model_sale_log )

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False

        #加入通知队列，做消息提醒和
        QueueService.addQueue( "pay",{
            "member_id": pay_order_info.member_id,
            "pay_order_id":pay_order_info.id
        })
        return True
    def addPayCallbackData(self,pay_order_id = 0,type = 'pay',data = ''):
        model_callback = PayOrderCallbackData()
        model_callback.pay_order_id = pay_order_id
        if type == "pay":
            model_callback.pay_data = data
            model_callback.refund_data = ''
        else:
            model_callback.refund_data = data
            model_callback.pay_data = ''

        model_callback.created_time = model_callback.updated_time = getCurrentDate()
        db.session.add( model_callback )
        db.session.commit()
        return True
    def geneOrderSn(self):
        m=hashlib.md5()                                                     #生成随机订单号
        sn=None
        while True:
            str="%s-%s" % (int(round(time.time()*1000)),random.randint(0,9999999))
            m.update(str.encode("utf-8"))
            sn=m.hexdigest()
            if not PayOrder.query.filter_by(order_sn=sn).first():           #查询数据库，不能有相同的订单号
                break
        return sn