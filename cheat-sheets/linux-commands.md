# Linux Commands Cheat Sheet — Beginner to Advanced

A practical reference for navigating Linux, managing files, searching text, controlling processes, working with networks, installing software, reading logs, and writing shell scripts.

**A command's exact options depend on the program, Linux distribution, and shell.** This guide focuses on commands commonly used in development. To learn every command available in your environment, use `help`, `man`, `info`, and the command's own help output.

## 1. How Linux commands work

A common command structure is:

```bash
command [options] [arguments]
```

Example:

```bash
ls -lh /home
```

- `ls` is the command.
- `-lh` requests a long listing with human-readable file sizes.
- `/home` is the path to inspect.

A shell, such as Bash or Zsh, interprets what you type and runs built-in commands or programs. Commands may receive input, print output, return an exit status, or write errors to standard error.

### Get help

| Command | Use |
|---|---|
| `command --help` | Show brief usage information, if supported. |
| `man command` | Read the command's manual page. |
| `info command` | Read Info documentation, where available. |
| `help` | List or explain shell built-ins in Bash. |
| `help cd` | Get Bash help for a built-in command. |
| `type command` | Find out whether a command is an alias, function, built-in, or external program. |
| `command -v python` | Check how the shell resolves a command name. |

Example:

```bash
man ls
ls --help
type cd
command -v python3
```

Not every command supports the same help syntax. For a shell built-in such as `cd`, use the shell's help facility.

## 2. Navigate directories

| Command | Use |
|---|---|
| `pwd` | Print the current working directory. |
| `ls` | List directory contents. |
| `ls -l` | Show details such as permissions, owner, size, and modification time. |
| `ls -a` | Include hidden entries. |
| `ls -lah` | Detailed listing, hidden entries, human-readable sizes. |
| `ls -lt` | Sort by modification time, newest first. |
| `ls -R` | Recursively list directories. |
| `cd path` | Change to a directory. |
| `cd ..` | Go up one directory. |
| `cd ../..` | Go up two directories. |
| `cd ~` | Go to your home directory. |
| `cd` | Usually return to your home directory. |
| `cd -` | Return to the previous working directory. |
| `cd /` | Go to the filesystem root. |
| `tree` | Display nested folders as a tree, if installed. |
| `tree -L 2` | Limit tree display to two levels. |
| `tree -d` | Display directories only. |

### Absolute and relative paths

An **absolute path** starts at the filesystem root, such as:

```text
/home/ganesh/projects/main.py
```

A **relative path** is interpreted from the current directory, such as:

```text
projects/main.py
```

If the current directory is `/home/ganesh`, then `projects/main.py` refers to `/home/ganesh/projects/main.py`.

**Good habit:** Before moving or deleting files, run `pwd` and inspect the target with `ls`.

## 3. Create, copy, move, and remove files

### Create directories and files

| Command | Use |
|---|---|
| `mkdir projects` | Create a directory. |
| `mkdir -p a/b/c` | Create parent directories as needed. |
| `touch file.txt` | Create an empty file if it does not exist; otherwise update timestamps. |
| `touch a.txt b.txt` | Create or update timestamps on multiple files. |

Example project structure:

```bash
mkdir -p my-project/src my-project/tests my-project/docs
touch my-project/README.md
```

### Copy files

| Command | Use |
|---|---|
| `cp source destination` | Copy a file. |
| `cp file.txt backup/` | Copy a file into a directory. |
| `cp -r folder backup-folder` | Copy a directory recursively. |
| `cp -i source destination` | Prompt before overwriting where applicable. |
| `cp -v source destination` | Print details about the copy. |
| `cp -n source destination` | Avoid overwriting existing destination files where supported. |

### Move and rename files

```bash
mv old-name.py new-name.py
mv main.py src/
mv -i report.txt reports/
```

`mv` can rename a file or move it into another directory. The `-i` option requests confirmation before overwriting an existing destination.

### Remove files and directories

| Command | Use |
|---|---|
| `rm file.txt` | Remove a file. |
| `rm -i file.txt` | Ask before removing. |
| `rmdir empty-folder` | Remove an empty directory. |
| `rm -r folder` | Remove a directory tree recursively. |
| `rm -f file.txt` | Force removal without ordinary prompts for certain conditions. |

**Danger:** Linux's `rm` generally does not move items to a graphical trash bin. Deleted files may be difficult or impossible to recover. Verify the path first.

