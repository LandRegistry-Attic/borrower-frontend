(function ($) {
  var $submit = $('#submit')
  var $naa = $('#accept-naa')
  var $agreeNaa = $('#agree-naa')
  var $errorMessageNaa = $('<p role="alert" class="error-message">Please indicate that you agree to the terms of use set out in the Network Access Agreement</p>')

  var dirty = false

  function resetForm () {
    $agreeNaa
        .closest('.form-group')
        .removeClass('error')
        .find('.error-message')
        .remove()
  }

  function updateButton () {
    if ($naa.is(':checked')) {
      $submit.removeAttr('disabled')
      $errorMessageNaa.remove()
      $agreeNaa.closest('.form-group').removeClass('error')
    } else {
      $submit.attr('disabled', true)

      if (dirty) {
        $agreeNaa.closest('.form-group').append($errorMessageNaa)

        $agreeNaa.closest('.form-group').addClass('error')
      } else {
        dirty = true
      }
    }
  }

  $naa.on('change', updateButton)
  $(document).ready(function () {
    resetForm()
    updateButton()
  })
})(window.jQuery)
