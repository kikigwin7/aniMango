$( document ).ready(link_starto());

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