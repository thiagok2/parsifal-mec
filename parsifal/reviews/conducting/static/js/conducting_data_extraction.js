$(function () {

  function save_data_extraction_field(ref) {
    var row = $(ref).closest(".form-group");
    var review_id = $("#review-id").val();
    var article_id = $(ref).closest(".panel-body").attr("data-article-id");
    var field_id = $(row).attr("data-field-id");
    var value = $(ref).val();
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: '/reviews/conducting/save_data_extraction/',
      data: {
        'review-id': review_id,
        'article-id': article_id,
        'field-id': field_id,
        'value': value,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $("span.error", row).text('');
        $("span.error", row).hide();
        $(row).removeClass("has-error");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $("span.error", row).text(jqXHR.responseText);
        $("span.error", row).show();
        $(row).addClass("has-error");
      }
    });
  }

  $(".data-extraction-panel input[type='text'], .data-extraction-panel select, .data-extraction-panel textarea").change(function () {
    save_data_extraction_field($(this));
  });

  $(".data-extraction-panel input[type='checkbox']").click(function () {
    save_data_extraction_field($(this));
  });

  $(".data-extraction-panel").on("click", ".js-mark-as-finished", function () {
    var panel = $(this).closest(".panel");
    var article_id = $(".panel-body", panel).attr("data-article-id");
    $.ajax({
      url: '/reviews/conducting/save_data_extraction_status/',
      type: 'post',
      data: {
        'review-id': $("#review-id").val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        'article-id': article_id,
        'action': 'mark_as_done'
      },
      success: function () {
        var tab = $("#data-extraction-tab").val();
        if (tab === "all") {
          var action_button = $(".js-finished-button", panel);
          $(".glyphicon", action_button).removeClass().addClass("glyphicon glyphicon-check");
          $(".action-text", action_button).text("Marcar como não resolvido");
          $(action_button).removeClass().addClass("js-finished-button js-mark-as-not-finished");
        } 
        else {
          $(panel).fadeOut(200);
        }
      }
    });
  });

  $(".data-extraction-panel").on("click", ".js-mark-as-not-finished", function () {
    var panel = $(this).closest(".panel");
    var article_id = $(".panel-body", panel).attr("data-article-id");
    $.ajax({
      url: '/reviews/conducting/save_data_extraction_status/',
      type: 'post',
      data: {
        'review-id': $("#review-id").val(),
        'csrfmiddlewaretoken': $("input[name=csrfmiddlewaretoken]").val(),
        'article-id': article_id,
        'action': 'mark_as_undone'
      },
      success: function () {
        var tab = $("#data-extraction-tab").val();
        if (tab === "all") {
          var action_button = $(".js-finished-button", panel);
          $(".glyphicon", action_button).removeClass().addClass("glyphicon glyphicon-unchecked");
          $(".action-text", action_button).text("Marcar como resolvido");
          $(action_button).removeClass().addClass("js-finished-button js-mark-as-finished");
        } 
        else {
          $(panel).fadeOut(200);
        }
      }
    });
  });
  
  $.fn.loadActiveArticle = function () {
    var article_id = $(".article-link").attr("oid");
    var review_id = $("#review-id").val();
    var container = $(this);


    $.ajax({
      url: '/reviews/conducting/article_details_confirm/',
      data: {'review-id': review_id, 'article-id': article_id},
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(container).spinner();
      },
      success: function (data) {
    	console.log(data);
        $(container).html(data);

      },
      complete: function () {
        $(container).spinner();
      }
    });
  };
	  
  $(".article-container").on("click", ".article-link", function () {
	  
	  
      $("#modal-article .modal-body").css("height", $(window).height() * 0.7);
      $("#modal-article .modal-body").loadActiveArticle();
      $("#modal-article").modal('show');
	    
  });
  
  $(".btn-save-article").click(function () {
	  var article_id = $("#modal-article #article-id").val();
	  $.ajax({
		  url: '/reviews/conducting/save_article_details_confirm/',
	      cache: false,
	      data: $("#article-details").serialize(),
	      type: 'post',
	      beforeSend: function () {
	        $(".btn-save-article").prop("disabled", true);
	      },
	      success: function (data) {
	    	
	          $("#modal-article .alert .modal-alert").text("Artigo salvo com sucesso!");
	          $("#modal-article .alert").removeClass("alert-error").addClass("alert-success");
	          $("#modal-article .alert").removeClass("hide");
	          
	          $("#title-study-"+article_id).html($("#modal-article #title").val());
	          $("#subtitle-study-"+article_id).html($("#modal-article #author").val() + '(' +$("#modal-article #year").val()+ ')');
	         
	      },
	      error: function () {
	          $("#modal-article .alert .modal-alert").text("Algo deu errado! Isso é tudo que sabemos :(");
	          $("#modal-article .alert").removeClass("alert-success").addClass("alert-error");
	          $("#modal-article .alert").removeClass("hide");
	      },
	      complete: function () {
	        $(".btn-save-article").prop("disabled", false);
	      }
	    });
  });
  

});