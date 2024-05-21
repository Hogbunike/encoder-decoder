from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import EncodeDecodeSerializer
import base64

# Create your views here.

def encode_payload(payload: str, salt_key: str, salt_index: int) -> str:
    base64_bytes = base64.b64encode(payload.encode('utf-8'))
    base64_str = base64_bytes.decode('utf-8')
    if salt_index > len(base64_str):
        raise ValueError("Salt index is out of range")
    salted_base64_str = base64_str[:salt_index] + salt_key + base64_str[salt_index:]
    return salted_base64_str

def decode_payload(salted_base64_str: str, salt_key: str, salt_index: int) -> str:
    if salted_base64_str[salt_index:salt_index+len(salt_key)] != salt_key:
        raise ValueError("Invalid salt key or index")
    base64_str = salted_base64_str[:salt_index] + salted_base64_str[salt_index+len(salt_key):]
    base64_bytes = base64_str.encode('utf-8')
    payload_bytes = base64.b64decode(base64_bytes)
    payload = payload_bytes.decode('utf-8')
    return payload

@api_view(['POST'])
def encode_view(request):
    serializer = EncodeDecodeSerializer(data=request.data)
    if serializer.is_valid():
        payload = serializer.validated_data['payload']
        salt_key = serializer.validated_data['salt_key']
        salt_index = serializer.validated_data['salt_index']
        
        try:
            encoded_payload = encode_payload(payload, salt_key, salt_index)
            return Response({'encoded_payload': encoded_payload})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def decode_view(request):
    serializer = EncodeDecodeSerializer(data=request.data)
    if serializer.is_valid():
        encoded_payload = serializer.validated_data['encoded_payload']
        salt_key = serializer.validated_data['salt_key']
        salt_index = serializer.validated_data['salt_index']

        try:
            decoded_payload = decode_payload(encoded_payload, salt_key, salt_index)
            return Response({'decoded_payload': decoded_payload})
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



