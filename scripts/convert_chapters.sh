#!/bin/bash
# Convert chapters 4-11 to text

for num in 04 05 06 07 08 09 10 11; do
    docx_file=$(ls output/chapter_${num}_*.docx 2>/dev/null | head -1)
    if [ -f "$docx_file" ]; then
        python3 -c "import docx2txt; text = docx2txt.process('$docx_file'); print(text)" > "output/txt/chapter_${num}.txt"
        echo "Converted $docx_file"
    fi
done
