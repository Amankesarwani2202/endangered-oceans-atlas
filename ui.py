"""Small, shared visual refinements; page structure and data behavior stay unchanged."""
POLISH_CSS = """
<style>
/* A restrained ocean accent, with native theme colors for form readability. */
:root { --atlas-accent: #126b80; --atlas-line: rgba(75, 133, 157, .20); }
[data-testid="stMainBlockContainer"] { padding-top: 2.2rem; padding-bottom: 2.8rem; }
[data-testid="stMain"] h1 { letter-spacing: -.025em; }
[data-testid="stMain"] h3 { letter-spacing: -.012em; }
[data-testid="stSidebarNav"] { padding-top: 1rem; }
[data-testid="stSidebarNav"] a { border-radius: 9px; margin: .16rem .4rem; transition: background .16s ease; }
[data-testid="stSidebarNav"] a:hover { background: rgba(18, 107, 128, .08); }
[data-testid="stSidebarNav"] a[aria-current="page"] { background: rgba(18, 107, 128, .12); font-weight: 600; }
[data-testid="stMetric"] {
    border: 1px solid var(--atlas-line); border-top: 3px solid var(--atlas-accent);
    border-radius: 12px; padding: 1rem 1.1rem;
    background: var(--secondary-background-color);
}
[data-testid="stMetricValue"] { letter-spacing: -.035em; }
[data-testid="stMetricLabel"] { opacity: .85; }
[data-testid="stForm"] {
    border: 1px solid var(--atlas-line); border-radius: 16px;
    padding: 1.35rem; box-shadow: 0 4px 18px rgba(10, 61, 98, .035);
}
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stNumberInput"] input { line-height: 1.55; }
[data-testid="stTextArea"] textarea { min-height: 110px; }
[data-testid="stButton"] button,
[data-testid="stFormSubmitButton"] button,
[data-testid="stDownloadButton"] button,
[data-testid="stLinkButton"] a {
    border-radius: 9px; min-height: 2.65rem; font-weight: 500;
    transition: border-color .16s ease, box-shadow .16s ease;
}
[data-testid="stButton"] button:hover,
[data-testid="stDownloadButton"] button:hover,
[data-testid="stLinkButton"] a:hover {
    border-color: var(--atlas-accent); box-shadow: 0 2px 8px rgba(18, 107, 128, .09);
}
[data-testid="stFormSubmitButton"] button:not(:disabled) {
    background: #0d6074; color: #fff; border-color: #0d6074;
}
[data-testid="stFormSubmitButton"] button:not(:disabled):hover { background: #094c5c; border-color: #094c5c; }
[data-testid="stFormSubmitButton"] button:not(:disabled) p { color: #fff; }
button:focus-visible, a:focus-visible, input:focus-visible, textarea:focus-visible {
    outline: 3px solid #35a5bc !important; outline-offset: 3px;
}
[data-testid="stAlert"] { border-radius: 11px; }
[data-testid="stExpander"] { border-color: var(--atlas-line); border-radius: 12px; }
.nav-card, .sp-card { box-shadow: 0 3px 14px rgba(10, 61, 98, .035); }
.nav-card { min-height: 196px; }
.sp-card { border-top: 3px solid #c4e5ec; }
.sp-help, .sp-fact { line-height: 1.6; }
.hero { box-shadow: 0 8px 26px rgba(10, 61, 98, .12); }
@media (max-width: 640px) {
    [data-testid="stMainBlockContainer"] { padding-top: 1.2rem; padding-left: 1rem; padding-right: 1rem; }
    .hero { padding: 2rem 1.35rem; border-radius: 15px; }
    .hero-title { font-size: 2.55rem; }
    .hero-subtitle { font-size: 1rem; }
    .crisis-bar { padding: .9rem 1rem; line-height: 1.6; }
    .species-hero { padding: 1.5rem 1.25rem; }
    .nav-card { min-height: unset; }
    [data-testid="stForm"] { padding: 1rem; }
}
@media (prefers-reduced-motion: reduce) {
    .nav-card, [data-testid="stSidebarNav"] a, button, a { transition: none !important; }
    .nav-card:hover { transform: none; }
}
</style>
"""
