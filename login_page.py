"""
login_page.py — Login & Sign-Up UI for Agro Guidance
Renders a beautiful authentication page using Streamlit.
"""

import streamlit as st
from auth import register_user, login_user


def _inject_styles():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── Global reset ── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* ── Dark page background ── */
        .stApp {
            background: radial-gradient(ellipse at 20% 20%, #0d2b1a 0%, #0a0f0d 60%, #050a07 100%);
            min-height: 100vh;
        }

        /* ── Hide Streamlit chrome ── */
        #MainMenu, footer, header { visibility: hidden; }

        /* ── Auth card wrapper ── */
        .auth-container {
            max-width: 480px;
            margin: 0 auto;
            padding: 0 1rem;
        }

        /* ── Logo / hero section ── */
        .auth-hero {
            text-align: center;
            padding: 2.5rem 0 1.5rem;
        }
        .auth-hero .logo-icon {
            font-size: 3.5rem;
            display: block;
            margin-bottom: 0.4rem;
            filter: drop-shadow(0 0 18px rgba(74, 222, 128, 0.55));
            animation: float 3s ease-in-out infinite;
        }
        @keyframes float {
            0%, 100% { transform: translateY(0); }
            50%       { transform: translateY(-7px); }
        }
        .auth-hero h1 {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #4ade80 0%, #22c55e 50%, #86efac 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        .auth-hero p {
            color: #6b7280;
            font-size: 0.9rem;
            margin-top: 0.3rem;
        }

        /* ── Card ── */
        .auth-card {
            background: rgba(15, 30, 20, 0.85);
            border: 1px solid rgba(74, 222, 128, 0.18);
            border-radius: 20px;
            padding: 2rem 2rem 1.5rem;
            box-shadow:
                0 25px 50px rgba(0, 0, 0, 0.5),
                inset 0 1px 0 rgba(74, 222, 128, 0.08);
            backdrop-filter: blur(16px);
            margin-bottom: 1.5rem;
        }

        /* ── Tab switcher ── */
        .tab-switcher {
            display: flex;
            background: rgba(0, 0, 0, 0.35);
            border-radius: 12px;
            padding: 4px;
            margin-bottom: 1.6rem;
            gap: 4px;
        }
        .tab-btn {
            flex: 1;
            text-align: center;
            padding: 0.55rem 0;
            border-radius: 9px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.25s ease;
            color: #9ca3af;
            border: none;
            background: transparent;
        }
        .tab-btn.active {
            background: linear-gradient(135deg, #16a34a, #15803d);
            color: #ffffff;
            box-shadow: 0 3px 10px rgba(22, 163, 74, 0.4);
        }

        /* ── Input fields ── */
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.4) !important;
            border: 1px solid rgba(74, 222, 128, 0.2) !important;
            border-radius: 10px !important;
            color: #e5e7eb !important;
            font-size: 0.9rem !important;
            padding: 0.65rem 0.9rem !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: rgba(74, 222, 128, 0.6) !important;
            box-shadow: 0 0 0 3px rgba(74, 222, 128, 0.12) !important;
            outline: none !important;
        }
        .stTextInput > div > div > input::placeholder { color: #4b5563 !important; }

        /* ── Labels ── */
        .stTextInput > label {
            color: #9ca3af !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            letter-spacing: 0.02em !important;
            text-transform: uppercase !important;
        }

        /* ── Primary button ── */
        .stButton > button {
            width: 100%;
            background: linear-gradient(135deg, #16a34a 0%, #15803d 50%, #166534 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.5rem !important;
            font-size: 0.95rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            cursor: pointer !important;
            transition: all 0.25s ease !important;
            box-shadow: 0 4px 15px rgba(22, 163, 74, 0.35) !important;
            margin-top: 0.5rem !important;
        }
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(22, 163, 74, 0.5) !important;
        }
        .stButton > button:active { transform: translateY(0) !important; }

        /* ── Alerts ── */
        .stSuccess, .stError, .stWarning {
            border-radius: 10px !important;
            font-size: 0.875rem !important;
        }

        /* ── Divider label ── */
        .section-label {
            color: #6b7280;
            font-size: 0.72rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 0.2rem 0 0.7rem;
        }

        /* ── Footer note ── */
        .auth-footer {
            text-align: center;
            color: #374151;
            font-size: 0.75rem;
            padding-bottom: 2rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_login_page():
    """Render the full authentication page (login + sign-up)."""
    _inject_styles()

    # ── Hero ──────────────────────────────────────────────
    st.markdown(
        """
        <div class="auth-hero">
            <span class="logo-icon">🌱</span>
            <h1>Agro Guidance</h1>
            <p>Your intelligent farming companion</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Tab state ─────────────────────────────────────────
    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"

    # ── Card start ────────────────────────────────────────
    st.markdown('<div class="auth-container"><div class="auth-card">', unsafe_allow_html=True)

    # Tab switcher using Streamlit radio (styled)
    col_login, col_signup = st.columns(2)
    with col_login:
        if st.button("🔑  Sign In", key="tab_login_btn", use_container_width=True):
            st.session_state.auth_tab = "login"
    with col_signup:
        if st.button("✨  Sign Up", key="tab_signup_btn", use_container_width=True):
            st.session_state.auth_tab = "signup"

    st.divider()

    # ── LOGIN FORM ────────────────────────────────────────
    if st.session_state.auth_tab == "login":
        st.markdown('<p class="section-label">Sign in to your account</p>', unsafe_allow_html=True)

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username", key="login_username")
            password = st.text_input("Password", placeholder="Enter your password", type="password", key="login_password")
            submitted = st.form_submit_button("Sign In →")

        if submitted:
            if not username or not password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Verifying credentials…"):
                    result = login_user(username, password)

                if result["success"]:
                    st.session_state.logged_in = True
                    st.session_state.current_user = result["user"]
                    st.success(f"Welcome back, {result['user']['first_name']}! 🌾")
                    st.rerun()
                else:
                    st.error(result["message"])

    # ── SIGN-UP FORM ──────────────────────────────────────
    else:
        st.markdown('<p class="section-label">Create a new account</p>', unsafe_allow_html=True)

        with st.form("signup_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name", placeholder="Ravi", key="su_first")
            with col2:
                last_name = st.text_input("Last Name", placeholder="Sharma", key="su_last")

            username  = st.text_input("Username", placeholder="ravi_farmer", key="su_username")
            email     = st.text_input("Email", placeholder="ravi@example.com", key="su_email")
            password  = st.text_input("Password", placeholder="Min. 6 characters", type="password", key="su_password")
            submitted = st.form_submit_button("Create Account →")

        if submitted:
            with st.spinner("Creating your account…"):
                result = register_user(first_name, last_name, username, email, password)

            if result["success"]:
                st.success(result["message"])
                st.session_state.auth_tab = "login"
                st.rerun()
            else:
                st.error(result["message"])

    st.markdown('</div></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="auth-footer">🌿 Agro Guidance · Empowering Farmers with Technology</div>',
        unsafe_allow_html=True,
    )
