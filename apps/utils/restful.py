from django.http import JsonResponse

class HttpCode:
    ok = 200
    paramserror = 400
    noauth = 401
    methoderror = 405
    servererror = 500

def result(code=HttpCode.ok,message='',data=None,kwargs=None):
    json_dict = {'code':code,'message':message,'data':data}
    # 判断是否有其他字典类型的数据传给前端
    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)
    # 返回json数据
    return JsonResponse(json_dict)

def ok():
    return result()

def noauth(message='没用权限'):
    return result(code=HttpCode.noauth,message=message)

def paramserror(message='参数错误'):
    return result(code=HttpCode.paramserror,message=message)

def methoderror(message='请求方法错误'):
    return result(code=HttpCode.methoderror,message=message)

def servererror(message='服务器内部错误'):
    return result(code=HttpCode.servererror,message=message)
