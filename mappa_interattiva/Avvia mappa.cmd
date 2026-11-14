@echo off
powershell -NoProfile -Command "$mapDir='%~dp0'; Start-Process -FilePath 'node.exe' -ArgumentList ('"' + (Join-Path $mapDir 'server.cjs') + '"') -WorkingDirectory $mapDir -WindowStyle Hidden; Start-Sleep -Milliseconds 700; Start-Process 'http://127.0.0.1:8767/mappa_interattiva/index.html'"
