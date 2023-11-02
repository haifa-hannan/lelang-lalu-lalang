from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import Product
from helpers.utils import insert_data, validate_payload_credentials, result_covert_simple
from django.core.files.base import ContentFile

import base64

# Create your views here.
class GetProduct(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductViews(APIView):
    def post(self,request):
        results = []
        payload = request.data
        if not isinstance(payload, list) or not all(isinstance(item,dict) for item in payload):
            return Response({
                "error": "Invalid payload format. Expecting a list of dictionaries"
            }, status=400)
        
        for data in payload:
            keys = ["prodname", "desc","img","price"]
            valid_res = validate_payload_credentials(data, keys)
            if valid_res['creds'] is None:
                res = {
                    "missing": valid_res['missing_fields']
                }
                return Response(res, status=400)
            creds = valid_res["creds"]

            
            try:
                e = creds['img']
                fmt, docu = e.split(";base64,")
                ext = fmt.split("/")[-1]
                decoded_data = base64.b64decode(docu)
                file_data = ContentFile(decoded_data, name=f"image.{ext}")
                binary_data = file_data.read()
            except Exception as e:
                return Response({
                    "message": "failed to decode image file",
                    "details": str(e)
                }, status=400)
        
        # prodname = request.data.get("prodname")
        # desc = request.data.get("desc")
        # img = request.data.get("img")
        # price = request.data.get("price")
        # status = request.data.get("status")

            try:
                new_data = {
                    "prodname": data['prodname'],
                    "desc": data['desc'],
                    # "img": binary_data,
                    "price": data['price'],
                    # "status": data['status'],
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
                res = {
                    "status":400,
                    "message": "Product add failed",
                    "details": str(e)
                }
                results.append(res)

            try:
                file = {
                    "img": binary_data
                }
                Image.objects.create(**file)
                res = {
                    "status": 201,
                    "message": "Image added successfully"
                }
                results.append(res)

                return Response(result_covert_simple(res))
            except Exception as e:
                res = {
                    "status": 400,
                    "message": "Error adding image"
                }
                results.append(res)

        if all(r['status']!=201 for r in results):
            return Response({
                "message": "something went wrong",
                "data": results
            }, status=400)
        return Response({
            "message": "product added",
            "details": results
        }, status=200)
        

class UpdateStatus(APIView):
    def post(self,request):
        keys = ['productid','statusid']
        valid_res = validate_payload_credentials(request, keys)
        if valid_res['creds'] is None:
            res = {
                "missing": valid_res['missing_fields']
            }
            return Response(res, status=400)
        data = valid_res["creds"]

        try:
            stat = Status.objects.get(stat=data['status'])
            prodid = Product.objects.get(prodid=data['productid'])
            prodid.status = stat.status
            prodid.save()
            return Response({"message": "status updated successfully"})
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=500)