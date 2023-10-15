from flask import Flask, render_template, request
from whoosh import index
from whoosh.qparser import QueryParser

from indexer import not_indexed, refresh

if not_indexed():
    refresh()

app = Flask(__name__)
ix = index.open_dir("toot_index")
app.query_parser = QueryParser("content", schema=ix.schema)


@app.route("/", methods=["GET"])
def home() -> str:
    """Home page."""
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search() -> list:
    """Do the search."""
    args = request.args
    query = app.query_parser.parse(args["query"])

    with ix.searcher() as s:
        results = sorted(
            [dict(x) for x in s.search(query, limit=1000)],
            key=lambda x: x["datestamp"],
            reverse=True,
        )

        for result in results:
            result["datestamp"] = str(result["datestamp"])

        return results


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
