from flask import Flask, render_template, send_from_directory, request
import youtube

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
@app.route('/<part>')
def root(part=None):
	if request.method == "POST":
		if request.form.get("func") == "youtube":
			api_key = request.form.get("apikey")
			keyword = request.form.get("keyword")
			return youtube.YoutubeSearch(api_key, keyword)
	elif(part is None):
		return render_template('index.html')
	elif(part == 'm1'):
		return render_template('m1.html')
	elif(part == 'm2'):
		return render_template('m2.html')
	elif(part == 'm3'):
		return render_template('index.html', part=part)
	elif(part == 'm4'):
		return render_template('index.html', part=part)
	elif(part == 'favicon.ico'):
		return send_from_directory(app.static_folder, 'favicon.ico')
	return "<h2>Not found.</h2>"


if __name__=="__main__":
	# app.run()
	# debug를 할 때
	app.run(debug=True)
	# host 등을 직접 지정하고 싶다면
	# app.run(host="127.0.0.1", port="5000")
