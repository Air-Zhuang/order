SERVER_PORT=5000
DEBUG=False
SQLALCHEMY_ECHO=False

AUTH_COOKIE_NAME="mooc_food"

##过滤url
IGNORE_URLS=[
    "^/user/login",
]

##过滤不需要cookie验证的url
IGNORE_CHECK_LOGIN_URLS=[
    "^/static",
    "^/favicon.ico"
]

API_IGNORE_URLS=[
    "^/api"
]

PAGE_SIZE=50    #每页展示多少条
PAGE_DISPLAY=10 #展示多少页

STATUS_MAPPING={
    "1":"正常",
    "0":"已删除"
}
MINA_APP={
    'appid':'wxfd1db552eeac1b97',
    'appkey':'f80619a5c1db3f19afbea06d1c0d3cfb',
    'paykey':'xxxx',                            #key设置路径：微信商户平台(pay.weixin.qq.com)-->账户设置-->API安全-->密钥设置
    'mch_id':'xxxx',                            #商户id
    'callback_url':'/api/order/callback'        #下单之后的回调地址
}

UPLOAD={
    'ext':['jpg','gif','bmp','jpeg','png'],
    'prefix_path':'/web/static/upload/',
    'prefix_url':'/static/upload/',
}

APP={
    'domain':'http://127.0.0.1:5000'
}

PAY_STATUS_DISPLAY_MAPPING={
    "0":"订单关闭",
    "1":"支付成功",
    "-8":"待支付",
    "-7":"代发货",
    "-6":"待确认",
    "-5":"待评价"
}