```bash
pwd
ls -la old-folder
rm -ri old-folder
```

The example uses interactive recursive removal. Avoid running destructive commands copied from the internet unless you understand exactly what they target. In particular, `rm -rf` can erase directory trees without ordinary confirmation.

## 4. Read and edit file content

| Command | Use |
|---|---|
| `cat file.txt` | Print a file's contents. |
| `cat a.txt b.txt` | Print multiple files consecutively. |
| `less file.txt` | Read a long file interactively. |
| `head file.txt` | Show the first ten lines by default. |
| `head -n 20 file.txt` | Show the first twenty lines. |
| `tail file.txt` | Show the last ten lines by default. |
| `tail -n 50 app.log` | Show the last fifty lines. |
| `tail -f app.log` | Follow new log entries as they appear. |
| `nano file.txt` | Edit a file in Nano, if installed. |
| `vim file.txt` | Edit a file in Vim, if installed. |

### Useful controls for `less`

- `Space`: next screen.
- `b`: previous screen.
- `/error`: search forward for the word or pattern.
- `n`: next match.
- `q`: quit.

### Editing with Nano

Open a file:

```bash
nano main.py
```

Common Nano controls include `Ctrl+O` to save, `Enter` to confirm, and `Ctrl+X` to exit.

### Editing with Vim

Vim uses modes. Press `i` to start inserting text, `Esc` to return to normal mode, and type `:wq` to save and quit. Use `:q!` to exit without saving the current edits.

### Create a file from the terminal

```bash
cat > notes.txt
```

Type the contents and press `Ctrl+D` to finish. **Caution:** `>` replaces existing file contents, so make sure you are not overwriting something important.

## 5. Search for files and text

### Find files using `find`

| Command | Use |
|---|---|
| `find . -name "main.py"` | Find paths named main.py under the current directory. |
| `find . -name "*.py"` | Find Python files. |
| `find . -type d -name "tests"` | Find directories named tests. |
| `find . -type f -size +100M` | Find files larger than 100 MB. |
| `find . -type f -mtime -1` | Find files modified within roughly the last day. |
| `find . -iname "readme*"` | Find case-insensitive matches for a name pattern. |

Check the result of a `find` query before adding a deletion or modification action.

### Search file contents with `grep`

| Command | Use |
|---|---|
| `grep "error" app.log` | Find lines containing error. |
| `grep -i "error" app.log` | Search without case sensitivity. |
| `grep -n "def main" main.py` | Include matching line numbers. |
| `grep -Rni "TODO" src/` | Search recursively, case-insensitively, with line numbers. |
| `grep -w "error" app.log` | Match a whole word. |
| `grep -l "API_KEY" file1 file2` | List files containing a match. |

Example: count error lines in a log:

```bash
grep -i "error" app.log | wc -l
```

### Other search tools

| Command | Use |
|---|---|
| `locate main.py` | Search a filename index, if the utility and database are available. |
| `which python` | Show an executable path when `which` is available and can find it. |
| `type cd` | Identify how the current shell resolves a command. |
| `command -v python3` | Check whether the shell can resolve a command name. |
| `git grep "TODO"` | Search tracked Git content when in a repository. |

`locate` can be fast but may not know about recently created files until its database is updated. Use `find` when you need to search the current filesystem directly.

## 6. Pipes, redirection, and chaining

These shell features connect commands so that one command's output can become another command's input.

### Pipe: `|`

```bash
ps aux | grep python
grep "ERROR" app.log | wc -l
```

A pipe sends standard output from the command on the left to standard input for the command on the right. Avoid unnecessary pipelines when a command can accept a filename directly.

### Redirect output: `>` and `>>`

```bash
ls > files.txt
echo "New log entry" >> app.log
```

- `>` redirects output to a file and usually replaces its previous contents.
- `>>` appends output to a file.

### Redirect input: `<`

```bash
sort < names.txt
```

The file's contents become standard input to the command.

### Redirect errors: `2>`

```bash
python main.py 2> errors.log
```

File descriptor `2` is standard error. To combine standard output and standard error in Bash:

```bash
python main.py > output.log 2>&1
```

The order matters: this redirects standard output to the file, then sends standard error to the same destination.

### Chain commands

