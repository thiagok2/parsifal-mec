$(function () {

  $(".js-leave").click(function () {
    $(this).closest("form").submit();
  });
  
  $(".js-open-update-articles").click(function () {
	  
	  $("#update-articles-modal").modal('show');
  });

  $(".js-open-remove-author").click(function () {  
	
	var user_container = $(this).closest("li");

    var co_author_id = $(this).closest("li").attr("data-user-id");
    var review_id = $("#review-id").val();
    
    var csrf_token = $("[name='csrfmiddlewaretoken']").val();
    $.ajax({
        url: '/reviews/get_review_info',
        data: {
        	'csrfmiddlewaretoken': csrf_token,
        	'review-id':review_id,
        	'co-author-id':co_author_id
        },
        type: 'get',
        cache: false,
        beforeSend: function () {
        	console.log('beforeSend')
        },
        success: function (data) {
        	evaluations_count = data.evaluations_count;
        	if( evaluations_count > 0){
        		$('#count_evaluations').html(data.evaluations_count);
        		$('#msg-no-evaluations').addClass('hidden');
        		$('#msg-count-evaluations').removeClass('hidden');
        	}else{
        		$('#msg-count-evaluations').addClass('hidden');
        		$('#msg-no-evaluations').removeClass('hidden');
        	}
        	
        	(parseInt(data.co_authors_count) < 2) ? $('#msg-unique-coauthor').removeClass('hidden') : $('#msg-unique-coauthor').addClass('hidden');
        	
        		
        	
        	console.log(data);
        },
        error: function (jqXHR, textStatus, errorThrown) {
          $.parsifal.alert("Um erro ocorreu: ", jqXHR.responseText);
        }
      });
    
    $('#co-author-id').val(co_author_id);
    $("#remove-author-modal").modal('show');

  });

  $(".js-remove-visitor").click(function () {

    var user_container = $(this).closest("li");

    var csrf_token = $("[name='csrfmiddlewaretoken']").val();
    var user_id = $(this).closest("li").attr("data-user-id");
    var review_id = $("#review-id").val();
    var url = $(this).closest("ul").attr("data-remove-url");

    $.post(url, {
      'csrfmiddlewaretoken': csrf_token,
      'user-id': user_id,
      'review-id': review_id
    }, function () {
      $(user_container).fadeOut(400, function () {
        $(this).remove();
      });
      
      location.reload();
    });

  });

  var REGEX_EMAIL = '([a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*@' +
                    '(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)';

  $("*.contacts").selectize({
      persist: false,
      maxItems: null,
      valueField: 'email',
      labelField: 'name',
      searchField: ['name', 'email'],
      options: contacts_ok,
      render: {
          item: function(item, escape) {
              return '<div class="invite-minibox">' +
                  (item.name ? '<span class="name">' + escape(item.name) + '</span>' : '') +
                  (item.email ? '<span class="email">' + escape(item.email) + '</span>' : '') +
              '</div>';
          },
          option: function(item, escape) {
              var label = item.name || item.email;
              var caption = item.name ? item.email : null;
              return '<div>' +
                  '<span>' + escape(label) + '</span>' +
                  (caption ? '<span class="caption">' + escape(caption) + '</span>' : '') +
              '</div>';
          }
      },
      createFilter: function(input) {
          var match, regex;

          // email@address.com
          regex = new RegExp('^' + REGEX_EMAIL + '$', 'i');
          match = input.match(regex);
          if (match) return !this.options.hasOwnProperty(match[0]);

          // name <email@address.com>
          regex = new RegExp('^([^<]*)\<' + REGEX_EMAIL + '\>$', 'i');
          match = input.match(regex);
          if (match) return !this.options.hasOwnProperty(match[2]);

          return false;
      },
      create: function(input) {
          if ((new RegExp('^' + REGEX_EMAIL + '$', 'i')).test(input)) {
              return {email: input};
          }
          var match = input.match(new RegExp('^([^<]*)\<' + REGEX_EMAIL + '\>$', 'i'));
          if (match) {
              return {
                  email : match[2],
                  name  : $.trim(match[1])
              };
          }
          alert('Email inválido.');
          return false;
      }
  });
  
  




});
