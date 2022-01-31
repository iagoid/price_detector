document.onclick = hideMenu;
document.oncontextmenu = rightClick;

function hideMenu() {
    document.getElementById("contextMenu")
        .style.display = "none"
}

function rightClick(e) {
    var x = event.clientX
    var y = event.clientY
    var elementMouseIsOver = document.elementFromPoint(x, y);
    var parent = $(elementMouseIsOver).parent()
    var id = parent.data("identifier")

    if (id) {
        e.preventDefault();

        if ($("#contextMenu").css("display") == "block") {
            hideMenu();
        } else {
            var menu = $("#contextMenu")
            var deleteLink = $("#delete__link")
            deleteLink.attr('href', `/delete/${id}`)
            menu.css("display", 'block')
            menu.css("left", e.pageX + "px")
            menu.css("top", e.pageY + "px")
        }
    }
}