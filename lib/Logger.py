# LogSystem
import logging
import logging.handlers
import os

# LogReceiverSocketServer
import socket
from datetime import datetime
import threading
import struct
import pickle

import config as cfg
"""
# class LogSystem
# info : Logger 설정
# - function(fileLogger) : 파일 로거 설정
# - function(socketLogger) : 소켓 로거 설정
"""


class LogSystem:
    """
    # function(socketLogger)
    # info : 소켓 로거 설정
    # return : 로거 인스턴스 반환
    """

    def socketLogger(self, loggerServerIP, loggerServerPort):
        logger = logging.getLogger('root')
        try:
            # loggingPort = 9020
            socketHandler = logging.handlers.SocketHandler(
                loggerServerIP, loggerServerPort)

            logger.addHandler(socketHandler)
            logger.setLevel(logging.DEBUG)
        except Exception as ex:
            print(f"[socketLogger] ErrorMsg : {ex}")
        finally:
            del loggerServerIP, loggerServerPort, socketHandler
            return logger

    """
    # function(loggerFile)
    # info : 파일 로거 설정

    # return : 로거 인스턴스 반환
    """

    def fileLogger(self, logDir, logName):
        try:
            # logger 생성 및 지정
            # logger = logging.getLogger('root') # 단일 프로세스용
            logger = logging.getLogger(logName)  # 멀티 프로세스용

            # 로그 저장경로
            logPath = logDir
            # 로그 저장 디렉토리 없으면 디렉토리 생성
            if not os.path.exists(logPath):
                os.makedirs(logPath)

            # 로그파일 저장경로
            filename = logPath + "/" + logName

            # 로그 출력 형식 지정([로거이름 - 로그작성시간] | [로그레벨] [쓰레드이름] : 로그메세지)
            # 지정된 로그변수는 %()로 호출하며 s는 문자형 데이터로 지정하며 s앞에 숫자는 출력 자리수 지정
            formatter = logging.Formatter(
                f'[{logName} - %(asctime)s] | [%(levelname)-8s] [%(threadName)-15s] : %(message)s')

            # when 에서 지정한 주기로 로그파일 작성
            fileHandler = logging.handlers.TimedRotatingFileHandler(
                filename=filename,  # 로그파일 이름지정
                when='midnight',  # 자정기준
                interval=1,  # 1번씩
                encoding='utf-8',  # 로그 인코딩형식
                backupCount=0)  # 로그파일 백업제한 없음

            # 로그파일 백업시 접미사에 지정한 문자 추가(연도-월-일.log)
            fileHandler.suffix = "%Y-%m-%d.log"

            # 지정한 포맷을 handler 에 추가
            fileHandler.setFormatter(formatter)

            # 지정한 handler 를 logger 에 추가
            logger.addHandler(fileHandler)
            # logger 로그레벨 설정 (지정된 로그레벨보다 같거나 큰로그만 작성함)
            # 로그 레벨 : CRITICAL(50), ERROR(40), WARNING(30), INFO(20), DEBUG(10), NOTSET(0)
            logger.setLevel(logging.DEBUG)

        except Exception as ex:
            print(f"[fileLogger] ErrorMsg : {ex}")
        finally:
            try:
                del logDir, logName, logPath, filename, formatter, fileHandler
            except UnboundLocalError:
                pass
            finally:
                return logger


"""
# class LogReceiverSocketServer
# info : 동기식 SocketServer
# - function(run) : 동기식 소켓 통신을 위한 Listen 및 Accept 실행
# - function(ListenStart) : 소켓 통신을 위한 bind 및 listen 실행
# - function(ServerAccept) : 클라이언트 접속 받기위한 Accept 무한루프 실행(다중 클라이언트 접속허용)
# - function(ReadPacket) : 클라이언트로부터 데이터 수신후 LogFile 저장
"""


