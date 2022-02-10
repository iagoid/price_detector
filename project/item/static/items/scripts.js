document.onclick = hideMenu;
document.oncontextmenu = rightClick;

function hideMenu() {
    document.getElementById("contextMenu")
        .style.display = "none"
}

var linkIdentifier

function rightClick(e) {
    var x = event.clientX
    var y = event.clientY
    var elementMouseIsOver = document.elementFromPoint(x, y);
    var parentMouseIsOver = $(elementMouseIsOver).parent()

    if (parentMouseIsOver.parent('a').length) {
        linkIdentifier = parentMouseIsOver.parent('a')
    } else {
        linkIdentifier = parentMouseIsOver
    }

    var id = linkIdentifier.data("identifier")

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


$(".alert").fadeTo(5000, 1, function () {
    $(this).animate({
        right: '-200px',
        opacity: 0
    }, 2000)
});


$("#delete__link").click(function (e) {
    e.preventDefault()

    var deleteLink = $("#delete__link")
    var url = deleteLink.attr('href')

    $.ajax({
        type: "get",
        url: url,
        success: function () {
            linkIdentifier.fadeOut(1000)
        }
    });
});

$(".back__to__top").click(function () {
    reload()
    $("html, body").animate({
        scrollTop: 0,
    }, "slow");
});

function reload() {
    setTimeout(function () {
        $('.leaderboard__products').fadeOut(500);
        $('.icon__back__top').fadeOut(500, function () {
            location.reload(true);
        });
    }, 0);
}