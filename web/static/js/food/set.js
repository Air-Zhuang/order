;
var upload = {                                              //实现上传封面图的error和success方法
    error: function (msg) {
        common_ops.alert(msg);
    },
    success: function (file_key) {
        if (!file_key) {
            return;
        }
        var html = '<img src="' + common_ops.buildPicUrl(file_key) + '"/>'               //拼装html
                + '<span class="fa fa-times-circle del del_image" data="' + file_key + '"></span>';

        if ($(".upload_pic_wrap .pic-each").size() > 0) {                                //如果没有图片增加一条数据
            $(".upload_pic_wrap .pic-each").html(html);
        } else {
            $(".upload_pic_wrap").append('<span class="pic-each">' + html + '</span>');    //如果有直接进行编辑
        }
        food_set_ops.delete_img();
    }
};
var food_set_ops = {
    init: function () {
        this.ue = null;
        this.eventBind();
        this.initEditor();
        this.delete_img();
    },
    eventBind: function () {
        var that = this;

        $(".wrap_food_set .upload_pic_wrap input[name=pic]").change(function () {       //实现无刷新上传技术:建立一个隐藏的iframe,form表单target指向iframe
            $(".wrap_food_set .upload_pic_wrap").submit();
        });

        $(".wrap_food_set select[name=cat_id]").select2({                               //select2插件
            language: "zh-CN",
            width: '100%'
        });

        $(".wrap_food_set input[name=tags]").tagsInput({                                 //tagsinput插件
            width: 'auto',
            height: 40,
            onAddTag: function (tag) {
            },
            onRemoveTag: function (tag) {
            }
        });

        $(".wrap_food_set .save").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理!!请不要重复提交~~");
                return;
            }

            var cat_id_target = $(".wrap_food_set select[name=cat_id]");
            var cat_id = cat_id_target.val();

            var name_target = $(".wrap_food_set input[name=name]");
            var name = name_target.val();

            var price_target = $(".wrap_food_set input[name=price]");
            var price = price_target.val();

            var summary = $.trim(that.ue.getContent());          //下面initEditor定义that为Ueditor

            var stock_target = $(".wrap_food_set input[name=stock]");
            var stock = stock_target.val();

            var tags_target = $(".wrap_food_set input[name=tags]");
            var tags = $.trim(tags_target.val());               //$.trim() 函数用于去除字符串两端的空白字符。

            if (parseInt(cat_id) < 1) {
                common_ops.tip("请选择分类~~", cat_id_target);
                return;
            }

            if (name.length < 1) {
                common_ops.alert("请输入符合规范的名称~~");
                return;
            }

            if (parseFloat(price) <= 0) {
                common_ops.tip("请输入符合规范的售卖价格~~", price_target);
                return;
            }

            if ($(".wrap_food_set .pic-each").size() < 1) {
                common_ops.alert("请上传封面图~~");
                return;
            }

            if (summary.length < 10) {
                common_ops.tip("请输入描述，并不能少于10个字符~~", price_target);
                return;
            }

            if (parseInt(stock) < 1) {
                common_ops.tip("请输入符合规范的库存量~~", stock_target);
                return;
            }

            if (tags.length < 1) {
                common_ops.alert("请输入标签，便于搜索~~");
                return;
            }

            btn_target.addClass("disabled");

            var data = {
                cat_id: cat_id,
                name: name,
                price: price,
                main_image: $(".wrap_food_set .pic-each .del_image").attr("data"),
                summary: summary,
                stock: stock,
                tags: tags,
                id: $(".wrap_food_set input[name=id]").val()
            };

            $.ajax({
                url: common_ops.buildUrl("/food/set"),
                type: 'POST',
                data: data,
                dataType: 'json',
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/food/index");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            });

        });


    },
    initEditor: function () {                           //作Ueditor插件的初始化
        var that = this;
        that.ue = UE.getEditor('editor', {              //官方文档用法 'editor'为编辑器的id字段
            toolbars: [                                 //工具栏太多，筛选几个有用的工具栏
                ['undo', 'redo', '|',
                    'bold', 'italic', 'underline', 'strikethrough', 'removeformat', 'formatmatch', 'autotypeset', 'blockquote', 'pasteplain', '|', 'forecolor', 'backcolor', 'insertorderedlist', 'insertunorderedlist', 'selectall', '|', 'rowspacingtop', 'rowspacingbottom', 'lineheight'],
                ['customstyle', 'paragraph', 'fontfamily', 'fontsize', '|',
                    'directionalityltr', 'directionalityrtl', 'indent', '|',
                    'justifyleft', 'justifycenter', 'justifyright', 'justifyjustify', '|', 'touppercase', 'tolowercase', '|',
                    'link', 'unlink'],
                ['imagenone', 'imageleft', 'imageright', 'imagecenter', '|',
                    'insertimage', 'insertvideo', '|',
                    'horizontal', 'spechars', '|', 'inserttable', 'deletetable', 'insertparagraphbeforetable', 'insertrow', 'deleterow', 'insertcol', 'deletecol', 'mergecells', 'mergeright', 'mergedown', 'splittocells', 'splittorows', 'splittocols']

            ],
            enableAutoSave: true,               //设置编辑自动保存
            saveInterval: 60000,                //设置自动保存时间
            elementPathEnabled: false,          //不显示元素路径(无关紧要)
            zIndex: 4,                          //浮在层的上面
            serverUrl: common_ops.buildUrl('/upload/ueditor')           //设置上传路径
        });
    },
    delete_img: function () {                                           //实现可点击封面图上传后右上角的x
        $(".wrap_food_set .del_image").unbind().click(function () {     //先解除事件绑定
            $(this).parent().remove();                                  //父层的html删除
        });
    }
};

$(document).ready(function () {
    food_set_ops.init();
});