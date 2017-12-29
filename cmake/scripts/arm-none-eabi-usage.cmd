REM -- Python wrapper for Windows
REM -- http://www.georgevreilly.com/blog/2007/01/13/PythonBatchfileWrapperRedux.html

@echo off
setlocal
set PythonExe=
set PythonExeFlags=-u

for %%i in (cmd bat exe) do (
  for %%j in (python.%%i) do (
    call :SetPythonExe "%%~$PATH:j"
  )
)

for /f "tokens=2 delims==" %%i in ('assoc .py') do (
  for /f "tokens=2 delims==" %%j in ('ftype %%i') do (
    for /f "tokens=1" %%k in ("%%j") do (
      call :SetPythonExe %%k
    )
  )
)

"%PythonExe%" %PythonExeFlags% "%~dpn0.py" %*
goto :EOF

:SetPythonExe
if not [%1]==[""] (
  if ["%PythonExe%"]==[""] (
    set PythonExe=%~1
  )
)
goto :EOF
