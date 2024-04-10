from vticket_app.utils.response import RestResponse

def not_found_404_handler(request, exception):
    return RestResponse().defined_error().set_message("Tài nguyên không tồn tại!").response