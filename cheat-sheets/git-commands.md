# Git Commands Cheat Sheet

A practical quick reference for everyday Git use, collaboration, troubleshooting, and safe recovery.

**Git** manages version history locally. **GitHub** hosts repositories and adds collaboration features such as pull requests and issues. Commands beginning with `git` belong to Git; commands such as `gh pr create` belong to the separate GitHub CLI.

Git has additional specialist and plumbing commands, so this sheet focuses on the commands most useful in real projects. To list commands available in your own installation, run `git help -a`.

## 1. The basic Git workflow

```bash
git status
git diff
git add <file>
git diff --staged
git commit -m "Describe the change"
git push
```

The four key stages are:

1. **Working directory** — edit files.
2. **Staging area** — select changes with `git add`.
3. **Local repository** — record a snapshot with `git commit`.
4. **Remote repository** — publish commits with `git push`.

`git add` and `git commit` do not upload code to GitHub. `git push` publishes commits to a remote.

## 2. Help, version, and configuration

| Command | Use |
|---|---|
| `git --version` | Show the installed Git version. |
| `git --help` | Open general help. |
| `git help -a` | List available Git commands. |
| `git help <command>` | Open detailed help for one command, e.g. `git help rebase`. |
| `git <command> -h` | Show concise help where supported. |
| `git config --global user.name "Your Name"` | Set the default commit author name. |
| `git config --global user.email "you@example.com"` | Set the default commit author email. |
| `git config --global --list` | Show global configuration. |
| `git config --list` | Show effective configuration values. |
| `git config --show-origin --list` | Show config values and where they came from. |
| `git config --global init.defaultBranch main` | Set the default branch name for new repositories. |
| `git config --global alias.st status` | Create the shortcut `git st`. |

Use an appropriate commit email. If you use GitHub's privacy email, configure that address when you want to avoid publishing your personal email in commit metadata.

## 3. Create or copy a repository

| Command | Use |
|---|---|
| `git init` | Initialise Git in the current folder. |
| `git init <folder>` | Create a folder and initialise a repository there. |
| `git clone <url>` | Download a repository and its available history. |
| `git clone <url> <folder>` | Clone into a chosen local folder. |
| `git clone --branch <branch> <url>` | Clone and check out the specified branch. |
| `git clone --depth 1 <url>` | Create a shallow clone with limited history. |

**Use `git init`** for a local folder that is not yet a Git repository. **Use `git clone`** when a repository already exists.

## 4. Check and inspect changes

| Command | Use |
|---|---|
| `git status` | Show branch, staged changes, unstaged changes, and untracked files. |
| `git diff` | Show unstaged changes compared with the index. |
| `git diff --staged` | Show what is staged for the next commit. |
| `git diff --cached` | Alias for the same staged diff. |
| `git diff HEAD` | Compare working-tree content with the current commit. |
| `git diff --stat` | Summarise changed files and change size. |
| `git diff --name-only` | List paths shown in a diff. |
| `git diff --check` | Check for common whitespace errors. |
| `git show` | Inspect the current commit by default. |
| `git show <commit>` | Inspect a specific commit and its changes. |
| `git ls-files` | List tracked paths. |
| `git grep "text"` | Search tracked project content for text. |

**Before committing, check both:**

```bash
git status
git diff --staged
```

## 5. Stage, unstage, and manage files

| Command | Use |
|---|---|
| `git add <file>` | Stage one file's current changes. |
| `git add file1 file2` | Stage specific files. |
| `git add .` | Stage changes beneath the current directory. |
| `git add -A` | Stage additions, modifications, and deletions across the working tree. |
| `git add -u` | Stage changes and deletions to tracked files, not new untracked files. |
| `git add -p` | Interactively select parts of changes to stage. |
| `git restore --staged <file>` | Unstage a file but keep its working-copy edits. |
| `git rm <file>` | Remove a tracked file and stage the deletion. |
| `git rm --cached <file>` | Stop tracking a file but keep the local copy. |
| `git mv <old> <new>` | Move or rename a file and stage the change. |

Prefer adding specific files when you can. Review the staged diff so you don't accidentally include secrets, build output, or unrelated edits.

## 6. Commit and inspect history

