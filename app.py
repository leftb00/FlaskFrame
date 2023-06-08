from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
@app.route('/<part>')
def root(part=None):
	if(part is None):
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


if __name__=="__name__":
	# app.run()
	# debug를 할 때
	app.run(debug=True)
	# host 등을 직접 지정하고 싶다면
	# app.run(host="127.0.0.1", port="5000")
