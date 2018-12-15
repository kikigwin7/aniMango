$(document).ready(function () {
    link_starto();
    archiveSize();
});

function link_starto() {
    // Initialises the mobile menu
    $('.button-collapse').sideNav({
        closeOnClick: true
    });
    // Display messages, if any
    if (typeof pageMessages == 'function') {
        pageMessages();
    }
    // Initialise select
    $('select').material_select();
    // Initialise modal
    $('.modal-trigger').leanModal();
    // Add progress to member edit form
    $('#memberedit').click(function () {
        $("#progress-container").append(
            `<div class="progress">
              <div class="indeterminate blue darken-3"></div>
          </div>`
        );
    });
}

function archiveSize() {
    $(window).on('load', function () {
        let urlTmp = window.location.pathname;
        let url = urlTmp.replace(/\/(?!.*\/).*/, '');
        if (url === "/archive/item") {
            image = document.getElementsByClassName("archive-image")[0];
            console.log(image.naturalWidth);
            console.log(image.clientWidth);
            if (image.clientWidth !== image.naturalWidth) {
                document.getElementById("resize-notification").style.display = 'block';
            }
        }
    })

}