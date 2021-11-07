import logging
import logging.handlers
import datetime # TODO: MongoHandler에 사용됨, 불필요하게 되면 삭제


class CsvLog():
    def __init__(self, path='', format=None, name='csvlog'):
        """SlackLog 초기화

        Args:
            path (str, optional): csv 저장 경로path
            format (str, optional): 
            name (str, optional): log 이름
        """
        # format = {
        #    'fmt': '%(name)s,%(asctime)s,%(created)f,%(module)s,%(process)d,%(thread)d,%(message)s',
        #    'datefmt': '%H:%M:%S'  
        # }

        format = {
           'fmt': '%(name)s,%(asctime)s,%(message)s',
           'datefmt': '%Y-%m-%d %H:%M:%S'  
        } if format == None else format

        formatter = logging.Formatter(
            **format
        )

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler(path, encoding="UTF-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        self.logger = logger


def log_csv(msg, level='info', path='test.csv', format=None, name='csvlog'):
    """csv으로 log 메시지를 보냄

    Args:
        msg (str): 메시지
        name (str, optional): log 이름
        path (str, optional): csv 저장 경로path
    """

    csvlog = CsvLog(path=path, format=format, name=name)
    if level == 'debug':
        csvlog.logger.debug(msg)
    elif level == 'info':
        csvlog.logger.info(msg)
    elif level == 'warning':
        csvlog.logger.warning(msg)
    elif level == 'error':
        csvlog.logger.error(msg)
    elif level == 'critical':
        csvlog.logger.critical(msg)
    else:
        csvlog.logger.debug(msg)   


if __name__ == "__main__":
    # csvLog
    # opts = {
    #     "name": "csvlog",
    #     "path": "log.csv",
    # }
    csvlog = CsvLog("log.csv")
    msg = 'test logger csv'
    log_csv(msg, level='info', name='csvlog', path='test.csv')

    # csvlog.error("CSV LOG TEST")
