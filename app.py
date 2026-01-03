"""Flask web app entrypoint for the Paralegal AI Assistant."""
from __future__ import annotations

import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv

from model_client import ModelClient
from prompts import build_document_prompt
from auth import login_required, login_user, logout_user, current_user, authenticate, admin_required
from users import create_user, list_users, delete_user, get_user, generate_token, validate_token, consume_token
from mail import init_mail, send_invite_email, send_password_reset_email
from flask_wtf import CSRFProtect
from flask_wtf.csrf import generate_csrf

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-for-local")

# Email configuration
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "localhost")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 25))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "false").lower() == "true"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@paralegal-agent.local")

init_mail(app)

# Enable CSRF protection for forms
app.config.setdefault("WTF_CSRF_TIME_LIMIT", None)
csrf = CSRFProtect(app)
app.jinja_env.globals["csrf_token"] = generate_csrf

# Initialize model client. It reads API config from environment variables.
model_client = ModelClient()


@app.route("/", methods=["GET"])
@login_required
def index():
    user = current_user()
    return render_template("index.html", user=user)


@app.route("/ask", methods=["POST"])
@login_required
def ask():
    query = request.form.get("query", "").strip()
    doc_type = request.form.get("document_type", "General")
    jurisdiction = request.form.get("jurisdiction", "Federal")
    if not query:
        flash("Please enter a question or prompt.")
        return redirect(url_for("index"))

    prompt = build_document_prompt(doc_type=doc_type, jurisdiction=jurisdiction, user_text=query)

    try:
        resp = model_client.generate(prompt)
    except Exception as exc:
        flash(f"Model error: {exc}")
        return redirect(url_for("index"))

    return render_template("index.html", result=resp, query=query, user=current_user())


@app.route("/login", methods=["GET", "POST"])
def login():
    """Simple username/password login. Uses `AUTH_USERNAME` and `AUTH_PASSWORD` env vars.

    If `AUTH_USERNAME` is not set, authentication is disabled for local development.
    """
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    next_url = request.form.get("next") or url_for("index")

    if not os.environ.get("AUTH_USERNAME") and not list_users():
        # No auth configured and no users in DB: create a dev user and sign in
        login_user(username or "dev")
        flash("Authentication is not configured; signed in as development user.")
        return redirect(next_url)

    if authenticate(username, password):
        login_user(username)
        flash("Signed in")
        return redirect(next_url)

    flash("Invalid credentials")
    return redirect(url_for("login"))


@app.route("/logout", methods=["POST"]) 
def logout():
    logout_user()
    flash("Signed out")
    return redirect(url_for("login"))


@app.route("/admin", methods=["GET"])
@login_required
@admin_required
def admin():
    users_list = list_users()
    return render_template("admin.html", users=users_list)


@app.route("/admin/create", methods=["POST"])
@login_required
@admin_required
def admin_create():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    is_admin_flag = bool(request.form.get("is_admin"))
    if not username or not password:
        flash("Username and password required")
        return redirect(url_for("admin"))
    create_user(username, password, is_admin=is_admin_flag)
    flash(f"Created user {username}")
    return redirect(url_for("admin"))


@app.route("/admin/delete", methods=["POST"])
@login_required
@admin_required
def admin_delete():
    username = request.form.get("username")
    if not username:
        flash("Username required")
        return redirect(url_for("admin"))
    delete_user(username)
    flash(f"Deleted user {username}")
    return redirect(url_for("admin"))


@app.route("/admin/invite", methods=["POST"])
@login_required
@admin_required
def admin_invite():
    """Create an invite link for a new user (not yet created in DB)."""
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    
    if not username or not email:
        flash("Username and email required")
        return redirect(url_for("admin"))
    
    # Check if user already exists
    if get_user(username):
        flash(f"User {username} already exists")
        return redirect(url_for("admin"))
    
    token = generate_token(username, "invite", expires_in_hours=72)
    base_url = request.url_root.rstrip("/")
    invite_link = f"{base_url}/join?token={token}"
    
    # Send email
    if send_invite_email(email, username, invite_link):
        flash(f"Invite sent to {email}")
    else:
        flash(f"Failed to send invite email. Link: {invite_link}")
    
    return redirect(url_for("admin"))


@app.route("/join", methods=["GET", "POST"])
def join():
    """Accept an invite and set up a new user account."""
    token = request.args.get("token") or request.form.get("token")
    
    if request.method == "GET":
        if not token:
            flash("Invalid or missing invite token")
            return redirect(url_for("login"))
        
        username = validate_token(token, "invite")
        if not username:
            flash("Invite token expired or invalid")
            return redirect(url_for("login"))
        
        return render_template("join.html", token=token, username=username)
    
    # POST: set password and create account
    username = validate_token(token, "invite")
    if not username:
        flash("Invite token expired or invalid")
        return redirect(url_for("login"))
    
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")
    
    if not password or password != confirm:
        flash("Passwords do not match or are empty")
        return render_template("join.html", token=token, username=username)
    
    if len(password) < 8:
        flash("Password must be at least 8 characters")
        return render_template("join.html", token=token, username=username)
    
    create_user(username, password, is_admin=False)
    consume_token(token)
    flash("Account created successfully! Please sign in.")
    return redirect(url_for("login"))


@app.route("/reset", methods=["GET", "POST"])
def reset():
    """Request a password reset link."""
    if request.method == "GET":
        return render_template("reset_request.html")
    
    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    user = get_user(username)
    
    if not user or not email:
        # For security, do not reveal if user exists
        flash("If the account exists, a password-reset link will be sent to the email on file.")
        return redirect(url_for("login"))
    
    token = generate_token(username, "password_reset", expires_in_hours=1)
    base_url = request.url_root.rstrip("/")
    reset_link = f"{base_url}/reset-password?token={token}"
    
    # Send email
    if send_password_reset_email(email, username, reset_link):
        flash("Password reset link sent to your email (valid for 1 hour).")
        return redirect(url_for("login"))
    else:
        flash("Failed to send password-reset email. Contact support.")
        return redirect(url_for("login"))


@app.route("/reset", methods=["GET"])
@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    """Use a password-reset token to set a new password."""
    token = request.args.get("token") or request.form.get("token")
    
    if request.method == "GET":
        if not token:
            flash("Invalid or missing reset token")
            return redirect(url_for("login"))
        
        username = validate_token(token, "password_reset")
        if not username:
            flash("Reset token expired or invalid")
            return redirect(url_for("login"))
        
        return render_template("reset_password.html", token=token, username=username)
    
    # POST: set new password
    username = validate_token(token, "password_reset")
    if not username:
        flash("Reset token expired or invalid")
        return redirect(url_for("login"))
    
    password = request.form.get("password", "")
    confirm = request.form.get("confirm", "")
    
    if not password or password != confirm:
        flash("Passwords do not match or are empty")
        return render_template("reset_password.html", token=token, username=username)
    
    if len(password) < 8:
        flash("Password must be at least 8 characters")
        return render_template("reset_password.html", token=token, username=username)
    
    create_user(username, password, is_admin=False)
    consume_token(token)
    flash("Password reset successfully! Please sign in.")
    return redirect(url_for("login"))


if __name__ == "__main__":
    # For local development only
    app.run(debug=True)
