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

### Run the server

```bash
make serve
```

And there should be something happening at http://localhost:8000/

## Updating your archive

The first time it runs, it searches for the (semantically) latest file under `archive/` and unpacks it to `toots/`, and as long as `toots/` remains populated it will not unpack on subsequent runs. If you get a newer archive file, you can run

```bash
make refresh serve
```

to nuke `toots/` and force the new content to be extracted.

## How it searches

The search method is hopelessly naive:

```python
return list(filter(lambda x: query.upper() in x["object"]["content"].upper(), toots))
```

It's basically looking for a (case-insensitive) match for the string `query` *anywhere* in the content of the toots. If you search for `a` or something you're gonna get a lot of results.

## This is mostly terrible

This idea formed itself as I was riding my bike round Victoria Park this lunchtime, and I've basically lashed this whole thing together this afternoon - a valid use of my day off, I'm sure you'll agree. Anyway, if you have ideas about

* how to implement better searching (that doesn't involve ElasticSearch or something), or
* how to make the design look less shit

I'd *really* like to hear from you.
