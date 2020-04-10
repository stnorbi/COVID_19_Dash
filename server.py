STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
@server.route('/static/<resource>')
def serve_static(resource):
    return send_from_directory(STATIC_PATH, resource)