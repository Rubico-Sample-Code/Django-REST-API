from rest_framework import status
from rest_framework.response import Response


# def api_response(data=None, message=None, status_code=status.HTTP_200_OK):
#     response_data = {}
#     if data is not None:
#         response_data["data"] = data

#     if message is not None:
#         response_data["message"] = message
#     return Response(response_data, status=status_code)


def api_response(data=[], message=None, status_code=status.HTTP_200_OK):
    response_data = {}
    if message is not None:
        response_data["message"] = message

    if data is not None and status_code < 400:
        response_data["data"] = data
    else:
        response_data["errors"] = data

    return Response(response_data, status=status_code)