| Command | Use |
|---|---|
| `git commit -m "message"` | Create a commit from staged changes. |
| `git commit` | Create a commit using the configured editor for the message. |
| `git commit -a -m "message"` | Commit changes/deletions to tracked files; it does not include new untracked files. |
| `git commit --amend` | Replace the latest commit, incorporating staged changes if present. |
| `git commit --amend -m "message"` | Replace the latest commit and set its message. |
| `git log` | Show commit history. |
| `git log --oneline` | Show compact one-line history. |
| `git log --graph --oneline --all` | Draw an ASCII history graph including branches. |
| `git log -n 5` | Show the five most recent commits. |
| `git log -- <file>` | Show commits affecting a path. |
| `git log -p -- <file>` | Show file history with patches. |
| `git log --since="2 weeks ago"` | Filter commits by date. |
| `git blame <file>` | Show line-by-line commit/author history for a file. |
| `git reflog` | Show recent local updates to refs such as HEAD; can help recover from some mistakes. |
| `git shortlog -sn` | Summarise commit counts by author. |

Commit messages should describe the change, e.g. `Add API key security guide` or `Fix attendance calculation`.

**Caution with `git commit --amend`:** it changes the latest commit and its ID. Avoid amending commits other people already rely on unless the team has coordinated.

## 7. Branches

| Command | Use |
|---|---|
| `git branch` | List local branches. |
| `git branch -a` | List local and remote-tracking branches. |
| `git branch -r` | List remote-tracking branches. |
| `git branch <name>` | Create a branch without switching to it. |
| `git switch <branch>` | Switch to an existing branch. |
| `git switch -c <name>` | Create and switch to a new branch. |
| `git switch -` | Switch back to the previously checked-out branch when possible. |
| `git branch -m <new-name>` | Rename the current branch. |
| `git branch -d <name>` | Delete a local branch Git considers safely merged. |
| `git branch -D <name>` | Force-delete a local branch, even if unmerged. |
| `git checkout <branch>` | Older multi-purpose command; can switch branches. |
| `git checkout -b <name>` | Create and switch to a new branch using checkout. |

Example feature workflow:

```bash
git switch main
git pull
git switch -c add-login
# Make changes, test, stage, and commit
git add .
git diff --staged
git commit -m "Add login flow"
git push -u origin add-login
```

## 8. Remotes, fetch, pull, and push

| Command | Use |
|---|---|
| `git remote` | List configured remotes. |
| `git remote -v` | Show remote names and URLs for fetch/push. |
| `git remote add origin <url>` | Add a remote named `origin`. |
| `git remote get-url origin` | Show the remote URL. |
| `git remote set-url origin <url>` | Change a remote URL. |
| `git remote rename <old> <new>` | Rename a remote. |
| `git remote remove <name>` | Remove a remote from local configuration. |
| `git fetch origin` | Download refs and objects from `origin` without integrating them into the current branch. |
| `git fetch --all` | Fetch from configured remotes. |
| `git pull` | Fetch then integrate remote updates, commonly via merge or rebase depending on options/config. |
| `git pull --rebase` | Fetch then rebase local commits onto the updated upstream. |
| `git push` | Publish commits to a remote branch. |
| `git push -u origin <branch>` | Push the branch and set its upstream. |
| `git push origin <branch>` | Push a named branch. |
| `git push --tags` | Push local tags. |
| `git push --delete origin <branch>` | Request deletion of a remote branch. |

**Fetch vs pull vs push**

- `fetch` downloads remote updates but doesn't integrate them into the current branch.
- `pull` fetches and then integrates remote changes.
- `push` sends your local commits to the remote.

When connecting a local repository to an existing GitHub repository:

```bash
git remote add origin https://github.com/USERNAME/REPOSITORY.git
git remote -v
git push -u origin main
```

Replace the URL and branch with your actual repository details.

## 9. Merge and resolve conflicts

| Command | Use |
|---|---|
| `git merge <branch>` | Integrate the named branch into the current branch. |
| `git merge --no-ff <branch>` | Create a merge commit instead of fast-forwarding, when possible. |
| `git merge --abort` | Try to abort an in-progress merge. |
| `git mergetool` | Launch a configured merge-conflict tool. |

Example:

```bash
git switch main
git merge add-login
```

A conflict means Git could not automatically combine some changes. Edit each conflicted file, remove conflict markers, confirm the intended final content, then stage resolved files. Complete the merge as directed by `git status`.

```bash
git status
git add <resolved-file>
git commit
```

If appropriate, cancel the in-progress merge with `git merge --abort`.

## 10. Rebase and cherry-pick

