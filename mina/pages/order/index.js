//获取应用实例
var app = getApp();

Page({
    data: {
        goods_list: [],
        default_address: null,
        yun_price: "0.00",
        pay_price: "0.00",
        total_price: "0.00",
        params: null
    },
    onShow: function () {
        var that = this;
        this.getOrderInfo();
    },
    onLoad: function (e) {                  //e获取传过来的信息
        var that = this;
        that.setData({
            params:JSON.parse(e.data)       //获取get请求url中的参数信息
        });
    },
    createOrder: function (e) {
        wx.showLoading();
        var that = this;
        var data={
            type:this.data.params.type,             //依旧获取从哪个地方获取的订单信息和订单详情
            goods:JSON.stringify(this.data.params.goods)
        };
        wx.request({                                    //将参数信息作为请求，得到返回的数据库信息
            url: app.buildUrl("order/create"),           //下单处理
            header: app.getRequestHeader(),
            method: 'POST',
            data: data,
            success: function (res) {
                wx.hideLoading();                   //微信中间转圈圈的loading图标
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                wx.navigateTo({
                    url: "/pages/my/order_list"
                });
            }
        });
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },
    getOrderInfo:function () {              //获取用户的订单信息，(onLoad方法已经从get请求中获取订单信息并放在全局变量params中)
        var that=this;
        var data={
            type:this.data.params.type,
            goods:JSON.stringify(this.data.params.goods),
        };
        wx.request({                        //将参数信息作为请求，得到返回的数据库信息
            url:app.buildUrl("order/info"),
            header:app.getRequestHeader(),
            method:'POST',
            data:data,
            success:function (res) {
                var resp=res.data;
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }
                that.setData({
                    goods_list:resp.data.food_list,
                    default_address:resp.data.default_address,
                    yun_price:resp.data.yun_price,
                    pay_price:resp.data.pay_price,
                    total_price:resp.data.total_price
                })
            }
        });
    }

});
