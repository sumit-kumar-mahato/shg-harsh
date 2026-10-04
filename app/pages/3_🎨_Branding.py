"""
AI Branding & Content Studio Page
==================================
Generates localized brand names, emotional taglines, storytelling descriptions,
WhatsApp broadcast templates, Instagram posts, and hashtags for rural SHG products.
"""

import streamlit as st
import sys, os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from app.utils.styles import get_css

# ── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="SHG AI Branding Studio",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Inject Custom CSS ──────────────────────────────────────────────────────
st.markdown(get_css(), unsafe_allow_html=True)

# ── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-header-inner">
        <h1>🎨 AI Branding & Digital Content Studio</h1>
        <p>Localized Brand Creation & Omnichannel Social Media Campaign Generator</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <strong>✨ Autonomous Marketing Engine:</strong> Create localized branding and multi-channel digital marketing 
    content for rural micro-enterprises in seconds. Generates brand names, catchy taglines, story-driven product 
    narratives, WhatsApp broadcast templates, and social media campaigns with one-click export.
</div>
""", unsafe_allow_html=True)

# Import branding engine
try:
    from ai_branding.content_generator import SHGBrandingEngine
    engine = SHGBrandingEngine()
except Exception as e:
    st.error(f"❌ Error initializing branding engine: {e}")
    st.stop()

# ── Input Form ──────────────────────────────────────────────────────────────
st.markdown("### 📝 Enter Product & Enterprise Details")

col1, col2 = st.columns(2)

with col1:
    shg_name = st.text_input("Self Help Group Name", "Lakshmi Mahila SHG",
                              help="Official name of the SHG collective")
    product_name = st.text_input("Product / Produce Name", "Organic Turmeric Powder",
                                  help="Specific product item to be branded")
    product_category = st.selectbox(
        "Product Sector",
        ["Agriculture", "Dairy", "Handicrafts", "Textiles",
         "Food Processing", "Beauty/Personal Care", "Retail", "Services"]
    )

with col2:
    state = st.selectbox(
        "Origin State (for cultural resonance)",
        sorted([
            "Uttar Pradesh", "Bihar", "Madhya Pradesh", "Rajasthan",
            "Jharkhand", "Odisha", "Andhra Pradesh", "Telangana",
            "Tamil Nadu", "Karnataka", "Maharashtra", "West Bengal",
            "Assam", "Kerala", "Gujarat"
        ]),
        index=2
    )
    price_range = st.text_input("Price / Offer Range", "₹180 - ₹320 per pack",
                                 help="e.g., ₹150 - ₹300, Bulk rate on request")
    content_types = st.multiselect(
        "Select Content Artifacts to Generate",
        ["Brand Names", "Taglines", "Product Descriptions",
         "WhatsApp Broadcasts", "Instagram Captions", "Hashtags",
         "Complete 360° Kit"],
        default=["Complete 360° Kit"]
    )

generate_btn = st.button("🚀 Generate Digital Marketing Kit", use_container_width=True, type="primary")


# ── Render Helpers ──────────────────────────────────────────────────────────
def _display_brand_names(names: list):
    st.markdown("#### 🏷️ Recommended Brand Names")
    cols = st.columns(min(len(names), 3))
    for i, name in enumerate(names):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="content-card" style="text-align:center; padding:1.2rem;">
                <span style="font-size:0.75rem; color:#8E95AA; text-transform:uppercase; letter-spacing:1px;">Concept #{i+1}</span>
                <h3 style="margin:0.4rem 0 0 0; font-size:1.25rem;">{name}</h3>
            </div>
            """, unsafe_allow_html=True)


def _display_taglines(taglines: list):
    st.markdown("#### 💬 High-Impact Taglines")
    for i, tagline in enumerate(taglines, 1):
        st.markdown(f"""
        <div class="content-card">
            <span style="color:#6C63FF; font-weight:700; font-size:0.9rem;">Option {i}:</span>
            <span style="color:#F3F4F6; font-style:italic; font-size:1rem; margin-left:0.5rem;">"{tagline}"</span>
        </div>
        """, unsafe_allow_html=True)


def _display_descriptions(descriptions: list):
    st.markdown("#### 📝 Storytelling Product Descriptions")
    for i, desc in enumerate(descriptions, 1):
        with st.expander(f"📄 Description Narrative #{i} (Click to expand)", expanded=(i == 1)):
            st.markdown(desc)


def _display_whatsapp(messages: list):
    st.markdown("#### 📱 Ready-to-Send WhatsApp Broadcasts")
    for i, msg in enumerate(messages, 1):
        st.markdown(f"**Broadcast Template #{i}:**")
        st.markdown(f'<div class="whatsapp-msg">{msg}</div>', unsafe_allow_html=True)
        st.code(msg, language=None)
        st.markdown("")


