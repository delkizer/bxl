import socket
from decimal import Decimal

class Utils:
    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def daynight(x) :
        r0:str = ""

        if x <= 1500 :
            r0 = '주간'
        else :
            r0 = '야간'

        return r0

    @staticmethod
    def homegame(x,y) :
        if x!=y :
            z = '원정'
        else :
            z ='홈'

        return z

    @staticmethod
    def whowins(x, y):
        if x > y:
            z = '원정'
        elif x < y:
            z = '홈'
        else:
            z = '무'

        return z

    @staticmethod
    def drawgame(x):
        if x == '무':
            y = 1
        else:
            y = 0

        return y

    @staticmethod
    def result_define(ha, a, h):
        if ha == '원정':
            if a > h:
                res = '승'
            elif a < h:
                res = '패'
            else:
                res = '무'
        else:
            if a < h:
                res = '승'
            elif a > h:
                res = '패'
            else:
                res = '무'
        return res

    @staticmethod
    def ball_type(ball_type_eng:str) :
        if ball_type_eng == 'Cutter' :
            return_msg = '커터'
        elif ball_type_eng == 'Sinker' :
            return_msg = '싱커'
        elif ball_type_eng == 'Fastball' :
            return_msg = '패스트볼'
        elif ball_type_eng == 'Curveball' :
            return_msg = '커브'
        elif ball_type_eng == 'Slider' :
            return_msg = '슬라이더'
        elif ball_type_eng == 'Splitter' :
            return_msg = '스플리터'
        elif ball_type_eng =='ChangeUp' :
            return_msg = '체인지업'
        elif ball_type_eng =='Sweeper' :
            return_msg = '스위퍼'
        else :
            return_msg = '미분류'

        return return_msg

    @staticmethod
    def game_type(game_type):
        if game_type == 'S':
            return "시범경기"

        if game_type == 'R':
            return "정규시즌"

        if game_type == 'W':
            return "와일드카드"

        if game_type == 'PT':
            return "플레이오프"

        if game_type == 'K':
            return "한국시리즈"

        if game_type == 'RD':
            return "순위결정전"

        if game_type == 'M':
            return "준플레이오프"

    @staticmethod
    def inn_conv(x):
        x = x.lower()

        if x == 'bot':
            y = '말'
        else:
            y = '초'
        return y

    @staticmethod
    def runner_conv(base_status:str) :
        if base_status =='000':
            return '주자 없음'

        if base_status == '100' :
            return '주자 1루'

        if base_status == '020' :
            return '주자 2루'

        if base_status == '003' :
            return '주자 3루'

        if base_status == '120' :
            return '주자 1,2루'

        if base_status == '023' :
            return '주자 2,3루'

        if base_status == '103' :
            return '주자 1,3루'

        if base_status == '123' :
            return '주자 만루'

        return '모르겠음'

    @staticmethod
    def convert_decimal(data):
        if isinstance(data, list):
            return [Utils.convert_decimal(item) for item in data]
        elif isinstance(data, dict):
            return {key: Utils.convert_decimal(value) for key, value in data.items()}
        elif isinstance(data, Decimal):
            return float(data)  # 또는 int(data)
        else:
            return data

    @staticmethod
    def get_hostname():
        """호스트 이름(서버 hostname)을 반환"""
        return socket.gethostname()
