from appdir import app

if __name__ == '__main__':
    app.run(debug=True)

@app.route("/")
def index():
    return "<h1 style='color:red'>Hello World</h1>"

if __name__ == "__main__":
    app.run()