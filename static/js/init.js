/**
 * 收集表单内容的函数
 * @param form_id
 * @returns
 */

/*菜单高亮*/
$(document).ready(function () {
    var menu_dict = {}
    $("#mainnav-menu a").each(function () {
        menu_dict[$(this).attr("href")] = this;
        if($(this).attr("href") == location.pathname){
            $(this).parent().addClass("active-link").parent().addClass("in").parent().addClass("active");
            return false;
        }
    })
    
});


function collect_form(form_id) {
    var form_dict = {};

    $("#" + form_id).find("[name]").each(function () {
        form_dict[$(this).attr("name")] = $(this).val()
    })
    return form_dict;
}


/**
 * add a msg to display success or danger
 * @param form_id
 * @param form_item_msg
 * @param status
 */
function get_form_msg(form_id, form_item_msg, status) {
    $("#" + form_id).find(".msg").remove();
    if (status == 0) {
        $("#" + form_id).prepend("<span class='text-success msg'>" + form_item_msg + "</span>");
    } else {
        $.each(form_item_msg, function (name, list) {
            $("#" + form_id).find("[name=" + name + "]").after("<span class='text-danger msg'>" + list[0] + "</span>")
        })
    }
}

String.prototype.lsplit = function (seq, n) {
    var j = n;
    var str_list = new Array();
    var temp = "";
    for (var i in this) {
        temp += this[i];
        if (j == 0) {
            str_list.push(temp);
            break;
        }
        if (i == seq) {
            str_list.push(temp);
            temp = "";
        }
    }
}


var str01 = "hello/world";
str01.lsplit("/", 1);


/**
 * url parse
 * @param {any} url
 * example: http://www.abc.com/a/b/c?name=Bob&age=24
 * return example:
 * {
 *   "host": "www.abc.com",
 *   "path": "/a/b/c",
 *   "querys": {
 *     name:Bob, age:24
 *   }
 * }
 */
function url_parse(url) {
    var url_dict = {
        host: null,
        path: null,
        querys: {},
    };
    var path = null,
        querys = null;

    if (url.split("//").length === 2) {
        url = url.split("//")[1];

        var parts = url.split("/");
        url_dict.host = parts.splice(0, 1)[0];
        url = "/" + parts.join("/");
    }




    if (url.split("?").length === 2) {
        path = url.split("?")[0];
        querys = url.split("?")[1];
    } else {
        path = url.split("?")[0];
    }

    url_dict.path = path;

    if (typeof querys === "string") {
        var query_key_list = new Object();
        $.each(querys.split("&"), function (i, query) {
            var k = query.split("=")[0];
            if(!(k in query_key_list)){
                query_key_list[k]=1;
                url_dict.querys[k] = decodeURI(query.split("=")[1]);
            }else{
                query_key_list[k]++;
                if(query_key_list[k] == 2){
                    var tmp_data = url_dict.querys[k];
                    url_dict.querys[k] = new Array();
                    url_dict.querys[k].push(tmp_data);
                }

                url_dict.querys[k].push(decodeURI(query.split("=")[1]))
            }
            
            
        });
    }

    return url_dict;
}

function search_query(url, key) {
    var url_dict = url_parse(url)
    var value = url_dict["querys"][key]
    return value;
}
/**
 * url unparse: reverse by url_parse
 * url item make to url
 * @param {any} url_dict
 */
function url_unparse(url_dict) {
    var url = "";
    var query_list = []

    if (url_dict.host) {
        url += "//" + url_dict.host;
    }

    url += url_dict['path'] + "?";
    $.each(url_dict.querys, function (k, v) {
        query_list.push(k + "=" + encodeURI(v));
    });
    url += query_list.join("&");
    return url
}

function add_query(url, dict) {
    var url_dict = url_parse(url);

    $.each(dict, function (k, v) {
        url_dict["querys"][k] = v;
    });

    url = url_unparse(url_dict);
    return url;
}





