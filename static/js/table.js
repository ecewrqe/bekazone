/**
 * table前端自定义生成表
 * version: v1.21
 */

isInArray = function (item, array) {
    for (let it of array) {
        if (item === it) {
            return true;
        }
    }
    return false;
}

function TableBuilder(option) {

    this.option = option;
    this.parent_obj = document.getElementById(this.option.parent);

    this.table_tag = document.createElement('table');
    this.parent_obj.appendChild(this.table_tag);
    if (this.option.paginator) {
        this.page_tag = document.getElementById(this.option.paginator);
    }
    if (this.option.searcher) {
        this.search_tag = document.getElementById(this.option.searcher);
    }
}

TableBuilder.prototype.option = {
    object_name: "tb01",
    table: "tb01",
    parent: "parent",
    attrs: {"style": "width:300px"},
    classes: ["table", "is-bordered"],
    column_options: ["animal", "price"]
}

/**
 * 初始化表格：
 * 表格的位置，表格的头部定义，表格样式等
 * 传入总的数据
 * 定义分页规则:从第一页开始，默认每页10条数据，定义规则按page_row_count
 *
 * 如果不传column_options, 数据必须传数组，没有键值一说，按顺序渲染
 * 如果指定module是2，说明是详细列表
 * @param {*} data_array
 */
TableBuilder.prototype.init = function (data_array) {
    this.data_array = data_array ? data_array : new Array();
    this.data_array_length = this.data_array.length;
    this.tr_array = new Array();
    this.option.other_column_options = this.option.other_column_options || new Object();

    this.fields_obj = new Object();   // tname和字段对象的键值
    this.tname_list = new Array();   //  tname的顺序

    this.column_head_gen();

    this.render();


    // 定义分页
    if (this.page_tag) {
        this.page_row_count = this.option.page_row_count || 10;
        this.page_count = parseInt(this.data_array_length / this.page_row_count);
        this.last_page_row_rount = this.data_array_length % this.page_row_count;
        if (this.last_page_row_rount != 0) {
            this.page_count += 1
        }
    }

    // 搜索

    if (this.search_tag) {
        //search_input
        let input_tag = document.createElement("input");
        input_tag.setAttribute("type", "text");
        input_tag.setAttribute("name", "search");
        if (this.option.searcher_class) {
            for (let cla of this.option.searcher_class) {
                input_tag.classList.add(cla);
            }
        }

        input_tag.setAttribute("onkeyup", this.option.object_name + ".search(this.value)");
        input_tag.setAttribute("placeholder", "搜索");
        this.search_tag.appendChild(input_tag);

        this.search_data = this.tr_array;
        this.search_fields = this.option.search_fields;
        // let tb_obj = this;
        // this.search_tag.onkeyup = function(){
        //     tb_obj.search(this.value);
        // }
    }


}

/**
 * 定义头部和整体的样式
 *
 */
