'slient run, no cmd win popup
Set ws = CreateObject("Wscript.Shell")     
currentpath = createobject("Scripting.FileSystemObject").GetFolder(".").Path
ws.run "cmd /c "&currentpath&"\sh-dd373.bat",0