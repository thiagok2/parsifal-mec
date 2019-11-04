function isScrolledIntoView(elem) {
    var docViewTop = $(window).scrollTop();
    var docViewBottom = docViewTop + $(window).height();

    var elemTop = $(elem).offset().top;
    var elemBottom = elemTop + $(elem).height();

    return ((elemBottom <= docViewBottom) && (elemTop >= docViewTop));
}

$(function () {

    $("body").on("click", ".btn-remove-file", function () {
        var tr = $(this).closest("tr");
        var btn = $(this);
        var file_id = $(tr).attr("data-file-id");
        var review_id = $("#review-id").val();
        var csrf_token = $("#file-form input[name='csrfmiddlewaretoken']").val();
        $.ajax({
        url: '/reviews/conducting/remove_article_file/',
        data: {
            'review-id': review_id,
            'file-id': file_id,
            'csrfmiddlewaretoken': csrf_token
        },
        type: 'post',
        cache: false,
        beforeSend: function () {
            $(btn).ajaxDisable();
        },
        success: function (data) {
            //$(tr).remove();
            $("#tab-files").html(data);

        },
        error: function (jqXHR, textStatus, errorThrown) {
        	$.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação. "+jqXHR.responseText);
        	console.log(textStatus, errorThrown+': '+jqXHR);
        },
        complete: function () {
            $(btn).ajaxEnable();
        }
        });
    });


  $("body").on("click", ".js-start-upload", function () {
    $(this).siblings("input[type='file']").click();
  });

  $("body").on("change", "#id_article_file", function () {

    var data = new FormData();
    data.append("article_file", $(this)[0].files[0]);

    $.ajax({
      url: '/reviews/conducting/articles/upload/',
      data: data,
      cache: false,
      contentType: false,
      processData: false,
      type: 'post',
      beforeSend: function () {
        $.parsifal.pageLoading();
      },
      success: function (data) {
        $("#tab-files").html(data);
      },
      error: function (jqXHR, textStatus, errorThrown) {
    	  $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação. "+jqXHR.responseText);
    	  console.log(textStatus, errorThrown);
      },
      complete: function () {
        $.parsifal.pageLoading();
      }
    });

  });

  $(".source-tab-content").on("click", ".btn-add-manual", function () {
    var container = $("#modal-add-article .modal-body");
    var review_id = $("#review-id").val();
    var div = $(this).closest(".source-buttons");
    var source_id = $("input[name=source-id]", div).val();
    $.ajax({
      url: '/reviews/conducting/new_article/',
      data: {'review-id': review_id, 'source-id': source_id},
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(container).loading();
      },
      success: function (data) {
        $(container).html(data);
      },
      error: function (jqXHR, textStatus, errorThrown) {
    	  $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação. "+jqXHR.responseText);
    	  console.log(textStatus, errorThrown+":"+jqXHR.responseText);
      },
      complete: function () {
        $(container).stopLoading();
      }
    });
    $("#modal-add-article").modal('show');
  });

  $("#source-tab a").click(function () {
    var radio_value = $("input[name='filter']:checked").val();
    var source_id = $(this).attr("source-id");
    var active_source_id = $("ul#source-tab li.active a").attr("source-id");
    var searchParams = new URLSearchParams(window.location.search);
    var param = '1';
    var active_filter = '';

    $("ul#source-tab li").removeClass("active");
    $(this).closest("li").addClass("active");

    if (searchParams.has('page') && active_source_id === source_id) {
        param = searchParams.get('page')
    }

    //console.log(searchParams.get('active_filter'))
    //console.log(radio_value)
    //console.log('sources ', active_source_id === source_id)

    if (searchParams.has('active_filter') && searchParams.get('active_filter') !== null && radio_value === undefined) {
        // console.log('1')
        active_filter = searchParams.get('active_filter')
        //param = '1'
    } else if (radio_value !== undefined && searchParams.get('active_filter') === null) {
        // console.log('2')
        active_filter = radio_value
        param = '1'
        if (radio_value === 'ALL') active_filter = ''
    } else if (radio_value === searchParams.get('active_filter')) {
        // console.log('3')
        active_filter = radio_value
    } else if (radio_value !== undefined && radio_value !== searchParams.get('active_filter')) {
        // console.log('4')
        active_filter = radio_value
        param = '1'
        if (radio_value === 'ALL') active_filter = ''
    }

    $.ajax({
      url: '/reviews/conducting/source_articles/',
      data: { 'review-id': $("#review-id").val(), 'source-id': source_id, 'page': param, 'active_filter': active_filter },
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(".source-tab-content").spinner();
      },
      success: function (data) {
        $(".source-tab-content").html(data);
        $(".source-tab-content table").tablesorter({ headers: { 0: { sorter: false }}});
      },
      error: function (jqXHR, textStatus, errorThrown) {
    	  $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação. "+jqXHR.responseText);
    	  console.log(textStatus, errorThrown+":"+jqXHR.responseText);
      },
      complete: function () {
        $(".source-tab-content").spinner();
      }
    });

    return false;
  });

  $.fn.loadActiveArticle = function () {
    var article_id = $(".source-articles tbody tr.active").attr("oid");
    var review_id = $("#review-id").val();
    var container = $(this);

    var total_articles = $(".source-articles tbody tr:visible").length;
    var current_article = 0;
    $(".source-articles tbody tr:visible").each(function () {
      current_article++;
      if ($(this).attr("oid") == article_id) {
        return false;
      }
    });

    $("#modal-article span.current-article").text(current_article);
    $("#modal-article span.total-articles").text(total_articles);

    $.ajax({
      url: '/reviews/conducting/article_details/',
      data: {'review-id': review_id, 'article-id': article_id},
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(container).spinner();
      },
      success: function (data) {
        $(container).html(data);

      },
      error: function (jqXHR, textStatus, errorThrown) {
    	  $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação. "+jqXHR.responseText);
    	  console.log(textStatus, errorThrown+":"+jqXHR.responseText);
      },
      complete: function () {
        $(container).spinner();
      }
    });
  };

  $(".source-tab-content").on("click", "tbody .table-link", function () {
    if (!$(this).closest('tr').hasClass("no-data")) {
        $(".source-articles tbody tr").removeClass("active");
        $(this).closest('tr').addClass("active");
        $("#modal-article .modal-body").css("height", $(window).height() * 0.7);
        $("#modal-article .modal-body").loadActiveArticle();
        var status = $(".source-articles tbody tr.active select[id^='evaluation-status']").val();
        $("#modal-article").modal('show');
        $("#modal-article").on('shown.bs.modal', function(e) {
            $('#modal-article #article-evaluation #status').val(status)
            $('#modal-article a[href="#tab-details"]').tab('show')
        })
    }
  });

  $("body").keydown(function (event) {
    var keyCode = event.which?event.which:event.keyCode;

    if (keyCode == ESCAPE_KEY) {
      if ($("body").hasClass("modal-open")) {
        $(".modal").modal('hide');
      }
      else {
        $(".source-articles tbody tr").removeClass("active");
      }
    }
    else if (!$("body").hasClass("modal-open")) {
      if (keyCode == UP_ARROW_KEY) {
        event.preventDefault();
        move(BACKWARD);
      }
      else if (keyCode == DOWN_ARROW_KEY) {
        event.preventDefault();
        move(FORWARD);
      }
      else if (keyCode == ENTER_KEY) {
       $(".source-articles tbody tr.active").click();
      }
    }
  });

  function move(step) {
    var row = $(".source-articles tbody tr.active");

    var active = $(".source-articles tbody tr.active").index();
    var old_active = active;
    var size = $(".source-articles tbody tr").size();
    var next;
    do {
      active = (active + step) % size;
      next = $(".source-articles tbody tr:eq("+active+")");
    } while($(next).is(":hidden"));
    $(".source-articles tbody tr").removeClass("active");
    $(next).addClass("active");

    if (!isScrolledIntoView(row)) {
      if (active > old_active)
        $('html, body').animate({scrollTop: $(row).offset().top}, 2000);
      else
        $('html, body').animate({scrollTop: $(row).offset().top - $(window).height()}, 2000);
    }
  }

  $("#btn-previous").click(function () {
    move(BACKWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });

  $("#btn-next").click(function () {
    move(FORWARD);
    $("#modal-article .modal-body").loadActiveArticle();
  });

  function save_article(move_next) {
    var article_id = $("#modal-article #article-id").val();
    $.ajax({
      url: '/reviews/conducting/save_article_details/',
      cache: false,
      data: $("#article-details").serialize(),
      type: 'post',
      beforeSend: function () {
        $(".btn-save-article").prop("disabled", true);
      },
      success: function (data) {
        $(".source-articles table tbody tr[oid=" + article_id + "]").replaceWith(data);
        $(".source-articles table tbody tr[oid=" + article_id + "]").addClass("active");
        if (move_next) {
          move(FORWARD);
          $("#modal-article .modal-body").loadActiveArticle();
        }
        else {
          $("#modal-article .alert .modal-alert").text("Artigo salvo com sucesso!");
          $("#modal-article .alert").removeClass("alert-error").addClass("alert-success");
          $("#modal-article .alert").removeClass("hide");
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
          $("#modal-article .alert .modal-alert").text("Algo deu errado! Isso é tudo que sabemos :(");
          $("#modal-article .alert").removeClass("alert-success").addClass("alert-error");
          $("#modal-article .alert").removeClass("hide");
          console.log(textStatus, errorThrown+": "+jqXHR.responseText);

          $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação. "+jqXHR.responseText);
      },
      complete: function () {
        $(".btn-save-article").prop("disabled", false);
      }
    });
    var is_solving_conflict = $('#article-solve-conflict #status').val()
    var is_reopening =  $('#article_reopen_evaluation #status').val()
    if (is_solving_conflict || is_reopening) {
        article_solve_conflict();
    } else {
        save_article_evaluation();
    }
  }

  $("body").on("change", "select[id^='evaluation-status']", function () {
    is_rejeitado = $(this).val()
    if (is_rejeitado == 'R') {
        if (!$(this).closest('tr').hasClass("no-data")) {
            $(".source-articles tbody tr").removeClass("active");
            $(this).closest('tr').addClass("active");
            $("#modal-article .modal-body").css("height", $(window).height() * 0.7);
            $("#modal-article .modal-body").loadActiveArticle();
            $("#modal-article").modal('show');
            $("#modal-article").on('shown.bs.modal', function(e) {
                $('#modal-article #article-evaluation #status').val('R')
                $('#modal-article a[href="#tab-evaluation"]').tab('show')
            })
        }
    } else {
        save_article_evaluation($(this));
    }

  });

  function save_article_evaluation(ref="") {
    var serialize = '';
    var article_id = "";
    var evaluation_id = "";
    var form;

    if (ref !== "") { // via lista
        article_id = $(ref).closest('tr').attr('oid')
        evaluation_id = $(ref).attr('data-evaluation-id');
        form = $("#article-evaluation-" + article_id + "-" + evaluation_id);

    } else { // via modal
        article_id = $("#modal-article #article-id").val();
        form = $("#article-evaluation");

        if( $("#article-evaluation-finished-"+article_id).val() == "True"){
        	console.log('article-evaluation-finished');
        	return false;
        }
    }

    form = $(form).serialize();

    $.ajax({
        url: '/reviews/conducting/save_article_evaluation/',
        cache: false,
        data: form,
        type: 'post',
        beforeSend: function () {
            $(".btn-save-article").prop("disabled", true);
        },
        success: function (data) {
            $(".source-articles table tbody tr[oid=" + article_id + "]").replaceWith(data);
            $(".source-articles table tbody tr[oid=" + article_id + "]").addClass("active");
            //$("#article-evaluation-id").val();
        },
        error: function (jqXHR, textStatus, errorThrown) {
        	 $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação."+jqXHR.responseText);
        	 console.log(textStatus, errorThrown + ': ' + jqXHR.responseText);
        },
        complete: function () {
            $(".btn-save-article").prop("disabled", false);
        }
    });
  }

  function article_solve_conflict() {
	var data_form;
	var new_status = false;
	var article_id = $("#modal-article #article-id").val();
	if($('#article-solve-conflict').length){
		data_form =  $("#article-solve-conflict").serialize();
		new_status = true;
	}else {
		var reopen_evaluation = $('#reopen_evaluation-'+article_id).length ? $('#reopen_evaluation-'+article_id).val() : false;
		if(reopen_evaluation){
			data_form =  $("#article_reopen_evaluation").serialize();
			new_status = true;
		}
	}

	if( new_status ){
		$.ajax({
	        url: '/reviews/conducting/article_solve_conflict/',
	        cache: false,
	        data: data_form,
	        type: 'post',
	        beforeSend: function () {
	            $(".btn-save-article").prop("disabled", true);
	        },
	        success: function (data) {
	        	$(".source-articles table tbody tr[oid=" + article_id + "]").replaceWith(data);
	            $(".source-articles table tbody tr[oid=" + article_id + "]").addClass("active");
	        },
	        error: function (jqXHR, textStatus, errorThrown) {
	        	$.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação."+jqXHR.responseText);
	       	 	console.log(textStatus, errorThrown+': ' + jqXHR.responseText);
	        },
	        complete: function () {
	            $(".btn-save-article").prop("disabled", false);
	        }
	    });
	}

  }

  $(".btn-save-article").click(function () {
    save_article(false);
  });

  $("#modal-article").on("click", "ul.tab a", function () {
    var tab_id = $(this).attr("href");
    $("#modal-article div.tabs form > div").hide();
    $("#modal-article ul.tab li").removeClass("active");
    $(this).closest("li").addClass("active");
    $(tab_id).show();
    return false;
  });

  $("#modal-article").on("change", "#status", function () {
    if ($("#save-and-move-next").is(":checked")) {
      save_article(false);
    }
  });

  function filter_articles(status) {
    if (status == "ALL") {
      $(".source-articles table tbody tr").show();
    }
    else {
      $(".source-articles table tbody tr").hide();
      $(".source-articles table tbody tr[article-status=" + status + "]").show();
    }
    $(".source-tab-content input[type=checkbox]").prop("checked", false);
    $(".source-articles tbody tr").removeClass("active");
  }

  $(".source-tab-content").on("click", "input[name=filter]", function () {
    $("#source-tab li.active a").click();
    //filter_articles($(this).val());
    updateSelectedArticlesCount();
  });

  $(".source-tab-content").on("click", "table tbody tr td input[type=checkbox]", function (event) {
    event.stopPropagation();
  });

  $(".source-tab-content").on("click", "#ck-all-articles", function () {
    $(".source-tab-content table tbody tr td input[type=checkbox]").prop("checked", false);
    if ($(this).is(":checked")) {
      $(".source-tab-content table tbody tr:visible td input[type=checkbox]").prop("checked", true);
    }
    updateSelectedArticlesCount();
  });

  function multiple_articles_actions(article_ids, action) {
    var review_id = $("#review-id").val();
    var csrf_token = $(".source-tab-content table").attr("csrf-token");

    $.ajax({
      url: '/reviews/conducting/multiple_articles_action/' + action + '/',
      data: {
        'review-id': review_id,
        'article_ids': article_ids,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(".go-button").prop("disabled", true);
        $(".go-button").text("Processando...");
      },
      success: function (data) {
        switch (action) {
          case "remove":
            $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
              $(this).closest("tr").remove();
            });
            break;
          case "accept":
            $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
              var row = $(this).closest("tr");
              $(row).attr("article-status", "A");
              $("span", row).replaceWith("<span class='label label-success'>Aceito</span>");
            });
            break;
          case "reject":
            $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
              var row = $(this).closest("tr");
              $(row).attr("article-status", "R");
              $("span", row).replaceWith("<span class='label label-danger'>Rejeitado</span>");
            });
            break;
          case "duplicated":
            $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
              var row = $(this).closest("tr");
              $(row).attr("article-status", "R");
              $("span", row).replaceWith("<span class='label label-warning'>Duplicado</span>");
            });
            break;
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
     	 $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação. "+jqXHR.responseText);
     	 console.log(textStatus, errorThrown+": "+ jqXHR.responseText);
      },
      complete: function () {
        $(".go-button").prop("disabled", false);
        $(".go-button").text("Executar");
        updateSelectedArticlesCount();
      }
    });
  }

  $(".source-tab-content").on("click", ".go-button", function () {
    var article_ids = '';
    var action = $(".source-tab-content .select-action").val();
    if (action) {
      $(".source-articles table tbody input[type=checkbox]:checked").each(function () {
        article_ids += $(this).val() + "|";
      });
      if (article_ids) {
        article_ids = article_ids.substring(0, article_ids.length - 1);
        switch (action) {
          case "remove":
            multiple_articles_actions(article_ids, action);
            break;
          case "accept":
            multiple_articles_actions(article_ids, action);
            break;
          case "reject":
            multiple_articles_actions(article_ids, action);
            break;
          case "duplicated":
            multiple_articles_actions(article_ids, action);
            break;
        }
      }
    }
  });


  $(".source-tab-content").on("click", "table tbody tr td#actions input[type=checkbox]", function () {
    var total = $(".source-articles table tbody tr td#actions input[type='checkbox']:visible").length;
    var checked = $(".source-articles table tbody tr td#actions input[type='checkbox']:checked").length;
    if (checked == total) {
      $("#ck-all-articles").prop("checked", true);
    }
    else {
      $("#ck-all-articles").prop("checked", false);
    }
    updateSelectedArticlesCount();
  });

  $(".source-tab-content").on("click", "table tbody tr td:first-child", function (e) {
    e.stopPropagation();
    $("input[type='checkbox']", this).click();
    return false;
  });

  var updateSelectedArticlesCount = function () {
    var total = $(".source-articles table tbody tr td#actions input[type='checkbox']:visible").length;
    var checked = $(".source-articles table tbody tr td#actions input[type='checkbox']:checked").length;
    $(".articles-selected").text(checked);
    $(".articles-total").text(total);
  };

  $(".source-tab-content").on("click", ".btn-find-duplicates", function () {
    $.ajax({
      url: '/reviews/conducting/find_duplicates/',
      data: {'review-id': $("#review-id").val()},
      type: 'get',
      cache: false,
      beforeSend: function () {
        $("#modal-duplicates .modal-body").css("max-height", $(window).height() * 0.7);
        $("#modal-duplicates").modal('show');
        $("#modal-duplicates .modal-body").loading();
      },
      success: function (data) {
        $("#modal-duplicates .modal-body").html(data);
      },
      error: function (jqXHR, textStatus, errorThrown) {
          console.log(textStatus, errorThrown+": "+jqXHR.responseText);
          $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação."+jqXHR.responseText);
      },
      complete: function () {
        $("#modal-duplicates .modal-body").stopLoading();
      }
    });
  });

  $("#modal-duplicates").on("click", ".btn-resolve", function () {
    var row = $(this).closest("tr");
    var btn = $(this);
    var review_id = $("#review-id").val();
    var article_id = $(row).attr("article-id");
    var duplicate = $(row).attr("duplicate");
    var csrf_token = $("#modal-duplicates input[name=csrfmiddlewaretoken]").val();
    $.ajax({
      url: '/reviews/conducting/resolve_duplicated/',
      data: {
        'review-id': review_id,
        'article-id': article_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).prop("disabled", true);
        $(btn).text("Resolving...");
      },
      success: function (data) {
        $("span", row).replaceWith("<span class='label label-warning'>Duplicado</span>");
        $(btn).text("Resolvido");
        $(row).attr("resolved", "true");
        var duplicates = $("#modal-duplicates .modal-body tr[duplicate=" + duplicate + "]");
        var duplicates_resolved = $("#modal-duplicates .modal-body tr[duplicate=" + duplicate + "][resolved=true]");

        if (duplicates.length - duplicates_resolved.length == 1) {
          var btn_resolved = $("#modal-duplicates .modal-body tr[duplicate=" + duplicate + "][resolved=false] button");
          $(btn_resolved).text("Resolvido");
          $(btn_resolved).prop("disabled", true);
        }

        var article_row = $(".source-tab-content .source-articles tr[oid=" + article_id + "]");
        $(article_row).attr("article-status", "D");
        $("span", article_row).replaceWith("<span class=\"label label-warning\">Duplicado</span>");
      },
      error: function (jqXHR, textStatus, errorThrown) {
        $(btn).prop("disabled", false);
        $(btn).text("Resolve");
        console.log(textStatus, errorThrown+": "+jqXHR.responseText);
        $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação."+jqXHR.responseText);
      }
    });
  });

  $("#btn-resolve-all").click(function () {
    var review_id = $("#review-id").val();
    var csrf_token = $("#modal-duplicates input[name=csrfmiddlewaretoken]").val();
    var btn = $(this);
    $.ajax({
      url: '/reviews/conducting/resolve_all/',
      data: {
        'review-id': review_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).prop("disabled", true);
        $(btn).text("Resolving...");
      },
      success: function (data) {
        if (data != "") {
          var btn_modal = $("#modal-duplicates table tbody tr td button");
          $(btn_modal).prop("disabled", true);
          $(btn_modal).text("Resolvido");
          var ids = data.split(",");
          for (var i = ids.length - 1; i >= 0; i--) {
            var article_row = $(".source-tab-content .source-articles tr[oid=" + ids[i] + "]");
            $(article_row).attr("article-status", "D");
            $("span", article_row).replaceWith("<span class=\"label label-warning\">Duplicado</span>");
          };
        }
      },
      error: function (jqXHR, textStatus, errorThrown) {
        console.log(textStatus, errorThrown+': '+jqXHR.responseText);
        $.parsifal.alert("Tivemos problemas","Não conseguimos concluir a operação."+jqXHR.responseText);
      },
      complete: function () {
        $(btn).prop("disabled", false);
        $(btn).text("Resolver Todos");
      }
    });
  });

  // On page load

  if ($("ul#source-tab li").length > 0) {
    if($("ul#source-tab li.active").length == 0) {
      $("ul#source-tab li:eq(0)").addClass("active");
    }
    $("#source-tab li.active a").click();
  }

  $("#modal-article").on("click", ".btn-return-conflict", function () {
	  var article_id = $("#modal-article #article-id").val();

	  $('#reopen_evaluation-'+article_id).val(true);
	  $(this).fadeOut();
	  $('#new_evaluation_conflict').fadeIn("slow");

  });

});
