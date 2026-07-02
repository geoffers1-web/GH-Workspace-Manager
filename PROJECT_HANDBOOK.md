# GH Workspace Project Handbook

**Version:** 1.0
**Project:** GH Workspace
**Status:** Active Development

---

# 1. Project Vision

GH Workspace is a professional desktop application for managing GitHub-based projects from a single, modular interface.

The project's objectives are to:

* Provide a clean desktop interface for project management.
* Integrate Git and GitHub workflows.
* Monitor workspace health.
* Support a modular plugin architecture.
* Produce professional-quality software suitable for long-term maintenance and expansion.

---

# 2. Development Environment

## Primary Development Platform

Operating System:

* Linux

Python Version:

* Python 3.14.6

Standard Development Command:

```bash
python
```

Application Entry Point:

```text
src/main.py
```

Repository:

* Git (SSH)

Primary Branch:

* main

## Development Standard

Although both `python` and `python3` resolve to Python 3.14.6 on the development system, this project standardizes on the use of the `python` command throughout all documentation and build instructions.

---

# 3. Repository Structure

The project follows a professional modular architecture.

```text
src/
    config/
    core/
    gui/
    plugins/
    services/

docs/
releases/
Builder/
tests/
```

---

# 4. Development Workflow

Each release follows this process:

1. Design
2. Build
3. Test
4. Validate
5. Commit
6. Push to GitHub
7. Update documentation

Each completed release must include:

* Release Notes
* Test Checklist
* Changelog updates (where applicable)
* Git commit

---

# 5. Coding Standards

* Modular design.
* Small, focused modules.
* Clear naming conventions.
* Document public classes and functions.
* Avoid duplicate functionality.
* Prefer composition over duplication.

---

# 6. Documentation Standards

Project documentation includes:

* README.md
* CHANGELOG.md
* ROADMAP.md
* PROJECT_HANDBOOK.md
* Release Notes
* Developer Guides
* User Guides
* Architecture Documentation

Documentation is maintained alongside source code.

---

# 7. Release Philosophy

Releases are incremental.

Each release should:

* Introduce one logical improvement.
* Maintain compatibility where practical.
* Be fully tested before committing.

---

# 8. Current Status

Current development milestone:

* Professional Modular Desktop Application

Current Builder:

* Builder V3.1

Application Status:

* Desktop application launches successfully.
* Modular architecture established.
* Repository structure stabilized.
* Documentation framework established.

---

# 9. Long-Term Roadmap

Future development will include:

* Project Explorer
* Integrated Git Manager
* Plugin Manager
* Settings Dialog
* Search and Indexing
* Release Management
* Installer generation
* Production-ready desktop application

---

# 10. Handbook Maintenance

This handbook is a living document.

It should be updated whenever significant architectural, workflow, or development process changes occur.

Each major handbook revision should be recorded in the project history.
