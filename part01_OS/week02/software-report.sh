#!/bin/bash

output="software-report.tsv"

# Column headings
printf "Package\tDescription\tInstalled\tInstalled version or version to install\tLocation\tWebsite\n" > "$output"

while IFS="|" read -r package formula command description website; do

    location=$(which "$command" 2>/dev/null)

    if [ -n "$location" ]; then
        installed="Yes"

        # tmux uses -V instead of --version
        if [ "$command" = "tmux" ]; then
            version=$("$command" -V)
        else
            version=$("$command" --version 2>&1 | head -n 1)
        fi
     else
    installed="No"
    location="Not installed"

    brew_version=$(brew info "$formula" 2>/dev/null |
        head -n 1 |
        sed -E 's/.*stable ([^ ,]+).*/\1/')

    if [ -n "$brew_version" ]; then
        version="Homebrew would install $brew_version"
    else
        version="Version not found"
    fi
fi

printf "%s\t%s\t%s\t%s\t%s\t%s\n" \
        "$package" "$description" "$installed" \
        "$version" "$location" "$website" >> "$output"

done <<'PACKAGES'
python3|python|python3|Programming language|https://www.python.org/
R|r|R|Programming language for statistics and graphics|https://www.r-project.org/
git|git|git|Distributed version-control system|https://git-scm.com/
tree|tree|tree|Displays directories in a tree format|https://oldmanprogrammer.net/source.php?dir=projects/tree
wget|wget|wget|Downloads files from the internet|https://www.gnu.org/software/wget/
curl|curl|curl|Transfers data using URLs and network protocols|https://curl.se/
htop|htop|htop|Interactive system process viewer|https://htop.dev/
tmux|tmux|tmux|Manages multiple persistent terminal sessions|https://github.com/tmux/tmux
tldr|tlrc|tldr|Provides short examples for command-line programs|https://tldr.sh/
postgres|postgresql|postgres|Relational database management system|https://www.postgresql.org/
sqlite|sqlite|sqlite3|Lightweight file-based database system|https://sqlite.org/
ripgrep|ripgrep|rg|Fast recursive text-searching program|https://github.com/BurntSushi/ripgrep
jq|jq|jq|Searches and transforms JSON data|https://jqlang.org/
PACKAGES


