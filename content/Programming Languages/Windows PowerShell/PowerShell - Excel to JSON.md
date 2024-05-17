I was helping a co-worker and she needed to convert an Excel sheet into a JSON file. Below is a quick tip on how to do this. She was doing this manually so I thought she give PS a try to see if it can save her hours of copy/pasting.

- Open your Excel file and save the sheet as a .csv file
- Open [[Windows Powershell]] and cd into the folder location of where you saved the .csv file
- Type the code below into PS
``` powershell
$data = Import-Csv -Path "YOUR_FILE.csv"
$json = $data | ConvertTo-Json
Set-Content -Path "output.json" -Value $json
```