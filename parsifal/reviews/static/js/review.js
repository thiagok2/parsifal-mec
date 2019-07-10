$(function () {

  $(".js-leave").click(function () {
    $(this).closest("form").submit();
  });

  $(".js-remove-author").click(function () {

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
      options: contacts,
      render: {
          item: function(item, escape) {
              return '<div>' +
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
  
  $("#btn-open-import-protocol").click(function () {
	  
	
	
	$.ajax({
  		url: '/reviews/published_protocols/',
  		data: { 'review-id': $('#review-id').val() },
  		cache: false,
  		type: 'get',
  		success: function (data) {
  			
  			$("#modal-published-protocols table tbody").html(data);
  			$("#modal-published-protocols").before("<div class='shade'></div>");
  			$("#modal-published-protocols").slideDown(400, function () {
  				$("body").addClass("modal-open");
  			});
  		}
	   });
	
  });
  
  $("table#tbl-import-protocols").on("click", "tbody tr", function () {
  	
      var hiddenClass = $(this)[0].nextElementSibling;
      hiddenClass.className == "hidden"
      ? hiddenClass.className = ""
      : hiddenClass.className = "hidden"
  });

});