/*
* 定义一个有序字典
* f.set("aa","bb")
* f.set("cc","dd")
* f.get_index(0)
* f.set_index(1,"gg")   修改
* f.set_index(2,"88")   添加，
*
* f.each(function(k,v){return true})
* 循环要保证顺序执行
* */
function orderdict(keys, dict) {
    this.keys = keys || new Array();
    this.dict = dict || new Object();

    for (var k in dict) {
        if (!this.keys.indexof(k)) {
            this.keys.push(k);
        }
    }


    this.iset = function (i, k, v) {
        if (this.keys.indexof(k) == -1) {
            this.keys.splice(i, 0, k);
        }
        this.dict[k] = v;
    };


    this.set = function (k, v) {
        if (this.keys.indexof(k) == -1) {
            this.keys.push(k);
        }

        this.dict[k] = v;
    };

    this.insert = function (i, k, v) {
        if (i >= this.size()) {
            throw "index out of key size"
        }

        this.keys.splice(i, 0, k);
        this.dict[k] = v;
    }


    this.remove = function (k) {
        this.keys.remove(k);
        delete this.dict[k];
    };

    this.get_keys = function () {
        console.log(this.keys);
        return this.keys;
    };

    this.get_values = function () {
        var values = new Array();
        for (var k in this.keys) {
            values.push(this.dict[this.keys[k]]);
        }
        return values;
    };
    this.pop = function () {
        var res = {
            key: null,
            value: null,
        }
        res.key = this.keys.pop();
        res.value = this.dict[res.key];
        delete this.dict[res.key];
        return res;
    }

    this.join = function (str) {
        var res = this.get_values().join(str);
        return res;
    }



    this.get = function (k) {
        return this.dict[k];
    }

    this.iget = function (i) {
        var res = {
            key: this.keys[i],
            value: this.get(this.keys[i]),
        }
        return res;
    }


    this.each = function (fn) {
        for (var i in this.keys) {
            var flag = fn(this.keys[i], this.dict[this.keys[i]]);
            if (flag == true) {
                continue;
            } else if (flag == false) {
                break;
            }
        }
    }

    this.ieach = function (fn) {
        for (var i in this.keys) {
            var flag = fn(i, this.dict[this.keys[i]]);
            if (flag == true) {
                continue;
            } else if (flag == false) {
                break;
            }
        }
    }

    this.ieach2 = function (fn) {
        for (var i in this.keys) {
            var flag = fn(i, this.keys[i], this.dict[this.keys[i]]);
            if (flag == true) {
                continue;
            } else if (flag == false) {
                break;
            }
        }
    }
    this.size = function () {
        return this.keys.length;
    }
}

//array类添加insert属性
// array.prototype.insert = function (index,item) {
//     this.splice(index,0,item);
// };
// array.prototype.remove = function (item) {
//     var index = this.indexof(item);
//     this.splice(index,1);
// };
/**
 * 表格操作库，表格ajax接受，
 */
