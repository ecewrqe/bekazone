``` python
import logging

logging.basicConfig(filename="example.log",
                    filemode="w",
                    format="%(asctime)s,%(levelname)s,%(name)s,%(funcName)s,%(pathname)s,%(filename)s,%(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    level=logging.INFO,
                    )   #定义输出到文件
def func1():
    '''此函数打印日志'''
    logging.info("user logging 的")
    logging.warning("user logging warning")
    logging.critical("user logging critical")
func1()
```
##### log级别(level)
```
CRITICAL=FATAL=50(默认最严重的级别)
ERROR=40
WARNING=30
INFO=20
DEBUG=10(生产环境不要用这个级别)
NOTSET=0
```

### logging下的几个类：
##### logger:
logging.getLogger(logname->str)->loggerObj
logger.setLevel(level)
logger.addHandler(hdlr->handlerObj)
logger.hasHandler()->bool  ----是否有输出句柄
logger.error(msg,...)   -----用logger加句柄格式化输出
##### Formatter格式:
logging.Formatter(fmt->str,datafmt->str)->formatterObj
logging格式：
```
	%(<>)s          参考string的format
    %(name)s           logger名，root
    %(levelno)s         日志级别数值
    %(levelname)s       日志级别名称
    %(pathname)s        脚本文件路径
    %(filename)s        脚本文件名
    %(module)s          Module (name portion of filename)
    %(lineno)d          打印该日志的行号
    %(funcName)s       打印
    %(created)f         Time when the LogRecord was created (time.time()
                        return value)
    %(asctime)s           格式时间，用来接收datafmt参数
    %(msecs)d           Millisecond portion of the creation time
    %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                        relative to the time the logging module was loaded
                        (typically at application startup time)
    %(thread)d          线程ID
    %(threadName)s      线程名
    %(process)d         进程ID
    %(message)s         输出信息
```
datafmt参考时间格式

##### logging.Handler
filehandler基于streamhandler基于handler，用前面两个实现接口

logging.filehandler(filename,mode(a),encoding)    打印到文件
logging.streamhandler()打印到屏幕

handler.setLevel(level)     ----handler每个对象自己的级别设置
handler.setFormatter(fmt)    ----添加格式


