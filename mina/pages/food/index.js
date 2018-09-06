//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p:1,                //处理上拉刷新的分页
        processing:false    //处理上拉刷新是否正在处理请求，如果正在处理则不能发送请求
    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });
    },
    onShow:function(){                      //为了每次返回首页都能刷新页面获取最新值，使用onShow方法：页面只要显示就调用方法
        // this.setData({
        //     p:1,
        //     goods:[],
        //     loadingMoreHidden:true
        // });
        this.getBannerAndCat();             //调用方法返回banner和分类信息的json数据
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
	 toSearch:function( e ){
	        this.setData({
	            p:1,
	            goods:[],
	            loadingMoreHidden:true
	        });
	        this.getFoodList();
	},
    tapBanner: function (e) {                   //点击banner图事件
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id        //html中的data-id字段
            });
        }
    },
    toDetailsTap: function (e) {                //点击跳转到详情页
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id        //页面data-id值
        });
    },
    getBannerAndCat:function () {
        var that=this;
        wx.request({
            url:app.buildUrl("food/index"),     //返回banner_list和cat_list
            header:app.getRequestHeader(),
            success:function (res) {
                var resp=res.data;              //根据官方文档，res.data才是真正的返回数据
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }
                that.setData({                  //官方设置数据方法
                    banners:resp.data.banner_list,
                    categories:resp.data.cat_list
                });
                that.getFoodList();
            }
        });
    },
    catClick:function(e){
        this.setData({
            activeCategoryId:e.currentTarget.id,      //让activeCategoryId变为调catClick方法的id，使其状态变为高亮选中状态
            p:1,                                    //分类 查询时初始化 分页 查询信息
            goods:[],
            loadingMoreHidden:true
        });
        this.getFoodList();
    },
    onReachBottom: function () {                       //微信的上拉刷新功能
        var that=this;
        setTimeout(function () {             //触碰到底之后延迟0.5秒在执行方法
            that.getFoodList();
        },500);
    },
    getFoodList:function () {
        var that=this;
        if(that.data.processing){       //防止同时处理多个请求
            return;
        }

        if(!that.data.loadingMoreHidden){   //如果判断没有可查询出的数据时不再发送请求
            return;
        }

        that.setData({
           processing:true          //防止同时处理多个请求
        });

        wx.request({
            url:app.buildUrl("food/search"),
            header:app.getRequestHeader(),
            data:{
                cat_id:that.data.activeCategoryId,          //分类id
                mix_kw:that.data.searchInput,               //搜索框内容
                p:that.data.p
            },
            success:function (res) {
                var resp=res.data;              //根据官方文档，res.data才是真正的返回数据
                if(resp.code!=200){
                    app.alert({"content":resp.msg});
                    return;
                }

                var goods=resp.data.list;
                that.setData({
                    goods:that.data.goods.concat(goods),        //每次翻页将新查出的信息添加到原来的数据上，而不是替换
                    p:that.data.p+1,                //每次上拉刷新或查询完完分页变量p加一
                    processing:false                //防止同时处理多个请求
                });

                if(resp.data.has_more==0){
                    that.setData({
                       loadingMoreHidden:false      //html中的"没有数据了~~"取消隐藏
                    });
                }
            }
        });
    }
});