function table_func_tools(option) {
    this.init = function (option) {
        this.option = option;
        this.option.column_options = this.option.column_options || {};
        this.option.exist_column_options = this.option.exist_column_options || [];

        if (this.option.column_head_ajax && this.option.column_head_ajax.exec) {
            this.column_head_ajax();
        } else {
            this.column_head_gen();
        }

        if (this.option.tbody_ajax && this.option.tbody_ajax.exec) {
            this.tbody_ajax();
        }
    }

    this.csrftoken = $.cookie('csrftoken');

    this.option = {
        table: null,    //必须指定table id
        parent_fn: null,
        page: null,    //分页区域的id
        classes: null,

        attrs: {},
        column_head_gen: false,
        column_head_option: new orderdict(),//有数据库字段的字段，需要前端修改的，key必须为字符串，如果key为整数表示插入外来列

        url: null,
        column_options: new orderdict(),  //有数据库字段的字段，需要前端修改的，key必须为字符串，如果key为整数表示插入外来列

        column_head_ajax: {
            exec: false,
            url: "",
        },
        tbody_ajax: {
            exec: false,
            url: "",
            rows: 10,
            page_size: 7,
        },
        page_frame: {  //分页格式
            fn: "",    //坐落位置
            introdution: null,   //页面说明
            formatter: null,    //页码格式
        },
        search_field: [],
    }

    this.column_head_gen = function (data) {

        var table_tag = document.createelement('table');
        // if(this.option.table_fn){
        //     table_tag.classlist.add(this.option.table_fn);
        // }

        if (this.option.table_classes) {
            $(table_tag).addclass(this.option.table_classes);
        } else {
            table_tag.classlist.add("table");
        }

        if (this.option.attrs) {
            $(table_tag).attr(this.option.attrs);
        }
        $(table_tag).attr("id", this.option.table);


        var thead_tag = document.createelement('thead');
        var tbody_tag = document.createelement('tbody');
        var theadr_tag = document.createelement('tr');
        $(table_tag).append(thead_tag);
        $(table_tag).append(tbody_tag);
        $(thead_tag).append(theadr_tag);

        var table_obj = this;


        function field_gen(th_li) {

            table_obj.option.column_head_option.each(function (k, v) {

                if (typeof v === "function") {
                    th_li.set(k, v(k));
                } else {
                    th_li.set(k, "<th tname='" + k + "'>" + v + "</th>");
                }
            })

        }

        if (data) {
            /**这个data是个列表
             * 第一次循环data ,data中如果在option中有，则替换，所有存放在ul_li
             * 第二次循环option，如果在ul_li没有，就添加
             */
            var th_li = new orderdict();

            for (var i in data) {
                var k = data[i];
                var value = table_obj.option.column_head_option.get(k);
                if (value) {
                    if (typeof value === "function") {
                        th_li.set(k, value());
                    } else {
                        th_li.set(k, "<th tname='" + k + "'>" + value + "</th>");
                    }
                } else {
                    th_li.set(k, "<th tname='" + k + "'>" + k + "</th>");
                }
            }

            table_obj.option.column_head_option.ieach2(function (i, k, v) {

                if (typeof k === 'number') {
                    th_li.insert(k, k, v());
                } else {
                    if (!th_li.get(k)) {
                        th_li.iset(i, k, v());
                    }
                }

            })




        } else {
            var th_li = new orderdict();
            field_gen(th_li);
        }

        $(theadr_tag).html(th_li.join(""));
        $(this.option.parent_fn).append(table_tag);
    }
    this.column_head_ajax = function () {
        //规定_cont发送h就是列标，b就是body
        var table_obj = this;
        $.ajax({
            url: table_obj.option.column_head_ajax.url,
            type: "post",
            data: { "_cont": "h" },
            headers: { "x-csrftoken": this.csrftoken },
            async: false,
            datatype: "json",
            success: function (data) {
                //data的格式是[str,str,str]
                console.log("data===", data);
                table_obj.column_head_gen(data);
            }
        })
    };
    this.tbody_ajax = function (page) {
        var table_obj = this;
        var url = add_query(table_obj.option.tbody_ajax.url, { "_row": table_obj.option.tbody_ajax.rows });
        if (page) {
            url = add_query(url, { "_page": page });
        }
        if (table_obj.option.tbody_ajax && table_obj.option.tbody_ajax.page_size) {
            url = add_query(url, { "_page_size": table_obj.option.tbody_ajax.page_size })
        }


        $.ajax({
            url: url,
            type: "post",
            data: { "_cont": "b" },
            headers: { "x-csrftoken": this.csrftoken },
            async: false,
            datatype: "json",
            success: function (data) {
                table_obj.tbody_gen(data.data);
                // table_func_tools.page_gen(data.page);
            }
        })
    };
    this.tbody_gen = function (arr) {

        var table_obj = this;
        console.log(arr);
        var htr_list = $("#" + this.option.table).find("thead th");
        var tname_list = [];
        $("#" + table_obj.option.table).find("tbody").empty();
        htr_list.each(function () {
            if ($(this).attr("tname")) {
                tname_list.push($(this).attr("tname"));
            } else {
                tname_list.push(null);
            }
        });
        $.each(arr, function (i, row) {
            var td_list = [];
            //数据库配置列
            $.each(tname_list, function (j, field) {
                var td_cont = "";
                if (field) {
                    if (row[field]) {
                        td_cont = "<td>" + row[field] + "</td>";
                        if (table_obj.option.column_options[field]) {
                            td_cont = table_obj.option.column_options.get(field)(row[field]);
                        }
                    }
                }
                td_list.push(td_cont);

            })

            //其他配置列

            table_obj.option.column_options.ieach2(function (i, k, v) {
                if (typeof k === 'number') {
                    td_list.splice(k, 0, v());
                }
            })

            // for(var j in td_list){
            //     if(td_list[j].length === 0){
            //         td_list[j] = "<td></td>";
            //     }
            // }
            $("#" + table_obj.option.table).find("tbody").append("<tr>" + td_list.join("") + "</tr>");
        });


    }

    function introdution(page) {
        return "showing 1 to " + page.page_count + " of " + page.row_count + " entries";
    }
    function li_formatter(page, _page, intro) {

        if (!intro) {
            if (page == _page) {
                return "<li class=\"paginate_button active\"><a href=\"javascript:;\">" + page + "</a></li>"
            } else {
                return "<li class=\"paginate_button\"><a href=\"javascript:;\" onclick=\" + this.tbody_ajax(" + page + ")\">" + page + "</a></li>"
            }
        } else {
            return "<li class=\"paginate_button\"><a href=\"javascript:;\" onclick=\"this.tbody_ajax(" + page + ")\">" + intro + "</a></li>"
        }
    }

    this.page_gen = function (page) {
        var table_obj = this;

        if (table_obj.option.page_frame && table_obj.option.page_frame.fn) {
            var intro_tag = document.createelement("div");
            var introdution = this.option.page_frame.introdution ? this.option.page_frame.introdution :
                this.introdution;
            var li_formatter = this.option.page_frame.li_formatter ? this.option.page_frame.li_formatter :
                this.li_formatter;


            $(intro_tag).addclass("introdution");
            $(intro_tag).html(introdution(page));


            var page_tag = document.createelement("div");
            $(page_tag).addclass("page");
            var ul = document.createelement("ul");
            $(ul).addclass("pagination");
            $(page_tag).append(ul);

            var li_li = [];
            li_li.push(li_formatter(page._page - 1, page._page, "上一页", page));




            for (var i = page.start_page; i < page.end_page; i++) {
                li_li.push(li_formatter(i, page._page, null, page));
            }
            li_li.push(li_formatter(page._page + 1, page._page, "下一页", page));
            $(ul).append(li_li.join(""));

            $(this.option.page_frame.fn).empty().append(intro_tag);
            $(this.option.page_frame.fn).append(page_tag);
        }


    }
    this.check_all = function (itms, name) {
        $("[name='" + name + "']").each(function () {
            $(this).prop('checked', $(itms).prop('checked'));
        })
    }
    this.check_component = function (name, id) {
        var flg = true;
        $("[name='" + name + "']").each(function () {
            if (!$(this).prop('checked')) {
                flg = false;
                return flg;
            }
        });
        $("#" + id).prop('checked', flg);
    }
}



