import os

from flask import Flask
from flask import request
from flask import send_from_directory

app = Flask(__name__)

@app.route('/<path:path>')
def path(path):
    root_dir = os.path.dirname(os.getcwd())
    root_dir = os.path.join(root_dir, 'testing/Page')
    return send_from_directory(root_dir, path)
# If the script is run from the command line
if __name__ == "__main__":
    # Start a development server on port 8000
    # http://localhost:8000/test
    app.run(host="0.0.0.0", port=5000, debug=True)



# from flask import Flask, request, render_template
# from flask import send_from_directory
# import os

# app = Flask(__name__, static_url_path='')

# # # WORKING
# # @app.route('/path/<path:pathName>')
# # def path(pathName):
# # 	print(pathName)
# # 	root_dir = os.path.dirname(os.getcwd())
# # 	print(root_dir)
# # 	root_dir = os.path.join(root_dir, 'testing/Page')
# # 	print(root_dir+pathName)
# # 	return send_from_directory(root_dir,pathName)

# # NOT WORKING
# @app.route('/', defaults={'pathName':'HomePage.html'})
# @app.route('/<path:pathName>')
# @app.route('/path/<path:pathName>')
# def home(pathName):
# 	if pathName == '':
# 		pathName = "/HomePage.html"
# 	print(pathName)
# 	root_dir = os.path.dirname(os.getcwd())
# 	print(root_dir)
# 	root_dir = os.path.join(root_dir, 'testing/Page')
# 	print(root_dir+pathName)
# 	print(send_from_directory(root_dir,pathName))
# 	return send_from_directory(root_dir,pathName)

# if __name__ == "__main__":
# 	app.run(host='0.0.0.0', port=5000, debug=True)
