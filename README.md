# Searchodon

## Search your own Mastodon archive

Twitter search always served (at least) two purposes for me: searching the whole site for whatever news was breaking (or attempting to work out what that day's Main Character had done), but also, searching _my own_ Tweets. I understand the reasons why we don't generally have search on the Fediverse, but not being able to search my own posts was proving a pain. So:

## Getting your archive

You should be able to get your archive from your Mastodon instance. For me, it's at https://mastodon.me.uk/settings/export.

## Running this

You'll need `docker` installed, then:

### Get the code

```bash
git clone https://github.com/pikesley/searchodon.git
```

### Add your archive

```bash
cd searchodon
cp ~/Downloads/archive-197001010000-somehash.tar.gz archive/
```

### Build the image

```bash
make build
make run
```

### Index the Toots

We need to build a [Whoosh](https://whoosh.readthedocs.io/en/latest/intro.html) index:

```bash
make refresh
```

### Run the server

```bash
make serve
```

And there should be something happening at http://localhost:8000/

## Indexing your Toots

At startup, it looks for a Whoosh index at `toot_index`, and if that doesn't exist, it:

* unpacks the (semantically) latest file under `archive` into `toots`, then
* runs the indexer

If you get a newer archive, you can force building of a new index with

```bash
make refresh
```

## It looks terrible

This idea formed itself as I was riding my bike round Victoria Park this lunchtime, and I've basically lashed this whole thing together this afternoon - a valid use of my day off, I'm sure you'll agree. Anyway, if you have ideas about how to make the design look less shit, I'd *really* like to hear from you.
