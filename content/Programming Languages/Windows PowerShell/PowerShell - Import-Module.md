I was working on a large [[Windows Powershell]] tool at work that required me to load modules at runtime. Here is an easy way to determine if you are looking at a regular PS script versus a PS module.

- If the script ends in .ps1, regular PS script
- If the script ends in .psm1, this is a PS module

I use the modules to write small functions and this allows me to be very modular and makes it easy to debug and troubleshoot issues.

What I wanted to share with you all is the function I use to load the modules at run time. It is small and works very well.

``` powershell
function loadModules {
Param ($MODULES)
	foreach($MODULE in $MODULES) {
		$MOODULE_PATH = $PSScriptRoot + $MODULE.path
		Import-Module -Name $MODULE_PATH -Force -ErrorAction SilentlyContinue
	}
}
```

**Important:** If your module has any errors the code above will suppress the errors. So while in dev mode, remove the "-Force -ErrorAction SilentlyContinue" piece. Enjoy! 