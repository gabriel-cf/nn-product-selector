for i in $(find . -name "*.py" | grep -v __init); do pyreverse -o png -ASmy $i -p $(echo $i | rev | cut -d"/" -f1 | rev); done