class LogReceiverSocketServer:
    """
    # function(__init__)
    # info : 클래스 생성시 변수 초기화
    # - self.serverSocket : socket (All IP, serverPort)
    # - self.serverPortInt : int
    # - self.logSystem : LogSystem()
    # - self.logger : Logger
    """

    def __init__(self):
        # 동기식 서버 소켓 초기화
        self.serverSocket = None
        self.loggerServerIP = cfg.loggerServerIP
        self.loggerServerPort = cfg.loggerServerPort
        self.logSystem = LogSystem()
        self.logger = self.logSystem.fileLogger(cfg.logDir, cfg.logName)

    """
    # function(run)
    # info : 동기식 소켓 통신을 위한 Listen 및 Accept 실행
    # - serverPortInt : int 
    """

    def run(self):
        self.listenStart()
        self.serverAccept()

    """
    # function(ListenStart)
    # info : 소켓 통신을 위한 bind 및 listen 실행
    # - serverPortInt : int
    # - serverSocket : socket (All IP, serverPort)
    """

    def listenStart(self):
        try:
            # 주소 체계(address family)로 IPv4, 소켓 타입으로 TCP 사용
            self.serverSocket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
            # 포트 사용중이라 연결할 수 없다는 WinError 10048 에러 해결를 위해 필요
            # SO_REUSEADDR 옵션을 적용하면 bind() 단계에서 커널이 가져간 소켓소유권을 다시 돌려받으며 즉시 재시작 가능
            self.serverSocket.setsockopt(
                socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # bind 함수는 소켓을 특정 네트워크 인터페이스와 포트 번호에 연결하는데 사용
            self.serverSocket.bind(
                (self.loggerServerIP, self.loggerServerPort))
            # server 설정이 완료되면 listen 시작
            self.serverSocket.listen()
            print(
                f"{datetime.now()} - [SocketListener listenStart(Port:{self.loggerServerPort})] Start")
            self.logger.info(
                f"[SocketListener listenStart(Port:{self.loggerServerPort})] Start")
        except Exception as ex:
            self.logger.error(f"[SocketListener listenStart] ErrorMsg : {ex}")

    """
    # function(ServerAccept)
    # info : 클라이언트 접속 받기위한 Accept 무한루프 실행(다중 클라이언트 접속허용)
    # - serverPortInt : int
    # - clientSocket : socket
    # - _ : IP 및 Port (사용하지 않음)
    # - serverAcceptThread : thread
    """

    def serverAccept(self):
        try:
            # 서버는 여러 클라이언트가 접속하기 때문에 무한루프 사용
            while True:
                # client 접속이 발생하면 accept 발생
                # accept 함수에서 대기하다가 클라이언트가 접속하면 새로운 소켓 리턴
                clientSocket, _ = self.serverSocket.accept()

                serverAcceptThread = threading.Thread(
                    target=self.readPacket, args=(clientSocket,))
                serverAcceptThread.start()

                del clientSocket

        except Exception as ex:
            self.logger.error(f"[SocketListener serverAccept] ErrorMsg : {ex}")

        finally:
            # 에러로 인해 서버소켓 중지시 재시작
            self.run()

    """
    # function(ReadPacket)
    # info : 클라이언트로부터 데이터 수신후 데이터 전달
    # - tcpClientSocket : socket (클라이언트 정보)
    """

    def readPacket(self, tcpClientSocket):
        try:
            # 소켓 통신후 계속 데이터 수신
            while True:
                # 패킷길이 수신
                chunk = tcpClientSocket.recv(4)
                if len(chunk) < 4:
                    break
                # struct.unpack '>L' 빅엔디안 형식의 Long 자료형 정렬
                # Long 포맷의 경우 4바이트 크기
                # [0] 사용이유 (567,) 에서 값 얻어오기 위함
                slen = struct.unpack('>L', chunk)[0]
                # 패킷길이값을 제외한 나머지 패킷수신
                chunk = tcpClientSocket.recv(slen)
                while len(chunk) < slen:
                    chunk = chunk + tcpClientSocket.recv(slen - len(chunk))
                # 바이트객체 역직렬화
                obj = pickle.loads(chunk)
                record = logging.makeLogRecord(obj)
                # 로그 작성
                self.logger.handle(record)

        except Exception as ex:
            self.logger.error(f"[SocketListener readPacket] ErrorMsg : {ex}")
        finally:
            tcpClientSocket.close()
            del tcpClientSocket, chunk, slen, obj, record
