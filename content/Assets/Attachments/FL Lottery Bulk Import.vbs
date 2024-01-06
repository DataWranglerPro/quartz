'This code will grab the last 18 winning numbers and insert them into 
'sql table REVFlaLottery
 
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
 
 'Clear contents of REVFlaLottery 
 set rs = db.Execute("DELETE REVFlaLottery")
 
 set iim1= CreateObject ("imacros")
 iret = iim1.iimInit("")


 'Get one month worth of data
 iplay = iim1.iimPlay("The Florida Lottery Bulk")
 data = iim1.iimGetLastExtract()

 'Place macro results in an array
 If iplay = 1 and len (data) > 0 Then
 MyArray = Split(data, "[EXTRACT]")
 

  
 For num = 0 To arrLength(MyArray) - 1
 
 
 ' use SQL to insert new data
 sql = "insert into REVFlaLottery (Date, N1, N2, N3, N4, N5, N6) values ('" _
 & MyArray(num) & "', '" & MyArray(num + 1) & "' ,  '" & MyArray(num + 2) & "' ,  '" & MyArray(num + 3) & "' ,  '" & MyArray(num + 4) & "' , '" & MyArray(num + 5) & "' , '" & MyArray(num + 6) & "')"
 

 ' execute sql statement
 set rs = db.Execute(sql)
 

 'Increment counter
 num = num + 6
 
 Next

End If

    If iplay = 1 Then
	'MsgBox "The data was stored in the database. The script is now completed."
    ELSEIF iplay < 0 Then
	'MsgBox "Error!"
	 iret = iim1.iimSet("macro", "FL Lottery Bulk Import" + " " + iim1.iimGetLastError()) 
  	 iret = iim1.iimPlay("Gmail Error Template") 
    End If
 
 iret = iim1.iimExit


 'Find true length of any array
 Function arrLength(vArray)
 
 ItemCount = 0
 
 For ItemIndex = 0 To UBound(vArray)
 If Not(vArray(ItemIndex)) = Empty Then
     ItemCount = ItemCount + 1
 End If
 Next
 arrLength = ItemCount
 End Function

 

 
 WScript.Quit(0)
