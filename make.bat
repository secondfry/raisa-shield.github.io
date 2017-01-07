@ECHO OFF

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set BUILDDIR=build
set ALLSPHINXOPTS=-d %BUILDDIR%/doctrees %SPHINXOPTS% .

if "%1" == "" goto html

if "%1" == "html" (
	:html
	python scripts/update-npc.py
	python scripts/update-fits.py
	python scripts/wallet.py # && cp srp.json $(BUILDDIR)/
	%SPHINXBUILD% -b html %ALLSPHINXOPTS% %BUILDDIR%/
	echo ''>>%BUILDDIR%/.nojekyll
	if errorlevel 1 exit /b 1
	echo.
	echo.Build finished. The HTML pages are in %BUILDDIR%/html.
	goto end
)

if "%1" == "clean" (
	for /d %%i in (%BUILDDIR%\*) do rmdir /q /s %%i
	del /q /s %BUILDDIR%\*
	goto end
)

:end
