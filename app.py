"""
Fed-Dup - Federated Repository Duplication
Web UI built with Streamlit
"""

import sys
from pathlib import Path

import streamlit as st

# Ensure the package is importable when run from the repo root
sys.path.insert(0, str(Path(__file__).parent))

from feddup.config import (
    load_config,
    save_config,
    add_repository,
    remove_repository,
    get_repositories,
    get_setting,
)
from feddup.engine import duplicate_repository
from feddup.utils import get_repo_size, humanize_size

# Page config
st.set_page_config(
    page_title="Fed-Dup",
    page_icon="🛡️",
    layout="wide",
)

# Custom CSS (also see styles.css for the full stylesheet)
try:
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)
except Exception:
    pass

st.markdown(
    """
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown('<div class="main-header">🛡️ Fed-Dup</div>', unsafe_allow_html=True)
st.caption("*Federated Repository Duplication Engine*")
st.divider()

# Load config (session-cached to avoid re-reading mid-run)
config = load_config()

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.subheader("⚙️ Fed-Dup Settings")

    with st.expander("🔑 Credentials", expanded=True):
        gh_token = st.text_input(
            "GitHub Token",
            value=config.get("github_token", ""),
            type="password",
            help="Personal Access Token with repo access",
        )
        backup_token = st.text_input(
            "Backup Platform Token",
            value=config.get("backup_token", ""),
            type="password",
            help="Token for your backup Git host",
        )

        if st.button("💾 Save Credentials", use_container_width=True):
            config["github_token"] = gh_token
            config["backup_token"] = backup_token
            save_config(config)
            st.success("✅ Credentials saved securely")

    with st.expander("⚡ Sync Settings"):
        cleanup = st.toggle(
            "🧹 Cleanup after sync",
            value=bool(get_setting(config, "cleanup_after_sync", False)),
            help="Delete local mirror cache after push to save disk space",
        )
        config.setdefault("settings", {})
        config["settings"]["cleanup_after_sync"] = cleanup
        save_config(config)

        interval_min = st.number_input(
            "⏱️ Auto-sync interval (minutes)",
            min_value=1,
            value=int(get_setting(config, "auto_sync_interval", 3600)) // 60 or 60,
            step=5,
            help="How often the background worker runs",
        )
        config["settings"]["auto_sync_interval"] = interval_min * 60
        save_config(config)

        st.caption("📁 Workspace: `./feddup_workspace/`")

# ---------------------------------------------------------------------------
# Main content
# ---------------------------------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📦 Repositories to Duplicate")

    with st.expander("➕ Add Repository", expanded=False):
        with st.form("add_repo", clear_on_submit=True):
            name = st.text_input("Friendly Name", placeholder="my-awesome-project")
            source = st.text_input(
                "Source URL", placeholder="https://github.com/user/repo.git"
            )
            destination = st.text_input(
                "Destination URL", placeholder="https://gitlab.com/user/repo.git"
            )

            if st.form_submit_button("Add to Fed-Dup", use_container_width=True):
                if name and source and destination:
                    add_repository(config, name, source, destination)
                    st.success(f"✅ Added {name} to duplication queue")
                    st.rerun()
                else:
                    st.error("❌ All fields are required")

    repos = get_repositories(config)

    if not repos:
        st.info("💡 No repositories configured. Add one above to start duplicating.")
    else:
        for idx, repo in enumerate(repos):
            with st.container():
                cols = st.columns([3, 1.5, 0.8, 0.8])

                with cols[0]:
                    st.markdown(f"**{repo['name']}**")
                    st.caption(f"📍 {repo['source']}")
                    st.caption(f"🎯 {repo['destination']}")

                with cols[1]:
                    workspace_path = Path("./feddup_workspace")
                    size = get_repo_size(workspace_path, repo["name"])
                    if size > 0:
                        st.caption(f"💾 {humanize_size(size)} cached")

                with cols[2]:
                    if st.button("🔄 Sync", key=f"sync_{idx}"):
                        if not gh_token or not backup_token:
                            st.error("❌ Please configure credentials first")
                        else:
                            with st.spinner(f"⏳ Duplicating {repo['name']}..."):
                                success, msg = duplicate_repository(
                                    repo,
                                    gh_token,
                                    backup_token,
                                    cleanup=bool(
                                        get_setting(config, "cleanup_after_sync", False)
                                    ),
                                )
                                if success:
                                    st.success(f"✅ {msg}")
                                else:
                                    st.error(f"❌ {msg}")

                with cols[3]:
                    if st.button("🗑️", key=f"del_{idx}", help="Remove from Fed-Dup"):
                        remove_repository(config, idx)
                        st.rerun()

                st.divider()

with col2:
    st.subheader("📊 Dashboard")

    st.metric("📦 Repositories", len(repos))
    interval = get_setting(config, "auto_sync_interval", 3600)
    st.metric("🔄 Auto-Sync Interval", f"{interval // 60} min")
    st.metric(
        "🧹 Cleanup",
        "Enabled" if get_setting(config, "cleanup_after_sync", False) else "Disabled",
    )

    if repos:
        if st.button("🔄 Sync All Now", use_container_width=True, type="primary"):
            if not gh_token or not backup_token:
                st.error("❌ Please configure credentials first")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                cleanup_flag = bool(get_setting(config, "cleanup_after_sync", False))

                for i, repo in enumerate(repos):
                    status_text.text(f"⏳ Syncing: {repo['name']}...")
                    success, msg = duplicate_repository(
                        repo, gh_token, backup_token, cleanup=cleanup_flag
                    )
                    progress_bar.progress((i + 1) / len(repos))

                status_text.text("✅ All repositories synced!")

    st.divider()

    with st.expander("❓ How to use Fed-Dup"):
        st.markdown("""
            1. **Generate a GitHub PAT** with `repo` scope
            2. **Generate a token** for your backup platform
            3. **Add repositories** you want to duplicate
            4. **Click Sync** to duplicate immediately
            5. **Fed-Dup auto-syncs** on the configured interval in the background
            """)

# Footer
st.divider()
st.caption(
    "🛡️ Fed-Dup v1.0.0 • Federated Repository Duplication Engine • No database required"
)