| Command | Use |
|---|---|
| `git rebase <branch>` | Replay current-branch commits onto the named base. |
| `git rebase --continue` | Continue after resolving a rebase conflict. |
| `git rebase --abort` | Abort the current rebase. |
| `git rebase --skip` | Skip the commit currently being replayed. |
| `git rebase -i HEAD~3` | Interactively edit the recent commit sequence. |
| `git cherry-pick <commit>` | Apply one commit's changes to the current branch as a new commit. |
| `git cherry-pick --continue` | Continue cherry-picking after resolving conflicts. |
| `git cherry-pick --abort` | Abort an in-progress cherry-pick. |

Interactive rebase actions can include `pick`, `reword`, `edit`, `squash`, `fixup`, and `drop`.

**Caution:** Rebase rewrites commit identities. Avoid rewriting shared history without coordinating with collaborators. Cherry-pick only a commit when its required dependent changes are available on the target branch.

## 11. Undo mistakes and restore work

| Command | Use |
|---|---|
| `git restore <file>` | Discard unstaged changes to a tracked file by restoring from the index. |
| `git restore --staged <file>` | Unstage a file while preserving working-copy edits. |
| `git restore --source=HEAD <file>` | Restore a file from the current commit. |
| `git reset` | Unstage staged changes by default; preserves working-copy content. |
| `git reset --soft HEAD~1` | Move the branch back one commit while keeping changes staged. |
| `git reset --mixed HEAD~1` | Move back one commit and unstage changes, keeping file content in the working tree. |
| `git reset --hard HEAD~1` | Move back one commit and reset index/worktree; uncommitted work can be lost. |
| `git revert <commit>` | Create a new commit that reverses a chosen commit. |
| `git revert HEAD` | Create a commit reversing the current commit. |
| `git revert --continue` | Continue a revert after resolving conflicts. |
| `git revert --abort` | Abort an in-progress revert. |

**Reset vs revert**

- `reset` moves a branch and can change the index and working tree; often used for local history adjustments.
- `revert` adds a new commit that reverses an earlier commit; often appropriate for changes already shared with others.

### Reset modes

- `--soft` — keep changes staged.
- `--mixed` — unstage changes but keep them in the working tree.
- `--hard` — reset tracked working-tree content too; this can destroy uncommitted changes.

Before any destructive operation, run `git status` and protect anything important.

## 12. Stash unfinished changes

| Command | Use |
|---|---|
| `git stash` | Save eligible changes temporarily. |
| `git stash push -m "message"` | Save changes with a description. |
| `git stash -u` | Include untracked files. |
| `git stash -a` | Include ignored files as well; use carefully. |
| `git stash list` | List saved stashes. |
| `git stash show -p` | Show a stash's changes. |
| `git stash apply` | Apply a stash and keep it listed. |
| `git stash pop` | Apply a stash and usually remove it if successful. |
| `git stash drop` | Remove a stash entry. |
| `git stash clear` | Remove all stash entries. |

Example:

```bash
git stash push -m "unfinished feature"
git switch main
# Do the urgent work
git switch feature-branch
git stash pop
```

A stash is temporary storage, not a permanent backup.

## 13. Tags and releases

| Command | Use |
|---|---|
| `git tag` | List tags. |
| `git tag v1.0.0` | Create a lightweight tag at the current commit. |
| `git tag -a v1.0.0 -m "First release"` | Create an annotated tag with a message. |
| `git show v1.0.0` | Inspect a tag. |
| `git tag -d v1.0.0` | Delete a local tag. |
| `git push origin v1.0.0` | Push a specific tag. |
| `git push origin --tags` | Push local tags. |

Tags are useful for identifying releases or important checkpoints.

## 14. Ignore files and clean up

| Command | Use |
|---|---|
| `git check-ignore -v <file>` | Show the ignore rule matching a path, if applicable. |
| `git ls-files --others --exclude-standard` | List untracked files not excluded by standard ignore rules. |
| `git clean -n` | Preview untracked files and directories that a clean would remove. |
| `git clean -fd` | Delete untracked files/directories. |
| `git clean -fdX` | Delete ignored, untracked files/directories. |
| `git clean -fdx` | Delete all untracked files/directories, including ignored files. |

