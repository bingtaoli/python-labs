'''
Created on 2013-1-27

@author: Magic
'''
import logging.handlers
import traceback

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARN = logging.WARN
ERROR = logging.ERROR
FATAL = logging.CRITICAL


class LoggerError(Exception):
    pass


def get_logger(name):
    if logging.getLogger(name) is logging.root:
        raise LoggerError('logger name:%s have not been initialized'%name)
    return logging.getLogger(name)


class CutByDay:

    def __init__(self, days=1):
        self.__days = days

    def getHandler(self, **argv):
        return logging.handlers.TimedRotatingFileHandler(argv['fname'],when='midnight',
            interval=self.__days)


class CutBySize:
    def __init__(self, size=3*1024*1024, backup_count=10):
        self.__size = size
        self.__backup_count = backup_count

    def getHandler(self,**argv):
        return logging.handlers.RotatingFileHandler(argv['fname'], 'a', 
            self.__size, self.__backup_count, 'utf-8') 

        
class Logger(object):
    def __init__(self):
        pass
    
    def initialize(self, filename='default', priority=DEBUG, cutter=CutByDay(1),
                   backup_count=10, date_format="%Y-%m-%d %H:%M:%S", 
                   data_format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s'):
        try:
            self.__logger = logging.getLogger(filename)
            self.__logger.setLevel(int(priority))
            handler = cutter.getHandler(fname=filename)
            handler.setLevel(priority)
            formatter = logging.Formatter(
                data_format, date_format)
            handler.setFormatter(formatter)
            self.handler = handler
            self.__logger.addHandler(handler)
        except Exception, e:
            # if init failed, I just return thre false
            print str(e)
            return False
        # init the logger success
        return True

    def setLevel(self, level):
        self.__logger.setLevel(level)
        self.handler.setLevel(level)
        self.__logger.addHandler(self.handler)

    def logger(self):
        return self.__logger

    def close(self):
        self.__logger.close()

    def debug(self, msg, *args):
        logmsg = msg
        if not isinstance(logmsg, basestring):
            try:
                logmsg = str(msg)
            except UnicodeError:
                logmsg = msg
        if args:
            logmsg = logmsg % args
        try:
            self.__logger.debug(logmsg.decode('utf-8'))
        except Exception, e:
            self.__logger.error("!!!!!!ERROR IN WRITING LOG!!!!!!  %s"%str(e))

    
    def info(self, msg, *args):
        logmsg = msg
        if not isinstance(logmsg, basestring):
            try:
                logmsg = str(msg)
            except UnicodeError:
                logmsg = msg
        if args:
            logmsg = logmsg % args
        try:
            self.__logger.info(logmsg.decode('utf-8'))
        except Exception, e:
            self.__logger.error("!!!!!!ERROR IN WRITING LOG!!!!!!  %s"%str(e))
            
        
    def warn(self, msg, *args):
        logmsg = msg
        if not isinstance(logmsg, basestring):
            try:
                logmsg = str(msg)
            except UnicodeError:
                logmsg = msg
        if args:
            logmsg = logmsg % args
        try:
            self.__logger.warning(logmsg.decode('utf-8'))
        except Exception, e:
            self.__logger.error("!!!!!!ERROR IN WRITING LOG!!!!!!  %s"%str(e))
    
    def error(self, msg, *args):
        logmsg = msg
        if not isinstance(logmsg, basestring):
            try:
                logmsg = str(msg)
            except UnicodeError:
                logmsg = msg
        if args:
            logmsg = logmsg % args
        try:
            self.__logger.error(logmsg.decode('utf-8'))
        except Exception, e:
            self.__logger.error("!!!!!!ERROR IN WRITING LOG!!!!!!  %s"%str(e))
    
    def fatal(self, msg, *args):
        logmsg = msg
        if not isinstance(logmsg, basestring):
            try:
                logmsg = str(msg)
            except UnicodeError:
                logmsg = msg
        if args:
            logmsg = logmsg % args
        try:
            self.__logger.critical(logmsg.decode('utf-8'))
        except Exception, e:
            self.__logger.error("!!!!!!ERROR IN WRITING LOG!!!!!!  %s"%str(e))

    def logexc(self, msg, *args):
        self.error(msg, *args)
        s=traceback.format_exc()
        self.warn(s, *args)
    
    
if __name__ == '__main__':
    logger = Logger()
    logger1 = Logger()
    if (logger.initialize('a.log', DEBUG, CutByDay(1)) and logger1.initialize('../ab.log', DEBUG, CutBySize())):
        logger.debug('aaaaaaaaaaaaaafdfdafafaa')
        logger.error('bbbbbbbbbbbbbbbb')
        logger.debug('aaaaaaaaaaaaaafdfdafafaa')
        logger1.debug('aaaaaaaaaaaaaaaaaaaaaaa')
    else:
        print 'init log error'
    print logging.getLogger('a').name
    print logging.getLogger('ab').name
