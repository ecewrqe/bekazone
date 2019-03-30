/**
 * to verify title name is repeat
 * @param {any} itm: current target
 */
function check_title_repeat(itm) {
    var inp_value = $(itm).val();
    var original_title = $(itm).attr("original");
    if (original_title && original_title == inp_value) {
        $("#title_msg").empty();
        return;
    }

    $.ajax({
        url: "/blog-backend/blog-title-verify/",
        type: "POST",
        data: { "value": inp_value, "typ": "normal" },
        dataType: "JSON",
        success: function (data) {
            if (data.status == 0) {
                var msg_tag = `<span class="text-success"><i class="fa fa-check"></i></span>`
                $(itm).parent().siblings()[1].innerHTML = msg_tag
            } else {
                var msg_tag = `<span class="text-danger"><i class="fa fa-exclamation"></i></span>`
                $(itm).parent().siblings()[1].innerHTML = msg_tag

            }
        }
    })
}


function kind_repeat_verify(itm, verify_field) {
    var value = $(itm).val();
    $.ajax({
        url: "/blog-backend/verify-kind/",
        type: "POST",
        data: { "verify_field": verify_field, "value": value },
        dataType: "JSON",
        success: function (data) {
            var judgement = data.data;
            var parent_tag = $(itm).parent().siblings()[1];
            if (judgement == "ok") {
                var tag = `<span class="text-success"><i class="fa fa-check"></i></span>`;
                console.log(tag)
                parent_tag.innerHTML = tag;
                $(itm).attr("err", "0");
            } else {
                console.log($(itm).parent().siblings());
                var tag = `<span class="text-danger"><i class="fa fa-exclamation"></i></span>`;
                console.log(tag)
                parent_tag.innerHTML = tag;
                $(itm).attr("err", "1");
            }
        }
    })
}

/**
 * submit to create kind
 * @param {any} typ: redi/unredi
 * redi: redirect 
 * unredi: unredirect
 */
function submit_kind_create_form(typ) {
    var name = $("#kind_name").val();

    if (!name) {
        $("#kind_create_msg").text("name must be not empty");
        setTimeout(function () {
            $("#kind_create_msg").text("");
        }, 500)
        return;
    }
    var name_err = $("#kind_name").attr("err");
    var alias_err = $("#kind_alias").attr("err");
    if (name_err == "1" || alias_err == "1") {
        $("#kind_create_msg").text("create failure");
        setTimeout(function () {
            $("#kind_create_msg").text("");
        }, 500)
        return;
    }
    var kc_send_ser = $("#kind_create").serialize();
    $.ajax({
        url: "/blog-backend/kind-list/",
        type: "POST",
        data: kc_send_ser,
        dataType: "JSON",
        success: function (data) {

            if (data.status == 0) {
                if (typ == "redi") {
                    location.href = data.url;
                } else {
                    var kd_sel = document.getElementById("blog_kind_select");
                    var op = document.createElement("option");
                    op.value = data.id;
                    op.innerText = data.name;
                    op.selected = true;
                    console.log(op)
                    $(kd_sel).append(op);
                    console.log(kd_sel);
                    $('#blog_kind_select').trigger("chosen:updated");
                    

                }
                
            } else {
                $("#kind_create_msg").text(data.data);
                setTimeout(function () {
                    $("#kind_create_msg").text("");
                }, 500)
            }
        }
    })
    return false;

}

/**
 * delete selected kinds, output the delete dialog
 * if those selected kinds are having relactived blog,
 * else
 * 0: can delete
 * 1: can't delete
 * 300: has exception
 * */
