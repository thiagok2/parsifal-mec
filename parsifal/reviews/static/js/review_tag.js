$(function () {

    $("#tags").selectize({
      plugins: ['remove_button'],
      multiple: true,
      selectOnTab: true,
      persist: false,
      preload: true,
      create: function(input, callback) {
        var review_id = $("#review-id").val();
        var csrf_token = $("#tag-form input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: '/reviews/save_tag/',
            data: {
              'review-id': review_id,
              'tag-id': 'None',
              'description': input,
              'csrfmiddlewaretoken': csrf_token
            },
            type: 'post',
            cache: false,
            success: function (response) {
              return callback({
                  value: response.id,
                  text: response.tag
              });
            }
        });
      },
      onInitialize: function() {
        var selectize = this;
        var review_id = $("#review-id").val();
        $.ajax({
            url: '/reviews/load_tags/',
            type: 'get',
            data: {
                'review-id': review_id
            },
            success: function(response) {
                var review_tags = [];
                $.each(response, function(e, tag) {
                    selectize.addOption({value: tag.id, text: tag.tag});
                    review_tags.push(tag.id);
                })
                selectize.setValue(review_tags);
            }
        })
      },
      onItemRemove: function(tagId) {
        var review_id = $("#review-id").val();
        var tag_id = tagId
        var csrf_token = $("#tag-form input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            url: '/reviews/remove_tag/',
            data: {
                'review-id': review_id,
                'tag-id': tag_id,
                'csrfmiddlewaretoken': csrf_token
            },
            type: 'post',
            cache: false
        });
      }
    });

  });
