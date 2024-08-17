import socket
import cv2
import numpy as np
import struct

# 클라이언트 설정
UDP_IP = '0.0.0.0'  # 서버의 IP 주소 입력
UDP_PORT = 12345

# 소켓 설정
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

latest_timestamp = 0

while True:
    # 데이터 수신
    data, _ = sock.recvfrom(65535)  # 최대 수신 버퍼 크기

    # 타임스탬프와 이미지 데이터 분리
    timestamp_data = data[:8]  # double형은 8바이트
    image_data = data[8:]

    # 타임스탬프 디코딩
    timestamp = struct.unpack('d', timestamp_data)[0]

    # 최신 타임스탬프만 처리
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

# 소켓 종료
sock.close()
cv2.destroyAllWindows()
