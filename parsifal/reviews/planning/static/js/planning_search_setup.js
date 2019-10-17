$(function () {

    $("#is-metaanalysis").change(function() {
        value = $(this).val();

        if (value === 'True') {
            $('#metaanalysis-setup').show()
        } else {
            $('#metaanalysis-setup').hide()
        }
    });

    $("#conclusion-model").change(function() {
        value = $(this).val();

        if (value === 'COHEN') {
            $("#developmental_effects").prop('readonly', true)
            $("#teacher_effects").prop('readonly', true)
            $("#zone_desired_effects").prop('readonly', true)

            $("#no_effect").prop('readonly', false)
            $("#small_effect").prop('readonly', false)
            $("#intermediate_effect").prop('readonly', false)
            $("#large_effect").prop('readonly', false)
        } else if (value === 'HATTIE') {
            $("#developmental_effects").prop('readonly', false)
            $("#teacher_effects").prop('readonly', false)
            $("#zone_desired_effects").prop('readonly', false)

            $("#no_effect").prop('readonly', true)
            $("#small_effect").prop('readonly', true)
            $("#intermediate_effect").prop('readonly', true)
            $("#large_effect").prop('readonly', true)
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
