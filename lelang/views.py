from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
from helpers.utils import insert_data, validate_payload_credentials, result_covert_simple, validate_credentials
from django.core.files.base import ContentFile
from django import forms
from decimal import Decimal

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
            keys = ["prodname", "desc","file","price"]
            valid_res = validate_payload_credentials(data, keys)
            if valid_res['creds'] is None:
                res = {
                    "missing": valid_res['missing_fields']
                }
                return Response(res, status=400)
            creds = valid_res["creds"]
            
            try:
                e = creds['file']
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
                file = {"img": binary_data}
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
    
# class UpdateProduct(APIView):
#     def post(self, request):
#         results = []
#         payload = request.data
#         keys = ["prodname", "desc","price"]

#         # lookup_field = f"{'productid'}__exact"
#         # query = {lookup_field : creds['productid']}
#         # if not Product.objects.filter(**query).exists():
#         #     raise ValueError("product not found")
        
#         for data in payload:
#             valid_res = validate_credentials(data, keys)
#             if valid_res['creds'] is None:
#                 res = {
#                     "missing": valid_res['missing_fields']
#                 }
#                 return Response(res, status=400)
#             creds = valid_res["creds"]
            
#             try:
#                 new_data = {
#                     "prodname": data['prodname'],
#                     "desc": data['desc'],
#                     "price": data['price']
#                 }
#                 nd = Product.objects.get(productid=creds['productid'])
#                 for k,v in new_data.items():
#                     setattr(nd, k, v)
#                     nd.save()
#                 return Response({
#                     "message": "Product updated successfully",
#                     "details": f"{creds['productid']} has been updated"
#                 })

#             except Exception as e:
#                 return Response({
#                     "message":"Product update failed",
#                     "details": [{
#                         "raw_error": str(e),
#                     }]
#                 }, status=400)
            
class UpdateProduct2(APIView):
    def post(self, request):
        keys = ["prodname", "desc","price"]
        vlk = validate_credentials(request, keys)
        if vlk['creds'] is None:
            res = {
                "message": vlk['missing_fields']
            }
            return Response(res, status=400)
        data = vlk["creds"]

        try:
            prod  = Product.objects.get(productid=data["productid"])
            for k,v in data.items():
                setattr(prod, k, v)
            prod.save()
            return Response({
                "message": "Product edited successfully",
                "details": f"{data['productid']} has been updated"
            })
        except Exception as e:
            return Response({
                "message": "something went wrong",
                "details": str(e)
            }, status=400)
class DeleteProduct(APIView):
    def delete(self, request):
        keys = ['productid']
        results = []
        deleted = []
        valid_res = validate_credentials(request, keys)
        if valid_res['creds'] is None:
            res = {
                "missing": valid_res['missing_fields']
            }
            return Response(res, status=400)
        creds = valid_res["creds"]  

        try:
            # for v in creds['productid']:
            for v in creds.get('productid', []):
                prod = Product.objects.get(productid__exact=v)
                prod.delete()
                deleted.append(v)
            res = {
                "status": 200,
                "details": f"{prod.prodname} has been removed"
            }
            results.append(res)
        except Exception as e:
            res = {
                "status": 400,
                "details": str(e)
            }
            results.append(res)

        if all(r['status']!=200 for r in results):
            return Response(results, status=400)
        # results['deleted'] = deleted
        return Response(results, status=200)                

class UpdateStatus(APIView):
    def post(self,request):
        keys = ['productid','statusid']
        valid_res = validate_credentials(request, keys)
        if valid_res['creds'] is None:
            res = {
                "missing": valid_res['missing_fields']
            }
            return Response(res, status=400)
        data = valid_res["creds"]

        try:
            stat = Status.objects.get(statusid=data['statusid'])
            prodid = Product.objects.get(productid=data['productid'])
            prodid.statusid = stat.statusid
            prodid.save()
            return Response({"message": "status updated successfully"})
        except Product.DoesNotExist:
            return Response({"message": "Product not found"}, status=404)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=500)
        
class TransactionViews(APIView):
    def post(self, request):
        keys = ["productid","lastprice","statusid"]
        vld = validate_credentials(request, keys)
        if vld['creds'] is None:
            res = {
                "missing": vld['msissing_fields']
            }
            return Response(res, status=400)
        data = vld["creds"]

        bidamount = Decimal(data['lastprice'])
        product = Product.objects.get(productid=data['productid'])

        try:
            if bidamount > product.price:
                transact = Transaction(productid=product, lastprice=bidamount)
                # transact.lastprice = bidamount
                transact.save()

                product.price = bidamount
                product.save()

                return Response({"product details": {
                    "productid": product.productid,
                    "name": product.prodname,
                    "price": product.price
                }})
            else:
                return Response({"message":"bid must be higher than current price"})
        except Exception as e:
            return Response({
                "message": "something went wrong",
                "details": str(e)
            }, status=400)
        
class GetTransaction(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer