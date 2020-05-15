function Auth() {

}

Auth.prototype.LoginClick = function () {
    var self = this;
    var loginBtn = $("#login");
    var usernameInput = $("input[name='username']");
    var pwdInput = $('input[name="pass"]');
    var next = window.location.search;
    console.log("&*******************");
    console.log(next);
    loginBtn.click(function () {
        username = usernameInput.val();
        pwd = pwdInput.val();
        console.log("Login", username);
        console.log("pwd", pwd);
        xfzajax.post({
            'url': '/user/login/',
            'data': {
                'username': username,
                'pwd': pwd,
                'next': next
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    next_url = result['data']['next_url'];
                    if (next_url) {
                        var pattern = RegExp('operation');
                        var fav_url = pattern.test(next_url);
                        if (fav_url) {
                            window.location.href = "http://" + window.location.host + next_url;
                        } else {
                            window.location.href = '/' + next_url
                        }

                    } else {
                        window.location.href = '/';
                        // window.messageBox.show("登录成功!")
                    }
                } else {
                    var messageObject = result['message'];
                    if (typeof messageObject == 'string' || messageObject.constructor == String) {
                        window.messageBox.show(messageObject);
                    } else {
                        // {'username':['xxxxxxxxxxxxxxx','xxx'],'telephone':['xxxxxxx','xxxxxx']}
                        for (var key in messageObject) {
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message)
                        }
                    }
                }
            },
            "fail": function (err) {
                console.log(err)
            }
        })
    })

};
Auth.prototype.ListenRegistClick = function () {
    var self = this;
    var registButton = $("#regist");
    var telephoneInput = $("input[name='regname']");
    var pwd1Input = $('input[name="regpass"]');
    var pwd2Input = $('input[name="reregpass"]');


    registButton.click(function () {
        regname = telephoneInput.val();
        regpass = pwd1Input.val();
        reregpass = pwd2Input.val();
        xfzajax.post({
            'url': '/user/regist/',
            'data': {
                'regname': regname,
                'regpass': regpass,
                'reregpass': reregpass
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.show('注册成功!');
                    window.location.href = '/';
                } else {
                    var messageObject = result['message'];
                    if (typeof messageObject === 'string' || messageObject.constructor === String) {
                        window.messageBox.show(messageObject);
                    } else {
                        // {'username':['xxxxxxxxxxxxxxx','xxx'],'telephone':['xxxxxxx','xxxxxx']}
                        for (var key in messageObject) {
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.show(message)
                        }
                    }
                }
            },
            "fail": function (err) {
                console.log(err)
            }
        })

    })
};


Auth.prototype.run = function () {
    this.ListenRegistClick();
    this.LoginClick();
};
$(function () {
    var auth = new Auth();
    auth.run()
});