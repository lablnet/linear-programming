# check if $1 exists in parameter.
if [ -z "$1" ]; then
  echo "Usage: $0 pdf"
  echo "Usage: $0 html"
  exit 1
fi

# export
jupyter nbconvert notes.ipynb --to $1

# move expoted file to exported directory
mv notes.${1} exported/notes.${1}