def _display_instagram(captions: list):
    st.markdown("#### 📸 Instagram & Social Media Posts")
    for i, caption in enumerate(captions, 1):
        with st.expander(f"📷 Post Narrative #{i}", expanded=(i == 1)):
            st.markdown(caption)
            st.code(caption, language=None)


def _display_hashtags(hashtags: list):
    st.markdown("#### #️⃣ Recommended Viral & Niche Hashtags")
    tags_html = " ".join([f'<span class="hashtag-tag">{tag}</span>' for tag in hashtags])
    st.markdown(f'<div style="padding:0.6rem 0 1rem 0;">{tags_html}</div>', unsafe_allow_html=True)
    st.code(" ".join(hashtags), language=None)


def _compile_all_content(kit: dict, product_name: str) -> str:
    lines = [
        "=" * 60,
        f"SHG 360° DIGITAL BRANDING & MARKETING KIT — {product_name.upper()}",
        "Generated by Intelligent SHG Performance & Digital Support Platform",
        "=" * 60,
        "",
        "🏷️ BRAND NAME SUGGESTIONS:",
        "-" * 30
    ]
    for name in kit["brand_names"]:
        lines.append(f"  • {name}")
    
    lines.extend(["", "💬 TAGLINES:", "-" * 30])
    for tag in kit["taglines"]:
        lines.append(f'  • "{tag}"')
        
    lines.extend(["", "📝 STORYTELLING PRODUCT DESCRIPTIONS:", "-" * 30])
    for i, desc in enumerate(kit["product_descriptions"], 1):
        lines.append(f"\n[Description #{i}]\n{desc}")
        
    lines.extend(["", "📱 WHATSAPP BROADCAST TEMPLATES:", "-" * 30])
    for i, msg in enumerate(kit["whatsapp_messages"], 1):
        lines.append(f"\n[WhatsApp Template #{i}]\n{msg}")
        
    lines.extend(["", "📸 INSTAGRAM CAPTIONS:", "-" * 30])
    for i, cap in enumerate(kit["instagram_captions"], 1):
        lines.append(f"\n[Instagram Caption #{i}]\n{cap}")
        
    lines.extend(["", "#️⃣ HASHTAGS:", "-" * 30, " ".join(kit["hashtags"])])
    
    return "\n".join(lines)


# ── Generation Handling ─────────────────────────────────────────────────────
if generate_btn:
    with st.spinner("✨ Crafting tailored branding & digital storytelling..."):
        
        if "Complete 360° Kit" in content_types:
            kit = engine.generate_complete_branding_kit(
                shg_name, product_name, product_category, state, price_range
            )
            
            st.markdown("---")
            st.markdown("### 🎁 Generated 360° Digital Marketing Kit")
            
            tabs = st.tabs(["🏷️ Brand Names", "💬 Catchy Taglines", "📝 Story Descriptions",
                             "📱 WhatsApp Broadcast", "📸 Instagram Captions", "#️⃣ Social Hashtags"])
            
            with tabs[0]: _display_brand_names(kit["brand_names"])
            with tabs[1]: _display_taglines(kit["taglines"])
            with tabs[2]: _display_descriptions(kit["product_descriptions"])
            with tabs[3]: _display_whatsapp(kit["whatsapp_messages"])
            with tabs[4]: _display_instagram(kit["instagram_captions"])
            with tabs[5]: _display_hashtags(kit["hashtags"])
            
            st.markdown("---")
            all_content = _compile_all_content(kit, product_name)
            st.download_button(
                "📥 Download Complete Marketing Kit (.txt)",
                all_content, f"branding_kit_{product_name.replace(' ', '_').lower()}.txt",
                "text/plain", use_container_width=True
            )
        else:
            if "Brand Names" in content_types:
                names = engine.generate_brand_names(shg_name, product_category, state, num=5)
                _display_brand_names(names)
            
            if "Taglines" in content_types:
                taglines = engine.generate_taglines(product_name, product_category, num=5)
                _display_taglines(taglines)
            
            if "Product Descriptions" in content_types:
                descriptions = engine.generate_product_description(product_name, product_category, num=3)
                _display_descriptions(descriptions)
            
            if "WhatsApp Broadcasts" in content_types:
                messages = engine.generate_whatsapp_message(product_name, shg_name, price_range, num=3)
                _display_whatsapp(messages)
            
            if "Instagram Captions" in content_types:
                captions = engine.generate_instagram_caption(product_name, shg_name, product_category, num=3)
                _display_instagram(captions)
            
            if "Hashtags" in content_types:
                hashtags = engine.generate_hashtags(product_category, state, shg_name, num=20)
                _display_hashtags(hashtags)

# ── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <p><strong>SHG AI Branding Studio</strong> • Module 3 of Intelligent SHG Performance Platform</p>
</div>
""", unsafe_allow_html=True)
