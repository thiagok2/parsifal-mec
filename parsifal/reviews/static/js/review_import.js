$(function () {

	$("#btn-open-import-protocol").click(function () {

		
		var review_id = $('#review-id').val();
		$.ajax({
			url: '/reviews/published_protocols/',
			data: { 'review-id':  review_id},
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

	$("table#tbl-import-protocols").on("click", "tbody tr.exported-review", function () {

		var trDetails = $(this)[0].nextElementSibling;
		trDetails.className.includes("hidden") ? trDetails.className = "" : trDetails.className = "hidden";


		if(trDetails.className.includes("hidden")){
			$(this).removeClass('active');
			$(this).removeClass('font-bold');
			$(this).filter( "td.td-detail-protocol button span" ).addClass('glyphicon-zoom-in');
			$(this).filter( "td.td-detail-protocol button span" ).removeClass('glyphicon-zoom-out');
		}else{
			$(this).addClass('active');
			$(this).addClass('font-bold'); 
		}

		$(this).find('td.td-detail-protocol .glyphicon').filter(function() {
			if($(this).hasClass('glyphicon-zoom-in')){
				$(this).removeClass('glyphicon-zoom-in')
				$(this).addClass('glyphicon-zoom-out')
			}else{
				$(this).addClass('glyphicon-zoom-in')
				$(this).removeClass('glyphicon-zoom-out')
			}

		});

	});

	$("table#tbl-import-protocols").on("click", "tbody tr.exported-review button.btn-import-protocol", function () {
		var protocolId = $(this).data( "protocol-id" );
		var elementId = '#td-protocol-name-'+protocolId;
		var protocolName = $(elementId).text();

		$('#label_protocol_import1').text(protocolName);
		$('#label_protocol_import2').text(protocolName);

		$('#protocol-import-id').val(protocolId)

	});

	$("#enable-confirm-import").click(function () {
		if ($(this).is(":checked")) {
			$("#btn-confirm-import-protocol").prop("disabled", false);
		}
		else {
			$("#btn-confirm-import-protocol").prop("disabled", true);
		}
	});


	$("#btn-confirm-import-protocol").click(function () {

		$.ajax({
			url: '/reviews/import_protocol/',
			data: { 

				'review-id': $('#review-id').val(),
				'protocolId': $('#protocol-import-id').val(),
				'importDetail': $('#check_protocol_details').prop('checked'),
				'importProtocol': $('#check_protocol_protocol').prop('checked'),
				'importChecklist': $('#check_protocol_checklist').prop('checked'),
				'importRisks': $('#check_protocol_risks').prop('checked'),
				'importDataExtraction': $('#check_protocol_data_extraction').prop('checked')
				//'clearFiedls': $('#check_clear_review').prop('checked')

			},
			cache: false,
			type: 'get',
			success: function (data) {

				$("#modal-confirm-import").modal("hide");
				$("#modal-published-protocols").modal("hide");

				location.reload();


			}
		});
	});

});
