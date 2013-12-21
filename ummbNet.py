from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

@app.route('/', defaults={'dummy': ''})
@app.route("/<path:dummy>")
def catchAll(dummy):
	return render_template('ummbNet.html')

if __name__ == '__main__':
    app.run()
