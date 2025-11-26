from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import requests

from .serializers import IntentStringSerializer
from .models import IntentString


def test(request):
    return HttpResponse("Test")


class IntentStringViewSet(viewsets.ModelViewSet):
    queryset = IntentString.objects.all()
    serializer_class = IntentStringSerializer

    # POST 요청 커스터마이징
    def create(self, request, *args, **kwargs):
        # 1) 기존 DRF 저장 로직 (프론트에서 온 데이터 DB에 저장)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        intent_obj = serializer.save()  # DB 저장

        # 2) 외부 서버로 보낼 데이터
        #    → 프론트에서 온 데이터 기반으로 직렬화된 값 그대로 사용
        payload = serializer.data
        external_url = "http://115.145.179.159:5050/infer"
        print("\n===== [DEBUG] Sending payload to external server =====")
        print(f"URL: {external_url}")
        print(f"Payload: {payload}")
        print("=======================================================\n")

        # 3) 외부 서버로 전송
        try:
            response = requests.post(external_url, json=payload, timeout=5)
            external_response = response.text
        except Exception as e:
            external_response = f"Failed to send: {e}"

        # 4) Django 클라이언트에게 반환할 내용
        return Response({
            "saved": serializer.data,        # 백엔드에 저장된 내용
            "sent_to": external_url,         # 보낸 주소
            "external_payload": payload,     # 실제 전송한 데이터
            "external_response": external_response,  # 외부 서버 응답
        }, status=status.HTTP_201_CREATED)
