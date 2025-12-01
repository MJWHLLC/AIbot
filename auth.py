"""Basic session-based authentication helpers.

This module provides a minimal `login_required` decorator and helper functions
that use Flask sessions. Authentication is controlled by two environment
variables: `AUTH_USERNAME` and `AUTH_PASSWORD`. If `AUTH_USERNAME` is not set,
authentication is disabled (convenient for local development and tests).
"""
from __future__ import annotations

import os
from functools import wraps
from typing import Optional
from flask import session, redirect, url_for, request, flash

from . import users


def authenticate(username: str, password: str) -> bool:
    """Authenticate against the users DB if users exist; otherwise fall back
    to environment variables for development convenience.
    """
    # If DB has users, prefer DB authentication
    try:
        user_list = users.list_users()
    except Exception:
        user_list = []

    if user_list:
        return users.verify_password(username, password)

    expected_user = os.environ.get("AUTH_USERNAME")
    expected_pass = os.environ.get("AUTH_PASSWORD")
    if not expected_user:
        # No auth configured -> allow (development)
        return True
    return username == expected_user and password == expected_pass


def login_user(username: str) -> None:
    session["user"] = username


def logout_user() -> None:
    session.pop("user", None)


def current_user() -> Optional[str]:
    return session.get("user")


def is_current_user_admin() -> bool:
    """Return True if the current logged-in user is an admin. If the users DB
    is empty and no AUTH_USERNAME is configured, treat current user as admin
    for development convenience.
    """
    uname = current_user()
    if not uname:
        return False
    try:
        user = users.get_user(uname)
    except Exception:
        user = None
    if user:
        return bool(user.get("is_admin"))
    # Fallback: if AUTH_USERNAME present and matches, treat as admin
    expected_user = os.environ.get("AUTH_USERNAME")
    if expected_user and expected_user == uname:
        return True
    # Development fallback
    return not os.environ.get("AUTH_USERNAME")


def login_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        # If no auth configured and no users, do not require login
        if not os.environ.get("AUTH_USERNAME") and not users.list_users():
            return view_func(*args, **kwargs)

        if "user" in session:
            return view_func(*args, **kwargs)

        return redirect(url_for("login", next=request.url))

    return wrapped


def admin_required(view_func):
    @wraps(view_func)
    def wrapped(*args, **kwargs):
        if is_current_user_admin():
            return view_func(*args, **kwargs)
        flash("Admin privileges required")
        return redirect(url_for("index"))

    return wrapped
