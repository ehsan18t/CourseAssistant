@ECHO OFF
FOR %%A IN (src\*.css) DO (
    START /B npx tailwindcss -i "src/%%~nA.css" -o "public/%%~nA.css" --watch
    )