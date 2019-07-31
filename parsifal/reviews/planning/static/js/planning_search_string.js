$(function () {

  $(".btn-suggested-search-string").click(function () {
    var form = $(this).closest("form");
    $.ajax({
      url: '/reviews/planning/generate_search_string/',
      data: { 'review-id': $("#review-id").val() },
      cache: false,
      type: 'get',
      success: function (data) {
        $(".search-string", form).val(data);
      }
    });
  });

  $(".btn-save-generic-search-string").click(function () {
    var btn = $(this);
    var form = $(this).closest("form");
    var search_string = $(".search-string", form).val();
    $.ajax({
      url: '/reviews/planning/save_generic_search_string/',
      data: $(form).serialize(),
      cache: false,
      type: 'post',
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(btn).ajaxEnable();
      },
      error: function () {
        $(btn).ajaxEnableError();
        $.parsifal.alert("An error ocurred", "Algo deu errado! Por favor entre em contato com o administrador");
      }
    });
  });

});