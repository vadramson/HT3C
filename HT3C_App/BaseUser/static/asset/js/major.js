$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-major").modal("show");
      },
      success: function (data) {
        $("#modal-major .modal-content").html(data.html_form);
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
          $("#datatables-example tbody").html(data.html_major_list);
          $("#modal-major").modal("hide");
          swal("New Major Course!", "Added Successfully!", "success");
//          alert("Major Course!");
        }
        if (data.form_is_not_valid) {
          $("#datatables-example tbody").html(data.html_major_list);
          $("#modal-major").modal("show");
          swal("Form Error", "Please Fill the form Correctly", "error");
        }
        if (data.registered) {
          $("#datatables-example tbody").html(data.html_major_list);
          $("#modal-major").modal("show");
          swal("Redundancy", "You cant register twice for the same course", "error");
        }
        if (data.major_deleted) {
          $("#datatables-example tbody").html(data.html_major_list);
          $("#modal-major").modal("hide");
          swal("Major", "Dropped Successfully", "success");
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create major
  $(".js-create-major").click(loadForm);
  $("#modal-major").on("submit", ".js-major-create-form", saveForm);

  // Update major
  $("#datatables-example").on("click", ".js-update-major", loadForm);
  $("#modal-major").on("submit", ".js-major-update-form", saveForm);

  // Delete major
  $("#datatables-example").on("click", ".js-delete-major", loadForm);
  $("#modal-major").on("submit", ".js-major-delete-form", saveForm);

});
