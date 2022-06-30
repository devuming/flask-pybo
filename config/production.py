# 서버 환경에서 사용하는 환경변수
from config.default import *
from logging.config import dictConfig   # 로그를 파일로 저장하기 위함

dictConfig({            # 로그 설정
    'version':1,        # 고정값 1 사용
    'formatters':{      # 로그 출력 형식 지정
        'default':{
            'format':'[%(asctime)s] %(levelname)s in %(module)s: %(message)s',  # [현재시간] 로그레벨 in 로그 호출한 모듈명: 로그 내용
        }
    },
    'handlers':{        # 로그 출력 방식 지정
        'file':{        # file 핸들러 사용
            'level':'INFO',                                             # 출력 레벨 지정 : INFO
            'class':'logging.handlers.RotatingFileHandler',             # RotatingFileHandler 사용 : 파일 크기가 설정 값보다 커지면 파일 뒤 인덱스 붙여 백업, 파일 개수 일정하게 유지 > 디스크 꽉 차는 위험 방지
            'filename':os.path.join(BASE_DIR, 'logs/myproject.log'),    # 로그 파일명
            'maxBytes':1024 * 1024 * 5,                                 # 로그 최대 크기 : 5MB
            'backupCount':5,                                            # 로그 파일 5개로 유지
            'formatter':'default',
        },
    },
    'root':{        # 최상위 로거
        'level':'INFO',         # 로그 레벨 INFO로 지정
        'handlers':['file']     # 로그 핸들러 지정
    }
})
# 로그 레벨 : DEBUG < INFO < WARNING < ERROR < CRITICAL

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False     # 이벤트 처리 옵션

SECRET_KEY = b'qI\xc8B\xb0\x9f\xb1&\x16\t~\xca\xdc^$\xd6'      # 웹취약점 공격 방지 : 데이터 전달 시 도메인이 같은지 체크