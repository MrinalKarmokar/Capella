$(document).ready(function(){  });

$("#seeAnotherField").change(function() {
  if ($(this).val() == "yellow_gold" || $(this).val() == "rose_gold" || $(this).val() == "white_gold") {
    $('#otherFieldDiv').show();
    $('#otherField').attr('required', '');
    $('#otherField').attr('data-error', 'This field is required.');
  } else {
    $('#otherFieldDiv').hide();
    $('#otherField').removeAttr('required');
    $('#otherField').removeAttr('data-error');
  }
});
$("#seeAnotherField").trigger("change");