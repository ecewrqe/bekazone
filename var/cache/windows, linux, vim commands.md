[TOC]

## shortcut
### linux terminal shortcut
| 命令 | 说明 |
| ------ | ------ |
| ctrl+a,ctrl+e | 行首行尾 |
| ctrl+left | 向前单词末 |
| ctrl+right | 向后单词末 |
| ctrl+u | 删除行首到光标 |
| ctrl+k | 删除光标到行末 |
| ctrl+w | 向前删除一个单词 |
| ctrl+y | 撤销 |

### windows desktop shortcut
| 命令 | 说明 |
| ------ | ------- |
| win+d | 显示桌面 |
| alt+left,alt+right | 前进，后退 |
| win+[0-9] | 打开在任务栏的对应数字的窗口 |
| win+[left, right, up, down] | 窗口[靠左，靠右，最大化，还原] |
| win+E | 运行资源管理器 |

#### run, windows system app
| 命令 | 说明 |
| ------ | ------- |
| msconfig | 开机启动管理 |
| inetcpl.cpl | internet选项 |
| taskmgr | 任务管理器 |
| perfmon | 性能检测 |
| resmon | 资源检测 |
| appwiz.cpl | 软件卸载 |
| control | 控制面板 |
| control system | 系统 |
| sysdm.cpl | 系统属性，环境变量 |
| timedate.cpl | 时间日期 |
| fonts | 字体管理 |
| msinfo32 | system information |
| dxdiag | DirectX Diagnostic tool |
| regedit | 注册表 |
| services.msc | 服务 |
| ncpa.cpl | 网络连接器 |
| lusrmgr.msc | 用户和组管理 |
| win+x, a | administrator powershell |
| devmgmt.msc | 设备管理器 |

#### explore
| 命令 | 说明 |
| ------ | ------- |
| ctrl+L | 地址栏 |
| ctrl+tab | 下一个标签 |
| ctrl+shift+tab | 上一个标签 |

## vim
#### vim shortcut
| 说明 | 命令 |
| ------ | ------- |
| [n] | 0~9,hjkl,Enter... |
| 行首行末 | Home,End&0,$ |
| 屏幕中跳转 | H M L |
| 文章头行尾行 | gg,G |
| 文章行 | [n]gg |
| 上几个单词 | b, [n]b |
| 下个单词 | w,e,[n]w |
| 剪切整行 | cc, dd, [n]cc, [n]dd |
| 复制整行 | yy, [n]yy |
| 粘贴 | p |
| 光标前后insert | a, i |
| 句子前后insert | A, I |
| 句子前后行insert | o, O |
| 缩进 | >>,<< |
| 搜索,上一个,下一个 | /[关键字], n, N, [n]N |
| 执行shell | ![command] |
- 分屏
splite 横向, vsplite纵向, ctrl+w切换
:tabnew 分页操作
:tabonly 关闭其他分页
:tabclose

#### vim setting

| 命令 | 说明 |
| ------ | ------- |
| set all | 查看所有配置 |
| set nu/set nonu | 行号显示 |
| set autoindent | 自动缩进 |
| set shiftwidth=[n] | >>,<<缩进的大小 |
| set tabstop=[n] | tab的时候缩进的大小 |
| set expandtab | tab to space |
| set nohls | 取消搜索选中 |
| set encoding=utf8, set fileencoding | 设置编码 |

v 选择
ctrl v 纵向选择
批量行缩进,批量操作
1, ctrl+v纵向选择; 2, shift+i批量输入; 3,空格字符任意填写; 4,esc
批行删除第一个字符
1, ctrl+v纵向选择; 选择一列; 2, x

q recording

设置变量
let 变量=值





