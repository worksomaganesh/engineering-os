# GitHub: A Beginner-Friendly Guide with Real-Life Examples

GitHub is an online platform built around Git. It lets you store code and files, keep a history of changes, collaborate with others, review code, track work, automate tests and deployments, and publish projects.

A useful way to remember the difference:

- **Git** is the version-control tool that records a project's history.
- **GitHub** is a platform that hosts Git repositories and adds collaboration and development tools around them.

Git can work locally without GitHub. GitHub uses Git repositories and adds features such as pull requests, issues, code reviews, automation, project tracking, and community collaboration.

Official starting point: [GitHub Docs](https://docs.github.com/en).

## 1. What Problem Does GitHub Solve?

Imagine you are building an AI study assistant. You write code, change prompts, fix bugs, add files, and try new features. If you save every version manually, you may lose track of which change broke something.

Git helps record changes. GitHub gives you a place to keep that history online and work with other people.

GitHub helps answer questions such as:
- What files belong to this project?
- What changed between yesterday and today?
- Who introduced a change, and why?
- Can I try a new feature without breaking the stable version?
- How can a teammate review code before it is merged?
- Which bugs and planned features still need work?
- Can tests run automatically whenever code changes?
- How can another developer understand, use, or contribute to my project?

A repository contains project files and their revision history. Repositories can be public or private, and access can be shared with collaborators. See [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories).

## 2. The Main GitHub Building Blocks

| Feature | Meaning | Real-life example |
|---|---|---|
| Repository (repo) | A project's files and Git history | Your AI study assistant source code |
| README.md | The project introduction and starting instructions | Explain the app, features, setup, screenshots, and limitations |
| Commit | A recorded snapshot of changes with a message | "Add PDF upload validation" |
| Branch | An independent line of development | Build a login screen while main remains stable |
| Push | Send local Git commits to a remote such as GitHub | Upload changes made on your computer |
| Pull request (PR) | Propose changes and review them before merging | Ask a teammate to review a new retrieval pipeline |
| Issue | Track a bug, task, feature request, or question | "PDF upload fails for a large file" |
| Projects | Organize issues, PRs, and planned work in tables, boards, or roadmaps | Track features through To do, In progress, and Done |
| Actions | Automate workflows such as tests and deployment | Test a Python project after each push or PR |
| Releases | Package a version with release notes and downloads | Publish version 1.0 of a command-line tool |
| GitHub Pages | Publish supported static websites from a repository | Host a portfolio or documentation site |
| Codespaces | A configurable cloud development environment | Start working on a repo from a browser |
| Discussions | Community conversations for projects that enable them | Discuss a possible feature that is not yet a bug report |
| Packages | Host supported software packages and container images | Share a versioned library or container image |

Official guides: [repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories), [README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), [issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues), [projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects), and [releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

## 3. A Repository Is More Than a Folder in the Cloud

A small Python project might look like this:

```text
weather-cli/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── src/
│   └── weather_cli.py
├── tests/
│   └── test_weather_cli.py
└── .github/
    └── workflows/
        └── tests.yml
```

Each file has a job:
- **README.md:** explains what the project does and how to use it.
- **LICENSE:** states the terms under which others may use the project. Public visibility does not automatically grant every permission.
- **.gitignore:** tells Git which untracked files it should normally ignore, such as local environments and generated files.
- **requirements.txt:** lists Python dependencies for this example.
- **src/:** contains application code.
- **tests/:** contains automated tests.
- **.github/workflows/:** can contain GitHub Actions workflow files.

Not every repository needs this exact structure. Choose a layout that suits its language and complexity.

### What makes a good README?

A useful README usually explains:
1. What the project does and why it is useful.
2. Which problem it solves and who it is for.
3. Its main features.
4. How to install, configure, and run it.
5. The technologies it uses.
6. How to test it.
7. Known limitations or unfinished work.
8. How someone can contribute, if applicable.

A clear README helps reviewers understand your project before opening the code. See [About README files](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes).

## 4. From an Idea to Merged Code

A common collaboration workflow is:

```text
Idea or bug
    |
    v
Create an Issue
    |
    v
Create a feature branch
    |
    v
Edit files and make commits
    |
    v
Push the branch to GitHub
    |
    v
Open a Pull Request
    |
    v
Review code and run tests
    |
    v
Merge into the main branch
    |
    v
Deploy or publish, when appropriate
```

### Step 1 — Record the task

Create an issue such as "Add PDF type and file-size validation." This preserves the requirement, discussion, and progress.

### Step 2 — Work in a branch

The main branch usually represents the project's primary line of development. A branch lets you work on a change separately, so unfinished code does not have to go straight into main.

Example branch name: `feature/pdf-validation`.

### Step 3 — Make small commits

A commit records a set of changes. Prefer messages that describe the change, such as:
- `Add PDF upload validation`
- `Handle empty search queries`
- `Document local setup steps`

A commit is not the same as a push: a commit records the change in Git history; push sends local commits to a remote repository.

### Step 4 — Push and open a pull request

A pull request (PR) asks to merge proposed changes into another branch. It shows the diff, enables comments and code review, and can display automated test results.

### Step 5 — Review, revise, and merge

A reviewer might request better error handling, point out a bug, or approve the update. The author can push further commits to the same branch. When the change is ready, it can be merged according to the project's workflow.

This process is common in teams, but personal projects do not need heavy ceremony for every tiny change. Read [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow) and the [pull request review guide](https://docs.github.com/en/pull-requests/getting-started/quickstart-for-reviewing-pull-requests).

## 5. Basic Git Commands Used with GitHub

After installing Git, a typical local workflow looks like this:

```bash
# Download a remote repository to your computer
git clone https://github.com/OWNER/REPOSITORY.git

# Enter the project directory
cd REPOSITORY

# Check which files have changed
git status

# Create a new branch and switch to it
git switch -c feature/my-change

# Stage the files for the next commit
git add README.md

# Record the staged change
git commit -m "Improve project documentation"

# Send the branch and commits to GitHub
git push -u origin feature/my-change
```

Replace the example URL and paths with your own repository details. After pushing, open the repository on GitHub and create a pull request if you want the change reviewed or merged through a PR workflow.

When working alone, you can also commit and push directly to your own main branch. Use branches when you want safer experimentation or when the project expects pull requests.

For a fuller reference, see this repository's [Git commands cheat sheet](../../cheat-sheets/git-commands.md).

## 6. Real-Life Use Case: Build a Portfolio Project

Suppose you create an AI study assistant, a personal finance tracker, or an attendance dashboard.

Use GitHub to:
1. Keep the source code, documentation, tests, and history together.
2. Write a README explaining the problem, solution, and setup.
3. Track unfinished features as issues.
4. Use commits to preserve meaningful progress.
5. Add screenshots, a demo, and an architecture diagram to the README.
6. Publish a static project page with GitHub Pages if the project suits static hosting.
7. Link the repository from your resume or profile.

A reviewer should be able to understand what you built and how to run it, rather than seeing only a repository name. Never publish private user data, credentials, private datasets, or proprietary code just to make a portfolio visible.

Useful guides: [GitHub Pages](https://docs.github.com/en/pages) and [repository best practices](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories).

## 7. Real-Life Use Case: Collaborate on a Hackathon

Imagine a four-person team building an AI-powered campus assistant:
- One person builds the frontend.
- One builds the backend API.
- One handles retrieval or model integration.
- One writes tests, documentation, and deployment configuration.

The team can:
1. Keep the shared code in one repository.
2. Create issues for tasks and assign owners.
3. Use branches so changes can be developed independently.
4. Open PRs so teammates can inspect changes before merging.
5. Use labels such as `frontend`, `backend`, `bug`, or `documentation`.
6. Use GitHub Projects as a board for To do, In progress, and Done.
7. Keep setup instructions and demo links in the README.

This works even when teammates are in different colleges or cities. Agree on interfaces, branch naming, local setup, and how to handle secrets early. Collaboration tools cannot automatically solve coordination problems.

## 8. Real-Life Use Case: Contribute to Open Source

Open-source projects accept contributions under their chosen license and project rules. A common workflow is:

1. Read the project's README, license, and contribution instructions.
2. Find an issue that matches your skill level.
3. Ask clarifying questions before starting a large change.
4. Fork the repository if you do not have write access, then clone your fork.
5. Create a branch, make a focused change, and add or update tests when appropriate.
6. Push the branch and open a PR against the original project.
7. Respond respectfully to review feedback and update the change.
8. Follow the maintainer's testing and formatting instructions.

A contribution does not have to be a huge feature. Reproducing a bug, improving a confusing explanation, adding a test, or fixing a small documented problem can be valuable. Avoid low-quality PRs made only to increase contribution-graph activity; try to solve a real project need.

See the [GitHub Flow guide](https://docs.github.com/en/get-started/using-github/github-flow) and [Issues documentation](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues).

## 9. Real-Life Use Case: Automatically Test Code with GitHub Actions

Without automation, you might forget to run tests before pushing a change. GitHub Actions can run a workflow when an event such as a push or pull request occurs.

For a Python repository, create `.github/workflows/tests.yml`:

```yaml
name: Python tests

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
          pip install pytest

      - name: Run tests
        run: pytest
```

This example checks out the code, sets up Python, installs dependencies, and runs pytest. It assumes the repository contains compatible tests and dependencies. Review action versions and the Python version for the project.

If tests fail, the workflow logs help diagnose the issue. Teams can also require certain checks before merging, where suitable. Actions can automate tests, builds, releases, and deployments. Hosted runner quotas and charges depend on repository type, plan, and current terms; see [GitHub Actions documentation](https://docs.github.com/en/actions).

## 10. Real-Life Use Case: Publish a Portfolio with GitHub Pages

For a static site, such as HTML, CSS, JavaScript, or static-site-generator output, GitHub Pages can publish content from a repository.

Example structure:

```text
portfolio/
├── index.html
├── styles.css
├── script.js
└── assets/
    └── profile.png
```

A basic workflow:
1. Create a repository for the site.
2. Add the website files and a README.
3. Open repository Settings and find Pages.
4. Choose a supported publishing source, such as a branch and folder, or configure a GitHub Actions workflow.
5. Open the published URL shown by GitHub after deployment.

GitHub Pages is for static site hosting. It does not directly run a persistent Python or Node.js backend. If the site needs server-side logic, host a backend separately and connect the frontend to it.

Availability depends on repository visibility and GitHub plan. Check [GitHub Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages).

## 11. Real-Life Use Case: Track Bugs and Product Ideas

Issues can track more than software bugs:
- Feature: "Add dark mode."
- Defect: "Search fails for an empty input."
- Research task: "Compare two embedding approaches."
- Documentation task: "Add local setup instructions."
- Release task: "Verify tests and deployment before launch."

GitHub Projects can group issues and pull requests into a table, board, or roadmap. For an individual, a simple To do / In progress / Done board may be enough. Teams can use labels, assignees, priorities, and milestones to coordinate work.

Official references: [About Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues) and [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects).

## 12. Releases: Mark Useful Versions

A commit is a change in project history. A **release** packages and announces a version of the project, often with release notes and downloadable files. Releases are based on Git tags.

Example version labels:
- `v0.1.0`: first experimental version.
- `v1.0.0`: first stable release.
- `v1.1.0`: a later release that adds a feature or fixes problems.

These are examples, not a mandatory versioning scheme. For a command-line tool, a release page might explain new features, known limitations, installation, and download assets. See [About releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

## 13. Codespaces: Start Coding in a Browser

GitHub Codespaces provides a cloud-hosted development environment configured for a repository. It can help when you do not want to install every dependency locally, when a team needs a consistent setup, or when you want to explore a project from a supported device.

A repository can use development-container configuration to describe tools and setup. Codespaces is a development environment, not the same thing as deploying an app. Availability, usage quotas, and billing depend on the current plan and account settings.

See [GitHub Codespaces documentation](https://docs.github.com/en/codespaces).

## 14. GitHub as a Learning and Career Tool

Your GitHub profile can make engineering work visible, but it is not a score that automatically measures skill. Build a portfolio that provides evidence of what you can build and explain.

- **Pinned repositories:** highlight projects that best represent your current skills.
- **Useful READMEs:** show what each project does, how to run it, and its trade-offs.
- **Real progress:** preserve meaningful commits, issues, PRs, tests, and documentation.
- **Reproducible work:** include setup instructions, dependency files, sample configuration, and safe sample data.
- **Collaboration:** contribute to team or open-source projects when appropriate.
- **Professional hygiene:** avoid leaked secrets, copied projects you cannot explain, misleading claims, and empty repos made only for appearance.

For an AIML student, repositories might include a Python learning log, data analysis project, small API, model experiment with documented evaluation, or AI app with thoughtful security and setup instructions. A small project you understand deeply is more useful than a complex project you cannot explain during an interview.

Use GitHub as a record of engineering work—not to chase green squares or star counts alone.

## 15. Public vs Private Repositories

A **public repository** can be viewed by anyone. A **private repository** limits access to authorized people.

Use public repositories for work you are comfortable sharing under applicable license and data constraints. Use private repositories for work you are not ready to publish, but remember that private does not mean secrets should be committed.

Before making a repository public, check for:
- API keys, passwords, access tokens, and private certificates.
- Personal, customer, or confidential data.
- Files or dependencies you do not have permission to redistribute.
- Local datasets, environment files, and accidental build artifacts.
- License, attribution, and data-use requirements.

A `.gitignore` file helps prevent selected untracked files from being added accidentally; it does not remove secrets already committed. If a credential is exposed, revoke or rotate it immediately. Removing it in a later commit may not erase it from history or from existing clones.

## 16. Security Features Worth Knowing

GitHub offers security features that can help identify leaked credentials, vulnerable dependencies, and code issues. Depending on repository type and plan, these may include:
- **Dependabot alerts and updates:** identify certain vulnerable dependencies and help update them.
- **Secret scanning:** detects supported secret patterns in repository content and history.
- **Push protection:** can block pushes containing supported secrets when available and enabled.
- **Code scanning:** analyzes code for certain vulnerabilities and coding errors.

Feature availability and configuration vary by plan, organization settings, and whether a repository is public or private. Do not assume every feature is enabled automatically.

Read the [repository security quickstart](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository) and [security and analysis settings](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-security-and-analysis-settings-for-your-repository).

## 17. Common Beginner Confusions

**"Git and GitHub are the same."**  
No. Git is version-control software; GitHub is a service built around Git plus collaboration and development tools.

**"Commit and push mean the same thing."**  
No. Commit records a change in local Git history. Push sends commits to a remote repository.

**"A branch is a separate repository."**  
No. A branch is a line of development inside a repository. A fork is a separate repository created from another repository.

**"A pull request downloads changes."**  
No. A pull request proposes changes for review and merging. Pulling with Git fetches and integrates remote changes into your local branch, which is related but different.

**"Public on GitHub means open source."**  
Not automatically. Repository visibility and software licensing are different things. A license states what others are permitted to do with the code.

**"The most popular GitHub project is the best one to study."**  
Popularity can help discovery, but fit, documentation, activity, maintainers' guidelines, issue quality, and your learning goal matter too.

**"More commits means more skill."**  
Commit count is only a rough activity signal. Thoughtful work, reliability, tests, clear explanations, and the ability to discuss design decisions matter more.

## 18. A Practical Beginner Learning Path

### Stage 1 — Repository basics
- Create a test repository.
- Write a clear README.
- Learn public vs private visibility and Git history.
- Add a suitable `.gitignore`.

### Stage 2 — Git workflow
- Practice clone, status, branch, add, commit, and push.
- Create a feature branch.
- Open and merge a pull request.
- Learn to resolve a simple merge conflict.

### Stage 3 — Project management
- Open issues for a few tasks.
- Use labels and a simple Projects board.
- Keep a small backlog and close issues when the work is done.

### Stage 4 — Quality and automation
- Add basic tests.
- Set up a small GitHub Actions workflow.
- Inspect workflow logs and fix a failing test.
- Learn how to protect secrets and review dependency alerts.

### Stage 5 — Publish and collaborate
- Publish a suitable static page with GitHub Pages.
- Create a release for a small versioned project.
- Read another project's contribution guide and make a useful, focused contribution when ready.

Learn features in the order that supports your current project. Do not enable every tool just to check boxes: understand why a feature is useful and when it is worth the complexity.

## 19. Official Documentation and Next Steps

- [GitHub Docs — Getting started](https://docs.github.com/en/get-started)
- [About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
- [GitHub Flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [Pull request reviews](https://docs.github.com/en/pull-requests/getting-started/quickstart-for-reviewing-pull-requests)
- [Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues)
- [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects)
- [GitHub Actions](https://docs.github.com/en/actions)
- [GitHub Pages](https://docs.github.com/en/pages)
- [Codespaces](https://docs.github.com/en/codespaces)
- [Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- [Repository security quickstart](https://docs.github.com/en/code-security/getting-started/quickstart-for-securing-your-repository)

## 20. Quick Self-Test

1. What is the difference between Git and GitHub?
2. What is a repository, and what should a README explain?
3. How is a commit different from a push?
4. Why create a branch before developing a feature?
5. What is a pull request, and why do teams review one?
6. When would you use an Issue versus a Project board?
7. What can GitHub Actions automate?
8. What is GitHub Pages suitable for, and what type of backend can it not directly run?
9. Why is removing a secret in a later commit not enough if it was already exposed?
10. What makes a repository useful as evidence of your engineering skill?

### Answer key

1. Git records source history and branches; GitHub hosts Git repositories and adds collaboration and development features.
2. A repository contains files and history. A README explains the project's purpose, setup, usage, and limitations.
3. A commit records changes in Git history; push sends local commits to a remote.
4. A branch isolates a change so unfinished work does not need to modify the main line of development.
5. A pull request proposes changes for review and merging; reviews help catch problems and communicate design decisions.
6. Use an Issue for a task, bug, question, or feature request; use Projects to organize and track many items together.
7. It can run tests, builds, and supported deployment or release workflows in response to configured events.
8. GitHub Pages suits static sites and supported static output. It does not directly host a persistent server-side Python or Node.js process.
9. The secret may remain in history, copies, or logs. Revoke or rotate it and investigate where it was exposed.
10. A useful README, clear implementation, reproducible setup, tests, sensible history, and the ability to explain design choices.

---

**Guiding principle:** make your work easy to understand, safe to collaborate on, repeatable to test, and honest about what it actually does.
