from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authentication import SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from user.authentication import CustomJWTAuthentication, CustomTokenAuthentication
from .models import Branch
from .serializer import BranchSerializer
from config.utils import success_response, error_response

class BranchView(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        CustomTokenAuthentication,
        CustomJWTAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            branches = Branch.objects.all()
            serializer = BranchSerializer(branches, many=True)

            return success_response(
                "Data Fetch Successfully",
                serializer.data
            )

        except Exception as e:
            return error_response(
                "Something went wrong",
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            serializer = BranchSerializer(data=request.data)

            if serializer.is_valid():
                branch = serializer.save()

                return success_response(
                    "Branch Created Successfully",
                    BranchSerializer(branch).data,
                    status_code=status.HTTP_201_CREATED
                )

            return error_response(
                "Validation Error",
                serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return error_response(
                "Something went wrong",
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BranchDetailView(APIView):
    authentication_classes = [
        SessionAuthentication,
        BasicAuthentication,
        CustomJWTAuthentication,
    ]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            branch = get_object_or_404(Branch, id=id)

            serializer = BranchSerializer(branch)

            return success_response(
                "Data Fetch Successfully",
                serializer.data
            )

        except Exception as e:
            return error_response(
                "Something went wrong",
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def patch(self, request, id):
        try:
            branch = get_object_or_404(Branch, id=id)

            serializer = BranchSerializer(
                branch,
                data=request.data,
                partial=True
            )

            if serializer.is_valid():
                branch = serializer.save()

                return success_response(
                    "Branch Updated Successfully",
                    BranchSerializer(branch).data
                )

            return error_response(
                "Validation Error",
                serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return error_response(
                "Something went wrong",
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    # DELETE /api/branches/1/
    def delete(self, request, id):
        try:
            branch = get_object_or_404(Branch, id=id)

            branch.delete()

            return success_response(
                "Branch deleted successfully",
                None,
                status_code=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            return error_response(
                "Something went wrong",
                str(e),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )