
class FormMixin(object):
    def get_error(self):
        if hasattr(self,'errors'):
            error_dict = {}
            errors = self.errors.get_json_data()
         # 错误信息格式为{'username': [{'message': '用户名不得少于4个字符', 'code': 'min_length'}], 'password': [{'message': '密码不得少于6个字符', 'code': 'min_length'}]}
            for key,message_dict in errors.items():
                messages = []
                for message in message_dict:
                    messages.append(message['message'])
                error_dict[key] = messages
            return error_dict
        else:
            return {}

#
# f = FormMixin()
# f.get_error()