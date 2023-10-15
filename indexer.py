import json
import tarfile
from datetime import datetime
from pathlib import Path

from whoosh import index
from whoosh.analysis import StemmingAnalyzer
from whoosh.fields import DATETIME, ID, KEYWORD, TEXT, Schema

schema = Schema(
    url=ID(stored=True),
    datestamp=DATETIME(stored=True),
    content=TEXT(analyzer=StemmingAnalyzer(), stored=True),
    hashtags=KEYWORD(stored=True, lowercase=True),
)


def unpack_archive(force: bool = False) -> None:
    """Unpack the Mastodon archive."""
    Path("toots").mkdir(exist_ok=True)

    unarchive = force
    if not Path("toots/outbox.json").exists():
        unarchive = True

    if unarchive:
        archive = sorted(Path("archive").glob("*"))[-1]
        print(f"unpacking {archive}")
        with tarfile.open(str(archive)) as ball:
            ball.extractall("toots")


def index_toots(refresh: bool = False) -> None:
    """Index the Toots."""
    if not Path("toot_index").exists():
        Path("toot_index").mkdir()

    do_index = refresh
    if not index.exists_in("toot_index"):
        do_index = True

    if do_index:
        print("indexing your toots")
        ix = index.create_in("toot_index", schema)

        ix = index.open_dir("toot_index")
        writer = ix.writer()

        outbox = json.loads(Path("toots/outbox.json").read_text())

        for count, toot in enumerate(outbox["orderedItems"]):
            if count % 100 == 0:
                print(f"{count}, ", end="", flush=True)

            if type(toot["object"]).__name__ == "dict":
                writer.add_document(
                    url=toot["object"]["url"],
                    content=toot["object"]["content"],
                    datestamp=datetime.fromisoformat(toot["object"]["published"]),
                    hashtags=" ".join(
                        x["name"]
                        for x in list(
                            filter(
                                lambda x: x["type"] == "Hashtag",
                                toot["object"]["tag"],
                            ),
                        )
                    ),
                )

        print("")
        print("committing index")
        writer.commit()


def not_indexed() -> bool:
    """Check if a toot search index doesn't already exist."""
    return not index.exists_in("toot_index")


def refresh() -> None:
    """Reindex for fresh toots."""
    unpack_archive(True)
    index_toots(True)


if __name__ == "__main__":
    refresh()
