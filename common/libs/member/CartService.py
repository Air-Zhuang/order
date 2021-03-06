from application import app,db
from common.models.member.MemberCart import MemberCart
from common.libs.Helper import getCurrentDate

class CartService():
    @staticmethod                       #删除购物车
    def deleteItem(member_id=0,items=None):
        if member_id<1 or not items:
            return False
        for item in items:              #遍历items,依次取出item['id']
            MemberCart.query.filter_by(food_id=item['id'],member_id=member_id).delete()
        db.session.commit()
        return True

    @staticmethod                       #修改或添加购物车
    def setItems(member_id=0,food_id=0,number=0):
        if member_id<1 or food_id<1 or number<1:
            return False
        cart_info=MemberCart.query.filter_by(food_id=food_id,member_id=member_id).first()
        if cart_info:                   #如果存在记录则修改，否则添加
            model_cart=cart_info
        else:
            model_cart=MemberCart()
            model_cart.member_id=member_id
            model_cart.created_time=getCurrentDate()

        model_cart.food_id=food_id
        model_cart.quantity=number
        model_cart.updated_time=getCurrentDate()
        db.session.add(model_cart)
        db.session.commit()
        return True