function kind_delete() {
    var name_list = [];
    // collect selected kindname
    $("#kind_list").children(".active").each(function () {
        var name = $(this).text();
        name_list.push(name);
    })
    var msg = "";
    var button_config = {};
    // verify relatived blog
    if (name_list.length == 0) {
        return;
    }
    $.ajax({
        url: "/blog-backend/verify-related/",
        type: "POST",
        data: { typ: "k_b", name_list: JSON.stringify(name_list) },
        dataType: "JSON",
        success: function (data) {
            if (data.status == 0) {
                // can delete
                msg = "kind:<span class='text-danger'>";
                msg += name_list.join(",");
                msg += "</span> will be deleted";
                button_config = {
                    "confirm": {
                        label: "confirm",
                        className: "btn-primary",
                        callback: function () {

                            $.ajax({
                                url: "/blog-backend/kind-delete/",
                                type: "POST",
                                data: { "name_list": JSON.stringify(name_list) },
                                dataType: "JSON",
                                success: function (data) {
                                    console.log(data);
                                    location.reload();
                                }
                            })
                        }
                    },
                    "cancel": {
                        label: "cancel",
                        className: "btn-default",

                    }
                }

            } else if (data.status == 1) {
                //cannot delete
                msg = `kind: <span class="text-danger">${data.name}</span> has related cannot delete`
                button_config = {
                    "cancel": {
                        label: "cancel",
                        className: "btn-default",

                    }
                }
            } else {
                msg = `name is error`
                button_config = {
                    "cancel": {
                        label: "cancel",
                        className: "btn-default",
                    }
                }
            }
            
            bootbox.dialog({
                "title": "warning",
                "message": msg,
                "buttons": button_config
            });
            
        }
    })

    


}
/**
 * 
 * @param {any} typ
 * redi: redirect
 * unredi: unredirect
 */
function submit_tag_create_form(typ) {
    
    var name = $("#tag_name").val();
    if (!name) {
        $("#tag_create_msg").text("name must be not empty");
        setTimeout(function () {
            $("#tag_create_msg").text("");
        }, 500)
        return;
    }
    $.ajax({
        url: "/blog-backend/tag-list/",
        type: "POST",
        data: { "name": name },
        dataType: "JSON",
        success: function (data) {
            if (typ == "redi") {
                location.reload();
            } else {
                //undirect
                var kd_sel = document.getElementById("blog_tag");
                var op = document.createElement("option");
                op.value = data.id;
                op.innerText = data.name;
                op.selected = true;
                console.log(op)
                $(kd_sel).append(op);
                console.log(kd_sel);
                $('#blog_tag').trigger("chosen:updated");
            }
            
        }
    })
}
function tag_repeat_verify(itm) {
    var name = $(itm).val();
    console.log(name);
    $.ajax({
        url: "/blog-backend/verify-tag/",
        type: "POST",
        data: { "name": name },
        dataType: "JSON",
        success: function (data) {

            var parent_tag = $(itm).parent().siblings()[1];

            if (data.status == 0) {
                var tag = `<span class="text-success"><i class="fa fa-check"></i></span>`;

                parent_tag.innerHTML = tag;
                $(itm).attr("err", "0");
            } else {

                var tag = `<span class="text-danger"><i class="fa fa-exclamation"></i></span>`;

                parent_tag.innerHTML = tag;
                $(itm).attr("err", "1");
            }
        }
    })
}



function tag_delete() {
    var name_list = [];
    $("#tag_box").children(".active").each(function () {
        var name = $(this).text()
        name_list.push(name)
    })

    if (name_list.length == 0) {
        return;
    }

    $.ajax({
        url: "/blog-backend/verify-related/",
        type: "POST",
        data: { typ: "t_b", name_list: JSON.stringify(name_list) },
        dataType: "JSON",
        success: function (data) {
            if (data.status == 0) {
                msg = "tag:<span class='text-danger'>";
                msg += name_list.join(",");
                msg += "</span> will be deleted, are you sure";
                button_config = {
                    "confirm": {
                        label: "confirm",
                        className: "btn-primary",
                        callback: function () {

                            $.ajax({
                                url: "/blog-backend/tag-delete/",
                                type: "POST",
                                data: { "name_list": JSON.stringify(name_list) },
                                dataType: "JSON",
                                success: function (data) {
                                    console.log(data);
                                    location.reload();
                                }
                            })
                        }
                    },
                    "cancel": {
                        label: "cancel",
                        className: "btn-default",

                    }
                }
            } else if (data.status == 1) {
                msg = `tag: <span class="text-danger">${data.name}</span> has related cannot delete`;
                button_config = {
                    "cancel": {
                        label: "cancel",
                        className: "btn-default",

                    }
                }
            } else {
                msg = `name is error`
                button_config = {
                    "cancel": {
                        label: "cancel",
                        className: "btn-default",

                    }
                }
            }
            bootbox.dialog({
                "title": "warning",
                "message": msg,
                "buttons": button_config
            });
        }
        
    })

    
    

}
