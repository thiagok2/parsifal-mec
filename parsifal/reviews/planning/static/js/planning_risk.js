$(function () {

    var cancel_research_risk_edition_row = new Array();

    $("#btn-add-risk").click(function () {
      var review_id = $("#review-id").val();
      var csrf_token = $("#risk-form input[name='csrfmiddlewaretoken']").val();
      $.ajax({
        url: '/reviews/planning/add_or_edit_risk/',
        data: {
          'review-id': review_id,
          'risk-id': 'None',
          'csrfmiddlewaretoken': csrf_token
        },
        type: 'post',
        cache: false,
        success: function (data) {
          $("#risk-form table tbody").append(data);
          $("#risk-form table tbody input[type='text']").last().focus();
        }
      });
    });

    $("#risk-form").on("click", ".btn-cancel-risk", function () {
      var tr = $(this).closest("tr");
      var risk_id = $(tr).attr("data-risk-id");
      if (risk_id == 'None') {
        $(tr).remove();
      }
      else {
        $(tr).replaceWith(cancel_research_risk_edition_row[risk_id]);
      }
    });

    $("#risk-form").on("click", ".btn-edit-risk", function () {
      var tr = $(this).closest("tr");
      var btn = $(this);
      var review_id = $("#review-id").val();
      var risk_id = $(tr).attr("data-risk-id");
      var csrf_token = $("#risk-form input[name='csrfmiddlewaretoken']").val();

      cancel_research_risk_edition_row[risk_id] = tr;

      $.ajax({
        url: '/reviews/planning/add_or_edit_risk/',
        data: {
          'review-id': review_id,
          'risk-id': risk_id,
          'csrfmiddlewaretoken': csrf_token
        },
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(btn).ajaxDisable();
        },
        success: function(data) {
          var newRow = $(tr).replaceWith(data);
          var input = $("tr[data-risk-id='" + risk_id + "'] input[type='text']");
          $(input).focus();
          /* This trick is done to put the cursor in the end of the input value */
          var tmpVal = $(input).val();
          $(input).val("");
          $(input).val(tmpVal);
        },
        complete: function () {
          $(btn).ajaxEnable();
        }
      });
    });

    $("#risk-form").on("click", ".btn-save-risk", function () {
      var tr = $(this).closest("tr");
      var btn = $(this);
      var review_id = $("#review-id").val();
      var risk_id = $(tr).attr("data-risk-id");
      var description = $("input[name='risk-description']", tr).val();
      var csrf_token = $("#risk-form input[name='csrfmiddlewaretoken']").val();
      
      if(!description){
    	  $.parsifal.alert("Campo obrigatório.", "Preencha a descrição para adicionar.");
    	  return null;
      }
    	  
      $.ajax({
        url: '/reviews/planning/save_risk/',
        data: {
          'review-id': review_id,
          'risk-id': risk_id,
          'description': description,
          'csrfmiddlewaretoken': csrf_token
        },
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(btn).ajaxDisable();
        },
        success: function(data) {
          $(tr).replaceWith(data);
          manageRisksOrder();
        },
        error: function (jqXHR, textStatus, errorThrown) {

        },
        complete: function () {
          $(btn).ajaxEnable();
        }
      });
    });

    $("#risk-form").on("click", ".btn-remove-risk", function () {
      var tr = $(this).closest("tr");
      var btn = $(this);
      var review_id = $("#review-id").val();
      var risk_id = $(tr).attr("data-risk-id");
      var csrf_token = $("#risk-form input[name='csrfmiddlewaretoken']").val();
      $.ajax({
        url: '/reviews/planning/remove_risk/',
        data: {
          'review-id': review_id,
          'risk-id': risk_id,
          'csrfmiddlewaretoken': csrf_token
        },
        type: 'post',
        cache: false,
        beforeSend: function () {
          $(btn).ajaxDisable();
        },
        success: function (data) {
          $(tr).remove();
        },
        error: function () {

        },
        complete: function () {
          $(btn).ajaxEnable();
        }
      });
    });

    $("#risk-form").on("keydown", "input[name='risk-description']", function (event) {
      if (event.keyCode == 13) { // Enter, Return
        var tr = $(this).closest("tr");
        $(".btn-save-risk", tr).click();
        return false;
      } else if (event.keyCode == 27) { // ESC
        var tr = $(this).closest("tr");
        $(".btn-cancel-risk", tr).click();
        return false;
      }
    });

    var manageRisksOrder = function () {
      var orders = "";
      $("#risk-form table tbody tr").each(function () {
        var riskId = $(this).attr("data-risk-id");
        var rowOrder = $(this).index();
        orders += riskId + ":" + rowOrder + ",";
        $("[name='risk-order']", this).val(rowOrder);
      });

      var review_id = $("#review-id").val();
      var csrf_token = $("#risk-form input[name='csrfmiddlewaretoken']").val();

      $.ajax({
        url: '/reviews/planning/save_risk_order/',
        type: 'post',
        cache: false,
        data: {
          'csrfmiddlewaretoken': csrf_token,
          'review-id': review_id,
          'orders': orders
        }
      });
    };

    $("#risk-form").on("click", ".js-order-research-risk-up", function () {
      var i = $(this).closest("tr").index();
      if (i > 0) {
        var sibling = $("#risk-form table tbody tr:eq(" + (i - 1) + ")");
        var row = $(this).closest("tr").detach();
        $(sibling).before(row);
        manageRisksOrder();
      }
      return false;
    });

    $("#risk-form").on("click", ".js-order-research-risk-down", function () {
      var container = $(this).closest("tbody");
      var rows = $("tr", container).length - 1;
      var i = $(this).closest("tr").index();
      if (i < rows) {
        var sibling = $("#risk-form table tbody tr:eq(" + (i + 1) + ")");
        var row = $(this).closest("tr").detach();
        $(sibling).after(row);
        manageRisksOrder();
      }
      return false;
    });
    
    $("table#tbl-import-risks").on("click", "tbody tr", function () {
    	
        var hiddenClass = $(this)[0].nextElementSibling;
        hiddenClass.className == "hidden"
        ? hiddenClass.className = ""
        : hiddenClass.className = "hidden"
    });
    
    
    $("table#tbl-import-risks").on("click", "#btn-import-risk", function () {

        var exported_review_id = $(this).data("review-ref-id")
        var fields = $("#form-suggested-risks-"+exported_review_id).serializeArray();
        var review_id = $("#review-id").val();

        risks_ids = []
        $.each(fields, function(i, field) {
        	field.name == 'id' ? risks_ids.push(field.value) : null
        });
 
        for (f of risks_ids) {
        	
            var step_risks = { id: f }
            $.each(fields, function(i, field) {
                if (field.name == 'risk-description-'+f) step_risks.description = field.value
                if (field.name == 'csrfmiddlewaretoken') step_risks.csrf_token = field.value
                
            });
            
            $.ajax({
                url: '/reviews/planning/save_risk/',
                data: {
                	'review-id': review_id,
                    'description': step_risks.description,
                    'risk-id': 'None',
                    'csrfmiddlewaretoken': step_risks.csrf_token
                },
                type: 'post',
                cache: false,
                success: function (data) {
                    $("#tbl-risks tbody").append(data);
                    $("#modal-suggested-risks").modal("hide");
                    manageRisksOrder();
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log(errorThrown);
                }
            });
        }


    });


    $("#btn-import-risk").click(function () {
    	$.ajax({
    		url: '/reviews/planning/suggested_risks/',
    		data: { 'review-id': $('#review-id').val() },
    		cache: false,
    		type: 'get',
    		success: function (data) {
	        
    			$("#modal-suggested-risks table tbody").html(data);
    			$("#modal-suggested-risks").before("<div class='shade'></div>");
    			$("#modal-suggested-risks").slideDown(400, function () {
    				$("body").addClass("modal-open");
    			});
    		}
	   });
	});

  
    $("#btn-confirm-risks-share").click(function () {
	    var csrf_token = $("#share-risks-form input[name='csrfmiddlewaretoken']").val();
	    
	    $.ajax({
	      url: '/reviews/planning/share_risks/',
	      data: {
	        'review-id': $('#review-id').val(),
	        'csrfmiddlewaretoken': csrf_token
	      },
	      cache: false,
	      type: 'post',
	      success: function (data) {
	    	  $("#modal-share-risks").modal("hide");
	      }
	    });
    });
 
});
