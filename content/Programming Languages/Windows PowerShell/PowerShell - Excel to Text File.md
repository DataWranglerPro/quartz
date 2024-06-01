At work, I had am employee who was avoiding a data task. He needed to Export a couple of columns into an Excel file. This is normally not that difficult, but he told me he needed help writing a script. He wanted every cell in the column to be exported into an individual text file. He started doing this manually (copy/paste) and realized this was going to take many hours. I think he had about 300+ files to create.

Here is the solution I came up with:

``` powershell
# set file paths
$excelFilePath = "C:\test\test_cases.xlsx"
$outputFolder = "C:\test\"

# open Excel file
$excel = New-Object -ComObject Excel.Application
$workbook = $excel.Workbooks.Open($excelFilePath)
$sheet = $workbook.Sheets.Item(1)

# set column and start row
$column = "A"
$startRow = 2
$endRow = 200

# loop through each cell in the column
for ($row = $startRow; $sheet.Cells.Item($row, $column).Value() -ne ""; $row++) {
	# get the cell value
	$cellValue = $sheet.Cells.Item($row, $column).Value()

	# exit on endRow
	if ($row -eq $endRow) {break}

	# create new text file for each cell
	$textFilePath = Join-Path -Path $outputFolder -ChildPath ("Column_$column-Cell_$row.txt")
	$cellValue | Out-File -FilePath $textFilePath -Encoding utf8
}

# close Excel file without saving
$workbook.Close($false)
$excel.Quit()
```