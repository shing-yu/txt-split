#!/bin/bash

CN=false
default_lang=$(locale | grep LANG= | cut -d= -f2)
if [[ $default_lang == zh* ]]; then
    CN=true
fi

print_with_locale() {
    if [ "$CN" = true ]; then
        echo "$1"
    else
        echo "$2"
    fi
}

input_with_locale() {
    if [ "$CN" = true ]; then
        read -p "$1"
    else
        read -p "$2"
    fi
}

if [ "$#" -lt 1 ]; then
    input_fn=$(input_with_locale "请输入分割文件名/路径:" \
                                 "Please input the file name/path to split:")
else
    input_fn="$1"
fi

output_fls=$(input_with_locale "请输入分割后每文件行数:" "Please input the number of lines per file:")
output_fnh=$(input_with_locale "请输入分割后文件名:" "Please input the file name after splitting:")

split_file() {
    input_file="$1"
    output_prefix="$2"
    num_lines_per_file="$3"

    line_number=1
    file_number=1
    output_file="${output_prefix}_${file_number}.txt"

    while IFS= read -r line; do
        echo "$line" >> "$output_file"
        ((line_number++))

        if [ "$line_number" -gt "$num_lines_per_file" ]; then
            line_number=1
            ((file_number++))
            output_file="${output_prefix}_${file_number}.txt"
        fi
    done < "$input_file"
}

split_file "$input_fn" "$output_fnh" "$output_fls"
