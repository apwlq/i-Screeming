import socket
import cv2
import numpy as np
import struct

# 클라이언트 설정
UDP_IP = '서버_IP'  # 서버의 실제 IP 주소를 입력
UDP_PORT = 12345
MAX_UDP_SIZE = 65507

# 소켓 설정
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

latest_timestamp = 0
buffer = b''

while True:
    # 데이터 수신
    data, _ = sock.recvfrom(MAX_UDP_SIZE)
    buffer += data
    
    # 데이터가 충분히 수신되었는지 확인
    if len(buffer) >= 8:  # 타임스탬프는 8바이트
        # 타임스탬프와 이미지 데이터 분리
        timestamp_data = buffer[:8]
        image_data = buffer[8:]
        
        # 타임스탬프 디코딩
        timestamp = struct.unpack('d', timestamp_data)[0]
        
        if timestamp > latest_timestamp:
            latest_timestamp = timestamp

            # 이미지 디코딩
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is not None:
                # 이미지 표시
                cv2.imshow('Received Screen', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        # 버퍼 초기화 (추가적인 데이터 패킷을 기다리기 위해)
        buffer = b''

# 소켓 종료
sock.close()
cv2.destroyAllWindows()
