#!/usr/bin/env bash

DESTINATION="/run/media/human/CIRCUITPY"

cp display.py "$DESTINATION"
cp ledNormal.py "$DESTINATION"
cp switchAndLed.py "$DESTINATION"
cp hardware.py "$DESTINATION"
cp tools.py "$DESTINATION"
cp game.py "$DESTINATION"
cp power.py "$DESTINATION"
cp main.py "$DESTINATION"

echo "Files copied successfully to $DESTINATION"
