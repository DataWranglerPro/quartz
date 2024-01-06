'Note: EXTRACT requires Internet Explorer 6.0 or better to be installed 
 
 Dim MyArray
 Dim objFileSystem, objOutputFile
 Dim strOutputFile
 Dim pos
 
 
 
 ' find out current folder
 myname = WScript.ScriptFullName
 mypath = Left(myname, InstrRev(myname, "\"))
 
 
 ' access database
 set db = CreateObject("ADODB.Connection")
 
 'Change CONNECTION STRING here for different database:
 db.Open("Provider=SQLNCLI10;Server=david\sqlexpress;Database=BizIntel; Trusted_Connection=yes")
 
  
 
 set iim1= CreateObject ("imacros")
 iret = iim1.iimInit("")
 
 
 For num = 1 To 1 
    str = cstr(num)  'Convert integer to string
    iret = iim1.iimDisplay("Listing No: " + str)
 
    pos = num '+ 4'start at 5: Offset for POS= statement
    str = cstr(pos)  'Convert integer to string
    iret = iim1.iimSet("-var1", str) 'Select a new link for each run
 
    iplay = iim1.iimPlay("The Florida Lottery")
    data = iim1.iimGetLastExtract()
    If iplay = 1 and len (data) > 0 Then
       MyArray = Split(data, "[EXTRACT]")
 
 ' use SQL to insert new data
 sql = "insert into FlaLottery (Date, N1, N2, N3, N4, N5, N6) values ('" _
 & MyArray(0) & "', '" & MyArray(1) & "' ,  '" & MyArray(2) & "' ,  '" & MyArray(3) & "' ,  '" & MyArray(4) & "' , '" & MyArray(5) & "' , '" & MyArray(6) & "')"
 
 
 ' execute sql statement
 set rs = db.Execute(sql)
 
 End If
 
 
    If iplay = 1 Then
	'MsgBox "The data was stored in the database. The script is now completed."
    ELSEIF iplay < 0 Then
	'MsgBox "Error!"
	 iret = iim1.iimSet("macro", "FL Lottery Import" + " " + iim1.iimGetLastError()) 
  	 iret = iim1.iimPlay("Gmail Error Template") 
    End If

 Next
 
 iret = iim1.iimExit
 

 
 WScript.Quit(0)
