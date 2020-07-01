[TOC]

## system
#### os, glob, subprocess
- exec not in new process
os.system(cmd)
os.popen(cmd)->iterator
- exec in new process `subprocess`
**subprocess.Popen**
```
args: command string or list
stdin, stdout, stderr: fp, subprocess.PIPE, DEVNULL
shell
```
返す値ファイルObjectと同じ取り扱い

#### io,buffer
ByteIO, StringIO, BinaryIO

#### file system
- path操作まとめ
	os.path.exists(path)->boolean
	os.path.join(path, file)->path2

	os.path.split(path)->(path2, file)
	os.path.splitdrive
	os.path.splitext

	os.path.abspath

	os.path.basename
	os.path.dirname

	os.path.commonpath(path_list)
	os.path.normcase(path) -> path2 `normalize case, all slashes into backslashes`
	os.path.normpath `normalize path, elimiting double slashes`

	samefile, samestat
	isabs, islink, isfile, ismount

```
# os & os.path
curdir = '.'
pardir = '..'
extsep = '.'
sep = '\\'
pathsep = ';'
altsep = '/'
defpath = '.;C:\\bin'
devnull = 'nul'
```

- os
	os.getcwd ⇔ os.path.abspath(os.path.curdir)
	os.kill(pid, sig)
	os.fork()->pid
```
#how to kill a python fork
os.kill(pid, signal.ITIMER_VIRTUAL)
```
- glob
	list directory's file
- shutil
	copyfileobj(fsrc->fileobj,fdst->fileobj,length)
	copyfile(src->str,dst->str,follow_symlinks=True)

	copymode(src->str,dst->str)
	copystat(src->str,dst->str)

	copy(src->str,dst->str)    # copymode and copyfile
	copy2(src->str,dst->str)    # copystat and copyfile
## 時間
#### time
time.time() -> float
time.ctime(self->time,seconds->float) -> str
time.localtime(seconds->float) -> struct_time
time.gmtime(seconds->float) -> struct_time
time.mktime(p_struct->struct_time) -> float

##### struct_time
``` C
struct tm
{
    int tm_sec;   // seconds after the minute - [0, 60] including leap second
    int tm_min;   // minutes after the hour - [0, 59]
    int tm_hour;  // hours since midnight - [0, 23]
    int tm_mday;  // day of the month - [1, 31]
    int tm_mon;   // months since January - [0, 11]
    int tm_year;  // years since 1900
    int tm_wday;  // days since Sunday - [0, 6]
    int tm_yday;  // days since January 1 - [0, 365]
    int tm_isdst; // daylight savings time flag
};
```
#### datetime
datetime.datetime
datetime.date
datetime.time

datetime.datetime.now()
datetime.datetime.today()
datetime.datetime.strftime()

datetime.datetime.strftime(fmt)->date_string
datetime.datetime.strptime(date_string, fmt)->datetime

時間の足り引き
datetime.timedelta(day)
datetime.timedelta(year, month...)

## 正規表現re
re.match(pattern, string, flags)->Match_obj
re.search(pattern, string, flags)->Match_obj
re.split(pattern, string, maxsplit, flags)->list
re.sub(pattern, value, string, count, flags)->list

- Match
カッコ掴んだグループを分けてインデックスで表示する、０全部、1,2..グループインデックス
Match.group(int)->string
Match.groups()->list　全部グループをlistで組んで表示する
Match.groupdict(string)->int

Match.start(group)->int
Match.end(group)->int
Match.span(group)->(start, stop)

- Pattern
Match.compile(pattern)->Pattern


## データ保存
#### json, pickle, yaml
**関数:**
dump, load
dumps, loads
```
[{"ken_id": 1, "ken_name": "北海道", "ken_furi": "ホッカイドウ"}, {"ken_id": 2, "ken_name": "青森県", "ken_furi": "アオモリケン"}]
```
- json.dumps(obj)->str
**params:**
ensure_ascii=True `if "False", the return can contain non-ASCII character, kanji will not change to ascii`
- json.loads(str)->obj
**params:**
encoding=None
parse_float=None
parse_int=None

