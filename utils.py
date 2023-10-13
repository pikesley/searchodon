import json
import tarfile
from pathlib import Path


def unpack_archive() -> None:
    """Unpack the Mastodon archive."""
    Path("toots").mkdir(exist_ok=True)
    archive = sorted(Path("archive").glob("*"))[-1]
    print(f"Unpacking {archive!s}")
    with tarfile.open(str(archive)) as ball:
        ball.extractall("toots")


def gather_toots() -> list:
    """Collect the toot data."""
    print("Collecting toots")
    outbox = json.loads(Path("toots/outbox.json").read_text())
    return [
        toot
        for toot in reversed(outbox["orderedItems"])
        if type(toot["object"]).__name__ == "dict"
    ]


def search_toots(toots: list, query: str) -> list:
    """Impossibly crude toot-searcher."""
    return list(
        filter(lambda x: query.upper() in x["object"]["content"].upper(), toots),
    )
