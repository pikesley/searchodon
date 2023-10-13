from pathlib import Path

from flask import Flask, render_template, request

from utils import gather_toots, search_toots, unpack_archive

app = Flask(__name__)
if not Path("toots/outbox.json").exists():
    unpack_archive()
app.toots = gather_toots()


@app.route("/", methods=["GET"])
def home() -> str:
    """Home page."""
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search() -> list:
    """Do the search."""
    args = request.args

    return search_toots(app.toots, args["query"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
