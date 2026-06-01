#!/bin/bash

# Usage: ./gitcheck.sh [-f] 2026-03-16 /path/to/projects "user name"
#        ./gitcheck.sh [-f] 2026-03-16 ~/Desktop/Workspace "user name\|user email"

FETCH_ENABLED=false
if [[ "$1" == "-f" ]]; then
    FETCH_ENABLED=true
    shift 
fi

TARGET_DATE=$1
PARENT_DIR=${2:-.}

GIT_CONFIG_NAME=$(git config --get user.name)
DEFAULT_NAMES="Max Huiskes\|max.huiskes"
USER_NAME=${3:-${GIT_CONFIG_NAME:-$DEFAULT_NAMES}}

if [ -z "$TARGET_DATE" ]; then
    echo "Usage: $0 [-f] YYYY-MM-DD [directory] [username]"
    exit 1
fi

echo "Checking activity for [$USER_NAME] on $TARGET_DATE..."
echo "Excluding: vendor/ and contrib/ folders"
echo "------------------------------------------------------"

# -prune prevents find from descending into the matching directories
find "$PARENT_DIR" \
    \( -name "vendor" -o -name "contrib" \) -prune \
    -o -name ".git" -type d -print | while read -r gitdir; do
    
    repo_dir=$(dirname "$gitdir")
    
    (
        cd "$repo_dir" || exit
        
        if [[ "$FETCH_ENABLED" == true ]]; then
            echo -ne "Fetching $repo_dir...\r"
            git fetch --all --quiet > /dev/null 2>&1
            echo -ne "\033[K" 
        fi
        
        logs=$(git log --all \
            --author="$USER_NAME" \
            --regexp-ignore-case \
            --since="$TARGET_DATE 00:00:00" \
            --until="$TARGET_DATE 23:59:59" \
            --decorate=short \
            --format="%h %d %ad %s" \
            --date=format-local:'%Y-%m-%d %H:%M:%S' \
            --shortstat)
        
        if [ -n "$logs" ]; then
            echo -e "\033[1;32mRepo: $repo_dir\033[0m"
            echo "$logs"
            echo "------------------------------------------------------"
        fi
    )
done