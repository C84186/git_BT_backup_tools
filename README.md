# git_BT_backup_tools

https://pypi.org/project/git-bt-backup-tools/

```bash
pip install git-bt-backup-tools
```

## Motivation

Versioning your bittorrent state folder can have a lot of benefits - If something goes wrong, for some clients (ahem, qbittorrent), 
corrupted fastresumes can really break your whole client, leaving you no easy way to get back to what you had. 

By restoring to a known, working state, you're able to reverse a catastrophic failure.

Almost every guide that directs you to do anything that touches your fastresumes (migrate across clients, across servers, etc) comes with
a great big warning "BACKUP YOUR BT_backup FOLDER BEFORE DOING THIS".

They're not wrong- I've f*cked things up with no way to unf*ck them besides starting fresh on a few occasions.

There are a lot of way to back your state folder up, but personally, I really like `git` for understanding how things change between versions.

Unfortunately, there are aspects of the `bencode` schema (the way that .torrent & .fastresume files are structured) that don't lend themselves to
comfortable viewing of differences with default git tools.

This package aims to provide convenience tools for making managing your bittorrent clients' state folder using `git` a bit easier.

In particular, (as of right now, at least) it provides a tool that parses the ugly `bencoded` torrents & emits pretty, diffable `yaml` equivalents.

## Background

Let's examine exactly what a `bencode` looks like:

```bash
cat ubuntu-20.04.2.0-desktop-amd64.iso.torrent
```
This is a fairly long file - here's the "good" part:

```
d8:announce35:https://torrent.ubuntu.com/announce13:announce-listll35:https://torrent.ubuntu.com/announceel40:https://ipv6.torrent.ubuntu.com/announceee7:comment29:Ubuntu CD releases.ubuntu.com10:created by13:mktorrent 1.113:creation datei1613070152e4:infod6:lengthi2877227008e4:name34:ubuntu-20.04.2.0-desktop-amd64.iso12:piece lengthi262144e6:pieces219520:
```

After this, we get something like the following:

```
pieces219520:؛0S(m2&Xcmc(u(轩)ΰcTGٵ$/}@S\Q_Yx@p9jFtoy
Q#~hL)VuA5īMcDGDK咮}aJ>!:솦ռwJBM5LQE    O{;ۯD:ih"                                 "
W;~s>^
u%
  2n(QEr{!KD$%qnnf|BuÈ-\r
```

Yes, that looks like garbage.

For a while. `bencode`s are fairly efficient, and (presumably) easy to parse encodings -
There's a few datatypes that are represented with a character at the start of the key, and the length of a given field is specified at the start of that field.

Fields like `pieces` tend to have variable length, and comprise most of a typical torrent file, as they contain information about the actual file/s to be downloaded.

These fields are also binary gobbedygook.

The changes in `bencode`d files actually follow a very sane, predictable pattern, however.

If we look at the "good" part of the above ubuntu torrent, we notice that, though its not to best to read, its pretty understandable.

If we tried to feed it to a git diff, however, it'd be hard to see what information has actually changed, as its all one line.

This package provides a tool for viewing these files without the cruft - It truncates the ugly binary down to a terse checksum (Which still lets us see if there's been a change!), and 
gives us nice, readable yaml for the rest.

Before:

```bash
git diff long_infohash.fastresume
```
```udiff
diff --git a/long_infohash.fastresume b/long_infohash.fastresume
index 1155eef..58691e9 100644
Binary files a/long_infohash.fastresume and b/long_infohash.fastresume differ
```

After:

```bash
git diff long_infohash.fastresume
```

```udiff
diff --git a/long_infohash.fastresume b/long_infohash.fastresume
index 1155eef..58691e9 100644
--- a/long_infohash.fastresume
+++ b/long_infohash.fastresume
@@ -1,9 +1,11 @@
 ---
-active_time: 329004
+active_time: 343400
 added_time: 1613033405
 allocation: sparse
 apply_ip_filter: 1
 auto_managed: 1
+banned_peers: 25...
+banned_peers6: ''
 completed_time: 1613250199
 disable_dht: 0
 disable_lsd: 0
@@ -11,21 +13,20 @@ disable_pex: 0
 download_rate_limit: -1
 file-format: libtorrent resume file
 file-version: 1
-finished_time: 112210
+finished_time: 126605
 httpseeds: []
 info-hash: long_infohash 
 last_download: 1613250199
-last_seen_complete: 1613280837
+last_seen_complete: 0
 last_upload: 1613252804
 libtorrent-version: 1.2.11.0
 max_connections: 100
 max_uploads: -1
-name: 'redacted'
 num_complete: 1
 num_downloaded: 16777215
-num_incomplete: 0
+num_incomplete: 1
 paused: 0
-peers: 6f77b...
+peers: 056b9...
 peers6: ''
 pieces: '0xcdf1046d'
 qBt-category: ''
@@ -39,7 +40,7 @@ qBt-seedingTimeLimit: -2
 qBt-tags: []
 save_path: /data/cool_storage/qBittorrent/Complete
 seed_mode: 0
-seeding_time: 112210
+seeding_time: 126605
 sequential_download: 0
 share_mode: 0
 stop_when_ready: 0
```

Wow! it's now super obvious what's changed - The torrent has been active a bit more, some peers appear to
have been banned, for some reason the name field has disappeared (whatever, it looks fine it qbittorrent i guess?).
Also, the peers have changed.


## Recovering Corrupted Fastresumes


> Faced the same issue, here is a workaround:
>
> In the BT_backup directory some files are empty, the size is 0
>
> ```
> $ ls -la *.fastresume
> -rw-r--r-- 1 pi pi  1417 Nov 22 10:37 0b42a9f27fcafd5492cfb3ca1b1c1ac305ca8453.fastresume
> -rw-r--r-- 1 pi pi  2194 Nov 22 10:39 14e482bccff6f09a41c320717bbaacd5df18b527.fastresume
> ...
> -rw-r--r-- 1 pi pi     0 Nov 21 15:47 ea2ac2a342f52a38e808efaebc3d0efcced33827.fastresume
> -rw-r--r-- 1 pi pi     0 Nov 21 15:50 ee0c9efe8aefb24d2c97dba6e64a6facd70d10f7.fastresume
> -rw-r--r-- 1 pi pi  1111 Nov 22 10:40 f3ff92ec3e565a5286a28e4e0317aa32896dedd3.fastresume
> ```
>
> Now, you have to close qBittorrent, replace the empty data files with a non-empty one
> 
> ```
> $ cp f3ff92ec3e565a5286a28e4e0317aa32896dedd3.fastresume ee0c9efe8aefb24d2c97dba6e64a6facd70d10f7.fastresume
> ```
> 
> Start qBittorrent again and you'll see this torrent's back. You would need to run a recheck on these recovered torrents. 
> 
> To recover all the files you can use something like this:
> ```
> VALID_FILE=$(find ~/.local/share/data/qBittorrent/BT_backup -name '*.fastresume' -size +1c -print -quit)
> find ~/.local/share/data/qBittorrent/BT_backup -name '*.fastresume' -size 0 -exec cp "${VALID_FILE}" "{}" \;
> ```

_Originally posted by @jackivanov in https://github.com/qbittorrent/qBittorrent/issues/4850#issuecomment-557485884_
