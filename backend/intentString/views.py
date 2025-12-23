from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import NaturalIntentSerializer, NetworkIntentSerializer, IntentInferenceSerializer
from .models import NaturalIntent, NetworkIntent
from .services.intentToPolicy import map_intent_struct_to_policy, generate_yaml
import requests
import json
import yaml

# Create your views here.

# Natural Intent
class NaturalIntentViewSet(viewsets.ModelViewSet):
    queryset = NaturalIntent.objects.all()
    serializer_class = NaturalIntentSerializer
    serializer_inference = IntentInferenceSerializer

    # POST 요청 커스터마이징
    def create(self, request, *args, **kwargs):
        # 1) 기존 DRF 저장 로직 (프론트에서 온 데이터 DB에 저장)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        intent_obj = serializer.save()  # DB 저장
        print(intent_obj.id)

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
        except Exception as e:
            external_response = f"Failed to send: {e}"

        # 4) 추론 결과 저장
        inference_obj = {
            # Intent
            "intent_action" : external_response["Intent"]["Action"],
            "intent_expectation_object" : external_response["Intent"]["ExpectationObject"],
            "intent_expectation_target" : external_response["Intent"]["ExpectationTarget"],
            # KGTriple
            "kg_head" : external_response["KGTriple"]["head"],
            "kg_relation" : external_response["KGTriple"]["relation"],
            "kg_tail" : external_response["KGTriple"]["tail"],
            # For extension
            "confidence" : external_response.get("confidence", 1.0),
            "degraded" : external_response.get("degraded", False),
            "degradation_note" : external_response.get("degradation_note", ""),

            "timestamp" : payload["timestamp"],

            "natural_intent" : intent_obj.id,
        }
        inferSerializer = self.serializer_inference(data=inference_obj)
        inferSerializer.is_valid(raise_exception=True)
        infer_obj = inferSerializer.save()  # DB 저장
            
        # 5) intent -> policy 변환
        intent = external_response.get("Intent")
        triple = external_response.get("KGTriple")
        confidence = external_response.get("confidence", 1.0)
        policy = map_intent_struct_to_policy(intent, triple, confidence)
        yaml_result = generate_yaml(policy) # yaml 생성

        print("\n===== [DEBUG] inferenct to policy =====")
        print(yaml_result)
        print("=======================================================\n")

        # 추가 예정 ============================================================================
        # try:    
        #     response = requests.post("edge server", json=yaml_result, timeout=5)
        #     edge_response = json.loads(response.text) # 보기 편하게 json 형태로 파싱
        # except Exception as e:
        #     external_response = f"Failed to send: {e}"
        # 추가 예정 ============================================================================

        # 6) Django 클라이언트에게 반환할 내용
        return Response({
            "saved": serializer.data,        # 백엔드에 저장된 내용
            "sent_to": external_url,         # 보낸 주소
            "external_payload": payload,     # 실제 전송한 데이터
            "external_response": external_response,  # 외부 서버 응답
            "yaml": yaml_result,                     # policy 전환
        }, status=status.HTTP_201_CREATED)

# Network Intent
class NetworkIntentViewSet(viewsets.ModelViewSet):
    queryset = NetworkIntent.objects.all()
    serializer_class = NetworkIntentSerializer
    serializer_inference = IntentInferenceSerializer

    # POST 요청 커스터마이징
    def create(self, request, *args, **kwargs):
        # 1) 기존 DRF 저장 로직 (프론트에서 온 데이터 DB에 저장)
        data = request.data.get('intent')
        print(data)
        obj = {
            "user" : request.data.get('user'),
            "intent" : {
                "name" : data['name'],
                "mac_address" : data['mac-address'],
                "ipv4_start" : data['range-ipv4-address']['start'],
                "ipv4_end" : data['range-ipv4-address']['end'],
                "ipv6_start" : data['range-ipv6-address']['start'],
                "ipv6_end" : data['range-ipv6-address']['end'],
            },
            "timestamp" : request.data.get('timestamp')
        } # 수동 파싱
        serializer = self.get_serializer(data=obj['intent'])
        serializer.is_valid(raise_exception=True)
        network_obj = serializer.save()  # DB 저장

        # 2) 외부 서버로 보낼 데이터 → "intent" label로 wrap해서 전송
        payload = obj
        external_url = "http://115.145.179.159:5050/infer"
        print("\n===== [DEBUG] Sending payload to external server =====")
        print(f"URL: {external_url}")
        print(f"Payload: {payload}")
        print("=======================================================\n")

        # 3) 외부 서버로 전송
        try:
            response = requests.post(external_url, json=payload, timeout=5)
            external_response = json.loads(response.text) # 보기 편하게 json 형태로 파싱
        except Exception as e:
            external_response = f"Failed to send: {e}"
            
        # 4) 추론 결과 저장
        inference_obj = {
            # Intent
            "intent_action" : external_response["Intent"]["Action"],
            "intent_expectation_object" : external_response["Intent"]["ExpectationObject"],
            "intent_expectation_target" : external_response["Intent"]["ExpectationTarget"],
            # KGTriple
            "kg_head" : external_response["KGTriple"]["head"],
            "kg_relation" : external_response["KGTriple"]["relation"],
            "kg_tail" : external_response["KGTriple"]["tail"],
            # For extension
            "confidence" : external_response.get("confidence", 1.0),
            "degraded" : external_response.get("degraded", False),
            "degradation_note" : external_response.get("degradation_note", ""),

            "timestamp" : payload["timestamp"],

            "network_intent" : network_obj.id,
        }
        inferSerializer = self.serializer_inference(data=inference_obj)
        inferSerializer.is_valid(raise_exception=True)
        infer_obj = inferSerializer.save()  # DB 저장

        # 5) intent -> policy 변환
        intent = external_response.get("Intent")
        triple = external_response.get("KGTriple")
        confidence = external_response.get("confidence", 1.0)
        policy = map_intent_struct_to_policy(intent, triple, confidence)
        yaml_result = generate_yaml(policy) # yaml 생성

        print("\n===== [DEBUG] inferenct to policy =====")
        print(yaml_result)
        print("=======================================================\n")
        
        # 6) Django 클라이언트에게 반환할 내용
        return Response({
            "saved": serializer.data,        # 백엔드에 저장된 내용
            "sent_to": external_url,         # 보낸 주소
            "external_payload": payload,     # 실제 전송한 데이터
            "external_response": external_response,  # 외부 서버 응답
            "yaml": yaml_result,                     # policy 전환
        }, status=status.HTTP_201_CREATED)
