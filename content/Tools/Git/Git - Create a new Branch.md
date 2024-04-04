
# Using PowerShell

**Note:** I am assuming you already have git installed on your machine or at work

``` powershell
# clone your repository
git clone https://someRepo/app.git

# navigate to your cloned repo
# git by default will create a new folder with the name of the last string in the url
cd app

# this tells you what branches are available and which branch you are currently on
git branch --list

# -b is used to create and switch to the new branch
git checkout -b myNewBranch

# if you wanted to switch to an existing branch
git checkout myExistingBranch

# if you made changes to your branch and want to stage all changes, including new, modified, and deleted files.
git add -A

# commit and add a commit message
git commit -m "add your commit message here"

# push changes back to your repo (assumming you are pushing back to master branch)
# you can also write this git push --set-upstream origin master
git push -u origin master

# push changes back to a branch named myNewBranch
git push --set-upstream origin myNewBranch
```