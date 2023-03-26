from json import dump
from datetime import datetime
import logging
import time

class CloneLogger(object):

    r"""
        write: log entry in file 
        console: log entry in console
        path: path log file
    """

    def __init__(
            self, 
            logger_name: str, 
            file_name: str | None = None, 
            write: bool = False, 
            console: bool = True, 
            path: str = "./"
        ):
        self.write = write
        self.console = console

        self.date_start = '{:%Y:%m:%d}'.format(datetime.now())
        self.path = path
        self.logger_name = logger_name
        # print(f"creaete {self.logger_name }")
        # create file name
        if file_name == None:
            self.file_name = f"""{self.path}/{self.logger_name}-{"{:%Y:%m:%d}.log".format(datetime.now())}"""    
        else:
            self.file_name = path + file_name 
        
        logger_ = self.__addHandlers()

        self.info = logger_.info

    def __addHandlers(self): 
        logger_ = logging.getLogger(self.file_name)
        logger_.setLevel(logging.DEBUG)

        format_write = logging.Formatter('%(asctime)s | %(message)s') #| %(name)s 

        if self.console: 
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)
            ch.setFormatter(format_write)
            logger_.addHandler(ch)

        if self.write: 
            fh = logging.FileHandler(self.file_name)
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(format_write)
            logger_.addHandler(fh)
        

        return logger_
    
    def __delHandlers(self):
        logger = logging.getLogger(self.logger_name)
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])

    def nextFile(self, file_name=None):
        # create file name
        if file_name == None:
            self.file_name = f"""{self.path}/{self.logger_name}-{"{:%Y:%m:%d}.log".format(datetime.now())}"""
        else:
            self.file_name = file_name
        self.info(f'text file "{self.file_name}"')

        self.__delHandlers()

        logger_ = self.__addHandlers()

        self.info = logger_.info

class Checker:
    def __init__(self, logger: CloneLogger):
        self.logger = logger
        # self.logger_info = CloneLogger("TEST", "none.log", True, True, "./")
        # self.logger_info.info("init")

    def check(self):
        if self.logger.date_start != "{:%Y:%m:%d}".format(datetime.now()):
            self.logger.nextFile()
        # self.logger_info.info(f"run, {self.logger.logger_name}")
        time.sleep(1)

async def write_in_file(data, name = "timeNow",):

    if name == "timeNow":
        name = "{:%Y:%m:%d-%H:%M:%S}".format(datetime.now())

    file_name = '{}.json'.format(name)

    f = open(file_name, "a")

    with open(file_name, 'w', encoding='utf8') as file_name:
        dump(data, file_name, ensure_ascii=False)

    f.close()   

    return file_name



# print("{:%Y:%m:%d-%H:%M:%S}".format(datetime.now()))