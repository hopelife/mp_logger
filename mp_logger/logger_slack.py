import logging
import logging.handlers
import datetime # TODO: MongoHandler에 사용됨, 불필요하게 되면 삭제


# - [조금 더 체계적인 Python Logging](https://hwangheek.github.io/2019/python-logging/)
# - [LogRecord 어트리뷰트](https://docs.python.org/ko/3/library/logging.html#logrecord-attributes)
# - [logging.handlers — 로깅 처리기](https://docs.python.org/ko/3/library/logging.handlers.html)
# - [logging — 파이썬 로깅](https://docs.python.org/ko/3/library/logging.html)
# - [Logging to MongoDB (로그 남기기)](http://blog.naver.com/PostView.nhn?blogId=wideeyed&logNo=222033147585)

# https://docs.python.org/ko/3/library/logging.html
# https://sematext.com/blog/logging-levels/
## https://www.webfx.com/tools/emoji-cheat-sheet/

## TODO: load log setting(yml), 

SLACK_TOKEN = 'xoxb-1601703181684-1806006278177-XfJxUZzDxsiWptynpJq1kEgs'


class SlackHandler(logging.handlers.HTTPHandler):
    def __init__(self, name, token, channel='#stock', format=None, emoji=True):
        """SlackHandler 초기화

        Args:
            name (str, optional): log 이름
            token (str, optional): slack token
            channel (str, optional): slack channel. Defaults to '#stock'.
            emoji (bool, optional): log에 emoji를 사용하는지 여부. Defaults to True.
        """
        super().__init__(host='slack.com', method='POST', url='/api/chat.postMessage', secure=True)
        self.token = token
        self.channel = channel
        self.emoji = emoji

        logger = logging.getLogger(name)

        self.logger = logger

        format = {
           'fmt': '%(name)s,%(asctime)s,%(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S'  
        } if format == None else format

        self.formatter = logging.Formatter(
            **format
        )


    # 수준	숫자 값
    # CRITICAL	50
    # ERROR	40
    # WARNING	30
    # INFO	20
    # DEBUG	10
    # NOTSET	0
    def mapLogRecord(self, record):
        """log record 매핑

        Args:
            record (obj): log record

        Returns:
            [dict]: {'token': '', 'channel': '', 'text': '', 'as_user': True}
        """
        if self.formatter is None:    # Formatter가 설정되지 않은 경우
            text = record.msg
        else:
            text = self.formatter.format(record)
        
        emoji = (
            '' if self.emoji == False else
            ':bug:' if record.levelname == 'DEBUG' else
            ':pencil2:' if record.levelname == 'INFO' else
            ':warning:' if record.levelname == 'WARNING' else
            ':fire:' if record.levelname == 'ERROR' else
            ':rotating_light:' if record.levelname == 'CRITICAL' else
            ':pushpin:'
        )

        return {
            'token': self.token,
            'channel': self.channel,
            'text': f'{emoji} {text}',
            'as_user': True,
        }


class SlackLog():
    def __init__(self, name, token, channel="#stock", format=None, emoji=True):
        """SlackLog 초기화

        Args:
            name (str, optional): log 이름
            token (str, optional): slack token
            channel (str, optional): slack channel. Defaults to '#stock'.
        """

        # formatter = logging.Formatter(
        #     fmt='%(asctime)s *%(module)s* : %(message)s',
        #     datefmt='%H:%M:%S',
        # )

        slack_handler = SlackHandler(name, token, channel=channel, format=format, emoji=emoji)
        slack_handler.setFormatter(slack_handler.formatter)
        slack_handler.logger.addHandler(slack_handler)

        # file_handler.setFormatter(formatter)
        # logger.addHandler(file_handler)

        self.logger = slack_handler.logger
        self.logger.setLevel(logging.DEBUG) # Note: logger level 설정


def log_slack(msg, level='info', name='slacklog', token=SLACK_TOKEN, channel='#stock', format=None, emoji=True):
    """slack으로 log 메시지를 보냄

    Args:
        msg (str): 메시지
        level (str): debug / info / warning / error
        name (str, optional): log 이름. Defaults to 'slacklog'.
        token (str, optional): slack token. Defaults to SLACK_TOKEN.
        channel (str, optional): slack channel. Defaults to '#stock'.
    """

    slacklog = SlackLog(name=name, token=token, channel=channel, format=format, emoji=emoji)

    if level == 'debug':
        slacklog.logger.debug(msg)
    elif level == 'info':
        slacklog.logger.info(msg)
    elif level == 'warning':
        slacklog.logger.warning(msg)
    elif level == 'error':
        slacklog.logger.error(msg)
    elif level == 'critical':
        slacklog.logger.critical(msg)
    else:
        slacklog.logger.debug(msg)              


if __name__ == "__main__":
    level = 'critical'
    msg = f'slack logger test({level})'
    log_slack(msg, level)