| Operator | Meaning |
|---|---|
| `&&` | Run the next command only if the previous one succeeds. |
| `||` | Run the next command if the previous one fails. |
| `;` | Run the next command after the previous one finishes, regardless of success. |

```bash
mkdir project && cd project
python main.py || echo "The program failed"
pwd; ls
```

### `tee`: display and save output

```bash
python main.py 2>&1 | tee run.log
```

This displays output and writes it to a log file. Add `tee -a` to append instead of replacing the file.

### Text-processing utilities

| Command | Use |
|---|---|
| `sort names.txt` | Sort lines alphabetically. |
| `sort -n scores.txt` | Sort lines numerically. |
| `uniq names.txt` | Collapse adjacent duplicate lines. |
| `sort names.txt | uniq` | Sort lines and remove duplicates. |
| `wc file.txt` | Count lines, words, and bytes. |
| `wc -l file.txt` | Count lines. |
| `cut -d, -f1 data.csv` | Extract the first comma-delimited field from each line. |
| `xargs` | Build command arguments from input; quote and delimit paths carefully. |

For filenames that may contain spaces or unusual characters, use null-delimited workflows such as `find ... -print0` with `xargs -0` where supported.

## 7. Users, groups, and permissions

### Identify users and groups

| Command | Use |
|---|---|
| `whoami` | Print the effective username. |
| `id` | Show user ID, primary group, and supplementary groups. |
| `id username` | Inspect another user account. |
| `groups` | Show the current user's groups. |
| `groups username` | Show a user's group memberships. |
| `who` | Display logged-in users. |
| `w` | Display logged-in users and activity information. |

### `sudo`: elevated privileges

```bash
sudo apt update
```

`sudo` runs an authorised command with elevated privileges. It is not a universal fix for permission errors. Use it only when necessary and only for commands you understand.

### `chmod`: change permissions

For ordinary files, permission symbols mean:
- `r`: read
- `w`: write
- `x`: execute

Permissions are commonly described for the file's owner, group, and others.

| Numeric value | Permission |
|---|---|
| `0` | None |
| `1` | Execute |
| `2` | Write |
| `3` | Write + execute |
| `4` | Read |
| `5` | Read + execute |
| `6` | Read + write |
| `7` | Read + write + execute |

Examples:

```bash
chmod 755 script.sh
chmod 644 README.md
chmod u+x script.sh
chmod g-w shared.txt
```

`755` gives the owner read/write/execute and group/others read/execute. `644` gives the owner read/write and group/others read. Symbolic forms such as `u+x` add execute for the owner; `g-w` removes group write access.

Avoid using `chmod -R 777` as a default fix. It can expose files unnecessarily. Give only the permissions required.

### `chown`: change ownership

```bash
sudo chown username file.txt
sudo chown username:groupname file.txt
sudo chown -R username:groupname project/
```

Recursive ownership changes affect an entire tree. Confirm the target carefully, especially when using administrative privileges.

### `umask`: set default permission restrictions

```bash
umask
umask 027
```

The mask removes permission bits from the defaults used when programs create files or directories. Resulting permissions depend on the creation mode specified by the program.

## 8. Processes and job control

A process is a running program.

| Command | Use |
|---|---|
| `ps` | Display processes. |
| `ps aux` | Show a broad process listing on common Linux implementations. |
| `ps -ef --forest` | Display processes in a tree-like format where supported. |
| `top` | Monitor processes, CPU, and memory live. |
| `htop` | Interactive process monitor, if installed. |
| `pgrep -a python` | Find processes matching a name or pattern. |
| `kill PID` | Send the default termination signal, usually SIGTERM. |
| `kill -9 PID` | Send SIGKILL; use only when necessary. |
| `pkill -TERM -f "pattern"` | Send a termination signal to matching processes; check the pattern carefully. |
| `jobs` | List jobs in the current shell. |
| `fg %1` | Bring shell job 1 to the foreground. |
| `bg %1` | Resume shell job 1 in the background. |
| `nohup command > output.log 2>&1 &` | Run a command in the background while ignoring hangup, with output redirected. |

Example:

```bash
ps aux | grep python
kill 1234
```

Replace `1234` with the actual process ID. Prefer ordinary termination first; `kill -9` prevents the process from handling a graceful shutdown.

Run a program in the background:

```bash
python script.py &
jobs
```

A background command is not automatically a persistent service. For production services, use the relevant service manager or process supervisor.

