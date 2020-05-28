//修改个人中心邮箱验证码

$(function () {
    //个人资料修改密码
    $('#jsUserResetPwd').on('click', function () {
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });

    $('#jsResetPwdBtn').click(function () {
        $.ajax({
            cache: false,
            type: "POST",
            dataType: 'json',
            url: "/user/resetpwd/",
            data: $('#jsResetPwdForm').serialize(),
            async: true,
            success: function (result) {
                console.log(result);
                if (result.password1) {
                    Dml.fun.showValidateError($("#pwd"), result.password1);
                } else if (result.password2) {
                    Dml.fun.showValidateError($("#repwd"), result.password2);
                } else if (result.code === 200) {
                    // Dml.fun.showTipsDialog({
                    //     title: '提交成功',
                    //     h2: '修改密码成功，请重新登录!',
                    // });
                    window.messageBox.show("修改成功！请重新登录");
                    // window.location.reload();
                    Dml.fun.winReload();
                } else if (result.code === 400) {
                    messageBox.show("两次密码不一致！")
                }
            }
        });
    });

    //个人资料头像
    $('.js-img-up').uploadPreview({
        Img: ".js-img-show", Width: 94, Height: 94, Callback: function () {
            $('#jsAvatarForm').submit();
        }
    });


    //input获得焦点样式
    $('.perinform input[type=text]').focus(function () {
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function () {
        $(this).parent('li').removeClass('focus');
    });

    laydate({
        elem: '#birthday',
        format: 'YYYY-MM-DD',
        max: laydate.now()
    });

    verify(
        [
            {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserBtn').on('click', function () {
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm');
        console.log($jsEditUserForm.serialize());
        verify = verifySubmit(
            [
                {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
            ]
        );
        if (!verify) {
            return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType: 'json',
            url: "/user/info/",
            data: $jsEditUserForm.serialize(),
            async: true,

            beforeSend: function (XMLHttpRequest) {
                _self.val("保存中...");
                _self.attr('disabled', true);
            },
            success: function (result) {
                console.log(result)
                if (result.nick_name) {
                    _showValidateError($('#nick_name'), result.nick_name);
                } else if (result.birday) {
                    _showValidateError($('#birthday'), result.birthday);
                } else if (result.email) {
                    _showValidateError($('#adress'), result.email);
                } else if (result.status == "failure") {
                    Dml.fun.showTipsDialog({
                        title: '保存失败',
                        h2: result.msg
                    });
                } else if (result.code === 200) {
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    setTimeout(function () {
                        window.location.reload()
                    }, 1000);
                }else if (result.code === 400){
                    window.messageBox.showError("请选择正确格式的日期！")
                }
            },
            complete: function (XMLHttpRequest) {
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });


});