- json.dump(obj, fp)
- json.load(fp)->obj

- yaml.dump(data, stream, other)
dump -> dump_all -> Dump
safe_dump_all -> dump_all -> SafeDump
load -> load_all -> FullLoader
full_load -> full_load_all -> load_all -> FullLoader
safe_load -> safe_load_all -> load_all
serialize -> serialize_all

data is a obj like dict or list
stream: save to
other: allow_unicode (json ensure_ascii), encoding

#### xml
xml.etree.ElementTree (ET)

- parse xml
ET.parser(sourcefile, parser) -> ET.ElementTree
ET.fromstring -> XML -> XMLParser.close() -> root



class ElementTree
```
__init__(element, file)
getroot()
parse(sourcefile, parser=None)
# parser: XMLParser
self._root = XMLParser.close() -> close_handler()
# _root is a element
```


- ET.Element
tag, attrib, text, tail
getchildren() -> children
append, extend, insert, remove **(elements in children)**
getitem, setitem, delitem **(children)**
**search:** find, findall, find
get, set, keys, items **(attrib)**
copy
makeelement **(create a new element)**

- ET.tostring
ET.tostring(element, encoding)
`encoding="unicode"`

#### excel
xlrd, xlwt, xlutils
excel file is a excel book, spreadsheet is page, a excel file has multiple spreadsheet，every sheet is a table
excel book(workbook), sheet(worktable), cell(col, row, cell, cell_value, cell_type), format(color, font, data_format, date), xfborder, xfbackground, xfalignment, 

##### xlrd
xlrd.open_workbook(filename)->excel_obj

open_workbook->book.open_workbook_xls->Book

- Book
Book.sheets()->sheet_obj_list
Book.sheet_by_index(index)->sheet_obj
Book.sheet_by_name(name)->sheet_obj
Book.sheet_names()->sheet_name_list

- Sheet
Sheet.row_values(nrow, start_col=0, stop_col=None) -> cell value's list of a row
Sheet.col_values(ncol, start_row=0, stop_row=None) -> cell value's list of a col
Sheet.row_slices(nrow, start_col=0, stop_col=None) -> cell's list of a row
Sheet.col_slices(ncol, start_row=0, stop_row=None) -> cell's list of a col
Sheet.row_types(nrow, start_col=0, stop_col=None) -> cell type's list of a row
Sheet.col_types(ncol, start_row=0, stop_row=None) -> cell type's list of a col

Sheet.cell(nrow, ncol)->cell
Sheet.cell_value(nrow, ncol)->cell_value[string]
Sheet.cell_types(nrow, ncol)->cell_type

ctype:
```
ctype_text = {
    XL_CELL_EMPTY: 'empty',
    XL_CELL_TEXT: 'text',
    XL_CELL_NUMBER: 'number',
    XL_CELL_DATE: 'xldate',
    XL_CELL_BOOLEAN: 'bool',
    XL_CELL_ERROR: 'error',
    XL_CELL_BLANK: 'blank',
}
```

##### xlwt
```
# create excel file
wb = xlwt.Workbook()

sheet01 = wb.add_sheet("test_sheet")
sheet01.write(0,0,"0.001")

wb.save("example.xls")
```

##### rd to wt
```
wb_rd = xlrd.open_workbook("example.xls")
st01 = wb_rd.get_sheet("st01")
```
xlrd.biffh.XLRDError: Can't load sheets after releasing resources.

解決方法：
```
from xlutils.copy import copy
wb_rd = xlrd.open_workbook("example.xls")
wb_wt = copy(wb_rd)
st01 = wb_rd.get_sheet("st01")
```
##### xlstyle
```
class XFStyle(object):
    def __init__(self):
        self.num_format_str  = 'General'
        self.font            = Formatting.Font()
        self.alignment       = Formatting.Alignment()
        self.borders         = Formatting.Borders()
        self.pattern         = Formatting.Pattern()
        self.protection      = Formatting.Protection()
```

