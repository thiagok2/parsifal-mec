function update_max_score() {
  $.ajax({
    url: '/reviews/planning/calculate_max_score/',
    data: {'review-id': $('#review-id').val()},
    type: 'get',
    cache: false,
    success: function (data) {
      $("#max-score").val(data);
    },
    error: function () {
      $("#max-score").val("0.0");
    }
  });
}

$(function () {

  //===========================================================================
  // QUALITY ASSESSMENT QUESTIONS
  //===========================================================================

  var cancel_question_edition_row = new Array();

  $("#btn-add-quality-question").click(function () {
    var review_id = $("#review-id").val();
    $.ajax({
      url: '/reviews/planning/add_quality_assessment_question/',
      data: {'review-id': review_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $("#tbl-quality-questions tbody").append(data);
        $("#tbl-quality-questions tbody tr:first-child .quality-question-description").focus();
      }
    });
  });

  $("table#tbl-quality-questions").on("click", ".btn-cancel-quality_question", function () {
    var row = $(this).closest("tr");
    var quality_question_id = $(row).attr("oid");
    if (quality_question_id == 'None') {
      $(row).fadeOut(400, function () {
        $(this).remove();
      });
    }
    else {
      $(row).replaceWith(cancel_question_edition_row[quality_question_id]);
    }
  });

  $("table#tbl-quality-questions").on("click", ".btn-save-quality_question", function () {
    var row = $(this).closest("tr");
    var review_id = $("#review-id").val();
    var description = $(".quality-question-description", row).val();
    var quality_question_id = $(row).attr("oid");
    var csrf_token = $(row).attr("csrf-token");
    var btn = $(this);

    $.ajax({
      url: '/reviews/planning/save_quality_assessment_question/',
      data: {'review-id': review_id,
        'description': description,
        'quality-question-id': quality_question_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      success: function (data) {
        $(row).replaceWith(data);
        $(btn).ajaxEnable();
        update_max_score();
      }
    });
  });

  $("table#tbl-quality-questions").on("click", ".btn-edit-quality-question", function () {
    var row = $(this).closest("tr");
    var quality_question_id = $(row).attr("oid");
    var review_id = $("#review-id").val();

    cancel_question_edition_row[quality_question_id] = row;

    $.ajax({
      url: '/reviews/planning/edit_quality_assessment_question/',
      data: {
        'review-id': review_id,
        'quality-question-id': quality_question_id
      },
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).replaceWith(data);
      }
    });
  });

  $("table#tbl-quality-questions").on("click", ".btn-remove-quality-question", function () {
    var quality_question_id = $(this).closest("tr").attr("oid");
    var review_id = $("#review-id").val();
    var row = $(this).closest("tr");

    $.ajax({
      url: '/reviews/planning/remove_quality_assessment_question/',
      data: {'review-id': review_id, 'quality-question-id': quality_question_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).remove();
        update_max_score();
      },
      error: function (jqXHR, textStatus, errorThrown) {

      }
    });

  });


  var manageQualityAssementQuestionsOrder = function () {
    var orders = "";
    $("table#tbl-quality-questions tbody tr").each(function () {
      var questionId = $(this).attr("oid");
      var rowOrder = $(this).index();
      orders += questionId + ":" + rowOrder + ",";
      $("[name='quality-question-order']", this).val(rowOrder);
    });

    var review_id = $("#review-id").val();
    var csrf_token = $("[name='csrfmiddlewaretoken']").val();

    $.ajax({
      url: '/reviews/planning/save_quality_assessment_question_order/',
      type: 'post',
      cache: false,
      data: {
        'csrfmiddlewaretoken': csrf_token,
        'review-id': review_id,
        'orders': orders
      }
    });

  };

  $("table#tbl-quality-questions").on("click", ".js-order-quality-question-up", function () {
    var i = $(this).closest("tr").index();
    if (i > 0) {
      var sibling = $("table#tbl-quality-questions tbody tr:eq(" + (i - 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).before(row);
      manageQualityAssementQuestionsOrder();
    }
    return false;
  });

  $("table#tbl-quality-questions").on("click", ".js-order-quality-question-down", function () {
    var container = $(this).closest("tbody");
    var rows = $("tr", container).length - 1;
    var i = $(this).closest("tr").index();
    if (i < rows) {
      var sibling = $("table#tbl-quality-questions tbody tr:eq(" + (i + 1) + ")");
      var row = $(this).closest("tr").detach();
      $(sibling).after(row);
      manageQualityAssementQuestionsOrder();
    }
    return false;
  });

  $("#btn-import-quality-questions").click(function () {
    $.ajax({
      url: '/reviews/planning/suggested_quality_assessment_questions/',
      data: { 'review-id': $('#review-id').val() },
      cache: false,
      type: 'get',
      success: function (data) {

        $("#modal-suggested-quality-questions table tbody").html(data);
        $("#modal-suggested-quality-questions").before("<div class='shade'></div>");
        $("#modal-suggested-quality-questions").slideDown(400, function () {
          $("body").addClass("modal-open");
        });
      }
    });
  });

  $("table#tbl-import-quality-questions").on("click", "tbody tr", function () {
    var hiddenClass = $(this)[0].nextElementSibling
    hiddenClass.className == "hidden"
    ? hiddenClass.className = ""
    : hiddenClass.className = "hidden"
  });

  $("table#tbl-import-quality-questions").on("click", "td#import-quality-questions", function () {
    var exported_review_id = $(this)[0].parentElement.children[0].innerHTML;
    var questions = $("#form-suggested-quality-questions-"+exported_review_id).serializeArray();
    var review_id = $("#review-id").val();

    questions_ids = []
    $.each(questions, function(i, question) {
        question.name == 'id' ? questions_ids.push(question.value) : null
    });

    for (f of questions_ids) {
        var step_questions = { id: f }
        $.each(questions, function(i, question) {
            if (question.name == 'description-'+f) step_questions.description = question.value
            if (question.name == 'csrfmiddlewaretoken') step_questions.csrf_token = question.value
        });

        $.ajax({
            url: '/reviews/planning/save_quality_assessment_question/',
            data: {'review-id': review_id,
                'description': step_questions.description,
                'quality-question-id': 'None',
                'csrfmiddlewaretoken': step_questions.csrf_token
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $("#tbl-quality-questions tbody").append(data);
                $("#modal-suggested-quality-questions").modal("hide");
                update_max_score();
            }
        });
    }
   });

   $("#btn-confirm-quality-questions-share").click(function () {
    var csrf_token = $("#share-quality-questions-form input[name='csrfmiddlewaretoken']").val();
    $.ajax({
      url: '/reviews/planning/share_quality_assessment_questions/',
      data: {
        'review-id': $('#review-id').val(),
        'csrfmiddlewaretoken': csrf_token
      },
      cache: false,
      type: 'post',
      success: function (data) {
        $("#modal-share-quality-questions").modal("hide");
      }
    });
  });


  //===========================================================================
  // QUALITY ASSESSMENT ANSWERS
  //===========================================================================

  var cancel_answer_edition_row = new Array();

  $("#btn-add-quality-answer").click(function () {
    var review_id = $("#review-id").val();
    $.ajax({
      url: '/reviews/planning/add_quality_assessment_answer/',
      data: {'review-id': review_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $("#tbl-quality-answers tbody").append(data);
        $("#tbl-quality-answers tbody tr:first-child .quality-answer-description").focus();
      }
    });
  });

  $("table#tbl-quality-answers").on("click", ".btn-save-quality-answer", function () {
    var row = $(this).closest("tr");
    var review_id = $("#review-id").val();
    var description = $(".quality-answer-description", row).val();
    var weight = $(".quality-answer-weight", row).val();
    var quality_answer_id = $(row).attr("oid");
    var csrf_token = $(row).attr("csrf-token");

    $.ajax({
      url: '/reviews/planning/save_quality_assessment_answer/',
      data: {'review-id': review_id,
        'description': description,
        'weight': weight,
        'quality-answer-id': quality_answer_id,
        'csrfmiddlewaretoken': csrf_token
      },
      type: 'post',
      cache: false,
      success: function (data) {
        $(row).replaceWith(data);
        update_max_score();
      }
    });
  });

  $("table#tbl-quality-answers").on("click", ".btn-cancel-quality-answer", function () {
    var row = $(this).closest("tr");
    var quality_answer_id = $(row).attr("oid");
    if (quality_answer_id == 'None') {
      $(row).fadeOut(400, function () {
        $(this).remove();
      });
    }
    else {
      $(row).replaceWith(cancel_answer_edition_row[quality_answer_id]);
    }
  });

  $("table#tbl-quality-answers").on("click", ".btn-edit-quality-answer", function () {
    var row = $(this).closest("tr");
    var quality_answer_id = $(row).attr("oid");
    var review_id = $("#review-id").val();
    cancel_answer_edition_row[quality_answer_id] = row;

    $.ajax({
      url: '/reviews/planning/edit_quality_assessment_answer/',
      data: {'review-id': review_id, 'quality-answer-id': quality_answer_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).replaceWith(data);
      }
    });
  });

  $("table#tbl-quality-answers").on("click", ".btn-remove-quality-answer", function () {
    var quality_answer_id = $(this).closest("tr").attr("oid");
    var review_id = $("#review-id").val();
    var row = $(this).closest("tr");

    $.ajax({
      url: '/reviews/planning/remove_quality_assessment_answer/',
      data: {'review-id': review_id, 'quality-answer-id': quality_answer_id},
      type: 'get',
      cache: false,
      success: function (data) {
        $(row).remove();
        update_max_score();
      },
      error: function (jqXHR, textStatus, errorThrown) {

      }
    });
  });

  $("#add-suggested-answers").click(function () {
    $.ajax({
      url: '/reviews/planning/add_suggested_answer/',
      data: {'review-id': $("#review-id").val()},
      type: 'get',
      cache: false,
      success: function (data) {
        $("#tbl-quality-answers tbody").replaceWith("<tbody>" + data + "</tbody>");
        $(".no-answers").fadeOut();
        update_max_score();
      }
    });
  });

  $("#save-cutoff-score").click(function () {
    var btn = $(this);
    var review_id = $("#review-id").val();
    var cutoff_score = $("#cutoff-score").val();

    $.ajax({
      url: '/reviews/planning/save_cutoff_score/',
      data: {'review-id': review_id, 'cutoff-score': cutoff_score},
      type: 'get',
      cache: false,
      beforeSend: function () {
        $(btn).ajaxDisable();
      },
      complete: function () {
        $(btn).ajaxEnable();
      }
    });

  });

});
