"""
Modern Aesthetic CSS & Plotly Theme for SHG Platform
======================================================
Carefully scoped styles with high contrast, glassmorphic cards,
vibrant badges, and responsive modern layout.
"""


def get_css() -> str:
    """Return polished, safely scoped CSS for Streamlit."""
    return """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700;800&display=swap');
        
        /* ── Typography & Global Smoothing ───────────────────── */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        h1, h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif !important;
            font-weight: 600;
            color: #F8F9FA !important;
        }

        /* ── Main Gradient Header ────────────────────────────── */
        .main-header {
            background: linear-gradient(135deg, #6C63FF 0%, #00D4AA 50%, #FF6B6B 100%);
            padding: 2px;
            border-radius: 18px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 30px rgba(108,99,255,0.2);
        }
        .main-header-inner {
            background: linear-gradient(135deg, #121124 0%, #1A1A2E 100%);
            border-radius: 16px;
            padding: 1.8rem 2.2rem;
            text-align: center;
        }
        .main-header-inner h1 {
            font-size: 2.1rem !important;
            font-weight: 800 !important;
            background: linear-gradient(90deg, #A8A0FF, #00D4AA, #FFA8A8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0 0 0.3rem 0 !important;
        }
        .main-header-inner p {
            color: #A0A5BA !important;
            font-size: 0.95rem;
            margin: 0;
            font-weight: 400;
        }

        /* ── Section Title Banner ────────────────────────────── */
        .section-header {
            background: linear-gradient(90deg, rgba(108,99,255,0.15) 0%, rgba(26,26,46,0.5) 100%);
            border-left: 4px solid #6C63FF;
            border-radius: 8px;
            padding: 0.8rem 1.2rem;
            margin: 1.6rem 0 1.2rem 0;
            font-family: 'Poppins', sans-serif;
            font-weight: 600;
            font-size: 1.15rem;
            color: #F0F2F6 !important;
            box-shadow: 0 2px 10px rgba(0,0,0,0.15);
        }

        /* ── Metric Cards ────────────────────────────────────── */
        .metric-card {
            background: #1A1A2E;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            margin-bottom: 0.8rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .metric-card:hover {
            transform: translateY(-2px);
            border-color: rgba(108,99,255,0.4);
            box-shadow: 0 6px 20px rgba(108,99,255,0.15);
        }
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0;
            width: 4px; height: 100%;
        }
        .metric-card.purple::before { background: #6C63FF; }
        .metric-card.green::before { background: #00D4AA; }
        .metric-card.gold::before { background: #FFB347; }
        .metric-card.blue::before { background: #4EA8DE; }
        .metric-card.red::before { background: #FF6B6B; }
        
        .metric-icon {
            font-size: 1.7rem;
            margin-bottom: 0.3rem;
            display: inline-block;
        }
        .metric-title {
            color: #9AA0B4 !important;
            font-size: 0.78rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 0.3rem;
        }
        .metric-value {
            font-family: 'Poppins', sans-serif;
            font-size: 1.75rem;
            font-weight: 700;
            color: #FFFFFF !important;
            line-height: 1.2;
        }

        /* ── Performance Badges ──────────────────────────────── */
        .perf-badge {
            display: inline-block;
            padding: 0.5rem 1.5rem;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1.05rem;
            text-align: center;
            letter-spacing: 0.3px;
            font-family: 'Poppins', sans-serif;
            margin: 0.5rem 0;
        }
        .perf-high {
            background: rgba(0,212,170,0.15);
            color: #00D4AA !important;
            border: 1.5px solid #00D4AA;
        }
        .perf-medium {
            background: rgba(255,179,71,0.15);
            color: #FFB347 !important;
            border: 1.5px solid #FFB347;
        }
        .perf-low {
            background: rgba(255,107,107,0.15);
            color: #FF6B6B !important;
            border: 1.5px solid #FF6B6B;
        }

        /* ── Information Callout ──────────────────────────────── */
        .info-box {
            background: rgba(108,99,255,0.08);
            border: 1px solid rgba(108,99,255,0.25);
            border-radius: 10px;
            padding: 1rem 1.2rem;
            margin: 1rem 0;
            color: #D1D5DB !important;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        /* ── Content Card (Branding) ─────────────────────────── */
        .content-card {
            background: #1A1A2E;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 12px;
            padding: 1.2rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        .content-card h3 {
            color: #A8A0FF !important;
            font-size: 1.15rem;
        }

        /* ── WhatsApp Message Bubble ─────────────────────────── */
        .whatsapp-msg {
            background: #0B4D3C;
            border: 1px solid #128C7E;
            padding: 1.1rem 1.3rem;
            border-radius: 0 16px 16px 16px;
            max-width: 95%;
            margin: 0.6rem 0;
            font-size: 0.92rem;
            line-height: 1.55;
            white-space: pre-wrap;
            color: #E8F5E9 !important;
            box-shadow: 0 3px 12px rgba(0,0,0,0.25);
        }

        /* ── Hashtags ────────────────────────────────────────── */
        .hashtag-tag {
            display: inline-block;
            background: rgba(108,99,255,0.18);
            color: #B8B0FF !important;
            padding: 0.3rem 0.75rem;
            border-radius: 20px;
            margin: 0.2rem;
            font-size: 0.82rem;
            font-weight: 500;
            border: 1px solid rgba(108,99,255,0.3);
        }

        /* ── Footer ──────────────────────────────────────────── */
        .footer {
            text-align: center;
            padding: 2rem 0 1rem 0;
            margin-top: 3rem;
            border-top: 1px solid rgba(255,255,255,0.08);
            color: #717A94 !important;
            font-size: 0.85rem;
        }
        .footer strong {
            color: #A8A0FF !important;
        }
    </style>
    """


def get_metric_card_html(title: str, value: str, icon: str = "📊",
                         color: str = "purple") -> str:
    """Generate clean HTML for a styled metric card."""
    return f"""
    <div class="metric-card {color}">
        <span class="metric-icon">{icon}</span>
        <div class="metric-title">{title}</div>
        <div class="metric-value">{value}</div>
    </div>
    """


# ── Plotly Dark Theme Config ────────────────────────────────────────────────

PLOTLY_TEMPLATE = dict(
    layout=dict(
        paper_bgcolor='rgba(26, 26, 46, 0.6)',
        plot_bgcolor='rgba(18, 17, 36, 0.4)',
        font=dict(family='Inter, sans-serif', color='#D1D5DB', size=12),
        title=dict(font=dict(family='Poppins, sans-serif', size=15, color='#F3F4F6')),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='#9CA3AF'),
            title_font=dict(color='#D1D5DB')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.06)',
            zerolinecolor='rgba(255, 255, 255, 0.1)',
            tickfont=dict(color='#9CA3AF'),
            title_font=dict(color='#D1D5DB')
        ),
        legend=dict(
            bgcolor='rgba(26, 26, 46, 0.8)',
            font=dict(color='#D1D5DB'),
            bordercolor='rgba(255, 255, 255, 0.1)'
        ),
        colorway=['#6C63FF', '#00D4AA', '#FFB347', '#FF6B6B', '#4EA8DE',
                  '#9D4EDD', '#4ECB71', '#FF85A2', '#FFC75F', '#845EC2'],
        margin=dict(l=45, r=25, t=50, b=45),
    )
)

PERF_COLORS = {
    "High Performance": "#00D4AA",
    "Medium Performance": "#FFB347",
    "Low Performance": "#FF6B6B",
}