- Font
```
name='Arial'
height --- [size]
italic=FALSE
bold=FALSE
colour_index
underline=FALSE
```

- Alignment

```
horz:
  HORZ_GENERAL: 0X00
  HORZ_LEFT: 0x01
  HORZ_CENTER: 0X02
  HORZ_RIGHT: 0x03
  HORZ_FULLED: 0X04
vert:
  VERT_TOP: 0x00
  VERT_CENTER: 0x01
  VERT_BOTTOM: 0X02
orie: orientation
  ORIENTATION_NOT_ROTATED: 0X00
  ORIENTATION_STACKED: 0X01
  ORIENTATION_90_CC: 0X02
  ORIENTATION_90_CW: 0X03
```

- Pattern

背景, background
```
from xlwt import Pattern
pattern_obj = Pattern
pattern_obj.pattern = Pattern.SOLID_PATTEN: 0x01
pattern_obj.pattern_back_colour = 5  # yellow
```

- Border
边框

```
left, right, top, bottom:
	NO_LINE
	THIN
	MEDIUM
	DASHED
	DOTTED
	THICK
	DOUBLE
	HAIR

left_colour, right_colour, top_colour, bottom_colour
```

- xldate
xldate_to_datetime


## 永久配置
#### configparser

file_type: ini|conf
```
[default]
...
[section]
option=value
#comment
```
section, option, value, comment, defaultsection

cp.Configparser -> cp.RawConfigparser
- parse
read(filename, encoding=None)
read_file
read_string(string)
read_dict(dict)
readfp(fp)

- get ini
sections()
options(section)
has_section(section)->boolean
has_option(section, option)->boolean

get(section, option)->value
getint, getfloat, getboolean
- set ini
set(section, option, value)
add_option(section)

- del ini
remove_option(section, option)
remove_section(section)

- save
write(fp)

## 記録
#### logging
- level: debug, info, warning, error, critical
- 記録表示方法: スクリーン、ファイル、コンソール
ファイルでは、message, customize log file
- logger name
- basicConfig

``` python
logging.basicConfig(filename,level)
# other params: filemode-(dft:a), format, datefmt, stream, handle
logger = logging.getLogger(name)

logging.debug = logger.debug = _log(level...)
logger.debug(msg, args, exc_info=None, extra=None, stack_info=False) # debug, info, warning, error, critical
```

- Formatter: %()s
  default:
  - name, message
  - levelno, levelname
  - pathname, filename, module, lineno, funcName
  - asctime
  - thread, threadName, process
  extra params
  **asctime formatter: same as datetime**

- Handler:
  Handler->FileHandler
  Handler->StreamHandler

example
``` python
import logging, sys
FORMAT = '%(asctime)s %(clientip)s %(message)s'
handler1 = logging.FileHandler("example.log", )
handler2 = logging.StreamHandler()


logger01 = logging.Logger("stream", logging.INFO)
logger02 = logging.Logger("file", logging.INFO)

logger01.addHandler(handler1)
logger01.addHandler(handler2)

logger02.addHandler(handler2)


fmt01 = logging.Formatter("%(message)s")
fmt02 = logging.Formatter("%(asctime)s %(filename)s %(lineno)s %(message)s")

handler1.setFormatter(fmt02)
handler2.setFormatter(fmt02)

logger01.info("we have a error, quickly shutdown")
```

## 帮助文档help生成


## データ保存アプリ
#### pymysql
pymysql.Connect->Connections()
- Connection()
```
host, user, password(passwd), database(db), port, bind_address,
unix_socket, read_timeout, write_timeout,
charset, cursorclass, server_public_key,
max_allow_packet=16*2014*2014
```

**local_infile**: read my.ini or my.cnf

conn.cursor()->Cursor
- Cursor
Cursor, DictCursor, SSCursor, SSDictCursor

- execute
execute(), excutemany()

- result
fetchone(), fetchmany(size), fetchall()

```
cursor.execute(query, args)
res = cursor.fetchall() // res <array? dict>
```

#### redis

#### mongodb

