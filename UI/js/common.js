var web_url = "/relation";

function commonErrorHandler(jqXHR, textStatus, errorThrown) {
    // Clear all timeouts
    var id = window.setTimeout(function () {}, 0);
    while (id--) {
        console.log(id);
        window.clearTimeout(id);
    }

    var err_title = 'alert_err_title';
    var err_str = "";

    if (jqXHR.status === 401) {
        authFailedHandler(jqXHR.responseJSON);
        return;
    } else if (jqXHR.status === 502) {
        err_str = 'alert_err_lost_connect';
    } else {
        if (jqXHR.responseJSON) {
            err_str = jqXHR.status + ": " + jqXHR.responseJSON.errorCode + 'alert_err_contact_admin';
        } else {
            err_str = jqXHR.status + ": " + 'alert_err_contact_admin';
        }
    }

    var ErrorModalHTML = '\
          <div class="modal fade" id="ErrorModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" style="display: none;"> \
          <div class="modal-dialog" role="document"> \
            <div class="modal-content"> \
              <div class="modal-header"> \
                <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">x</span></button> \
                <h4 class="modal-title" id="ErrorModalTitle"><!--Error Title Here--></h4> \
              </div> \
              <div class="modal-body"> \
                <form> \
                  <div class="form-group"> \
                    <p id="ErrorModalMsg"><!--Error Message Here--></p> \
                  </div> \
                </form> \
              </div> \
              <div class="modal-footer"> \
                <button type="button" class="btn btn-default" data-dismiss="modal">Close</button> \
              </div> \
            </div> \
          </div> \
        </div>';

    if ($("#ErrorModal").length > 0) {
        $("#ErrorModal").remove();
    }
    $("body > div > div.content-wrapper > section.content").append(ErrorModalHTML);
    $("#ErrorModalTitle").text(err_title);
    $("#ErrorModalMsg").text(err_str);
    $('#ErrorModal').modal('show')
    console.error(err_title + '>>' + err_str);
}
function req_ajax_get(a, b) {
    a.type = 'GET';
    // a.contentType = "application/json";
    // a.dataType = "json";

    var orig_error_func = a.error;
    a.error = function (jqXHR, textStatus, errorThrown) {
        if (typeof(orig_error_func) == 'function') {
            orig_error_func(jqXHR, textStatus, errorThrown);
        }
        commonErrorHandler(jqXHR, textStatus, errorThrown);
    }
    return $.ajax(a, b);
}
function req_ajax(a, b) {
    a.type = 'POST';
    a.contentType = "application/json";
    a.dataType = "json";

    var orig_error_func = a.error;
    a.error = function (jqXHR, textStatus, errorThrown) {
        if (typeof(orig_error_func) == 'function') {
            orig_error_func(jqXHR, textStatus, errorThrown);
        }
        commonErrorHandler(jqXHR, textStatus, errorThrown);
    }

    if (a.data) {
        a.data = JSON.stringify(a.data);
    }

    return $.ajax(a, b);
}