function check_all(itms, name) {
    $("[name='" + name + "']").each(function () {
        $(this).prop('checked', $(itms).prop('checked'));
    })
}
function check_component(name, id) {
    var flg = true;
    $("[name='" + name + "']").each(function () {
        if (!$(this).prop('checked')) {
            flg = false;
            return flg;
        }
    });
    $("#" + id).prop('checked', flg);
}


function get_depart(sel) {
    $.ajax({
        url: "/kaoqing_api/department/",
        type: "GET",
        dataType: "JSON",
        success: function (data) {
            if (data.status == 0) {
                department_list = JSON.parse(data.data);
                let select_tag_list = $('.show_dep_list');
                for (let select_tag of select_tag_list) {
                    let option_tag = document.createElement("option");
                    option_tag.setAttribute("value", "");
                    option_tag.innerText = "";

                    select_tag.append(option_tag);
                }

                for (let depart of department_list) {
                    for (let select_tag of select_tag_list) {

                        let option_tag = document.createElement("option");
                        option_tag.setAttribute("value", depart.id);
                        if(depart.id == sel){
                            option_tag.selected = true;
                        }
                        option_tag.innerText = `${depart.name}:${depart.id}`;

                        select_tag.append(option_tag);
                    }


                }
                for (let select_tag of select_tag_list) {
                    $(select_tag).chosen({width: "100%"});
                }

            }
        }
    })
}

