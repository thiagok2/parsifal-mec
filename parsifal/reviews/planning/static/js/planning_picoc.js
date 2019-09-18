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
        $.parsifal.alert("Problemas aconteceram", "Algo deu errado! Por favor entre em contato com o administrador1.");
      }
    });
  });
  
  function update_inputs(pico_type){
	  if(pico_type == 'PICOC'){
    	  $('.picos').hide();
    	  $('.pico_free').hide();
    	  
    	  $('.picoc').show();
    	  $('.picoc').removeClass('hidden');
    	  $('.pico_type_title').text('PICOC');
      }else if(pico_type == 'PICOS'){
    	  $('.pico_free').hide();
    	  $('.picoc').hide();
    	  
    	  $('.picos').show();
    	  $('.picos').removeClass('hidden');
    	  $('.pico_type_title').text('PICOS');
      }else if(pico_type == 'Free Text'){
    	  $('.picoc').hide();
    	  $('.picos').hide();
    	  $('.pico_free').show();
    	  $('.pico_free').removeClass('hidden');
    	  $('.pico_type_title').text('Texto Livre');
      }
	  
	
	  
	  
  }
  
  $('.list-group a').click(function(e) {
      e.preventDefault()

      $that = $(this);
      
      var review_id = $('#review-id').val();
      var pico_type = $(this).attr('data-pico-value');
      $('#pico_type').val(pico_type);
      $("input[id=pico_type]").val(pico_type);
      
      update_inputs(pico_type);
      
      
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
            $.parsifal.alert("Problemas aconteceram", "Algo deu errado! Por favor entre em contato com o administrador2.");
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
	       
	        if($.parseJSON(data.toLowerCase().trim()))
	        	$('#import-pico-msg').html('Definição dos métodos de pesquisa compartilhados com sucesso.');
	        else{
	        	$('#import-pico-msg').html('Compartilhamento removido com sucesso.');
	        }
	        	
	      }
	    });
  });
  
  $("#btn-modal-import-pico").click(function () {
  	$.ajax({
  		url: '/reviews/planning/suggested_pico/',
  		data: { 'review-id': $('#review-id').val() },
  		cache: false,
  		type: 'get',
  		success: function (data) {
	        
  			$("#modal-suggested-pico table tbody").html(data);
  			$("#modal-suggested-pico").before("<div class='shade'></div>");
  			$("#modal-suggested-pico").slideDown(400, function () {
  				$("body").addClass("modal-open");
  			});
  		}
	   });
  });
  
  $("table#tbl-import-pico").on("click", "tbody tr", function () {
  	
      var hiddenClass = $(this)[0].nextElementSibling;
      hiddenClass.className == "hidden"
      ? hiddenClass.className = ""
      : hiddenClass.className = "hidden"
  });
  
  $("table#tbl-import-pico").on("click", "#btn-import-pico", function () {
	  var ref_review_id = $(this).data("review-ref-id");
	  var ref_review_title = $(this).data("review-ref-title");
	  var review_id = $("#review-id").val();
	  
	  $.ajax({
          url: '/reviews/planning/import_pico/',
          data: {
          	'review-id': review_id,
            'ref-review-id': ref_review_id,
          },
          type: 'get',
          cache: false,
          success: function (data) {
              //alert(JSON.stringify(data));
        	 
    		  $('#population').val(data.population);
        	  $('#intervention').val(data.intervention);
        	  $('#comparison').val(data.comparison);
        	  $('#outcome').val(data.outcome);
        	  $('#context').val(data.outcome);
        	  $('#study_type').val(data.study_type); 
        	  $('#pico_text').text(data.pico_text);
        	  
        	  $('#import-pico-msg').html('Definição do métodos de pesquisa importados com sucesso. Referência: '+ ref_review_title);
        	  $("input[id=pico_type]").val(data.pico_type);
        	  
        	  update_inputs(data.pico_type);
        	  
              $("#modal-suggested-pico").modal("hide");
          }
      });
  });
  
});