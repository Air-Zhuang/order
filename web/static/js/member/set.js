;
//会员列表 set.html 编辑会员信息
var member_set_ops={
    init:function () {
        this.eventBind();
    },
    eventBind:function () {
        $(".wrap_member_set .save").click(function () {
            var btn_target=$(this);                                             //绑定保存按钮
            if(btn_target.hasClass("disabled")){
                common_ops.alert("正在处理，请不要重复提交~~");
                return;
            }
            var nickname_target=$(".wrap_member_set input[name=nickname]");     //绑定输入框
            var nickname=nickname_target.val();                                 //获取输入框的输入内容

            if(nickname.length<1){
                common_ops.tip("请输入符合规范的姓名",nickname_target);
                return;
            }

            btn_target.addClass("disabled");

            var data={
                nickname:nickname,
                id:$(".wrap_member_set input[name=id]").val()                   //获取隐藏输入框中的id
            };

            $.ajax({
                url:common_ops.buildUrl("/member/set"),
                type:'POST',
                data:data,
                dataType:'json',
                success:function (res) {
                    btn_target.removeClass("disabled");
                    if(res.code==200){
                        callback=function () {
                            window.location.href=common_ops.buildUrl("/member/index");
                        }
                    }
                    common_ops.alert(res.msg,callback);
                }
            });

        });
    }
};

$(document).ready(function () {
    member_set_ops.init();
});