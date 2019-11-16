$(function () {

  $('.date').mask('99/99/9999');
  /*
  .focusout(function (event) {  
      var target, phone, element;  
      target = (event.currentTarget) ? event.currentTarget : event.srcElement;  
      phone = target.value.replace(/\D/g, '');
      element = $(target);  
      element.unmask();  
    
      element.mask("99/99/9999");  
      
  });
  */
	
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
    var is_empirical_value = $(this).data("empirical");

    if (is_empirical_value !== undefined) {
        save_empirical_value_fields($(this))
    } else {
        save_data_extraction_field($(this));
    }
  });

  $(".data-extraction-panel input[type='checkbox']").click(function () {
    checkbox_id = $(this)[0].id;

    if (checkbox_id === 'ck-empirical-data') {
        save_empirical_data($(this));
    } else {
        save_data_extraction_field($(this));
    }
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
          $(action_button).removeClass().addClass("btn btn-success js-finished-button js-mark-as-not-finished");
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
          $(action_button).removeClass().addClass("btn btn-success js-finished-button js-mark-as-finished");
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

  function change_empirical_data_type(ref) {

  }

  function save_empirical_data(ref) {
    var article_id = $(ref).closest(".panel-body").attr("data-article-id");
    var has_empirical_data = $(ref)[0].checked

    $.ajax({
        url: '/reviews/conducting/update_article_empirical_data/',
        data: {
            'article-id': article_id,
            'has-empirical-data': has_empirical_data,
        },
        type: 'get',
        cache: false,
        success: function (data) {
            console.log('article ', article_id)
            if (has_empirical_data) {
                $('#empirical-values-' + article_id).removeClass("hide")
            } else {
                $('#empirical-values-' + article_id).addClass("hide")
                $('#empirical-values-' + article_id + ' input[type="text"]').val('')
            }
            // $(row).replaceWith(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(errorThrown)
            $.parsifal.alert('Tivemos problemas',jqXHR.responseText);
        }
    });
  }

  function save_empirical_value_fields(ref) {
	console.log('save_empirical_value_fields');
    
	var article_id = $(ref).closest(".panel-body").attr("data-article-id");
    var review_id = $("#review-id").val();
    var field_type = ref[0].dataset['type'];
    var value = $(ref).val();
    var row = $(ref).closest(".form-group");

    if (value == 'P') {
        $('#effect-data-' + article_id).addClass('hide')
        $('#primary-data-' + article_id).removeClass('hide')
    } else if (value == 'E') {
        $('#effect-data-' + article_id).removeClass('hide')
        $('#primary-data-' + article_id).addClass('hide')
    }

    $.ajax({
        url: '/reviews/conducting/save_empirical_value_field/',
        data: $("#empirical-values-"+article_id).serialize(),
        type: 'get',
        cache: false,
        success: function (data) {
            $("span.error", row).text('');
            $("span.error", row).hide();
           // $(row).addClass("has-error");
            //console.log('article ', article_id)
            // $(row).replaceWith(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
            $("span.error", row).text(jqXHR.responseText);
            $("span.error", row).show();
            //$(row).addClass("has-error");
            console.log('errorThrown:'+errorThrown);
            console.log('textStatus:'+textStatus);
            console.log('jqXHR:'+jqXHR.responseText);
            $.parsifal.alert('Tivemos problemas',jqXHR.responseText);
        }
    });

  }


});
