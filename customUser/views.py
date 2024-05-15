import json
from django.shortcuts import render
from .models  import  UserData,AccessToken
from django.http import JsonResponse
# from rest_framework.views import APIView
import jwt, math, time
from django.views.decorators.csrf import csrf_exempt




def combine_response(msg,payload,data):
    
    return {
        "msg":msg,
        "payload":payload,
        'data': data
    }


@csrf_exempt
def register(request):
    requestData = json.loads(request.body)
    try:
        UserData.objects.values().get(email=requestData['email'])
        return JsonResponse("Email already exists", safe=False, status=200)
    except:
        UserData.objects.create(email=requestData['email'], password=requestData['password'])
        userId = UserData.objects.values().get(email=requestData['email'])
        
        access_payload={
            'token_type':'access',
            'id':userId['id'],
            'exp': math.floor(time.time() + 100),
            'iat': math.floor(time.time()),
        }
        refresh_payload={
            'token_type':'refresh',
            'jti': userId['email'],
            'id':access_payload.get('jti'),
            'exp': math.floor(time.time() + 2592000),
            'iat': math.floor(time.time()),
        }
        encoded_refresh_Jwt = jwt.encode(refresh_payload, "mrvishope",  algorithm="HS256")
        encoded_access_Jwt = jwt.encode(access_payload, "mrvishope",  algorithm="HS256")
        response = JsonResponse(combine_response("user created",{"refresh":refresh_payload, "access":access_payload},requestData), safe=False, status=200)
        response.set_cookie('refresh_token', encoded_refresh_Jwt) 
        response.set_cookie('access_token', encoded_access_Jwt) 
        AccessToken.objects.create(jti=refresh_payload.get('jti'), userid=access_payload.get('id'))
        return response






@csrf_exempt
def login(request):
    requestData = json.loads(request.body)
    
    refresh_token = request.COOKIES.get("refresh_token")
    access_token = request.COOKIES.get("access_token")
    if refresh_token:
        if access_token:
            try:
                access_payload = jwt.decode(access_token, 'mrvishope', algorithms='HS256')
                print(access_payload)
                data =  UserData.objects.values().get(pk=access_payload.get('id'))
                return JsonResponse( combine_response("Success", access_payload, data), safe=False, status=200)
            except:
                try:
                    refresh_payload = jwt.decode(refresh_token, 'mrvishope', algorithms='HS256')
                    accessTokenid = AccessToken.objects.values.get(jti=refresh_payload.get('jti'))
                    access_payload={
                        'token_type':'access',
                        'id':accessTokenid.get('userid'),
                        'exp': math.floor(time.time() + 100),
                        'iat': math.floor(time.time()),
                    }
                    
                    encoded_access_Jwt = jwt.encode(access_payload, "mrvishope",  algorithm="HS256")
                    response = JsonResponse(combine_response("user created",refresh_payload,requestData), safe=False, status=200)
                    response.set_cookie('access_token', encoded_access_Jwt) 
                    return response
                except:
                    print(refresh_payload)
                    return JsonResponse("Invalid Token", safe=False, status=200)
    try:
        data =  UserData.objects.values().get(email=requestData['email'],is_deleted=False)
        if data['password'] == requestData['password']:
            encodedJwt = jwt.encode(refresh_payload, "mrvishope",  algorithm="HS256")
            response = JsonResponse(combine_response("user Found",{"refresh":refresh_payload, "access":access_payload},data), safe=False, status=200)
            response.set_cookie('token', encodedJwt) 
            return response
        else:
            return JsonResponse("Invalid Pass User", safe=False, status=200)
    except:
        return JsonResponse("Invalid Email User", safe=False, status=200)
    
        

# @csrf_exempt
# def getData(request):
#     datas = list(UserData.objects.values().filter(is_deleted=False))
#     datawithoutPass = []
#     for data in datas:
#         datawithoutPass.append({
#             "id": data['id'],
#             "name": data['name'],
#             "email": data['email'],
#         }) 
#     payload={
#         'id':"1",
#         'exp': math.floor(time.time() + 100),
#         'iat': math.floor(time.time()),
#         'name':"Bishal Phuyal"
#     }

#     token = request.COOKIES.get("token")
#     if token:
#         try:
#             payload = jwt.decode(token, "mrvishope", algorithms="HS256")
#             return JsonResponse( combine_response("You need to login for getting data",payload,datawithoutPass), safe=False, status=400)
#         except:
#             return JsonResponse("False", safe=False, status=200)

#     encodedJwt = jwt.encode(payload, "mrvishope", algorithm="HS256")
#     response = JsonResponse(datawithoutPass, safe=False, status=200)
#     response.set_cookie('token',encodedJwt)
#     return JsonResponse("datawithoutPass", safe=False, status=200)

# @csrf_exempt
# def getUser(request, **userID):
#     user_id = userID["userid"]
#     data = UserData.objects.values().get(is_deleted=False, id=user_id)
#     datawithoutPass ={
#         "id": data['id'],
#         "name": data['name'],
#         "email": data['email'],
#     }
#     return JsonResponse(datawithoutPass, safe=False, status=200)





# @csrf_exempt
# def checkMailAvailable(request):
#     datas = UserData.objects.all()
#     isemailSet = False
#     emailId = json.loads(request.body)
#     for data in datas:
#         if data.email == emailId["checkEmailID"]:
#             isemailSet = True
#             break
#     return JsonResponse({"availability": not isemailSet } , safe=False, status=200)


# @csrf_exempt
# def patch(request, **userID):
#     user_id = userID["userid"]
#     data = json.loads(request.body)
#     updateuser = UserData.objects.get(pk=user_id)
#     updateuser.__dict__.update(data)
#     updateuser.save()
#     res = {
#                 "data": data,
#                 "message": "User Updated"
#             }
    
#     return JsonResponse(res, safe=False, status=200)
    
    
    
