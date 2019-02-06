import json
import datetime
import re
import time
from _io import BytesIO
from PIL import Image
import logging
import os
from bekazone.utils import BekaConfigParser
from bekazone.settings import CONFIGFILE_PATH

class JsonResponse(object):
    """
    传输给前端的json格式的类
    {"status":0, "data": "success","error": None}
    {"status":300, "data": None, "error": "xxxError:xxx"}
    """
    def __init__(self):
        self.status = None
        self.errors = None
        self.data = None

    def set_success(self, status, data):
        self.status = status
        self.data = data

    def set_status_append(self, status, data=None, errors=None):
        self.status = status
        if data and self.data:
            self.data += data
        elif data and not self.data:
            self.data = data
        elif errors and self.errors:
            self.errors += errors
        elif errors and not self.errors:
            self.errors = errors

    def set_error(self, status, errors):
        self.status = status
        self.errors = errors

    def set_json_pack(self):
        json_pack = json.dumps(self.__dict__)
        return json_pack


DATE = DATE_FORMATTER = "%Y-%m-%d"
TIME = TIME_FORMATTER = "%H:%M:%S"

DATETIME_FORMATTER = "%s %s" % (DATE, TIME)


class DateJsonEncode(json.JSONEncoder):
    """
    json调用时间对象时导入此类
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            time_str = obj.strftime(DATETIME_FORMATTER)
            return time_str
        elif isinstance(obj, datetime.date):
            time_str = obj.strftime(DATE)
            return time_str
        return json.JSONEncoder.default(self, obj)

def date_to_string(dt):
    '''
    日期转字符串格式：
    格式：%Y-%m-%d %H:%M:%S
    :param dt:
    :return:
    '''
    if isinstance(dt, datetime.datetime):
        dt_str = dt.strftime(DATETIME_FORMATTER)
    else:
        dt_str = dt
    return dt_str

def make_url(url, key, value):
    '''
    ///10.0.0.1/index/?a=10&b=20, key="c", value=30 => /index/?a=10&b=20&c=30
    合成一个url
    //index/
    '''
    url_params = url.split("//", 1)[-1].split("/", 1)[-1].split("?")
    if len(url_params) == 1:
        base_url = url_params[0]
        params = ""
    elif len(url_params) == 2:
        base_url, params = url_params
    else:
        return ""

    param_dict = {}
    if params != "":  # 如果?后面有内容
        for param in params.split("&"):
            k, v = param.split("=")
            param_dict[k] = "%s=%s" % (k, v)

    param_dict[key] = "%s=%s" % (key, value)

    params = "&".join(param_dict.values())

    return "/%s?%s" % (base_url, params)

def copy_dictset(sr_dict,ds_dict):
    '''
    复制dictset变成dict

    '''

    for key in sr_dict:
        ds_dict[key] = sr_dict[key]

class PageBranch(object):
    '''
    generate page number
    '''

    def __init__(self, current_page, row_in_page, row_count=None, data_list=None, ):
        """
        
        """
        
        self.data_list = data_list
        self.current_page = current_page
        self.row_in_page = row_in_page
        self.row_count = row_count or len(data_list)

        self.page_count, self.end_page_row_count = divmod(self.row_count, row_in_page)
        if self.end_page_row_count:
            self.page_count += 1

        self.page_start_index = (current_page - 1) * row_in_page
        self.page_stop_index = (current_page) * row_in_page

        self.page_list = []

        self.has_prev, self.has_next = False, False

    def get_data_list(self):

        return self.data_list[self.page_start_index:self.page_stop_index]

    def get_pglist1(self):
        """
        1 2 3 4 5 6 7 8 9
        :return:
        """
        self.page_list = []
        for page in range(self.page_count):
            self.page_list.append(page)

    def get_pglist2(self, page_range_size=5):
        '''

        1-10
        1 2 3| 4 5
        2 3 4| 5 6
        3 4 5| 6 7

        如果页数小于page_range_size  打印所有0--page_count
        如果页数大于page_range_size
            如果current_page < page_range_size // 2 + 1  1--page_range_size
            如果current_page > page_count - page_range_size // 2  page_count - page_range_size---page_count
        '''
        assert page_range_size % 2 == 1, "page_range_size should even"

        self.page_list = []
        if self.page_count <= page_range_size:
            for page in range(1, self.page_count + 1):
                self.page_list.append(page)
        else:
            delta = int(page_range_size / 2)

            if self.current_page < 1 + delta:
                range_start = 1
                range_stop = page_range_size
                pass
            elif self.current_page > self.page_count - page_range_size:
                range_start = self.page_count - page_range_size + 1
                range_stop = self.page_count
            else:
                range_start = self.current_page - delta
                range_stop = self.current_page + delta

            for page in range(range_start, range_stop + 1):
                self.page_list.append(page)

    def get_pglist3(self, page_range_size=5):
        '''
        1 2 3| 4 5

        1 2| 3 ... 6
        1 2 3| 4 ... 6
        1 ... 3 4| 5 6

        1 2 3| 4 ... 7
        1 ... 3 4| 5 ... 7
        1 ... 4 5| 6 7

        如果current_page - 1 <= 2  1---current + 1 ... 7   1 2 3 4 ... 7

        如果current_page + 1 >= 6  1 ... current---7     1 ... 4 5 6 7
        如果current_page - 1 > 2 and current + 1 < 6  1 ... current_page - 1--current + 1 ... 7
        :return:
        '''
        assert page_range_size % 2 == 1, "page_range_size should even"

        self.page_list = []
        if self.page_count <= page_range_size:
            for page in range(1, self.page_count + 1):
                self.page_list.append(page)
        else:
            assert page_range_size >= 3, "page_range_size should great than 1"
            delta = int((page_range_size - 2) / 2)

            if self.current_page - delta <= 2:
                range_start = 1
                range_stop = page_range_size - 1
                for page in range(range_start, range_stop + 1):
                    self.page_list.append(page)

                self.page_list.append("...")
                self.page_list.append(self.page_count)
            elif self.current_page + delta >= self.page_count - 1:
                range_start = self.page_count - page_range_size + 2
                range_stop = self.page_count

                self.page_list.append(1)
                self.page_list.append("...")
                for page in range(range_start, range_stop + 1):
                    self.page_list.append(page)
            elif self.current_page - delta > 2 and self.current_page + delta < self.page_count - 1:
                range_start = self.current_page - delta
                range_stop = self.current_page + delta

                self.page_list.append(1)
                self.page_list.append("...")
                for page in range(range_start, range_stop + 1):
                    self.page_list.append(page)
                self.page_list.append("...")
                self.page_list.append(self.page_count)

    def get_pgextend(self, is_pn=True, is_ae=True, is_english=False):
        '''
        :param is_pn:
        :param is_ae:
        :param is_english:
        :return:
        '''
        has_prev, has_next = self.has_prev, self.has_next

        if len(self.page_list) > 2 and (self.page_list[0] != 1 or self.page_list[1] == "..."):
            has_prev = True
        if len(self.page_list) < self.page_count - 1 and \
                (self.page_list[-1] != self.page_count or self.page_list[-2] == "..."):
            has_next = True

        if is_pn:
            if is_english:
                if has_prev:
                    self.page_list.insert(0, "prev")
                    self.prev_page = self.current_page - 1
                if has_next:
                    self.page_list.append("next")
                    self.next_page = self.current_page + 1

            else:
                if has_prev:
                    self.page_list.insert(0, "上一页")
                    self.prev_page = self.current_page - 1
                if has_next:
                    self.page_list.append("下一页")
                    self.next_page = self.current_page + 1
        if is_ae:
            if is_english:
                if has_prev:
                    self.page_list.insert(0, "first")
                    self.first_page = 1
                if has_next:
                    self.page_list.append("last")
                    self.last_page = self.page_count
            else:
                if has_prev:
                    self.page_list.insert(0, "首页")
                    self.first_page = 1
                if has_next:
                    self.page_list.append("尾页")
                    self.last_page = self.page_count

    def get_all_page_range(self):
        self.current_page = 1
        while self.current_page <= self.page_count:
            self.get_pglist3()
            self.get_pgextend()

            self.current_page += 1

    def get_url_page(self):
        pass



def img_cut(pic_url):
    '''
    图片切割,只接受jpg
    :param pic_url:
    :param size: (0,0,256,256)
    :param init:
    :return:
    '''

    img = Image.open(pic_url)
    if img.size[0] < img.size[1]:
        img = img.crop((0, 0, img.size[0],img.size[0]))
    else:
        img = img.crop((0, 0, img.size[1], img.size[1]))

    return img

def img_changesize(img, size):
    '''
    图片缩放,只接受jpg
    :param pic_url:
    :param size: 128
    :param init:
    :return:
    '''
    img.thumbnail(size)
    stream = BytesIO()
    img.save(stream, "JPEG")
    return stream


def demark_safe(text):
    """
    take the mark off
    """
    text = text.replace("<", "&lt").replace(">", "&gt")
    return text

def make_payload(token, data):
    """
    complate payload string

    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    Content-Disposition: form-data; name="data"

    {}
    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    Content-Disposition: form-data; name="data"

    {}
    ------WebKitFormBoundary7MA4YWxkTrZu0gW

    ------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="data"\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name="data"\r\n{}\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW

    --{token}
  > Content-Disposition: form-data; name="{key}"; filename="{filename}"

    {value}
    --{token} >

    :param token:
    :param data:{key: (filename,  value), key:(filename, value)}
    :return:
    """
    import json
    msg_li = []
    msg_li.append("--%s\r\n" % token)
    for k, v in data.items():
        msg_li.append("Content-Disposition: form-data; name=\"%s\"" % k)
        if v[0]:
            msg_li.append("; filename=\"%s\"" % v[0])
        msg_li.append("\r\n\r\n")
        v_tmp = v[1]
        if isinstance(v[1], dict):
            v_tmp = json.dumps(v_tmp)

        msg_li.append("%s\r\n" % v_tmp)

        msg_li.append("--%s" % token)
    return "".join(msg_li)

def parse_payload(payload):
    """
    解析payload
    payload
    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    Content-Disposition: form-data; name="data"

    {}
    ------WebKitFormBoundary7MA4YWxkTrZu0gW
    return:
    :param payload: {key: (filename,  value), key:(filename, value)}
    :return:
    """
    first_line_pattern = re.compile(r"--\w+")

    token_pattern = re.compile(r"--(\w+)")
    items_pattern = re.compile(r"(\r\nContent-Disposition: form-data; name=\"\w+\"; filename=\"\w+\"\r\n\r\n.*\r\n--\w+)")
    items_pattern2 = re.compile(r"(\r\nContent-Disposition: form-data; name=\"\w+\"\r\n\r\n\w+\r\n--\w+)")
    item_map_pattern = re.compile(r"\r\nContent-Disposition: form-data; name=\"(?P<name>\w+)\"; filename=\"(?P<filename>\w+)\"\r\n\r\n.*\r\n--(?P<value>\w+)")
    item_map_pattern2 = re.compile(r"\r\nContent-Disposition: form-data; name=\"(?P<name>.+)\"\r\n\r\n.*\r\n--(?P<value>\w.+)")

    pos = str()

    if first_line_pattern.match(payload):
        token_res = token_pattern.search(payload)
        pos = token_res.end()
        token = token_res.group(0)
    else:
        raise Exception("payload格式不正确")


    data_dict = dict()
    payload_len = len(payload)
    while True:
        match_res = items_pattern.match(payload[pos:])
        print([payload[pos:]])
        res = re.match(r".*", payload[pos:])
        print(res)
        if match_res:
            imap_res = item_map_pattern.match(payload[pos:])
            print(imap_res.groups())
            pos = imap_res.end()
            print([payload[pos]])
        else:
            match_res = items_pattern2.match(payload[pos:])
            if match_res:
                imap_res = item_map_pattern2.match(payload[pos:])
                print(imap_res.groups())
                pos = imap_res.end()
            else:
                raise Exception("payload格式不正确")
        if pos == payload_len:
            break

def time_clock(func):
    def inner(*args, **kwargs):
        start_clock = time.time()
        res = func(*args, **kwargs)
        stop_clock = time.time()
        print(stop_clock - start_clock)
        return res
    return inner

class LoggerCollection(object):
    """
    log analyse tool, log manage
    simplify log code, 
    """
    def __init__(self):
        cp = BekaConfigParser(CONFIGFILE_PATH)
        
        log_path = cp.get_config("logger", "log_path")
        log_file = cp.get_config("logger", "log_file")
        log_file = os.path.join(log_path, log_file)
        log_name = cp.get_config("logger", "log_name")
        # formatter
        format = cp.get_config("logger", "format")
        format = logging.Formatter(format)


        date_fmt = cp.get_config("logger", "date_fmt")
        screen_level = cp.get_config("logger", "screen_level")
        file_level = cp.get_config("logger", "file_level")
        
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(logging.NOTSET)
        
        
        fh = logging.FileHandler(log_file)
        sh = logging.StreamHandler()
        

        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

        fh.setLevel(file_level)
        sh.setLevel(screen_level)

        fh.setFormatter(format)
        sh.setFormatter(format)
        


    def log_output(self, level, msg):
        standard_level = ("debug", "info", "warning", "error", "critical")
        level = level.lower()
        if level in standard_level:
            #level = level.capitalize()
            
            getattr(self.logger, level, )(msg)
        else:
            assert "the level isn't belong with system_level"