## 9. System information and resource monitoring

| Command | Use |
|---|---|
| `uname -a` | Show kernel/system information. |
| `cat /etc/os-release` | Show distribution identity and version on systems using this file. |
| `hostname` | Display the hostname. |
| `uptime` | Show uptime and system load averages. |
| `date` | Display system date and time. |
| `lscpu` | Display CPU architecture information. |
| `lsmem` | List memory ranges where available. |
| `lspci` | List PCI devices when installed and accessible. |
| `lsusb` | List USB devices when installed and accessible. |
| `free -h` | Display memory and swap statistics in readable units. |
| `df -h` | Show filesystem space usage. |
| `du -sh project/` | Summarise disk usage for a path. |
| `du -h --max-depth=1 .` | Show sizes of immediate subdirectories where supported. |
| `watch -n 2 free -h` | Repeat memory report every two seconds. |

High memory usage alone doesn't necessarily mean there is a problem: Linux also uses memory for caching. Check available memory, swap activity, and which processes consume resources.

## 10. Networking and remote access

### Inspect network interfaces

| Command | Use |
|---|---|
| `ip addr` | Show network interfaces and addresses. |
| `ip link` | Show link state and interface details. |
| `ip route` | Show routing information. |
| `ss -tuln` | Show listening TCP/UDP sockets using numeric addresses and ports. |
| `sudo ss -tulpn` | Include process information where permitted. |

### Test connectivity

```bash
ping example.com
curl -I https://example.com
curl -v https://example.com
```

- `ping` tests ICMP reachability and response times, if permitted. A failed ping does not necessarily mean the website is unavailable.
- `curl -I` requests headers for a URL using the HTTP method chosen by curl for this mode.
- `curl -v` provides additional connection details.

### Make an API request with curl

```bash
curl -X POST https://api.example.com/items \
  -H "Content-Type: application/json" \
  -d '{"name":"example"}'
```

This is an illustrative request; substitute a real URL and a body matching the API contract. Do not paste real access tokens into public logs, shared terminal recordings, or screenshots.

### Download files

```bash
wget https://example.com/file.zip
wget -c https://example.com/file.zip
```

The `-c` option attempts to continue a supported partial download.

### SSH: connect to a remote server

```bash
ssh username@server.example.com
ssh -i ~/.ssh/id_ed25519 username@server.example.com
```

SSH is commonly used to administer cloud servers and securely access remote machines. Protect private SSH keys.

### SCP: copy files through SSH

```bash
scp report.txt username@server.example.com:/home/username/
scp username@server.example.com:/home/username/report.txt .
```

### Rsync: synchronise files and directories

```bash
rsync -av project/ backup/project/
rsync -avn project/ backup/project/
rsync -av project/ username@server.example.com:/home/username/project/
```

The `-n` option in the second example performs a dry run. The trailing slash on `project/` means to synchronise its contents. Be very careful with deletion options; a mistaken source or destination can remove data.

## 11. Package managers and software installation

Package manager commands differ by distribution. Use the manager that belongs to your operating system.

### Debian and Ubuntu: APT

| Command | Use |
|---|---|
| `sudo apt update` | Refresh package metadata. |
| `sudo apt upgrade` | Install available upgrades according to APT's rules. |
| `sudo apt install package-name` | Install a package. |
| `sudo apt remove package-name` | Remove a package. |
| `sudo apt purge package-name` | Remove a package and package-managed configuration files where supported. |
| `apt search keyword` | Search package names and descriptions. |
| `apt show package-name` | Display package details. |

**Remember:** `apt update` refreshes package metadata; it does not itself upgrade installed packages.

### Fedora and related systems: DNF

```bash
sudo dnf check-update
sudo dnf upgrade
sudo dnf install package-name
sudo dnf remove package-name
dnf search keyword
```

### Arch Linux: Pacman

```bash
sudo pacman -Syu
sudo pacman -S package-name
sudo pacman -R package-name
pacman -Ss keyword
```

Never assume commands from one distribution's package manager work on another distribution.

