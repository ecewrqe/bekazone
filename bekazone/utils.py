# --encoding:utf8--
from __future__ import unicode_literals
"""
去调用etc/bekazone/config.conf
config大致模块：
bekazone:平台的配置
mysql:平台数据库配置
logger:日志平台
"""
import ConfigParser
from django.shortcuts import render

class KaoqingConfigParser(object):
    """
    配置文件类
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.config_path)

    def get_config(self, section, option):
        """
        获取配置
        :param section:
        :param option:
        :return:
        """
        if self.config.has_option(section, option):
            res = self.config.get(section, option)
        else:
            res = None

        return res

    def get_mysql_config(self, option):
        """
        获取mysql配置
        :param option: mysql下的各种配置
        :return:
        """
        res = self.get_config("mysql", option)
        return res

def page_not_found(request):
    return render(request, 'pages-404.html')