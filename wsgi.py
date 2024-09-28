from test_server import app, test_vect_post

print("Starting the WSGI script")
if __name__ == '__main__':
    # test_vect_post()
    app.run(debug=True)
