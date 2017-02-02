(function ($) {
  var $submit = $('#submit')
  var $naa = $('#accept-naa')

  function updateButton () {
    if ($naa.is(':checked')) {
      $submit.removeAttr('disabled')
    } else {
      $submit.attr('disabled', true)
    }
  }

  $naa.on('change', updateButton)

  $(document).ready(function () {
    updateButton()
  })
})(window.jQuery)
