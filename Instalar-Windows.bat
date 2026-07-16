@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul && ( py -3 instalar.py & goto done )
where python >nul 2>nul && ( python instalar.py & goto done )
echo.
echo  Python 3 nao foi encontrado neste PC.
echo  Instale em: https://www.python.org/downloads/
echo  (marque a opcao "Add Python to PATH" durante a instalacao)
echo  Depois, execute este arquivo novamente.
echo.
pause
:done
