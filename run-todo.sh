#!/bin/bash

cd "$(dirname "$0")"

.venv/bin/python src/todo.py

rm -rf src/boxes_tui/__pycache__
rm -rf src/boxes_tui/widgets/__pycache__