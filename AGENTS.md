# Contributor & Agent Guide

This guide helps new contributors get started with the `django-allauth-vipps` repository. It covers the repository structure, how to set up a development environment, run tests, and follow our contribution guidelines. This document also maintains a transparent log of AI agent collaboration in this project's development.

## Table of Contents

- [Contributor \& Agent Guide](#contributor--agent-guide)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Repository Structure](#repository-structure)
  - [Environment Setup](#environment-setup)
  - [Testing \& Validation](#testing--validation)
  - [Development Workflow](#development-workflow)
  - [Pull Request \& Commit Guidelines](#pull-request--commit-guidelines)
  - [AI Agent Collaboration Log](#ai-agent-collaboration-log)
    - [Agents Deployed](#agents-deployed)
    - [Summary of Contributions](#summary-of-contributions)
    - [Human Oversight](#human-oversight)

## Overview

The `django-allauth-vipps` repository contains a single, reusable Django app designed to be installed as a third-party package. Its sole purpose is to provide a fully compliant and configurable social authentication provider for Vipps Login, built to integrate seamlessly with `django-allauth` and `dj-rest-auth`.

## Repository Structure

The repository is structured as a standard Python package managed with Poetry.

-   `vipps_auth/`: The core Django app source code.
    -   `provider.py`: Contains the main `VippsProvider` class, which defines the logic for interacting with the Vipps OIDC API.
    -   `views.py`: Contains the `VippsOAuth2Adapter` that connects the provider to `django-allauth`'s views.
    -   `settings.py`: A configuration helper that allows for user-configurable settings.
    -   `apps.py`: The Django AppConfig, used to register the provider with `allauth`.
    -   `urls.py`: Defines the browser-flow login and callback URLs.
-   `tests/`: The test suite for the package.
    -   `test_provider.py`: Unit tests for the `VippsProvider` logic.
    -   `test_flow.py`: An integration test that mocks API calls and validates the full `dj-rest-auth` login flow.
    -   `settings.py` & `urls.py`: A minimal Django configuration used exclusively for running the test suite.
-   `pyproject.toml`: The Poetry configuration file. It defines the package metadata, main dependencies, and development dependencies.
-   `README.md`: The public-facing documentation for package users.
-   `LICENSE`: The MIT license file for the project.
-   `AGENTS.md`: This document.

## Environment Setup

To create a local development environment for this package, you will need **Python 3.11+** and **Poetry**.

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/danpejobo/django-allauth-vipps.git
    cd django-allauth-vipps
    ```

2.  **Install Dependencies:**
    This command reads the `pyproject.toml` file, resolves all dependencies (both main and development), and installs them into a dedicated virtual environment managed by Poetry.
    ```bash
    poetry install
    ```

3.  **Activate the Virtual Environment:**
    To work within the project's environment, activate the shell created by Poetry.
    ```bash
    poetry shell
    ```
    Your command prompt should now change to indicate you are inside the virtual environment (e.g., `(django-allauth-vipps-py3.11) ...`).

## Testing & Validation

A robust test suite is included to ensure correctness and prevent regressions. Before submitting any changes, please ensure all tests pass.

-   **Run the full test suite:**
    ```bash
    poetry run pytest
    ```
-   The tests use `requests-mock` to simulate responses from the Vipps API, so no network calls are made.
-   All 5 tests should pass with the default configuration.

## Development Workflow

1.  Ensure your `main` branch is up-to-date.
2.  Create a new feature or bugfix branch with a descriptive name:
    ```bash
    git checkout -b feat/add-new-scope
    # or
    git checkout -b fix/resolve-login-issue
    ```
3.  Make your code changes.
4.  Add or update tests in the `tests/` directory to cover your changes.
5.  Run the full test suite to ensure all checks pass: `poetry run pytest`.
6.  Commit your changes following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard.
7.  Push your branch and open a pull request.

## Pull Request & Commit Guidelines

-   Please use **Conventional Commits** for your commit messages. This helps automate changelogs and makes the project history easy to read.
    -   `feat:` A new feature for the user.
    -   `fix:` A bug fix for the user.
    -   `docs:` Documentation-only changes.
    -   `test:` Adding or refactoring tests.
    -   `chore:` Build process, tooling, or dependency updates.
    -   `refactor:` A code change that neither fixes a bug nor adds a feature.
-   Ensure your PR has a clear description of the problem and solution.
-   Link to any relevant issues.

## AI Agent Collaboration Log

This project was developed in a pair-programming paradigm with AI assistants. This log maintains transparency about their roles.

### Agents Deployed

1.  **Agent 1: Scaffolding and Initial Development**
    * **Name:** Gemini (Provider: Google)
2.  **Agent 2: Advanced Debugging and Bug Resolution**
    * **Name:** Codex (Provider: OpenAI)

### Summary of Contributions

The development process involved two distinct phases:

1.  **Phase 1: Creation (with Gemini):** The project began with the high-level goal of creating a reusable Vipps login app. The Gemini agent successfully generated the complete package structure, core application logic (`provider.py`, `views.py`, `settings.py`), and a full test suite.

2.  **Phase 2: Hardening and Debugging (with Codex):** During initial testing, a persistent `TypeError` was encountered, indicating a subtle incompatibility between the specific library versions of `dj-rest-auth` and `django-allauth`. The human developer switched to the Codex agent for specialized debugging. Codex identified the issue as a known bug in the dependency, provided the correct remediation path (updating the library version via `poetry update`), and helped simplify the application code by removing now-unnecessary workarounds.

### Human Oversight

All code, architectural decisions, and suggestions generated by the AI agents were reviewed, tested, and approved by the human developer. The human developer retains final authority and responsibility for the code in this repository.

---
*This document was last updated on June 27, 2025.*