### Python packages: pip and virtual environments

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requests
```

Install dependencies from a project file:

```bash
python -m pip install -r requirements.txt
python -m pip list
```

A virtual environment helps keep project dependencies separate from other Python projects and system packages.

## 12. Archives and compression

### Tar archives

```bash
tar -czf project.tar.gz project/
tar -xzf project.tar.gz
tar -tzf project.tar.gz
```

- `c`: create an archive.
- `x`: extract.
- `t`: list contents.
- `z`: gzip compression.
- `f`: use the archive file named next.

Inspect unfamiliar archives before extracting them. Archive contents may have unexpected paths.

### Gzip

```bash
gzip application.log
gunzip application.log.gz
```

By default, gzip commonly replaces the input with the compressed file. Check the options if you need to preserve the original.

### Zip and unzip

```bash
zip -r project.zip project/
unzip -l project.zip
unzip project.zip
```

The `zip` and `unzip` programs may need to be installed.

## 13. Storage and filesystems

| Command | Use |
|---|---|
| `lsblk` | List block devices and partitions. |
| `blkid` | Display block-device identifiers and filesystem information, where available. |
| `findmnt` | Show mounted filesystems in structured form. |
| `mount` | List mounted filesystems or mount a filesystem. |
| `umount` | Unmount a filesystem. |
| `fdisk -l` | List partition information, subject to permissions and availability. |
| `df -h` | Show filesystem space usage. |
| `du -sh path` | Summarise path disk usage. |

**Do not experiment with partitioning or formatting on your main disk.** Filesystem creation, partition changes, or writes to raw block devices can destroy data. Practice only in a disposable virtual machine or safe test environment.

## 14. Users, services, and logs

Account-management commands can require administrator privileges.

| Command | Use |
|---|---|
| `passwd` | Change a password subject to system policy. |
| `sudo useradd username` | Create a user where this tool is used. |
| `sudo usermod -aG group username` | Add a user to an additional group. |
| `sudo userdel username` | Delete a user account according to the options used. |

### systemd service management

On systems using systemd:

```bash
systemctl status service-name
sudo systemctl start service-name
sudo systemctl stop service-name
sudo systemctl restart service-name
sudo systemctl enable service-name
sudo systemctl enable --now service-name
```

The service name and service manager vary by system. Confirm the correct unit before starting, stopping, or enabling it.

### Read system logs with journalctl

```bash
journalctl -n 100
journalctl -f
journalctl -u service-name
journalctl -u service-name -n 100
```

Use these to inspect recent logs, follow log activity, and investigate service failures on systems using the systemd journal.

## 15. Environment variables and shell history

| Command | Use |
|---|---|
| `env` | Display environment variables. |
| `printenv HOME` | Display one environment variable. |
| `printenv PATH` | Display the executable search path. |
| `export APP_ENV=development` | Set an environment variable for the current shell and its child processes. |
| `APP_ENV=development python main.py` | Set a variable for one command invocation. |
| `history` | Display shell command history, subject to shell configuration. |
| `alias ll='ls -lah'` | Create a shortcut in the current shell session. |

Example:

```bash
export APP_ENV=development
echo "$APP_ENV"
```

Environment variables don't automatically persist across sessions. Persistence depends on the shell and its configuration files.

**Security reminder:** Don't print secret environment variables into shared logs or screenshots. Shell history may also retain commands containing credentials, so avoid placing secrets directly in command arguments.

## 16. Basic Bash scripting

Scripts automate repeatable sequences of shell commands.

Create a file named `hello.sh`:

```bash
#!/usr/bin/env bash

echo "Hello, Linux!"
```

Make it executable and run it:

```bash
chmod +x hello.sh
./hello.sh
```

The first line, called a shebang, identifies the interpreter for direct execution. Alternatively, run `bash hello.sh`.

### Variables

```bash
name="Ganesh"
echo "Hello, $name"
```

In Bash, don't add spaces around the assignment `=`.

### Read input

```bash
read -r -p "Enter your name: " name
echo "Hello, $name"
```

### Conditions

```bash
if [[ -f "main.py" ]]; then
    echo "main.py exists"
else
    echo "main.py does not exist"
fi
```

Here `-f` checks whether the path is a regular file.

### Loops

```bash
for file in *.py; do
    [[ -e "$file" ]] || continue
    echo "Found Python file: $file"
