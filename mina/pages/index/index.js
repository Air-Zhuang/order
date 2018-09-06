//login.js
//获取应用实例
var app = getApp();
Page({
    data: {
        remind: '加载中',
        angle: 0,
        userInfo: {},
        regFlag:true                                            //判断是否已注册的标志
    },
    goToIndex: function () {
        wx.switchTab({
            url: '/pages/food/index',
        });
    },
    onLoad: function () {
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
        this.checkLogin();                                      //加载页面的时候就加载checkLogin方法
    },
    onShow: function () {

    },
    onReady: function () {
        var that = this;
        setTimeout(function () {
            that.setData({
                remind: ''
            });
        }, 1000);
        wx.onAccelerometerChange(function (res) {
            var angle = -(res.x * 30).toFixed(1);
            if (angle > 14) {
                angle = 14;
            }
            else if (angle < -14) {
                angle = -14;
            }
            if (that.data.angle !== angle) {
                that.setData({
                    angle: angle
                });
            }
        });
    },
    //检查是否已注册的方法
    checkLogin:function(){
        var that=this;
        wx.login({
            success:function (res) {
                if(!res.code){
                   app.alert({'content':'登录失败，请再次点击~~'});
                   return;
                }
                wx.request({                                     //调用微信的request方法
                    url:app.buildUrl('member/check-reg'),
                    header:app.getRequestHeader(),
                    method:'POST',
                    data:{code:res.code},
                    success:function (res) {
                        if(res.data.code!=200){                 //根据微信wx.request官方文档，返回值是在res.data中
                            that.setData({                      //微信的设置值的方法
                                regFlag:false
                            });
                            return;
                        }
                        app.setCache("token",res.data.data.token);  //添加缓存
                        // that.goToIndex();
                    }
               });
            }
        });
    },

    // 授权登录
    login:function (e) {
        var that=this;
        //app.console(e);                                       //查看用户信息
        if(!e.detail.userInfo){                                 //如果没有登录信息，则判断登录失败，返回return
            app.alert({'content':'登录失败，请再次点击~~'});     //调用自动生成的app里面的方法
            return;
        }
        var data=e.detail.userInfo;                             //data为用户信息

        wx.login({
           success:function (res) {                             //这里的res为返回的code
               if(!res.code){
                   app.alert({'content':'登录失败，请再次点击~~'});
                   return;
               }
               data['code']=res.code;                           //将获取到的code发送到后台系统去
               wx.request({                                     //调用微信的request方法
                    url:app.buildUrl('member/login'),
                    header:app.getRequestHeader(),
                    method:'POST',
                    data:data,
                    success:function (res) {
                        if(res.data.code!=200){                 //根据微信wx.request官方文档，返回值是在res.data中
                            app.alert({'content':res.msg});
                            return;
                        }
                        app.setCache("token",res.data.data.token);  //添加缓存
                        that.goToIndex();
                    }
               });
           }
        });
    }
});