# 🏘️ Intelligent SHG Performance and Digital Market Support Platform

## Using AI and Business Intelligence

An end-to-end platform combining **Business Intelligence**, **Machine Learning**, and **Generative AI** to support Self Help Groups (SHGs) across India. The platform monitors SHG performance, predicts outcomes, and generates digital marketing content.

---

## 🎯 Research Gap Addressed

Existing studies focus **separately** on SHG empowerment, digital banking, microfinance, and digitization. This project **unifies** three critical areas:

1. **SHG Performance Analytics** — Real-time BI dashboards
2. **AI Performance Prediction** — ML-based early warning system
3. **AI Branding Support** — Digital marketing content generation

---

## 🏗️ Project Architecture

```
SHG/
├── config.py                        # Centralized configuration
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── data/
│   ├── generate_shg_dataset.py      # Synthetic dataset generator (5000+ SHGs)
│   └── raw/
│       └── shg_performance_dataset.csv  # Generated dataset (64 columns)
│
├── ml/
│   ├── __init__.py
│   ├── data_preprocessing.py        # Data cleaning, encoding, scaling
│   ├── feature_engineering.py       # Advanced feature creation (19 new features)
│   ├── model_training.py            # Multi-model training pipeline
│   ├── model_evaluation.py          # Comprehensive evaluation & visualization
│   ├── saved_models/                # Trained model artifacts
│   └── evaluation_results/          # Plots, reports, metrics
│
├── ai_branding/
│   ├── __init__.py
│   └── content_generator.py         # AI branding engine (500+ templates)
│
└── app/
    ├── __init__.py
    ├── main.py                      # Streamlit app entry point
    ├── pages/
    │   ├── dashboard.py             # BI Dashboard (8 KPIs, 8 charts)
    │   ├── prediction.py            # ML Prediction interface
    │   ├── branding.py              # AI Content generation
    │   └── analytics.py             # Deep analytics & risk assessment
    └── utils/
        ├── __init__.py
        ├── helpers.py               # Utility functions
        └── styles.py                # Custom CSS styling
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Dataset

```bash
python data/generate_shg_dataset.py
```

This generates 5,000 SHG records with 64 features.

### 3. Train ML Model

```bash
python ml/model_training.py
```

This trains 8+ ML models, tunes hyperparameters, and saves the best model.

### 4. Launch Web Application

```bash
streamlit run app/main.py
```

Open your browser at `http://localhost:8501`

---

## 📊 Module 1: BI Dashboard

Interactive dashboard built with **Plotly** inside **Streamlit** (equivalent to Power BI):

- **8 KPI Cards**: Total SHGs, Members, Savings, Repayment Rate, Bank Linkage, Enterprise Rate, Attendance, Loans
- **Performance Pie Chart**: High/Medium/Low distribution
- **State Bar Chart**: SHGs by state
- **Savings Trend**: By group age
- **Scatter Plot**: Savings vs Repayment Rate
- **Heatmap**: State × Performance
- **Box Plot**: Savings distribution
- **Gauge Chart**: Overall repayment rate
- **Geographic Map**: India map visualization
- **Interactive Filters**: State, performance, bank linkage, age

---

## 🤖 Module 2: ML Performance Prediction

Predicts SHG performance as **High / Medium / Low**:

### Models Trained
| Model | Details |
|-------|---------|
| Logistic Regression | Multi-class, L-BFGS solver |
| Random Forest | 200 trees, tuned depth |
| XGBoost / Gradient Boosting | With hyperparameter tuning |
| SVM | RBF kernel, probability enabled |
| KNN | Distance-weighted, k=7 |
| Decision Tree | Pruned with min_samples |
| AdaBoost | 150 estimators |
| Extra Trees | 200 trees |
| **Ensemble** | Soft voting of top 3 |

### Feature Engineering (19 new features)
- Financial ratios: savings-to-loan, repayment efficiency, per-member metrics
- Governance scores: composite governance, digital readiness
- Interaction terms: savings × attendance, loan × repayment
- Age-based features: maturity flags, age categories

### Evaluation
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix
- Multi-class ROC Curves
- Feature Importance (top 25)
- SHAP Analysis

---

## 🎨 Module 3: AI Branding Engine

Generates marketing content for SHG products (offline, no API keys):

| Content Type | Output |
|---|---|
| Brand Names | 5 creative suggestions per request |
| Taglines | 5 catchy taglines |
| Product Descriptions | 3 detailed descriptions (150+ words) |
| WhatsApp Messages | 3 promotional messages with emojis |
| Instagram Captions | 3 story-driven captions |
| Hashtags | 20 relevant hashtags |

**Supports 8 product categories**: Agriculture, Dairy, Handicrafts, Textiles, Food Processing, Beauty/Personal Care, Retail, Services

---

## 🔬 Module 4: Deep Analytics

Advanced analytics beyond the dashboard:

- **Radar Chart**: Performance profile comparison
- **Parallel Coordinates**: Multi-metric visualization
- **Correlation Heatmap**: Financial metric correlations
- **Risk Assessment**: Risk scoring and categorization
- **Training Impact**: Before/after analysis
- **Digital Adoption**: Technology usage patterns

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Model Explainability | SHAP |
| Visualization | Plotly, Matplotlib, Seaborn |
| Web Application | Streamlit |
| AI Content | Template Engine (NLP-inspired) |

---

## 📈 Dataset Description

- **5,000 SHG records** with realistic synthetic data
- **64 features** covering:
  - Demographics (state, district, group size, age)
  - Financials (savings, loans, repayment)
  - Governance (meetings, books, audit)
  - Training (literacy, skills, enterprise)
  - Enterprise (type, income, market linkage)
  - Digital (payments, mobile banking, social media)
  - Federation (NRLM, cluster/block level)
- **Target**: Performance Category (High / Medium / Low)
- Weighted scoring algorithm based on domain expertise

---

## 📄 License

This project is for academic and research purposes.

---

## 👥 Contributors

Built as an industry-grade AI + BI project for SHG empowerment.
