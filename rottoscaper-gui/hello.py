
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_flask():
	return 'Hello Flasky! Debug on'

@app.route('/about')
def about():
	text = "If it can match URLs, can Flask also generate them?\
	Of course it can. To build a URL to a specific function you\
	can use the url_for() function. It accepts the name of the\
	function as first argument and a number of keyword arguments,\
	each corresponding to the variable part of the URL rule. Unknown\
	variable parts are appended to the URL as query parameters."
	return text


@app.route('/hello/<damon>')
def hello(damon):
	return 'Hello %s @developer of Daemon' % damon

@app.route('/hello/<int:postid>')
def show_post(postid):
	return 'Hello %d Post' % postid

if __name__ == '__main__':
	app.run(debug=True)