TableBuilder.prototype.column_head_gen = function () {
    // if(this.option.table_fn){
    //     table_tag.classlist.add(this.option.table_fn);
    // }
    let table_tag = this.table_tag;
    let classes = this.option.classes;
    let tname_list = this.tname_list;
    let fields_obj = this.fields_obj;

    for (let i in classes) {
        table_tag.classList.add(classes[i]);
    }

    let attrs = this.option.attrs;
    for (let k in attrs) {
        table_tag.setAttribute(k, attrs[k])
    }


    var thead_tag = document.createElement('thead');
    var tbody_tag = document.createElement('tbody');
    table_tag.appendChild(thead_tag);
    table_tag.appendChild(tbody_tag);
    if (!this.option.column_options) {
        return
    }


    // if(this.option.caption){
    //     var caption_tag = document.createElement('caption');
    //     caption_tag.innerText = this.option.caption;
    //     table_tag.appendChild(caption_tag);
    // }

    var theadtr_tag = document.createElement('tr');
    thead_tag.appendChild(theadtr_tag);

    let column_options = this.option.column_options;

    let other_column_options = this.option.other_column_options;
    let column_count;

    for (let i in this.option.column_options) this.tname_list.push(undefined);
    for (let i in this.option.other_column_options) this.tname_list.push(undefined);

    //如果column_options是数组，就不管other_column_options，如果是对象，还得看other_column_options
    if (column_options instanceof Array) {
        for (let index in column_options) {
            let th_tag = document.createElement("th")
            let tname = column_options[index]
            th_tag.setAttribute("tname", tname)
            th_tag.level = index;
            th_tag.innerText = tname

            this.fields_obj[tname] = th_tag;
            this.tname_list[index] = th_tag.innerText;
        }
        if (this.option.other_column_options == new Object()) {
            throw "普通字段是数组的情况下，批量字段不可用";
        }
    } else {
        for (let tname in column_options) {
            // 优先找func，没有，找name,
            let th_tag = document.createElement("th");
            if (column_options[tname].has_tname === undefined || column_options[tname].has_tname === true)
                th_tag.setAttribute("tname", tname);

            if (column_options[tname].width) th_tag.setAttribute("width", column_options[tname].width);
            // if(column_options[tname].colspan) th_tag.setAttribute("colspan", column_options[tname].colspan);

            if (column_options[tname].func === undefined) {
                th_tag.innerText = column_options[tname].name;
            } else {
                th_tag.innerHTML = column_options[tname].func();
            }


            fields_obj[tname] = th_tag;
            this.tname_list[column_options[tname].level] = tname;
        }
        for (let tname in other_column_options) {
            let th_tag = document.createElement("th");
            if (other_column_options[tname].has_tname === true || other_column_options[tname].has_tname === undefined)
                th_tag.setAttribute("tname", tname);

            if (other_column_options[tname].width) th_tag.setAttribute("width", other_column_options[tname].width);


            if (other_column_options[tname].func === undefined) {
                th_tag.innerText = other_column_options[tname].name;
            } else {
                th_tag.innerHTML = other_column_options[tname].func();
            }
            th_tag.body_func = other_column_options[tname].body_func;

            fields_obj[tname] = th_tag;
            this.tname_list[other_column_options[tname].level] = tname;
        }
    }

    for (let tname of this.tname_list) {

        theadtr_tag.appendChild(fields_obj[tname]);
    }


}

/**
 * 普通的渲染一个
 * @param {*} row
 */
TableBuilder.prototype.renderone = function (row) {
    let tr_array = this.tr_array;
    let tr_tag = document.createElement("tr");
    let td_li = new Array();
    let tname_list = this.tname_list;
    let fields_obj = this.fields_obj;
    if (row instanceof Array) {
        for (let data of row) {
            let td_tag = document.createElement("td");
            if (data instanceof Function) {
                td_tag.innerHTML = data();
            } else {
                td_tag.innerText = data;
            }
        }
    } else {
        for (var i in this.tname_list) {
            td_li.push("");
        }

        /**
         * 插入other_column_option的内容
         */
        var other_column_options = this.option.other_column_options;
        for (var level in tname_list) {
            let tname = tname_list[level];

            if (fields_obj[tname].body_func) {
                let td_tag = document.createElement("td");
                td_tag.innerHTML = fields_obj[tname].body_func(row);
                td_li[level] = td_tag;
            }
        }

        for (let key in row) {
            let level = this.tname_list.indexOf(key);
            if (level !== -1) {
                let td_tag = document.createElement("td");
                if (typeof row[key] === "string" || typeof row[key] === "number") {
                    td_tag.innerText = row[key];
                } else if (row[key] instanceof Function) {
                    td_tag.innerHTML = row[key](row);
                } else {

                    td_tag.innerText = row[key].value;
                    if (row[key].colspan) td_tag.setAttribute("colspan", row[key].colspan);
                    if (row[key].rowspan) td_tag.setAttribute("rowspan", row[key].rowspan);
                    if (row[key].style) td_tag.setAttribute("style", row[key].style);


                }
                td_li[level] = td_tag;
            }

        }
    }

    for (let level in td_li) {
        tr_tag.appendChild(td_li[level]);

    }
    tr_array.push(tr_tag);


}


/**
 * 渲染多个
 * @param {*} row_arr
 */
TableBuilder.prototype.rendermany = function (row_arr) {
    for (let row of row_arr) {
        this.renderone(row);
    }
}

/**
 * 渲染一个row是数组的
 * @param {*} row
 */
TableBuilder.prototype.renderarray = function (row) {
    let tr_array = this.tr_array;

    if (row instanceof Array) {
        let tr_tag = document.createElement("tr");
        let td_li = new Array();
        for (let data of row) {
            if (data instanceof Function) {
                td_li.push(data())
            } else {
                td_li.push("<td>" + data + "</td>");
            }
        }

        tr_tag.innerHTML = td_li.join("");
        tr_array.push(tr_tag);
    } else {
        throw "如果没有普通字段，每条记录只能是array"
    }
}

/**
 * 渲染详细列表
 */
