/**
 * Created by Qiansen on 17-1-18.
 */
$(document).ready(function () {
    $("#cancel").click(function () {
        window.location.href = '/';
    });
});

function closeMsg() {
    $(".container").hide();
}

function chStatus(todo_id) {
    $.post("/chstatus?todo_id=" + todo_id);
    window.location.reload();
}

function delTodo(todo_id) {
    $.post("/deltodo?todo_id=" + todo_id);
    window.location.reload();
}

function chPerm(user_id) {
    $.post("/chperm?user_id=" + user_id);
    window.location.reload();
}

function delResetUser(user_id) {
    $.post("/deluser?user_id=" + user_id);
    window.location.reload();
}