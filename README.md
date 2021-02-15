# git_BT_backup_tools

https://pypi.org/project/git-bt-backup-tools/

## Aim

This package aims to provide convenience tools for making managing your bittorrent clients' state folder using `git` a bit easier.

## Background

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

