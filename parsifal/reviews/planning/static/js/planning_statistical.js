$(function () {
  $(".btn-save-statistical-methods").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/planning/save_statistical_methods/',
      data: $('#form-statistical-methods').serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(btn).ajaxEnable();
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $(btn).ajaxEnableError();
        $.parsifal.alert("Um erro ocorreu", jqXHR.responseText);
      }
    });
  });
});