import logging
import sys
import datetime

class Log():
    def __init__(self, scriptName, logLocation):
        logger = logging.getLogger(scriptName)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

        fh = logging.FileHandler(logLocation)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)

        stdout = logging.StreamHandler(sys.stdout)
        stdout.setLevel(logging.INFO)
        stdout.setFormatter(formatter)
       
        if not logger.hasHandlers():
                logger.addHandler(fh)
                logger.addHandler(stdout)
               
        self.logger = logger
        self.buffer = []
        self.stdout = stdout

    def writeBuffer(self, type, msg):
        t = datetime.datetime.now().strftime('%s')
        self.buffer.append('{} {} : {}'.format(t, type, msg))

    def error(self, msg):
        self.writeBuffer('ERROR', msg)
        self.logger.error(msg)

    def info(self, msg):
        self.logger.info(msg)

    def debug(self, msg):
        self.logger.debug(msg)

    def warn(self, msg):
        self.logger.warn(msg)

    def email(self, msg):
        self.writeBuffer('INFO', msg)
        self.logger.info(msg)

    def critical(self, msg):
        self.writeBuffer('CRITICAL', msg)
        self.logger.error(msg)
        sys.exit()