$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-minor").modal("show");
      },
      success: function (data) {
        $("#modal-minor .modal-content").html(data.html_form);
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
          $("#datatables-example tbody").html(data.html_minor_list);
          $("#modal-minor").modal("hide");
          swal("New Minor Course!", "Added Successfully!", "success");
//          alert("minor Course!");
        }
        if (data.form_is_not_valid) {
          $("#datatables-example tbody").html(data.html_minor_list);
          $("#modal-minor").modal("show");
          swal("Form Error", "Please Fill the form Correctly", "error");
        }
        if (data.registered) {
          $("#datatables-example tbody").html(data.html_minor_list);
          $("#modal-minor").modal("show");
          swal("Redundancy", "You cant register twice for the same course", "error");
        }
        if (data.minor_deleted) {
          $("#datatables-example tbody").html(data.html_minor_list);
          $("#modal-minor").modal("hide");
          swal("Minor", "Dropped Successfully", "success");
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create minor
  $(".js-create-minor").click(loadForm);
  $("#modal-minor").on("submit", ".js-minor-create-form", saveForm);

  // Update minor
  $("#datatables-example").on("click", ".js-update-minor", loadForm);
  $("#modal-minor").on("submit", ".js-minor-update-form", saveForm);

  // Delete minor
  $("#datatables-example").on("click", ".js-delete-minor", loadForm);
  $("#modal-minor").on("submit", ".js-minor-delete-form", saveForm);

});
