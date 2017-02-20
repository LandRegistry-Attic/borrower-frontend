(function ($) {
  var count = 0
  var interval = 5000
  var maxTries = 12

  // The behaviour is bound to this data attribute. If it's not present, bail out
  if (!$('[data-confirming-deed]').length) {
    return
  }

  // Call our main endpoint via ajax
  // This kicks off the call to deed api
  $.ajax({
    dataType: 'json',
    method: 'POST',
    cache: false,
    data: {
      auth_code: $('input[name="auth_code"]').val()
    },
    url: 'verify-auth-code',
    timeout: interval * maxTries, // Make it wait for the full duration
    success: function (data) {
      if (data.error) {
        window.location = data.redirect
      }
    }
  })

  // Function to check the status of the request periodically
  function checkDeedIsSigned () {
    count++

    // Call our checking endpoint via ajax
    $.ajax({
      dataType: 'json',
      method: 'GET',
      cache: false,
      url: 'confirm-mortgage-is-signed',
      success: function (data) {
        // If it's ready, redirect, otherwise go round again
        if (data.result) {
          window.location = data.redirect
        }
        // If error occurs redirect to error page
        if (data.error) {
          window.location = data.redirect
        }
      }
    })

    if (count < maxTries) {
      setTimeout(checkDeedIsSigned, interval)
    } else {
      window.location = 'service-unavailable/deed-not-confirmed'
    }
  }

  // Every 5 seconds check again
  setTimeout(checkDeedIsSigned, interval)
})(window.jQuery)
