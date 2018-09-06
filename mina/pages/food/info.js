//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');      //开源代码：详情页面的商品介绍
var utils = require('../../utils/util.js');             //teacher封装的公共代码

Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax:1,            //getInfo.resp.data.info.stock
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 0,      //shopCarNum为购物车右上角角标数字
        commentCount:2
    },
    onLoad: function (e) {
        var that = this;

        that.setData({
            id:e.id             //id直接从e中取
        });

        that.setData({
            commentList: [
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                },
                {
                    "score": "好评",
                    "date": "2017-10-11 10:20:00",
                    "content": "非常好吃，一直在他们加购买",
                    "user": {
                        "avatar_url": "/images/more/logo.png",
                        "nick": "angellee 🐰 🐒"
                    }
                }
            ]
        });
    },
    onShow:function(){
        this.getInfo();
    },
    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    addShopCar: function () {       //添加到购物车
        var that=this;
        var data={
            "id":this.data.info.id,
            "number":this.data.buyNumber
        };
        wx.request({
            url:app.buildUrl("cart/set"),
            header:app.getRequestHeader(),
            method:'POST',
            data:data,
            success:function (res) {
                var resp=res.data;
                app.alert({'content':resp.msg});
                that.setData({
                    hideShopPopup:true
                });
            }
        });
    },
    buyNow: function () {           //现在购买
        var data={
            goods:[{
                "id":this.data.info.id,
                "price":this.data.info.price,
                "number":this.data.buyNumber,
            }]
        };
        this.setData({              //感觉没啥卵用
            hideShopPopup:true
        });
        wx.navigateTo({
            url: "/pages/order/index?data="+JSON.stringify(data)        //get传参
        });
    },
    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    },
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    },
    numJianTap: function () {
        if( this.data.buyNumber <= this.data.buyNumMin){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    },
    numJiaTap: function () {
        if( this.data.buyNumber >= this.data.buyNumMax ){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    getInfo:function () {
        var that=this;
        wx.request({
            url:app.buildUrl("food/info"),
            header:app.getRequestHeader(),
            data:{
                id:that.data.id
            },
            success:function (res) {
                var resp=res.data;              //根据官方文档，res.data才是真正的返回数据
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }

                that.setData({
                    info:resp.data.info,
                    buyNumMax:resp.data.info.stock,
                    shopCarNum:resp.data.cart_number        //获取购物车数量，shopCarNum为购物车右上角角标数字
                });
                WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);  //开源代码：详情页面的商品介绍
            }
        });
    },
    onShareAppMessage:function () {          //官方文档微信小程序转发功能，************************************************
        var that=this;
        return {
            title: that.data.info.name,
            path: '/page/food/info?id='+that.data.info.id,
            success:function (res) {
                //转发成功
                wx.request({
                    url: app.buildUrl("member/share"),
                    header: app.getRequestHeader(),
                    method:'POST',
                    data: {
                        url:utils.getCurrentPageUrlWithArgs()
                    },
                    success:function (res) {
                        
                    }
                });
            },
            fail:function (res) {
                //转发失败
            }
        }
    }
});