/**
 * 获取所有员工，类名show_user_list
 * option键值类型为：微信号:人名
 * */
function get_employee() {
    $.ajax({
        url: "/kaoqing_api/employee/",
        type: "GET",
        dataType: "JSON",
        success: function (data) {
            if (data.status == 0) {
                let data_in_data = JSON.parse(data.data);

                let userid_tag_list = $(".show_user_list");
                for (let userid_tag of userid_tag_list) {
                    let option_tag = document.createElement("option");
                    option_tag.setAttribute("value", "");
                    option_tag.innerText = "";
                    $(userid_tag).append(option_tag);
                    for (let userid of data_in_data) {
                        let option_tag = document.createElement("option");
                        option_tag.setAttribute("value", userid.userid);
                        option_tag.innerText = `${userid.name}:${userid.emp_num}`;
                        $(userid_tag).append(option_tag);
                    }
                    $(userid_tag).chosen({width: "100%"});
                }

            }

        }
    })
}

/**
 * 获取所有地区，类名为：show_area_list
 * option键值类型：地区编号:地区名
 * */
function get_area() {
    $.ajax({
        url: "/kaoqing_api/area/",
        type: "GET",
        dataType: "JSON",
        success: function (data) {
            if (data.status == 0) {
                let area_list = JSON.parse(data.data)
                let area_sel_list = $(".show_area_list")
                for (let area_sel of area_sel_list) {
                    let option_tag = document.createElement("option");
                    option_tag.setAttribute("value", "");
                    option_tag.innerText = "";
                    $(area_sel).append(option_tag);
                    for (let area of area_list) {
                        let option_tag = document.createElement("option");
                        option_tag.setAttribute("value", area);
                        option_tag.innerText = `${area}`;
                        $(area_sel).append(option_tag);

                    }
                    $(area_sel).chosen({width: "100%"});
                }
            }
        }
    })
}

/**
 * 重新形成页码*/
function get_page_li_class(fields) {
    $(".pagination li").each(function () {
        let tmp_url = $(this).find("a").attr("href");
        if (tmp_url) {
            for (let field of fields) {
                let query_dic = {};
                if(field[1]===null){
                    query_dic[field[0]] = field[2];
                }else{
                    query_dic[field[0]] = $(field[1]).val();
                }

/*                console.log(field[0])
                console.log(field[1])
                console.log($(field[1]).val())
                console.log($("#depart_sel").val())*/
                tmp_url = add_query(tmp_url, query_dic);
            }
            $(this).find("a").attr("href", tmp_url)

        }


    })
}

/**
 * 让所有的日期输入框都变成可以选择
 * 统一类名：date_show*/
function get_date_show() {
    $(".date_show").datepicker({
        format: "yyyy-mm-dd",
        todayBtn: "linked",
        autoclose: true,
        todayHighlight: true
    })
}

/**
 * 让所有时间输入框都变成选择
 * 统一类名: time_show
 * */
function get_time_show() {
    $(".time_show").timepicker({
        showMeridian:false,
        showSeconds:false
    })
}

/**
 * 搜索框脚本*/
function submit_search(itm) {
    let url = add_query(location.href, {"_s": $(itm).val()});
    location.href = url;
}

/**
 * 让一组按钮变成选择框形式的按钮
 * 输入指定name的一组*/
function change_active(check_name){
    $(`[name='${check_name}']`).click(function () {
        if($(this).hasClass("active")){
            $(this).removeClass("active");
        }else{
            $(this).addClass("active");
            let it_list = $("[name='rule_type']");
            for(let it of it_list){
                if(it !== this){
                    $(it).removeClass("active");
                }
            }
        }

    })
}

/**
 * 日期筛选框统一设置:
 * 开始日期id:search_start_date
 * 结束日期id:seart_stop_date
 * send_url: url?start_date=xxx&stop_date=xxx
 * */
function date_search_filter() {
    let start_date = $("#search_start_date").val();
    let stop_date = $("#search_stop_date").val();
    let url = location.href;
    url = add_query(url, {
        "start_date": start_date,
        "stop_date": stop_date
    })
    location.href = url;
}
