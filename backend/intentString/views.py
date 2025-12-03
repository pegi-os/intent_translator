from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import NaturalIntentSerializer, NetworkIntentSerializer
from .models import NaturalIntent, NetworkIntent
from .services.intentToPolicy import map_intent_struct_to_policy, generate_yaml
from .models import PolicyIntent
from .serializers import PolicyIntentSerializer
import requests
import json
import yaml

# Create your views here.
def test(request):
      return HttpResponse("Test")

class NaturalIntentViewSet(viewsets.ModelViewSet):
    queryset = NaturalIntent.objects.all()
    serializer_class = NaturalIntentSerializer

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
            external_response = json.loads(response.text) # 보기 편하게 json 형태로 파싱
            
            # intent -> policy
            intent = external_response.get("Intent")
            triple = external_response.get("KGTriple")
            confidence = external_response.get("confidence", 1.0)
    
            policy = map_intent_struct_to_policy(intent, triple, confidence)
            yaml_result = generate_yaml(policy) # yaml 생성

            PolicyIntent.objects.create(
        action=intent.get("Action", ""),
        expectation_object=intent.get("ExpectationObject", ""),
        expectation_target=intent.get("ExpectationTarget", ""),
        head=triple.get("head", ""),
        relation=triple.get("relation", ""),
        tail=triple.get("tail", ""),
    )

            
        except Exception as e:
            external_response = f"Failed to send: {e}"

# # YAML 결과를 전송
#         try: #192.168.50.57   ,  18.129
#             next_url = "http://192.168.50.57"   # 원하는 URL
#             send_payload = {"yaml": yaml_result}

#             print(f"URL: {next_url}")
#             print(f"Payload: {send_payload}")
#             print("=======================================================\n")

#             forward_res = requests.post(next_url, json=send_payload, timeout=5)
#             forward_response = forward_res.text
#         except Exception as e:
#             forward_response = f"Failed to forward YAML: {e}"        


        # 4) Django 클라이언트에게 반환할 내용
        return Response({
            "saved": serializer.data,        # 백엔드에 저장된 내용
            "sent_to": external_url,         # 보낸 주소
            "external_payload": payload,     # 실제 전송한 데이터
            "external_response": external_response,  # 외부 서버 응답
            "yaml": yaml_result,                     # policy 전환
        }, status=status.HTTP_201_CREATED)
    
class NetworkIntentViewSet(viewsets.ModelViewSet):
    queryset = NetworkIntent.objects.all()
    serializer_class = NetworkIntentSerializer

    # POST 요청 커스터마이징
    def create(self, request, *args, **kwargs):
        # 1) 기존 DRF 저장 로직 (프론트에서 온 데이터 DB에 저장)
        data = request.data.get('intent')
        obj = {
            "name" : data['name'],
            "mac_address" : data['mac-address'],
            "ipv4_start" : data['range-ipv4-address']['start'],
            "ipv4_end" : data['range-ipv4-address']['end'],
            "ipv6_start" : data['range-ipv6-address']['start'],
            "ipv6_end" : data['range-ipv6-address']['end'],
        } # 수동 파싱
        serializer = self.get_serializer(data=obj)
        serializer.is_valid(raise_exception=True)
        intent_obj = serializer.save()  # DB 저장

        # 2) 외부 서버로 보낼 데이터
        #    → "intent" label로 wrap해서 전송
        payload = {"intent": serializer.data}
        external_url = "http://115.145.179.159:5050/infer"
        print("\n===== [DEBUG] Sending payload to external server =====")
        print(f"URL: {external_url}")
        print(f"Payload: {payload}")
        print("=======================================================\n")

        # 3) 외부 서버로 전송
        try:
            response = requests.post(external_url, json=payload, timeout=5)
            # external_response = response.text
            external_response = json.loads(response.text) # 보기 편하게 json 형태로 파싱
        except Exception as e:
            external_response = f"Failed to send: {e}"


        # 4) Django 클라이언트에게 반환할 내용
        return Response({
            "saved": serializer.data,        # 백엔드에 저장된 내용
            "sent_to": external_url,         # 보낸 주소
            "external_payload": payload,     # 실제 전송한 데이터
            "external_response": external_response,  # 외부 서버 응답
        }, status=status.HTTP_201_CREATED)