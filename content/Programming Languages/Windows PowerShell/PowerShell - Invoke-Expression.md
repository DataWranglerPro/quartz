I needed a way to run a [[Windows Powershell]] command and save the contents of the results in a variable. At first, I was not sure how to run a command inside a PS window.

Here is how I did it.
``` powershell
# let's say I wanted to ping an IP Address and save the results of the ping in a variable
$result = Invoke-Expression 'ping 8.8.8.8'

# here are the contents of the results
$result

Pinging 8.8.8.8 with 32 bytes of data:
Reply from 8.8.8.8: bytes=32 time=26ms TTL=56
Request timed out.
Reply from 8.8.8.8: bytes=32 time=30ms TTL=56
Request timed out.

Ping statistics for 8.8.8.8:
    Packets: Sent = 4, Received = 2, Lost = 2 (50% loss),
Approximate round trip times in milli-seconds:
    Minimum = 26ms, Maximum = 30ms, Average = 28ms

# now you can search the variable for specific sub strings
if ($result -like "*100% loss*") {
	# do something
} else {
	# do something
}
```
