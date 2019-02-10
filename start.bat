@echo off

:Loop
IF "%1"=="-d" GOTO Development
IF "%1"=="-p" GOTO Production
SHIFT
GOTO Loop

:Development
echo Starting development server
docker-compose -f docker-compose.dev.yml --build up
GOTO:EOF

:Production
echo Starting production server
docker-compose -f docker-compose.prod.yml --build up
GOTO:EOF