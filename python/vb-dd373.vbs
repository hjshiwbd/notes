'slient run, no cmd win popup
Set ws = CreateObject("Wscript.Shell")     
currentpath = createobject("Scripting.FileSystemObject").GetFile(Wscript.ScriptFullName).ParentFolder.Path
'msgbox currentpath
ws.run "cmd /c "&currentpath&"\sh-dd373.bat",0