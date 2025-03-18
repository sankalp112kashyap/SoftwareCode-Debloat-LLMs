#!/bin/bash

# Check if all arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <file> <model> <prompt>"
    exit 1
fi

# Assign arguments to variables
file=$1
model=$2
prompt=$3

# Create a branch name based on file, model, and prompt
branch_name="${file}_${model}_${prompt}"

# Create the new branch, add, commit, and push the changes
git checkout -b "$branch_name" && git add . && git commit -m "Debloat"

# Create the pull request with a title containing the prompt
gh pr create --title "Debloat ${file} using ${model}: Prompt ${prompt}" --body "Prompt: ${prompt}"