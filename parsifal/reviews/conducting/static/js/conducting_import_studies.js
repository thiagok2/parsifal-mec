$(function () {
  $(".btn-import-bibtex").click(function () {
    var container = $(this).closest("td");
    $("input[type=file]", container).click();
  });


  $("input[name='bibtex']").change(function () {
    var form = $(this).closest("form");
    $(form).submit();
  });

  $(".js-import-bibtex-raw-content").click(function () {
    var source_id = $(this).attr("data-source-id");
    $("#bibtex-raw-content-source-id").val(source_id);
  });

  $("#parse-bibtex").on("shown.bs.modal", function () {
    $("#bibtex_raw_content").focus();
  });
  
  /******************************************************************************8*/
  
  $(".js-new-document").click(function () {
    var url = $("#modal-document").attr("data-remote-url");
    var source_id = $(this).attr("data-source-id");
    var review_id = $(this).attr("data-review-id");
    $.ajax({
      url: url,
      data: {
    	  'source-id':source_id,
    	  'review-id': review_id
      },
      type: 'get',
      cache: false,
      success: function (data) {
        $("#modal-document .modal-dialog").html(data.html);
        
      }
    });
    $("#modal-document").modal('show');
  });
  
  $("#modal-document").on("click", ".js-save-new-document", function () {
	  
	if(validarForm()){
		$.parsifal.alert("Dados Inválidos", "Dados inválidos ou ausentes. Corrija e envie novamente.");
		return false;
	}else{
		var form = $("#form-new-document");
	    $.ajax({
	      url: $(form).attr("action"),
	      data: $(form).serialize(),
	      type: $(form).attr("method"),
	      success: function (data) {
	        if (data.status === 'success') {
	         
	          $("#modal-document").modal('hide');
	          location.reload();
	          //location.href = data.redirect_to;
	        }
	        else {
	          $("#modal-document .modal-dialog").html(data.html);
	        }
	      }
	    });
	}
	  
    
  });
  
  $("#modal-document > .form-group").hide();
  $("#modal-document > .article").parent().show();
  $("#modal-document > .form-type").parent().show();
  
  $("#modal-document").on("change", "#id_entry_type", function () {
	  
	  var classe = '.'+$("#id_entry_type").val();
	  
	  $(".form-group").hide();
	  $(classe).parent().show();
	  
	  $(".form-type").parent().show();
	  //$(".generic").parent().show();
	  
	  var classe_required = classe +'-r';
	  $(classe_required).attr('required',true);
	  
  });
});

function validarForm(){
	var isValid = true;
	  $('form input').map(function() {
		  isValid &= this.validity['valid'] ;
	  }) ;
	  if (isValid) {
		  //alert('valid!');
		  //
		  return true;
	  } else{
		  //alert('not valid!');
		  return false;
	  }
		 
}