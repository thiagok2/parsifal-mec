$(function () {
  $(".btn-save-picoc").click(function () {
    var btn = $(this);
    $.ajax({
      url: '/reviews/planning/save_picoc/',
      data: $("#picoc-form").serialize(),
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(btn).ajaxEnable();
      },
      error: function () {
        $(btn).ajaxEnableError();
        $.parsifal.alert("An error ocurred", "Algo deu errado! Por favor entre em contato com o administrador.");
      }
    });
  });
  
  $('.list-group a').click(function(e) {
      e.preventDefault()

      $that = $(this);
      
      $('#pico_type').val($(this).attr('data-pico-value'));

      $that.parent().find('a').removeClass('active');
      $that.addClass('active');
  });
  
});