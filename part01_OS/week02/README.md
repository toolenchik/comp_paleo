# Research software setup
software-report.sh: Checks whether 13 research tools (such as Python, R, git, tmux and jq) are installed and records each tool's version and location. For missing tools, it looks up the version Homebrew would install. Results are written to `software-report.tsv`. Usage: `./software-report.sh`
package_research.txt: brew info output for each package
