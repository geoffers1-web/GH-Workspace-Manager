"""
Application metadata for GH Workspace.

This file is the single source of truth for application identity.
"""

APP_NAME = "GH Workspace"
APP_VERSION = "5.5"
APP_RELEASE = "V6.2"
APP_AUTHOR = "Geoffrey D Hinds"
APP_DESCRIPTION = "Professional desktop workspace manager for GitHub-based projects."


def get_window_title() -> str:
    return f"{APP_NAME} {APP_RELEASE}"
