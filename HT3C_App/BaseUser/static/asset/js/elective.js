$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-elective").modal("show");
      },
      success: function (data) {
        $("#modal-elective .modal-content").html(data.html_form);
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
          $("#datatables-example tbody").html(data.html_elective_list);
          $("#modal-elective").modal("hide");
          swal("New elective Course!", "Added Successfully!", "success");
//          alert("elective Course!");
        }
        if (data.form_is_not_valid) {
          $("#datatables-example tbody").html(data.html_elective_list);
          $("#modal-elective").modal("show");
          swal("Form Error", "Please Fill the form Correctly", "error");
        }
        if (data.registered) {
          $("#datatables-example tbody").html(data.html_elective_list);
          $("#modal-elective").modal("show");
          swal("Redundancy", "You cant register twice for the same course", "error");
        }
        if (data.elective_deleted) {
          $("#datatables-example tbody").html(data.html_elective_list);
          $("#modal-elective").modal("hide");
          swal("elective", "Dropped Successfully", "success");
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create elective
  $(".js-create-elective").click(loadForm);
  $("#modal-elective").on("submit", ".js-elective-create-form", saveForm);

  // Update elective
  $("#datatables-example").on("click", ".js-update-elective", loadForm);
  $("#modal-elective").on("submit", ".js-elective-update-form", saveForm);

  // Delete elective
  $("#datatables-example").on("click", ".js-delete-elective", loadForm);
  $("#modal-elective").on("submit", ".js-elective-delete-form", saveForm);

});
