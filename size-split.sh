#!/bin/bash

# txt-split by shingyu
#
# To the extent possible under law, the person who associated CC0 with
# txt-split has waived all copyright and related or neighboring rights
# to txt-split.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

# Determine default locale

if [[ $LANG == *"zh"* ]]; then
    CN=true
else
    CN=false
fi

print_with_locale() {
    if $CN; then
        echo "$1"
    else
        echo "$2"
    fi
}

input_with_locale() {
    if $CN; then
        read -p "$1" input_var
    else
        read -p "$2" input_var
    fi
    echo "$input_var"
}

# Get input file name/path
if [ $# -lt 1 ]; then
    input_fn=$(input_with_locale "请输入分割文件名/路径:\n" \
                                 "Please input the file name/path to split:\n")
else
    input_fn=$1
fi

# Get split size
size_input=$(input_with_locale "请输入分割后每文件大小（如10MiB, 20MB, 300KB, 500KiB）:\n" \
                               "Please input the size of each file after splitting:\n"\
                               "(such as 10MiB, 20MB, 300KB, 500KiB):\n")

# Get output file name prefix
output_fnh=$(input_with_locale "请输入分割后文件名:\n" \
                               "Please input the file name after splitting:\n")

# Parse size function
parse_size() {
    size_str=$1
    declare -A units=(
        ["B"]=1 ["KB"]=1000 ["MB"]=1000000 ["GB"]=1000000000 ["TB"]=1000000000000
        ["KiB"]=1024 ["MiB"]=1048576 ["GiB"]=1073741824 ["TiB"]=1099511627776
    )
    size_str=$(echo "$size_str" | tr '[:lower:]' '[:upper:]' | sed 's/ //g')
    if [[ $size_str =~ ^([0-9]+(\.[0-9]+)?)([KMGT]?I?B)$ ]]; then
        size="${BASH_REMATCH[1]}"
        unit="${BASH_REMATCH[3]}"
        echo $(echo "$size * ${units[$unit]}" | bc)
    else
        echo "Invalid size string" >&2
        exit 1
    fi
}

# Split file function
split_file_by_size() {
    input_file=$1
    output_prefix=$2
    max_size=$3

    file_number=1
    current_size=0
    output_file="${output_prefix}_${file_number}.txt"

    while IFS= read -r line; do
        line_size=$(echo -n "$line" | wc -c)
        line_size=$(( line_size + 1 ))  # Account for newline character

        if [ $(( current_size + line_size )) -gt $max_size ]; then
            file_number=$(( file_number + 1 ))
            current_size=0
            output_file="${output_prefix}_${file_number}.txt"
        fi

        echo -n "$line" >> "$output_file"
        echo >> "$output_file"
        current_size=$(( current_size + line_size ))
    done < "$input_file"
}

# Parse input size
output_size=$(parse_size "$size_input")

# Call split function
split_file_by_size "$input_fn" "$output_fnh" "$output_size"
