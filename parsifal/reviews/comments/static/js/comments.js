$("a[id^='add-visitor-comment']").click(function () {
    var btn = $(this);
    about = btn.attr('data-about')
    $('#visitor-comment').modal('show')
    $("#visitor-comment input, textarea, select, button").prop("disabled", false)
    $('#visitor-comment input[name="about"]').val(about)
    $('#visitor-comment #about-text').text(about)
  });

$('#save-visitor-comment').click(function() {
    var btn = $(this);
    console.log($('#form-visitor-comment').serialize());
    $.ajax({
        url: '/reviews/comments/save_visitor_comment/',
        data: $('#form-visitor-comment').serialize(),
        type: 'post',
        cache: false,
        beforeSend: function () {
            $(btn).ajaxDisable();
        },
        success: function (data) {
            $(btn).ajaxEnable();
            $('#visitor-comment textarea[name="comment"]').val('')
            $('#visitor-comment select[name="to"]').val('0')
            $("#visitor-comment .alert .modal-alert").text(data);
            $("#visitor-comment .alert").removeClass("alert-error").addClass("alert-success");
            $("#visitor-comment .alert").removeClass("hide");
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $(btn).ajaxEnableError();
            $("#visitor-comment .alert .modal-alert").text("Um erro ocorreu", jqXHR.responseText);
            $("#visitor-comment .alert").removeClass("alert-success").addClass("alert-error");
            $("#visitor-comment .alert").removeClass("hide");
        }
    });
});

$('#save-new-comment').click(function() {
    var btn = $(this);
    console.log($('#form-add-new-comment').serialize());
    $.ajax({
        url: '/reviews/comments/save_visitor_comment/',
        data: $('#form-add-new-comment').serialize(),
        type: 'post',
        cache: false,
        beforeSend: function () {
            $(btn).ajaxDisable();
        },
        success: function (data) {
            $(btn).ajaxEnable();
            $('#form-add-new-comment textarea[name="comment"]').val('')
            $('#answers').append(data)
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $(btn).ajaxEnableError();
        }
    });
});

$('*[data-href]').on('click', function() {
    window.location = $(this).data("href");
});
