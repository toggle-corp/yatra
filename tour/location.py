import json
import requests
import urllib.parse

from tour.models import Destination


# def create_destination(address):
#     url = "https://maps.googleapis.com/maps/api/geocode/json?" + \
#         urllib.parse.urlencode({"address": address})
#
#     response = requests.get(url=url)
#     data = json.loads(response.text)
#
#     if len(data["results"]) == 0:
#         return None
#
#     for result in data["results"]:
#         add = result["address_components"]


# def get_dest_diff(d1, d2):
#     url = "https://maps.googleapis.com/maps/api/geocode/json?" + \
#         urllib.parse.urlencode({"address": d1})
#
#     response = requests.get(url=url)
#     data1 = json.loads(response.text)
#
#     if len(data1["results"]) == 0:
#         return 5
#
#     url = "https://maps.googleapis.com/maps/api/geocode/json?" + \
#         urllib.parse.urlencode({"address": d2})
#
#     response = requests.get(url=url)
#     data2 = json.loads(response.text)
#
#     if len(data2["results"]) == 0:
#         return 5
#
#     # Check if any address is same.
#
#     # There can be multiple results for same address, in which case
#     # we want the minimum distance.
#
#     result = 5
#
#     for result1 in data1["results"]:
#         for result2 in data2["results"]:
#
#             dist = 5
#
#             # Check if any admin level is same.
#             add1 = result1["address_components"]
#             add2 = result2["address_components"]
#
#             break_loop = False
#             for i, a1 in enumerate(add1):
#                 for j, a2 in enumerate(add2):
#                     if a1["short_name"] == a2["short_name"]:
#                         dist = (i/len(add1) + j/len(add2)) * 4
#                         break_loop = True
#                         break
#                 if break_loop:
#                     break
#
#             result = min(result, dist)
#
#     return result
