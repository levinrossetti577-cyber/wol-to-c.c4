@echo off
rem Ziehe deine Skin-PNG mit der Maus auf diese Datei.
if "%~1"=="" (
  echo Ziehe deine Skin-PNG mit der Maus auf diese Datei.
  pause
  exit /b
)
copy /Y "%~1" "%~dp0src\main\resources\assets\catgirlwolf\textures\entity\catgirl_wolf.png" >nul
if errorlevel 1 (echo Fehler beim Kopieren.) else (echo Skin eingesetzt. Jetzt die Mod bauen, siehe README.)
pause
