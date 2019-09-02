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
        $.parsifal.alert("Problemas aconteceram", "Algo deu errado! Por favor entre em contato com o administrador.");
      }
    });
  });
  
  $('.list-group a').click(function(e) {
      e.preventDefault()

      $that = $(this);
      
      var review_id = $('#review-id').val();
      var pico_type = $(this).attr('data-pico-value');
      $('#pico_type').val(pico_type);
      $("input[id=pico_type]").val(pico_type);
      
      
      $('#pico_type_title').text(pico_type);
      
      if(pico_type == 'PICOC'){
    	  $('.picos').hide();
    	  $('.pico_free').hide();
    	  
    	  $('.picoc').show();
    	  $('.picoc').removeClass('hidden');
      }else if(pico_type == 'PICOS'){
    	  $('.pico_free').hide();
    	  $('.picoc').hide();
    	  
    	  $('.picos').show();
    	  $('.picos').removeClass('hidden');
      }else if(pico_type == 'Free Text'){
    	  $('.picoc').hide();
    	  $('.picos').hide();
    	  $('.pico_free').show();
    	  $('.pico_free').removeClass('hidden');
      }
      
      $that.parent().find('a').removeClass('active');
      $that.addClass('active');
      
      $.ajax({
          url: '/reviews/planning/setting_pico/',
          data: {
        	  'pico_type': pico_type,
        	  'review-id': review_id
          },
          type: 'get',
          cache: false,
          success: function (data) {
            $($that).ajaxEnable();
          },
          error: function () {
            $($that).ajaxEnableError();
            $.parsifal.alert("Problemas aconteceram", "Algo deu errado! Por favor entre em contato com o administrador.");
          }
        });
  });
  
  $("#btn-confirm-pico-share").click(function () {
	    var csrf_token = $("#form-pico-share input[name='csrfmiddlewaretoken']").val();
	    $.ajax({
	      url: '/reviews/planning/share_pico/',
	      data: {
	        'review-id': $('#review-id').val(),
	        'csrfmiddlewaretoken': csrf_token
	      },
	      cache: false,
	      type: 'post',
	      success: function (data) {
	        $("#modal-pico-share").modal("hide");
	      }
	    });
  
});