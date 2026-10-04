"""
SHG Intelligent Branding & Digital Content Generation Engine
=============================================================
An autonomous AI branding and digital marketing content engine designed
specifically for Self Help Groups (SHGs) and rural micro-enterprises.
Generates localized brand names, taglines, rich storytelling product descriptions,
high-converting WhatsApp promotional messages, Instagram captions, and targeted hashtags.
"""

import os
import random
import re
from typing import List, Optional, Dict, Any


class SHGBrandingEngine:
    """
    Intelligent Branding & Digital Marketing Engine for Self Help Groups.
    Operates 100% locally with extensive domain knowledge for 8+ rural industry sectors.
    """
    
    def __init__(self):
        """Initialize comprehensive vocabulary, regional dictionaries, and copywriting patterns."""
        
        self.positive_adjectives = [
            "Pure", "Fresh", "Natural", "Organic", "Premium", "Authentic",
            "Traditional", "Handcrafted", "Artisan", "Exquisite", "Fine",
            "Golden", "Royal", "Divine", "Sacred", "Heritage", "Pristine",
            "Wholesome", "Finest", "Supreme", "Classic", "Elegant",
            "Genuine", "Original", "Delicate", "Rich", "Luxurious",
            "Timeless", "Graceful", "Blessed", "Vibrant", "Noble"
        ]
        
        self.empowerment_words = [
            "Shakti", "Nari", "Mahila", "Swayam", "Pragati", "Unnati",
            "Ujjwal", "Saheli", "Sangini", "Ekta", "Samriddhi", "Vikas",
            "Asha", "Jyoti", "Kiran", "Chetna", "Jagriti", "Swabhiman",
            "Saksham", "Samarth", "Udaan", "Umang", "Utsah", "Prerana",
            "Siddhi", "Ananya", "Matri", "Tejaswini"
        ]
        
        self.emotional_words = [
            "love", "care", "warmth", "passion", "dedication",
            "heart", "soul", "pride", "tradition", "heritage",
            "family", "community", "togetherness", "trust", "hope",
            "harmony", "integrity", "devotion"
        ]
        
        self.cta_phrases = [
            "Order now to support rural women artisans!",
            "Shop today & bring home authentic handcrafted goodness!",
            "Direct from rural self-help collectives to your doorstep!",
            "Limited batches freshly prepared — Place your order today!",
            "WhatsApp us now for bulk & festive gift orders!",
            "Support women entrepreneurs — Every purchase empowers a family!",
            "Taste and feel the authentic difference today!",
            "Pure quality guaranteed. Order your pack now!"
        ]
        
        self.product_terms = {
            "Agriculture": {
                "items": ["Spices", "Turmeric", "Millets", "Heritage Rice", "Cold-Pressed Mustard", "Organic Pulses", "Honey", "Wheat Grain"],
                "qualities": ["farm-fresh", "pesticide-free", "certified natural", "naturally sun-dried", "stone-ground", "unpolished", "traditional cultivar"],
                "benefits": ["rich in natural nutrients", "free from synthetic chemicals", "high in natural aroma & essential oils", "supports digestive immunity"],
                "hooks": ["Straight from fertile soil to your kitchen", "Reviving the forgotten taste of authentic farm harvests"]
            },
            "Dairy": {
                "items": ["Desi Ghee", "A2 Bilona Ghee", "Fresh Paneer", "Hand-Churned Butter", "Traditional Curd", "Organic Milk Mawa"],
                "qualities": ["slow-cooked bilona churned", "grass-fed native cow milk", "100% pure & preservative-free", "golden aromatic granular texture"],
                "benefits": ["boosts natural immunity & energy", "rich in healthy omega fatty acids", "promotes holistic Ayurvedic vitality"],
                "hooks": ["Experience the nostalgic golden aroma of authentic village ghee", "Crafted using Vedic clay-pot churning traditions"]
            },
            "Handicrafts": {
                "items": ["Bamboo Planters", "Terracotta Pottery", "Jute Craft Handbags", "Dokra Metal Artifacts", "Hand-Carved Wooden Toys", "Macrame Decor"],
                "qualities": ["hand-sculpted", "eco-friendly & biodegradable", "intricately hand-painted", "sustainable artisan grade"],
                "benefits": ["adds soulful rustic charm to modern homes", "100% sustainable planet-friendly material", "each piece is a unique collectible"],
                "hooks": ["Bring centuries of living rural folklore into your contemporary living room", "Where raw earth transforms into timeless artisan elegance"]
            },
            "Textiles": {
                "items": ["Handloom Cotton Saree", "Block-Printed Dupatta", "Embroidered Kurta", "Chanderi Silk Stole", "Organic Cotton Tote", "Khadi Linen"],
                "qualities": ["handloom woven", "plant-based natural dyes", "hand-block printed", "breathable gentle weave"],
                "benefits": ["skin-friendly & feather-light comfort", "long-lasting artisanal durability", "graceful aesthetic for every occasion"],
                "hooks": ["Wear the legacy of India’s master handloom weavers", "Fabric spun with generational skill and quiet empowerment"]
            },
            "Food Processing": {
                "items": ["Grandma's Mango Pickle", "Sun-Dried Crisp Papad", "Traditional Amla Murabba", "Organic Forest Honey", "Roasted Millet Snacks", "Chilli Garlic Chutney"],
                "qualities": ["authentic age-old secret recipe", "slow sun-cured with zero artificial preservatives", "stone-pounded natural spices", "small batch handcrafted"],
                "benefits": ["irresistible nostalgic homemade taste", "pure unadulterated ingredients", "mouth-watering culinary delight"],
                "hooks": ["That unforgettable taste of Maa-ke-haath ka swaad", "Preserving traditional family recipes passed down over generations"]
            },
            "Beauty/Personal Care": {
                "items": ["Cold-Pressed Herbal Hair Oil", "Neem & Haldi Soap Bar", "Ayurvedic Ubtan Scrub", "Rose Water Hydrosol", "Virgin Coconut Lip Balm"],
                "qualities": ["100% plant active based", "chemical-free & paraben-free", "Ayurvedic formulation", "gentle small-batch cure"],
                "benefits": ["rejuvenates glowing healthy skin", "deeply nourishes without heavy residue", "ancient wellness for daily modern ritual"],
                "hooks": ["Pure botanical nourishment inspired by ancient Ayurvedic wisdom", "Clean, gentle beauty crafted directly with nature’s purest herbs"]
            },
            "Retail": {
                "items": ["Daily Kitchen Essentials", "Rural Grocery Collective", "Handmade Household Pack"],
                "qualities": ["locally sourced", "uncompromised quality", "affordable pricing", "community backed"],
                "benefits": ["guaranteed freshness", "direct fair trade", "trustworthy quality"],
                "hooks": ["Pure community-backed daily essentials you can count on", "Fresh, honest essentials direct from producer women"]
            },
            "Services": {
                "items": ["Catering & Traditional Feasts", "Custom Tailoring & Stitching", "Handicraft Workshops"],
                "qualities": ["dedicated artisan touch", "personalized service", "hygienic & punctual", "fair and transparent"],
                "benefits": ["tailored to perfection", "authentic hospitality", "empowering community employment"],
                "hooks": ["Warm, authentic and dedicated services that feel like family", "Skilled craftsmanship delivered with genuine pride"]
            },
        }
        
        self.state_cultural_tags = {
            "Uttar Pradesh": ["Awadhi Heritage", "Ganga-Jamuni Craft", "Purvanchal Roots", "Brahmavart Pure"],
            "Bihar": ["Mithila Art", "Bhojpur Tradition", "Anga Harvest", "Magadha Heritage"],
            "Madhya Pradesh": ["Malwa Pure", "Bundelkhand Craft", "Narmada Valley", "Gond Artistry"],
            "Rajasthan": ["Marwar Heritage", "Shekhawati Colors", "Royal Rajputana", "Thar Natural"],
            "Jharkhand": ["Chotanagpur Forest", "Santhal Heritage", "Jharkhand Naturals", "Adivasi Craft"],
            "Odisha": ["Kalinga Craft", "Konark Heritage", "Utkal Naturals", "Pattachitra Legacy"],
            "Andhra Pradesh": ["Lepakshi Craft", "Telugu Naturals", "Coastal Andhra", "Rayalaseema Rich"],
            "Telangana": ["Deccan Heritage", "Kakatiya Craft", "Pochampally Glory", "Golkonda Pure"],
            "Tamil Nadu": ["Kongu Naturals", "Chola Heritage", "Madurai Craft", "Dravidian Pure"],
            "Karnataka": ["Mysuru Royal", "Karnata Naturals", "Malnad Fresh", "Hampi Heritage"],
            "Maharashtra": ["Sahyadri Naturals", "Desh Handloom", "Vidarbha Harvest", "Kokani Fresh"],
            "West Bengal": ["Bangla Handloom", "Sundarban Honey", "Shantiniketan Craft", "Rarh Harvest"],
            "Assam": ["Brahmaputra Valley", "Kaziranga Naturals", "Axom Handloom", "Assam Silk Heritage"],
            "Kerala": ["Malabar Spices", "God's Own Green", "Travancore Naturals", "Keralam Ayurvedic"],
            "Gujarat": ["Kathiawadi Pure", "Kutch Artisans", "Gir Forest Harvest", "Saurashtra Roots"],
        }
        
        self.sanskrit_stems = [
            "Vastra", "Anna", "Prakriti", "Swadeshi", "Gramin", "Nirmaan", "Srijan",
            "Kaushal", "Vriddhi", "Mangal", "Pavitra", "Amrit", "Rasayan", "Dharani",
            "Aarogyam", "Vana", "Shringaar", "Shrestha"
        ]

    # ════════════════════════════════════════════════════════════════════
    # BRAND NAME GENERATION
    # ════════════════════════════════════════════════════════════════════
    def generate_brand_names(self, shg_name: str, product_category: str,
                             state: str = "", num: int = 5) -> List[str]:
        """Generate creative, culturally aligned brand names."""
        names = set()
        cat = product_category if product_category in self.product_terms else "Retail"
        items = self.product_terms[cat]["items"]
        state_tags = self.state_cultural_tags.get(state, ["Desi", "Vedic", "Rural India", "Prakrit"])
        shg_base = shg_name.split()[0] if shg_name else "Shakti"
        clean_shg = re.sub(r'[^a-zA-Z]', '', shg_base)
        
        patterns = [
            lambda: f"{random.choice(state_tags)} {random.choice(items).split()[-1]} Co.",
            lambda: f"{random.choice(self.empowerment_words)} {random.choice(self.positive_adjectives)}",
            lambda: f"{random.choice(self.sanskrit_stems)} {random.choice(self.positive_adjectives)}",
            lambda: f"{clean_shg} {random.choice(self.empowerment_words)} Organics",
            lambda: f"Gramin {random.choice(self.sanskrit_stems)} Collective",
            lambda: f"{random.choice(self.positive_adjectives)} {random.choice(state_tags)}",
            lambda: f"{random.choice(self.empowerment_words)} {random.choice(items).split()[-1]} Works",
            lambda: f"{clean_shg} Artisan {random.choice(items).split()[-1]}s",
            lambda: f"Maa {clean_shg} Naturals",
            lambda: f"{random.choice(state_tags).split()[0]} {random.choice(self.sanskrit_stems)}",
            lambda: f"PureRoots {random.choice(self.empowerment_words)}",
            lambda: f"{random.choice(self.positive_adjectives)} {clean_shg} Creations",
            lambda: f"{random.choice(self.sanskrit_stems)} Veda",
            lambda: f"Swadeshi {clean_shg} Studio"
        ]
        
        attempts = 0
        while len(names) < num and attempts < 60:
            names.add(random.choice(patterns)())
            attempts += 1
            
        return list(names)[:num]

    # ════════════════════════════════════════════════════════════════════
    # TAGLINE GENERATION
    # ════════════════════════════════════════════════════════════════════
    def generate_taglines(self, brand_name: str, product_category: str,
                          num: int = 5) -> List[str]:
        """Generate punchy, memorable, bilingual & emotional taglines."""
        cat = product_category if product_category in self.product_terms else "Retail"
        qualities = self.product_terms[cat]["qualities"]
        items = self.product_terms[cat]["items"]
        
        pool = [
            f"Handcrafted with love, backed by Nari Shakti.",
            f"Pure. Authentic. Cultivated by rural women entrepreneurs.",
            f"From our village artisans straight to your conscious home.",
            f"Har fasal mein mehnat, har utpaad mein vishwas.",
            f"Empowering rural women, one {random.choice(items).lower()} at a time.",
            f"Rooted in ancient tradition, perfected for your modern lifestyle.",
            f"Wholesome, honest, and 100% {random.choice(qualities)}.",
            f"Made by hand. Nurtured by community. Cherished by families.",
            f"Where generational skill meets pure ethical sustainability.",
            f"Swaad aur shuddhata ka vishwas — Direct from {brand_name}.",
            f"Every purchase directly uplifts a woman artisan's family.",
            f"Pure nature. Honest craft. Unrivaled quality.",
            f"The soulful beauty of Indian craftsmanship in every detail.",
            f"Bridging rural heritage with mindful living."
        ]
        
        random.shuffle(pool)
        return pool[:num]

    # ════════════════════════════════════════════════════════════════════
    # PRODUCT DESCRIPTION GENERATION
    # ════════════════════════════════════════════════════════════════════
    def generate_product_description(self, product_name: str,
                                     product_category: str,
                                     features: Optional[List[str]] = None,
                                     num: int = 3) -> List[str]:
        """Generate high-converting, story-driven product descriptions."""
        cat = product_category if product_category in self.product_terms else "Retail"
        term = self.product_terms[cat]
        
        q1 = random.choice(term["qualities"])
        q2 = random.choice(term["qualities"])
        b1 = random.choice(term["benefits"])
        b2 = random.choice(term["benefits"])
        hook = random.choice(term["hooks"])
        cta = random.choice(self.cta_phrases)
        
        desc_1 = f"""✨ **{product_name} — Handcrafted Purity from Village Artisans**

🌿 **{hook}**
Our {product_name} represents the authentic mastery of rural women self-help collectives. Every single batch is {q1} and {q2}, meticulously prepared without synthetic adulteration or industrial shortcuts.

🌟 **Why You'll Love It:**
• **Authentic & Pure:** 100% {q1}, retaining all natural qualities.
• **Holistic Wellness:** Proven to be {b1}.
• **Zero Compromise:** Freshly prepared with traditional integrity and care.
• **Social Empowerment:** Provides dignified, sustainable livelihoods to over 15+ rural women.

💡 **The Community Impact:**
When you welcome {product_name} into your home, you aren’t simply buying a product — you are directly fueling children’s education, health security, and women-led rural financial independence.

📦 **Availability:** Small-batch artisanal harvest.
🛒 *{cta}*"""

        desc_2 = f"""🌟 **Experience the Heritage: {product_name}**

👩‍🌾 **Nurtured by Nari Shakti, Crafted for Discerning Homes**
Step into the world of genuine traditional excellence with our premium {product_name}. Sourced through ethical fair-trade practices, this product is {q1} and naturally {b2}.

🔍 **Key Highlights:**
✅ **Handmade Integrity:** {q2} by skilled women artisans.
✅ **Unmatched Freshness:** Prepared in small community-level batches.
✅ **Health & Safety:** Completely {b1} with zero chemical preservatives.
✅ **Ethical Footprint:** Eco-conscious packaging with minimal environmental waste.

💚 **Empowerment with Every Order:**
100% of the proceeds directly support the Self Help Group members and their families.

📦 *{cta}*"""

        desc_3 = f"""🌾 **{product_name} — Pure Village Tradition Delivered to Your Door**

🏡 **Generations of Wisdom in Every Pack**
Discover what real purity feels like. Our women’s collective brings you {product_name} — {q1}, wholesome, and brimming with rich authentic character. 

💎 **What Sets It Apart:**
• Handcrafted with patience, dedication, and deep generational expertise.
• Specially curated to be {b1} and {b2}.
• Strictly quality-tested and certified by community master trainers.

🤝 **Join the Movement:**
Support rural entrepreneurship and bring home honest, unadulterated goodness today.

👉 *{cta}*"""

        results = [desc_1, desc_2, desc_3]
        return results[:num]

    # ════════════════════════════════════════════════════════════════════
    # WHATSAPP PROMOTIONAL MESSAGE GENERATION
    # ════════════════════════════════════════════════════════════════════
    def generate_whatsapp_message(self, product_name: str, brand_name: str,
                                  price_range: Optional[str] = None,
                                  contact: Optional[str] = None,
                                  num: int = 3) -> List[str]:
        """Generate high-conversion WhatsApp broadcast messages."""
        price_str = f"💰 *Special Group Price:* {price_range}" if price_range else "💰 *Special Introductory Price:* Best Community Rate!"
        contact_str = f"📲 *Order/Inquire on WhatsApp:* {contact}" if contact else "📲 *Reply to this message to order instantly!*"
        
        msg_1 = f"""🌟🌟 *{brand_name} Presents: Fresh {product_name}* 🌟🌟

Namaste! 🙏 We are excited to announce our fresh, small-batch harvest of *{product_name}*, handcrafted with dedication by our Women’s Self Help Group! 👩‍🌾✨

✅ *100% Pure & Traditional*
✅ *Chemical-Free & Natural*
✅ *Handmade by Local Women Artisans*
✅ *Direct from Farm/Workshop to Home*

{price_str}
🚚 *Home Delivery & Express Dispatch Available!*
🎁 *Gift Hampers & Bulk Orders Accepted*

{contact_str}

🤝 *Every order directly empowers our village women entrepreneurs! Please share with family & friends!* 💚"""

        msg_2 = f"""🎉 *SPECIAL COMMUNITY OFFER — {brand_name}* 🎉

Looking for authentic, unadulterated *{product_name}*? Look no further! 🌿

✨ Freshly prepared with traditional recipes
✨ Zero artificial colors, flavors or harmful preservatives
✨ Loved by 500+ happy families across the region! ⭐⭐⭐⭐⭐

{price_str}
🔥 *Limited batches ready for dispatch!*

{contact_str}

💪 *Empower Women • Choose Local • Eat/Live Pure!* 🇮🇳"""

        msg_3 = f"""🌿 *Pure. Natural. Authentic.* 🌿

Dear friends, bring home the pure goodness of *{product_name}* from *{brand_name}*! 🏡✨

Why our customers keep coming back:
🔹 True artisanal taste & finish
🔹 Freshly made in hygienic community units
🔹 Honest prices straight from the makers

{price_str}
📦 *Dispatched within 24 hours of order!*

{contact_str}

🙏 *Thank you for supporting Self Help Group Women Artisans!*"""

        return [msg_1, msg_2, msg_3][:num]

    # ════════════════════════════════════════════════════════════════════
    # INSTAGRAM CAPTION GENERATION
    # ════════════════════════════════════════════════════════════════════
    def generate_instagram_caption(self, product_name: str, brand_name: str,
                                   product_category: str,
                                   num: int = 3) -> List[str]:
        """Generate aesthetic, story-driven Instagram captions."""
        cat = product_category if product_category in self.product_terms else "Retail"
        term = self.product_terms[cat]
        
        cap_1 = f"""Before sunrise, while the village is still asleep, our artisan sisters gather with a shared purpose: to create something pure, authentic, and truly impactful. 🌅✨

Introducing our handcrafted *{product_name}* from {brand_name} — where centuries-old tradition meets uncompromised quality. 

Every single piece tells a story of perseverance, financial independence, and rural pride. When you choose us, you aren't just shopping conscious — you're transforming lives. 💚

👉 Tap the link in our bio to order or send us a DM! 📩"""

        cap_2 = f"""Pure ingredients. Honest craftsmanship. Zero shortcuts. That's the {brand_name} promise. 🌿

Our {product_name} is fresh, {random.choice(term['qualities'])}, and lovingly made by the talented women of our Self Help Group collective. 

From our village courtyard straight to your conscious home. Double tap if you believe in the power of #VocalForLocal! ❤️

📦 DM us today for single & bulk festive orders!"""

        cap_3 = f"""There is something truly magical about products made by human hands with genuine love and care. 🤲💫

Meet our *{product_name}* — authentic, {random.choice(term['qualities'])}, and proudly women-made. 

Join the movement of mindful consumers who value quality over mass production. ✨

🛒 Available now! Link in bio / DM to order. 📦"""

        return [cap_1, cap_2, cap_3][:num]

    # ════════════════════════════════════════════════════════════════════
    # HASHTAG GENERATION
    # ════════════════════════════════════════════════════════════════════
    def generate_hashtags(self, product_category: str, state: str = "",
                          brand_name: Optional[str] = None,
                          num: int = 20) -> List[str]:
        """Generate curated, high-reach social media hashtags."""
        tags = set([
            "#VocalForLocal", "#MadeInIndia", "#NariShakti", "#SHGProducts",
            "#WomenEntrepreneurs", "#RuralIndia", "#SupportSmallBusiness",
            "#HandmadeInIndia", "#AtmaNirbharBharat", "#SocialImpact",
            "#EmpowerWomen", "#SustainableLiving", "#ConsciousConsumer",
            "#DesiKarigari", "#ArtisansOfIndia", "#EthicalShopping"
        ])
        
        cat_hashtags = {
            "Agriculture": ["#OrganicFarming", "#DesiHarvest", "#PesticideFree", "#PureSpices", "#FarmToTable"],
            "Dairy": ["#A2Ghee", "#DesiGhee", "#BilonaGhee", "#PureDairy", "#VedicTradition"],
            "Handicrafts": ["#IndianHandicrafts", "#ArtisanMade", "#EcoFriendlyDecor", "#TerracottaArt", "#BambooCraft"],
            "Textiles": ["#HandloomLove", "#VocalForHandloom", "#IndianTextiles", "#HandBlockPrint", "#KhadiIndia"],
            "Food Processing": ["#HomeMadePickles", "#DesiSwaad", "#TraditionalFood", "#GrandmaRecipe", "#PureFood"],
            "Beauty/Personal Care": ["#AyurvedicSkincare", "#ChemicalFreeBeauty", "#HerbalCare", "#CleanBeautyIndia"],
            "Retail": ["#DailyEssentials", "#CommunityFirst", "#FairTradeIndia"],
            "Services": ["#WomenInBusiness", "#SkilledHands", "#ArtisanServices"]
        }
        
        if product_category in cat_hashtags:
            tags.update(cat_hashtags[product_category])
            
        if state:
            clean_state = re.sub(r'[^a-zA-Z]', '', state)
            tags.add(f"#{clean_state}Artisans")
            tags.add(f"#MadeIn{clean_state}")
            tags.add(f"#{clean_state}Culture")
            
        if brand_name:
            clean_brand = re.sub(r'[^a-zA-Z0-9]', '', brand_name)
            if clean_brand:
                tags.add(f"#{clean_brand}")
                
        all_tags = list(tags)
        random.shuffle(all_tags)
        return all_tags[:num]

    # ════════════════════════════════════════════════════════════════════
    # COMPLETE BRANDING KIT
    # ════════════════════════════════════════════════════════════════════
    def generate_complete_branding_kit(self, shg_name: str, product_name: str,
                                       product_category: str, state: str,
                                       price_range: Optional[str] = None) -> Dict[str, Any]:
        """Generate a synchronized, end-to-end multi-channel branding kit."""
        brand_names = self.generate_brand_names(shg_name, product_category, state, num=5)
        primary_brand = brand_names[0] if brand_names else (shg_name or "Shakti Collective")
        
        return {
            "brand_names": brand_names,
            "taglines": self.generate_taglines(primary_brand, product_category, num=5),
            "product_descriptions": self.generate_product_description(
                product_name, product_category, num=3
            ),
            "whatsapp_messages": self.generate_whatsapp_message(
                product_name, primary_brand, price_range, num=3
            ),
            "instagram_captions": self.generate_instagram_caption(
                product_name, primary_brand, product_category, num=3
            ),
            "hashtags": self.generate_hashtags(
                product_category, state, primary_brand, num=20
            ),
        }
