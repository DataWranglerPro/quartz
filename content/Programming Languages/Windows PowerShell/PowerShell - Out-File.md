I was working on a task in [[Windows Powershell]] and I needed to save the results of a variable into a text file. I used the code below to loop through the variable and append to a file. The PS code will create the text file if it does not exists at run time.

``` powershell
foreach ($r in $my_var) {
	$r | Out-File -append myFile.txt
}
```