//app.js
App({
    onLaunch: function () {
    },
    globalData: {
        userInfo: null,
        version: "1.0",
        shopName: "Python3 + Flask 订餐全栈系统",
        domain:"http://127.0.0.1:5001/api/"             //不用每次都写地址
    },
    tip:function( params ){
        var that = this;
        var title = params.hasOwnProperty('title')?params['title']:'提示信息';
        var content = params.hasOwnProperty('content')?params['content']:'';
        wx.showModal({
            title: title,
            content: content,
            success: function(res) {

                if ( res.confirm ) {//点击确定
                    if( params.hasOwnProperty('cb_confirm') && typeof( params.cb_confirm ) == "function" ){
                        params.cb_confirm();
                    }
                }else{//点击否
                    if( params.hasOwnProperty('cb_cancel') && typeof( params.cb_cancel ) == "function" ){
                        params.cb_cancel();
                    }
                }
            }
        })
    },
    alert:function( params ){
        var title = params.hasOwnProperty('title')?params['title']:'提示信息';
        var content = params.hasOwnProperty('content')?params['content']:'';
        wx.showModal({
            title: title,
            content: content,
            showCancel:false,
            success: function(res) {
                if (res.confirm) {//用户点击确定
                    if( params.hasOwnProperty('cb_confirm') && typeof( params.cb_confirm ) == "function" ){
                        params.cb_confirm();
                    }
                }else{
                    if( params.hasOwnProperty('cb_cancel') && typeof( params.cb_cancel ) == "function" ){
                        params.cb_cancel();
                    }
                }
            }
        })
    },
    console:function( msg ){
        console.log( msg);
    },
    getRequestHeader:function(){
        return {
            'content-type': 'application/x-www-form-urlencoded',
            'Authorization':this.getCache("token")                  //给后台member拦截器使用
        }
    },
    buildUrl:function (path,params) {
        var url=this.globalData.domain+path;
        var _paramUrl="";
        if(params){
            _paramUrl=Object.keys(params).map(function (k) {
                alert();
                return [encodeURIComponent(k),encodeURIComponent(params[k])].join("=");
            }).join("&");
            _paramUrl="?"+_paramUrl
        }
        return url+_paramUrl;
    },
    getCache:function (key) {                       //官方文档的 wx.getStorageSync 得到缓存  用同步的方式
        var value=undefined;
        try {
            value = wx.getStorageSync(key);
        }catch (e) {
        }
        return value;
    },
    setCache:function (key,value) {                 //官方文档的 wx.setStorage 添加缓存  用异步的方式
        wx.setStorage({
          key:key,
          data:value
        });
    }
});