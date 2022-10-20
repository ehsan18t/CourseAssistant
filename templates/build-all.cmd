@ECHO OFF
FOR %%A IN (src\*.css) DO (
    ECHO %%A
    npx tailwindcss -i "src/%%~nA.css" -o "public/%%~nA.css" --minify
    ECHO.
    )
PAUSE
