$(function () {

    $("#is-metaanalysis").change(function() {
        value = $(this).val();

        if (value === 'True') {
            $('#metaanalysis-setup').show()
        } else {
            $('#metaanalysis-setup').hide()
        }
    });

    $("#btn-save-setup").click(function () {
      var btn = $(this);
      $.ajax({
        url: '/reviews/planning/save_search_setup/',
        data: $('#form-setup').serialize(),
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