TableBuilder.prototype.rendervalign = function (row) {
    let tr_array = this.tr_array;
    let tr_tag = document.createElement("tr");
    let td_arr = new Array();

    if (row instanceof Array) {
        if (row[1] instanceof Array) {
            if (this.option.valign) {
                let rowspan = row[1].length;
                td_arr.push("<td tname=\"" + row[0] + "\" rowspan=\"" + rowspan + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row[0] + "</td>");
                if (row[1].length == 0) {
                    td_arr.push("<td></td>")
                } else {
                    td_arr.push("<td>" + row[1][0] + "</td>")
                }

                tr_tag.innerHTML = td_arr.join("");
                tr_array.push(tr_tag);

                for (let i in row[1]) {
                    if (i != 0) {
                        let tr_tag = document.createElement("tr");
                        let td_arr = new Array();
                        td_arr.push("<td>" + row[1][i] + "</td>");
                        tr_tag.innerHTML = td_arr.join("");
                        tr_array.push(tr_tag);
                    }
                }

            } else {
                td_arr.push("<td tname=\"" + row[0] + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row[0] + "</td>");
                let colspan = this.colspan;
                let row_length = row[1].length;
                if (row_length == 0) {
                    td_arr.push("<td colspan=\"" + colspan + "\"></td>");
                }
                for (let i in row[1]) {
                    if (i == row_length - 1) {
                        let delta = colspan - i;
                        td_arr.push("<td colspan=\"" + delta + "\">" + row[1][i] + "</td>");
                    } else {
                        td_arr.push("<td>" + row[1][i] + "</td>");
                    }
                }
                tr_tag.innerHTML = td_arr.join("");
                tr_array.push(tr_tag);
            }

        } else if (row[1] instanceof Function) {
            td_arr.push("<td tname=\"" + row[0] + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row[0] + "</td>");
            if (!this.option.valign) {
                td_arr.push("<td colspan=\"" + (this.colspan != 1 ? this.colspan : "") + "\">" + row[1]() + "</td>");
            } else {
                td_arr.push("<td>" + row[1]() + "</td>");
            }
            tr_tag.innerHTML = td_arr.join("");
            tr_array.push(tr_tag);
        } else {
            td_arr.push("<td tname=\"" + row[0] + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row[0] + "</td>");
            if (!this.option.valign) {
                td_arr.push("<td colspan=\"" + (this.colspan != 1 ? this.colspan : "") + "\">" + row[1] + "</td>");
            } else {
                td_arr.push("<td>" + row[1] + "</td>");
            }
            tr_tag.innerHTML = td_arr.join("");
            tr_array.push(tr_tag);
        }
    } else {
        if (row.value instanceof Array) {
            if (this.option.valign) {
                let rowspan = row.value.length;
                td_arr.push("<td tname=\"" + row.tname + "\" rowspan=\"" + rowspan + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row.name + "</td>");
                if (row.value.length == 0) {
                    td_arr.push("<td></td>")
                } else {
                    td_arr.push("<td>" + row.value[0] + "</td>")
                }
                tr_tag.innerHTML = td_arr.join("");
                tr_array.push(tr_tag);
                for (let i in row.value) {
                    if (i != 0) {
                        tr_tag = document.createElement("tr");
                        td_arr = new Array();
                        td_arr.push("<td>" + row.value[i] + "</td>");
                        tr_tag.innerHTML = td_arr.join("");
                        tr_array.push(tr_tag);

                    }

                }

            } else {
                let colspan = this.colspan;  // 整个数据中元素最多的记录

                td_arr.push("<td tname=\"" + row.tname + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row.name + "</td>");
                let row_length = row.value.length;  //3 4
                if (row.value.length == 0) {
                    td_arr.push("<td colspan=\"" + colspan + "\"></td>")
                }
                for (let i in row.value) {
                    if (i == row_length - 1) {
                        let delta = colspan - i;
                        td_arr.push("<td colspan=\"" + delta + "\">" + row.value[i] + "</td>");
                    } else {
                        td_arr.push("<td>" + row.value[i] + "</td>");
                    }
                }
                tr_tag.innerHTML = td_arr.join("");
                tr_array.push(tr_tag);
            }

        } else if (row.value instanceof Function) {
            td_arr.push("<td tname=\"" + row.tname + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row.name + "</td>");
            //td_arr.push("<td colspan=\""+(this.colspan != 1 ? this.colspan : "")+"\">"+row.value()+"</td>");
            if (!this.option.valign) {
                td_arr.push("<td colspan=\"" + (this.colspan != 1 ? this.colspan : "") + "\">" + row.value() + "</td>");
            } else {
                td_arr.push("<td>" + row.value() + "</td>");
            }
            tr_tag.innerHTML = td_arr.join("");
            tr_array.push(tr_tag);
        } else {
            //td_arr.push("<td colspan=\""+(this.colspan != 1 ? this.colspan : "")+"\">"+row.value+"</td>");
            td_arr.push("<td tname=\"" + row.tname + "\" width=\"" + (this.option.tname_width ? this.option.tname_width : "") + "\">" + row.name + "</td>");
            if (!this.option.valign) {
                td_arr.push("<td colspan=\"" + (this.colspan != 1 ? this.colspan : "") + "\">" + row.value + "</td>");
            } else {
                td_arr.push("<td>" + row.value + "</td>");
            }
            tr_tag.innerHTML = td_arr.join("");
            tr_array.push(tr_tag);
        }

    }
}
TableBuilder.prototype.render = function (row) {

    if (this.option.module == 2) {
        let data_array = this.data_array;
        this.colspan = 1;
        for (let row of data_array) {
            if (row instanceof Array) {
                if (row[1] instanceof Array) {
                    if (this.colspan < row[1].length) {
                        this.colspan = row[1].length;
                    }
                }
            } else if (row instanceof Object) {

                if (row.value instanceof Array) {
                    if (this.colspan < row.value.length) {
                        this.colspan = row.value.length;
                    }
                }
            }
        }

        for (let row of data_array) {
            this.rendervalign(row);
        }
    } else {
        if (row) {
            if (this.option.column_options) {
                this.renderone(row);
                if (this.search_tag) {
                    this.search(this.search_tag.getElementsByTagName("input")[0].value);
                }
            } else {
                this.renderarray(row);
            }
        } else {
            let data_array = this.data_array;
            if (this.option.column_options) {
                this.rendermany(data_array)


            } else {
                //只能是array
                for (let row of data_array) {
                    this.renderarray(row);

                }
            }
        }
    }


}