done
```

Quoting variables such as `"$file"` helps keep filenames with spaces together as a single argument.

### Exit statuses

```bash
python main.py
echo $?
```

An exit status of zero conventionally indicates success, while a nonzero status usually signals an error or another condition.

You can use `&&` to run follow-up work only after success:

```bash
python main.py && echo "Program succeeded"
```

For reliable automation, understand command exit status, quoting, error handling, and the difference between standard output and standard error.

## 17. Common developer workflows

### Create a Python project structure

```bash
mkdir -p my-ai-project/src my-ai-project/tests my-ai-project/data
cd my-ai-project
python3 -m venv .venv
source .venv/bin/activate
touch README.md requirements.txt
```

### Inspect a failing program

```bash
pwd
ls -lah
python main.py
echo $?
```

For log files:

```bash
tail -n 100 application.log
grep -ni "error" application.log
```

### Find large files

```bash
df -h
du -h --max-depth=1 . 
find . -type f -size +100M
```

The `--max-depth` option is supported by common GNU versions of `du`, but not every implementation.

### Check whether a port is listening

```bash
ss -tuln
sudo ss -tulpn
```

### Save command output for later troubleshooting

```bash
python main.py > output.log 2>&1
tail -f output.log
```

## 18. Dangerous commands and safety rules

| Command or operation | Why it needs care |
|---|---|
| `rm -rf path` | Recursively deletes a path without ordinary confirmation. Verify the exact target. |
| `sudo` with unknown commands | Elevated privileges can change system-wide files and configuration. |
| `chmod -R 777 path` | Grants excessively broad permissions in many contexts. |
| `chown -R ... path` | Recursively changes ownership and can break system or application access. |
| Partitioning or filesystem formatting tools | Can destroy data if directed at the wrong device. |
| `curl ... | sh` or equivalent downloaded-script execution | Runs remote content without first inspecting it. |
| `>` redirection | Can overwrite the destination file. |
| Deletion with `find` or `xargs` | An incorrect match or quoting error can target unintended files. |

Good habits:
- Check `pwd` before destructive operations.
- Use `ls` to verify paths.
- Preview file matches before using commands that delete or modify them.
- Back up important data.
- Use minimum necessary privileges.
- Read a command's help or manual when uncertain.
- Test scripts against harmless sample files first.

## 19. Quick-reference table

| Task | Command |
|---|---|
| Current directory | `pwd` |
| List hidden files and details | `ls -lah` |
| Enter directory | `cd path/` |
| Create directory tree | `mkdir -p path/to/folder` |
| Create empty file | `touch file.txt` |
| Copy file | `cp source destination` |
| Move or rename | `mv source destination` |
| Delete file with confirmation | `rm -i file.txt` |
| Read long file | `less file.txt` |
| Search text | `grep -n "text" file.txt` |
| Find a file | `find . -name "filename"` |
| Check permissions | `ls -l` |
| Add execute permission for owner | `chmod u+x script.sh` |
| Kernel/system information | `uname -a` |
| Memory usage | `free -h` |
| Disk space | `df -h` |
| Directory size | `du -sh folder/` |
| Processes | `ps aux` |
| Live process monitoring | `top` |
| Network addresses | `ip addr` |
| Test an HTTP endpoint | `curl -I https://example.com` |
| Connect to a server | `ssh user@host` |
| Update Ubuntu package metadata | `sudo apt update` |
| Install an Ubuntu package | `sudo apt install package-name` |
| Read a manual | `man command` |
| Show command help | `command --help` |

## 20. Suggested learning order

1. **Navigation:** `pwd`, `ls`, `cd`, `tree`.
2. **Files and folders:** `mkdir`, `touch`, `cp`, `mv`, `rm`.
3. **Reading and searching:** `cat`, `less`, `head`, `tail`, `grep`, `find`.
4. **Shell fundamentals:** pipes, redirection, `&&`, `||`, exit statuses.
5. **Permissions:** `whoami`, `id`, `chmod`, `chown`, `sudo`.
6. **Processes and resources:** `ps`, `top`, `kill`, `free`, `df`, `du`.
7. **Development and networking:** `curl`, `ssh`, `rsync`, package managers, Python virtual environments.
8. **Automation:** Bash variables, conditions, loops, and scripts.
9. **System administration:** services, logs, storage, and account-management tools in a safe test environment.

Don't attempt to memorise every command. Learn what problem each command solves, practise on a disposable directory, and use the manual when you need an option.

## Further reading

- [GNU Coreutils Manual](https://www.gnu.org/software/coreutils/manual/)
- [GNU Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html)
- [The Linux man-pages project](https://www.kernel.org/doc/man-pages/)
