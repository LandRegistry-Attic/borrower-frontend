document.getElementById('check-checkbox').disabled = true;

function myFunction(status) {
  if ($('#accept-naa').is(':checked')) {
    document.getElementById('check-checkbox').disabled = false;
  }
  else {
    document.getElementById('check-checkbox').disabled = true;
  }};