/**
 * 更改
 * @param {*} sfs
 */
TableBuilder.prototype.ch_searchfield = function (sfs) {
    for (let sf of sfs) {
        let index = this.column_li.indexOf(sf);
        if (index == -1) {
            throw "field not in the table fields"
        }
    }
    try {
        if (this.search_tag) {
            this.search_fields = sfs;
            this.search(this.search_tag.getElementsByTagName("input")[0].value);
            this.appendrow_batch(1)
        } else {
            throw "search tag not found!"
        }
    } catch (arr) {
    }
}

TableBuilder.prototype.ch_prcound = function (num) {
    try {
        if (this.page_tag) {
            this.option.page_row_count = num;
            if (this.search_tag) {
                this.search(this.search_tag.getElementsByTagName("input")[0].value);
            }
            this.appendrow_batch(1)
        } else {
            throw "page tag not found!"
        }
    } catch (arr) {
    }
}

/**
 * 插入一行，
 * data_rows = [1,2,3,4]
 * @param {*} data_row
 */
TableBuilder.prototype.append_row = function (data_row) {
    if (data_row instanceof Element) {
        this.table_tag.getElementsByTagName("tbody")[0].appendChild(data_row);
    } else {
    }
}

TableBuilder.prototype.appendrow_batch = function (page) {
    this.clearTbody();
    let tr_array;
    if (this.search_tag) {
        tr_array = this.search_data;
    } else {
        tr_array = this.tr_array
    }

    //每页数据
    if (this.page_tag) {
        this.column_count = this.data_array.length;
        this.current_page = page;
        this.start_row = (page - 1) * this.page_row_count;
        this.stop_row = page * this.page_row_count;
        tr_array = tr_array.slice(this.start_row, this.stop_row);
    }
    for (let i of tr_array) {
        this.append_row(i);
    }

    //页码生成
    this.paginate();
}


TableBuilder.prototype.clearTbody = function () {
    this.table_tag.getElementsByTagName("tbody")[0].innerHTML = "";
}

/**
 * 页码生成函数
 * <ul class="pagination-list">
 <li><a class="pagination-link" aria-label="Goto page 1">1</a></li>
 <li><span class="pagination-ellipsis">&hellip;</span></li>
 <li><a class="pagination-link" aria-label="Goto page 45">45</a></li>
 <li><a class="pagination-link is-current" aria-label="Page 46" aria-current="page">46</a></li>
 <li><a class="pagination-link" aria-label="Goto page 47">47</a></li>
 <li><span class="pagination-ellipsis">&hellip;</span></li>
 <li><a class="pagination-link" aria-label="Goto page 86">86</a></li>
 </ul>
 * @param {*} page_li
 */
