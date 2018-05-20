$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-required").modal("show");
      },
      success: function (data) {
        $("#modal-required .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#datatables-example tbody").html(data.html_required_list);
          $("#modal-required").modal("hide");
          swal("New required Course!", "Added Successfully!", "success");
//          alert("required Course!");
        }
        if (data.form_is_not_valid) {
          $("#datatables-example tbody").html(data.html_required_list);
          $("#modal-required").modal("show");
          swal("Form Error", "Please Fill the form Correctly", "error");
        }
        if (data.registered) {
          $("#datatables-example tbody").html(data.html_required_list);
          $("#modal-required").modal("show");
          swal("Redundancy", "You cant register twice for the same course", "error");
        }
        if (data.required_deleted) {
          $("#datatables-example tbody").html(data.html_required_list);
          $("#modal-required").modal("hide");
          swal("required", "Dropped Successfully", "success");
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create required
  $(".js-create-required").click(loadForm);
  $("#modal-required").on("submit", ".js-required-create-form", saveForm);

  // Update required
  $("#datatables-example").on("click", ".js-update-required", loadForm);
  $("#modal-required").on("submit", ".js-required-update-form", saveForm);

  // Delete required
  $("#datatables-example").on("click", ".js-delete-required", loadForm);
  $("#modal-required").on("submit", ".js-required-delete-form", saveForm);

});
