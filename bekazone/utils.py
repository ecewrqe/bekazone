
from configparser import ConfigParser
from django.shortcuts import render

class BekaConfigParser(object):
    """
    config file class
    """
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = ConfigParser()
        self.config.read(self.config_path, encoding="utf8")

    def get_config(self, section, option):
        """
        gain a section and a option, display the value
        """
        if self.config.has_option(section, option):
            res = self.config.get(section, option)
        else:
            res = None

        return res

    def get_option_dict(self, section):
        options = self.config.options(section)
        return options
    def get_mysql_config(self, option):
        """
        gain a mysql config
        """
        res = self.get_config("mysql", option)
        return res

def page_not_found(request):
    return render(request, 'pages-404.html')