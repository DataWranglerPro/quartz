In Jenkins we are able to run shell commands in the runtime container.

# How to create folders

- `ls`: This command lists the files and directories in a directory.
- `-a` (all): Includes hidden files (those starting with `.`) in the listing.
- `-l` (long): Displays detailed information about each file, including permissions, ownership, and timestamps.
- `-R` (recursive): Lists the contents of subdirectories recursively.

``` sh
container('my-container'){
	sh "mkdir /var/folder1/outbox"
	sh "chmod -R 777 /var/folder1"
	sh "echo '================='"
	sh "ls -alR /var/folder1"
}
```