Example `.gitignore` rules for a Python project:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
.env
.env.*
!.env.example
dist/
build/
```

The exact rules should match the project. `.gitignore` does not automatically untrack files already committed.

**Security:** Never commit private keys, API keys, passwords, or real credentials in `.env`. If a secret was committed, revoke or rotate it; removing it from the latest file does not invalidate it.

## 15. Troubleshooting and history investigation

| Command | Use |
|---|---|
| `git blame <file>` | Trace line-by-line history. |
| `git bisect start` | Begin a search for the commit that introduced a bug. |
| `git bisect bad` | Mark current version as bad during bisect. |
| `git bisect good <commit>` | Mark a known-good commit. |
| `git bisect reset` | End the bisect session and return to the previous checkout state. |
| `git log -S "text" -- <file>` | Search history for changes in the occurrence count of a string. |
| `git log -G "regex" -- <file>` | Search history for patches matching a regex. |
| `git reflog` | Inspect recent local reference movements. |
| `git fsck` | Check repository object validity/connectivity. |
| `git grep "text"` | Search tracked content. |

Reflog can help find a recent commit after some accidental resets or branch movements, but it is not a permanent backup and entries can expire.

## 16. Worktrees and submodules

| Command | Use |
|---|---|
| `git worktree list` | List working trees associated with a repository. |
| `git worktree add <path> <branch>` | Create a linked working tree for a branch. |
| `git worktree remove <path>` | Remove a linked worktree, subject to its state. |
| `git submodule add <url>` | Add another Git repository as a submodule. |
| `git submodule update --init --recursive` | Initialise and update submodules, including nested submodules. |

Worktrees can let you work on multiple branches in separate directories. Submodules are for including another repository as a separately versioned dependency; they require additional care when cloning and updating.

## 17. Git internals and maintenance

These are useful for advanced diagnostics, scripting, and repository maintenance, but most learners won't need them every day.

| Command | Use |
|---|---|
| `git rev-parse HEAD` | Print the commit ID referenced by HEAD. |
| `git show-ref` | Display references. |
| `git ls-tree HEAD` | List contents of a commit's tree. |
| `git cat-file -t <object>` | Display an object's type. |
| `git cat-file -p <object>` | Print object content where possible. |
| `git hash-object <file>` | Compute an object ID for file content. |
| `git update-ref <ref> <object-id>` | Update a reference. Use carefully. |
| `git gc` | Perform repository housekeeping. |
| `git count-objects -vH` | Report object-storage information. |
| `git archive --format=zip -o project.zip HEAD` | Create a ZIP archive of the current commit's files. |
| `git bundle create project.bundle --all` | Bundle repository refs/history for transfer. |

For a complete list and exact options, use `git help -a` and the official [Git command reference](https://git-scm.com/docs).

## 18. Commands to treat with care

| Command | Why caution is needed |
|---|---|
| `git reset --hard` | Can discard uncommitted changes to tracked files. |
| `git clean -fdx` | Deletes all untracked files/directories, including ignored files. Preview with `git clean -ndx` first. |
| `git branch -D <branch>` | Force-deletes a local branch, even if work is unmerged. |
| `git push --force` | Can overwrite remote branch history. If force-pushing is truly needed, consider `--force-with-lease` and coordinate first. |
| Rebase on shared commits | Rewrites commit identities and can disrupt collaborators. |
| `git prune` | Removes eligible unreachable objects; direct use requires care. |

## 19. A safe everyday workflow

```bash
# 1. Check the repository and current branch
git status
git branch
git remote -v

# 2. Get remote updates
git fetch origin

# 3. Create a feature branch
git switch -c add-feature

# 4. Edit and inspect your files
git status
git diff

# 5. Stage only intended files
git add README.md src/main.py

# 6. Review the exact staged change
git diff --staged

# 7. Commit locally
git commit -m "Add feature"

# 8. Publish branch to remote
git push -u origin add-feature
```

For shared projects, open a pull request on GitHub and follow the team's review and merge process.

## 20. The 12 commands to learn first

1. `git status` — understand the current state.
2. `git add` — stage changes.
3. `git diff` — inspect changes.
4. `git commit` — record a snapshot.
5. `git log` — inspect history.
6. `git clone` — copy a remote repository.
7. `git switch` — move between branches.
8. `git fetch` — download remote updates.
9. `git pull` — integrate remote changes.
10. `git push` — publish commits.
11. `git restore` — restore or unstage file changes.
12. `git revert` — safely reverse a commit by creating another commit.

**Mental model:** Git tracks the evolution of your files. Stage the changes you intend to save, inspect them, commit a logical snapshot, and push when you want to share it.

## Further reading

- [Official Git documentation](https://git-scm.com/docs)
- [Pro Git book](https://git-scm.com/book/en/v2)
- [GitHub: Getting started with Git](https://docs.github.com/en/get-started/learning-to-code/getting-started-with-git)
