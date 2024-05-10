I was working on an extensive [[Windows Powershell]] project where we needed to install certain tools via a simple unzip. The set of tools where zipped up and all I had to do is move the zip file into the users computer, unzip the file, and then delete the original .zip file.

The task was more or less a simple one. The issue I had was that after the file was unzipped, I ended up with a weird looking folder name.

Let's look at some code.

``` powershell
# unzip a file
Expand-Archive -Path $source_path -DestinationPath $desc_path -Force
```

The code above simply grabs a zip file from a source directory and then unzips it in a different directory. 

The issue is that the unzipped folder ended with a weird name like:
- c:/apps/tools/coolTool20240101-v123

The end user wanted the folder name to say "coolTool" and remove any other text. I tried to mess with the Expand-Archive line but I was not getting the result I needed.

## Rename-Item
PS comes with a lot of functionality and it also has the ability to rename items. So this is what I needed to use to rename the folder after it was unzipped.

``` powershell
# unzip a file
Expand-Archive -Path $source_path -DestinationPath $dest_path -Force

# rename the folder
Rename-Item -Path $dest_path -NewName "coolTool" -Force

# remove original zip file
Remove-Item -Path $source_path -Force -ErrorAction SilentlyContinue
```