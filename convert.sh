#!/bin/bash

cd "$(dirname "$0")"

process_dir() {
    local dir_path="$1"
    output_dir_path="${dir_path/notebooks/src/boxes_tui}"
    if [ ! -e "$output_dir_path" ]; then
        mkdir "$output_dir_path"
    fi

    echo "Converting files in dir: $dir_path"

    for file in "$dir_path"/*.ipynb; do
        if [ -e "$file" ]; then
            output_file="${file/notebooks/src/boxes_tui}"
            echo "  > Converting $file to ${output_file%.ipynb}.py"
            $(pwd)/.venv/bin/jupyter nbconvert -y --log-level 'WARN' --to python $file --output-dir "$output_dir_path"
        fi
    done

    for file in "$dir_path"/*.py; do
        if [ -e "$file" ]; then
            echo "  > Copying $file to ${file/notebooks/src/boxes_tui}"
            cp $file ${file/notebooks/src/boxes_tui}
        fi
    done
}

export -f process_dir

find "$(pwd)/notebooks" -type d -exec bash -c 'process_dir "$0"' {} \;