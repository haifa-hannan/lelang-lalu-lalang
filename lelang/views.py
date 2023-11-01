from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Product
from helpers.utils import insert_data, validate_payload_credentials, result_covert_simple

# Create your views here.
class GetProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductViews(APIView):
    def post(self,request):
        results = []
        # payload = request.data
        # if not isinstance(payload, list) or not all(isinstance(item,dict) for item in payload):
        #     return Response({
        #         "error": "Invalid payload format. Expecting a list of dictionaries"
        #     }, status=400)
        
        # for data in payload:
        #     keys = ["prodname", "desc","img","price","status"]
        #     valid_res = validate_payload_credentials(data, keys)
        #     if valid_res['creds'] is None:
        #         res = {
        #             "missing": valid_res['missing_fields']
        #         }
        #         return Response(res, status=400)
        #     data = valid_res["creds"]
        try:
            prodname = request.data.get("prodname")
            desc = request.data.get("desc")
            img = request.data.get("img")
            price = request.data.get("price")
            status = request.data.get("status")

            new_data = {
                "prodname": prodname,
                "desc": desc,
                "img": img,
                "price": price,
                "status": status
            }
            # insert_data(Product, new_data)
            Product.objects.create(**new_data)
            res ={
                "status": 201,
                "message": "Product add successfully"
            }
            results.append(res)
            return Response(result_covert_simple(res))
        except Exception as e:
            return Response({
                "message":"something went wrong", 
                "details":str(e),
            }, status=400)
            # res = {
            #     "status": 400,
            #     "message":"error adding product",
            #     "detail": str(e)
            # }
            # results.append(res)