TableBuilder.prototype.paginate = function () {
    let page_list = [];
    for (let i = 0; i < this.page_count; i++) {
        page_list.push(i + 1);
    }
    page_list = this.get_pglist(page_list);
    let page_html_list = ["<ul class=\"pagination-list\">"];
    if (this.current_page - 1 != 0) {
        page_html_list.push("<li><a class=\"pagination-link\" onclick=\"" + this.option.object_name + ".appendrow_batch(" + (this.current_page - 1) + ")\">上一页</a></li>");
    }
    for (let i of page_list) {
        if (this.current_page == i) {
            page_html_list.push("<li><a class=\"pagination-link is-current\">" + i + "</a></li>")
        } else if (this.current_page == "...") {
            page_html_list.push("<li><span class=\"pagination-ellipsis\">&hellip;</span></li>")
        } else {
            page_html_list.push("<li><a class=\"pagination-link\" onclick=\"" + this.option.object_name + ".appendrow_batch(" + i + ")\">" + i + "</a></li>")
        }

    }

    if (this.current_page + 1 <= this.page_count) {
        page_html_list.push("<li><a class=\"pagination-link\" onclick=\"" + this.option.object_name + ".appendrow_batch(" + (this.current_page + 1) + ")\">下一页</a></li>");
    }
    page_html_list.push("</ul>")
    if (this.page_tag instanceof Element) {
        this.page_tag.innerHTML = page_html_list.join("");
    }


}

/**
 * 分页模式1
 * @param {*} pg_array
 */
TableBuilder.prototype.get_pglist = function (pg_array) {
    let page_list = [];
    let page_range_size = 3;

    if (this.page_count <= 5) {

        for (let page in pg_array) {
            page_list.push(parseInt(page) + 1);
        }
    } else {
        if (this.current_page <= 3) {
            page_list.push(1);
            page_list.push(2);
            page_list.push(3);
            page_list.push(4);
            page_list.push("...");
            page_list.push(this.page_count);

        }
        else if (this.current_page >= this.page_count - 2) {
            page_list.push(1);
            page_list.push("...");
            page_list.push(this.page_count - 3);
            page_list.push(this.page_count - 2);
            page_list.push(this.page_count - 1);
            page_list.push(this.page_count);
        } else {
            page_list.push(1);
            page_list.push("...");
            page_list.push(this.current_page - 1);
            page_list.push(this.current_page);
            page_list.push(this.current_page + 1);
            page_list.push("...");
            page_list.push(this.page_count);
        }

    }
    return page_list

}

TableBuilder.prototype.search = function (keyword) {
    let search_data = []
    for (let data of this.tr_array) {
        if (data instanceof Element) {
            let tds = data.getElementsByTagName("td");

            for (let field of this.search_fields) {
                let index = this.tname_list.indexOf(field);
                if (tds[index].innerText.match(keyword)) {
                    search_data.push(data);
                    break;
                }
            }

        }
    }
    if (search_data.length != 0) {
        this.data_array_length = search_data.length;
        this.search_data = search_data;
    } else {
        if (keyword) {
            this.search_data = [];
            this.data_array_length = search_data.length;
        } else {
            this.search_data = this.tr_array;
            this.data_array_length = this.tr_array.length;
        }
    }
    this.current_page = 1;
    this.page_row_count = this.option.page_row_count || 10;

    this.page_count = parseInt(this.data_array_length / this.page_row_count);
    this.last_page_row_rount = this.data_array_length % this.page_row_count;
    if (this.last_page_row_rount != 0) {
        this.page_count += 1
    }
    this.appendrow_batch(1);
}

/**
 * 查找checkbox打勾的元素，只能找每一行的第一个input
 * @param {*} attr
 */
TableBuilder.prototype.get_check = function (attr) {

    let check_trs = new Array();

    for(let tr of this.tr_array){
        let input = tr.getElementsByTagName("input")[0]
        if(input.checked){
            check_trs.push(input.getAttribute(attr));
        }
    }
    return check_trs;
}
TableBuilder.prototype.get_check2 = function (fields) {

    let tr_arr = new Array();

    for(let tr of this.tr_array){
        let input = tr.getElementsByTagName("input")[0];
        if(input.checked){
            let item_arr = new Array();

            let tds = tr.getElementsByTagName("td");
            for(let field of fields){

                item_arr.push(tds[field].innerText);
            }
            tr_arr.push(item_arr);
        }

    }


    return tr_arr
}

