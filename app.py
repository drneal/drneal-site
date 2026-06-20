"""
Dr Neal Aggarwal — AI Engineering Site
Flask application. All content lives in data/ (JSON) and content/posts/ (Markdown).
To add a post: drop a .md file in content/posts/ with YAML frontmatter.
To update the library or skills: edit data/library.json or data/skills.json.
"""

import os
import json
import re
from pathlib import Path
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import markdown
from flask import Flask, render_template, abort, request, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-neal-site-2026")

TAG_URLS = {
    "Claude API":           "https://www.anthropic.com/api",
    "OpenAI":               "https://en.wikipedia.org/wiki/OpenAI",
    "Gemini":               "https://en.wikipedia.org/wiki/Gemini_(language_model)",
    "RAG":                  "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
    "tool use":             "https://en.wikipedia.org/wiki/Prompt_engineering",
    "prompt engineering":   "https://en.wikipedia.org/wiki/Prompt_engineering",
    "Claude Code":          "https://www.anthropic.com/claude-code",
    "multi-agent":          "https://en.wikipedia.org/wiki/Multi-agent_system",
    "MCP":                  "https://modelcontextprotocol.io/introduction",
    "autonomous execution": "https://en.wikipedia.org/wiki/Autonomous_agent",
    "agent SDKs":           "https://en.wikipedia.org/wiki/Software_development_kit",
    "tool servers":         "https://modelcontextprotocol.io/docs/concepts/tools",
    "connectors":           "https://modelcontextprotocol.io/docs/concepts/resources",
    "local + remote":       "https://modelcontextprotocol.io/docs/concepts/transports",
    "PyTorch":              "https://en.wikipedia.org/wiki/PyTorch",
    "TensorFlow":           "https://en.wikipedia.org/wiki/TensorFlow",
    "transformers":         "https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)",
    "LoRA":                 "https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)",
    "PEFT":                 "https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)",
    "HuggingFace":          "https://en.wikipedia.org/wiki/Hugging_Face",
    "scikit-learn":         "https://en.wikipedia.org/wiki/Scikit-learn",
    "XGBoost":              "https://en.wikipedia.org/wiki/XGBoost",
    "statsmodels":          "https://www.statsmodels.org",
    "scipy":                "https://en.wikipedia.org/wiki/SciPy",
    "R":                    "https://en.wikipedia.org/wiki/R_(programming_language)",
    "spaCy":                "https://en.wikipedia.org/wiki/SpaCy",
    "NLTK":                 "https://en.wikipedia.org/wiki/Natural_Language_Toolkit",
    "BERT":                 "https://en.wikipedia.org/wiki/BERT_(language_model)",
    "clinical NLP":         "https://en.wikipedia.org/wiki/Natural_language_processing",
    "embeddings":           "https://en.wikipedia.org/wiki/Word_embedding",
    "vector search":        "https://en.wikipedia.org/wiki/Nearest_neighbor_search",
    "diagnostic AI":        "https://en.wikipedia.org/wiki/Artificial_intelligence_in_healthcare",
    "risk models":          "https://en.wikipedia.org/wiki/Risk_assessment",
    "FHIR":                 "https://en.wikipedia.org/wiki/Fast_Healthcare_Interoperability_Resources",
    "HL7":                  "https://en.wikipedia.org/wiki/Health_Level_7",
    "DICOM":                "https://en.wikipedia.org/wiki/DICOM",
    "pandas":               "https://en.wikipedia.org/wiki/Pandas_(software)",
    "data pipelines":       "https://en.wikipedia.org/wiki/Pipeline_(computing)",
    "anonymisation":        "https://en.wikipedia.org/wiki/Data_anonymization",
    "Arduino":              "https://en.wikipedia.org/wiki/Arduino",
    "ESP32":                "https://en.wikipedia.org/wiki/ESP32",
    "ESP-IDF":              "https://docs.espressif.com/projects/esp-idf/en/latest/",
    "Raspberry Pi":         "https://en.wikipedia.org/wiki/Raspberry_Pi",
    "LoRa":                 "https://en.wikipedia.org/wiki/LoRa",
    "I2C/SPI":              "https://en.wikipedia.org/wiki/I%C2%B2C",
    "Python":               "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "Flask":                "https://en.wikipedia.org/wiki/Flask_(web_framework)",
    "FastAPI":              "https://en.wikipedia.org/wiki/FastAPI",
    "C/C++":                "https://en.wikipedia.org/wiki/C%2B%2B",
    "LISP":                 "https://en.wikipedia.org/wiki/Lisp_(programming_language)",
    "EMACS":                "https://en.wikipedia.org/wiki/Emacs",
    "MQL5":                 "https://www.mql5.com/en/articles",
    "MetaTrader":           "https://en.wikipedia.org/wiki/MetaTrader_4",
    "quant finance":        "https://en.wikipedia.org/wiki/Quantitative_analysis_(finance)",
    "neural nets":          "https://en.wikipedia.org/wiki/Artificial_neural_network",
    "backtesting":          "https://en.wikipedia.org/wiki/Backtesting",
    "Bitcoin":              "https://en.wikipedia.org/wiki/Bitcoin",
    "Ethereum":             "https://en.wikipedia.org/wiki/Ethereum",
    "Solidity":             "https://en.wikipedia.org/wiki/Solidity",
    "Cardano":              "https://en.wikipedia.org/wiki/Cardano_(blockchain_platform)",
    "cryptography":         "https://en.wikipedia.org/wiki/Cryptography",
}

BASE = Path(__file__).parent
POSTS_DIR = BASE / "content" / "posts"
DATA_DIR = BASE / "data"


# ── helpers ──────────────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML-style frontmatter from a markdown file."""
    meta: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm_block = text[3:end].strip()
            body = text[end + 4:].strip()
            for line in fm_block.splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, body


def load_posts(limit: int = None) -> list[dict]:
    posts = []
    for path in sorted(POSTS_DIR.glob("*.md"), reverse=True):
        raw = path.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)
        # Generate excerpt — first non-empty paragraph
        excerpt_src = re.split(r'\n\n', body.strip(), maxsplit=3)
        excerpt = ""
        for chunk in excerpt_src:
            stripped = chunk.strip().lstrip("#").strip()
            if stripped and not stripped.startswith("!["):
                excerpt = stripped[:300]
                if len(stripped) > 300:
                    excerpt += "…"
                break
        posts.append({
            "slug": path.stem,
            "title": meta.get("title", path.stem.replace("-", " ").title()),
            "date": meta.get("date", ""),
            "category": meta.get("category", "AI"),
            "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
            "level": meta.get("level", ""),
            "read_time": meta.get("read_time", ""),
            "summary": meta.get("summary", excerpt),
            "featured": meta.get("featured", "false").lower() == "true",
        })
    if limit:
        return posts[:limit]
    return posts


def load_post(slug: str) -> dict | None:
    path = POSTS_DIR / f"{slug}.md"
    if not path.exists():
        return None
    raw = path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    html = markdown.markdown(
        body,
        extensions=["fenced_code", "tables", "toc", "nl2br", "attr_list"],
    )
    return {
        "slug": slug,
        "title": meta.get("title", slug.replace("-", " ").title()),
        "date": meta.get("date", ""),
        "category": meta.get("category", "AI"),
        "tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
        "level": meta.get("level", ""),
        "read_time": meta.get("read_time", ""),
        "summary": meta.get("summary", ""),
        "content": html,
    }


def load_json(filename: str) -> dict | list:
    path = DATA_DIR / filename
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


# ── routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    posts = load_posts()
    featured = [p for p in posts if p["featured"]][:1]
    recent = [p for p in posts if not p["featured"]][:8]
    return render_template("index.html", posts=posts, featured=featured, recent=recent)


@app.route("/post/<slug>")
def post(slug):
    p = load_post(slug)
    if not p:
        abort(404)
    all_posts = load_posts()
    idx = next((i for i, x in enumerate(all_posts) if x["slug"] == slug), None)
    prev_post = all_posts[idx + 1] if idx is not None and idx + 1 < len(all_posts) else None
    next_post = all_posts[idx - 1] if idx is not None and idx > 0 else None
    return render_template("post.html", post=p, prev_post=prev_post, next_post=next_post)


@app.route("/skills")
def skills():
    data = load_json("skills.json")
    return render_template("skills.html", skills=data, tag_urls=TAG_URLS)


@app.route("/library")
def library():
    data = load_json("library.json")
    category = request.args.get("cat", "all")
    author = request.args.get("author", "all")
    items = data.get("items", [])
    if category != "all":
        items = [i for i in items if i.get("type") == category]
    if author != "all":
        items = [i for i in items if author.lower() in i.get("author", "").lower()]
    authors = sorted(set(i.get("author", "") for i in data.get("items", [])))
    return render_template("library.html", items=items, authors=authors,
                           current_cat=category, current_author=author)


@app.route("/demos")
def demos():
    data = load_json("demos.json")
    return render_template("demos.html", demos=data.get("demos", []))


# ── Backtester ────────────────────────────────────────────────────────────────

def _run_backtest(config: dict) -> dict:
    """Pure-Python ML backtesting engine. No external data required."""
    import numpy as np
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    from sklearn.preprocessing import StandardScaler

    seed       = int(config.get("seed", 42))
    n_days     = int(config.get("n_days", 500))
    capital0   = float(config.get("capital", 10000))
    model_type = config.get("model", "logistic")
    features   = config.get("features", ["sma", "rsi", "momentum"])
    train_pct  = float(config.get("train_pct", 0.7))

    # ── Synthetic OHLCV (geometric random walk with slight upward drift) ──
    rng = np.random.default_rng(seed)
    daily_ret = rng.normal(0.0005, 0.015, n_days)
    closes = pd.Series(100.0 * np.cumprod(1 + daily_ret))

    # ── Features ──────────────────────────────────────────────────────────
    feat: dict = {}

    if "sma" in features:
        feat["sma_ratio"] = closes.rolling(10).mean() / closes.rolling(30).mean() - 1

    if "ema" in features:
        feat["ema_ratio"] = closes.ewm(span=12).mean() / closes.ewm(span=26).mean() - 1

    if "rsi" in features:
        delta = closes.diff()
        gain  = delta.clip(lower=0).rolling(14).mean()
        loss  = (-delta).clip(lower=0).rolling(14).mean()
        feat["rsi"] = 100 - 100 / (1 + gain / (loss + 1e-9))

    if "momentum" in features:
        feat["mom_5"]  = closes.pct_change(5)
        feat["mom_20"] = closes.pct_change(20)

    if "volatility" in features:
        r = closes.pct_change()
        feat["vol_10"]   = r.rolling(10).std()
        feat["vol_ratio"]= r.rolling(10).std() / (r.rolling(30).std() + 1e-9)

    if "macd" in features:
        ema12  = closes.ewm(span=12).mean()
        ema26  = closes.ewm(span=26).mean()
        macd   = ema12 - ema26
        sig9   = macd.ewm(span=9).mean()
        feat["macd_hist"] = (macd - sig9) / (closes + 1e-9)

    X_all = pd.DataFrame(feat)
    y_all = (closes.shift(-1) > closes).astype(int)

    combined = X_all.copy()
    combined["target"] = y_all
    combined["price"]  = closes
    combined.dropna(inplace=True)

    feat_cols   = list(feat.keys())
    X_mat       = combined[feat_cols].values
    y_vec       = combined["target"].values
    prices_vec  = combined["price"].values

    split = int(train_pct * len(X_mat))
    X_tr, X_te = X_mat[:split], X_mat[split:]
    y_tr, y_te = y_vec[:split], y_vec[split:]
    p_te        = prices_vec[split:]

    scaler   = StandardScaler()
    X_tr_sc  = scaler.fit_transform(X_tr)
    X_te_sc  = scaler.transform(X_te)

    # ── Model ─────────────────────────────────────────────────────────────
    if model_type == "rf":
        model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=seed)
    elif model_type == "gb":
        model = GradientBoostingClassifier(n_estimators=100, max_depth=3, random_state=seed)
    else:
        model = LogisticRegression(max_iter=1000)

    model.fit(X_tr_sc, y_tr)
    signals  = model.predict(X_te_sc)
    accuracy = float((signals == y_te).mean())

    # ── Backtest (long-only, fully invested when signal=1) ────────────────
    capital   = capital0
    position  = 0.0
    entry_px  = 0.0
    equity    = [capital]
    bnh       = [capital]
    trades    = []
    bnh_shares = capital / p_te[0]

    for i in range(len(p_te) - 1):
        px  = p_te[i]
        sig = signals[i]

        if sig == 1 and position == 0.0:
            position = capital / px
            entry_px = px
            capital  = 0.0
        elif sig == 0 and position > 0.0:
            capital = position * px
            trades.append((px - entry_px) / entry_px)
            position = 0.0

        mtm = capital if position == 0.0 else position * p_te[i + 1]
        equity.append(mtm)
        bnh.append(bnh_shares * p_te[i + 1])

    if position > 0.0:
        trades.append((p_te[-1] - entry_px) / entry_px)

    eq  = np.array(equity, dtype=float)
    bnh = np.array(bnh,    dtype=float)

    # ── Metrics ───────────────────────────────────────────────────────────
    ret_arr  = np.diff(eq) / (eq[:-1] + 1e-9)
    sharpe   = float(np.sqrt(252) * ret_arr.mean() / (ret_arr.std() + 1e-9))
    tot_ret  = float((eq[-1]  - eq[0])  / eq[0])
    bnh_ret  = float((bnh[-1] - bnh[0]) / bnh[0])
    run_max  = np.maximum.accumulate(eq)
    dd       = (eq - run_max) / (run_max + 1e-9)
    max_dd   = float(dd.min())
    n_tr     = len(trades)
    win_rate = float(sum(1 for p in trades if p > 0) / max(n_tr, 1))

    dates = pd.bdate_range(end="2026-06-19", periods=len(eq)).strftime("%Y-%m-%d").tolist()

    return {
        "equity":   [round(v, 2) for v in eq.tolist()],
        "bnh":      [round(v, 2) for v in bnh.tolist()],
        "drawdown": [round(v * 100, 3) for v in dd.tolist()],
        "dates":    dates,
        "metrics": {
            "total_return": round(tot_ret * 100, 2),
            "bnh_return":   round(bnh_ret * 100, 2),
            "sharpe":       round(sharpe, 3),
            "max_drawdown": round(max_dd * 100, 2),
            "win_rate":     round(win_rate * 100, 1),
            "n_trades":     n_tr,
            "accuracy":     round(accuracy * 100, 1),
        },
    }


@app.route("/backtester")
def backtester():
    return render_template("backtester.html")


@app.route("/backtester/run", methods=["POST"])
def backtester_run():
    try:
        config = request.get_json(force=True) or {}
        result = _run_backtest(config)
        return jsonify({"ok": True, **result})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


# ── Clinical Text NLP Extractor ───────────────────────────────────────────────

_NLP_MEDICATIONS = [
    # Cardiovascular
    "metoprolol","bisoprolol","atenolol","carvedilol","nebivolol",
    "lisinopril","ramipril","enalapril","perindopril","captopril","trandolapril",
    "amlodipine","nifedipine","diltiazem","verapamil","felodipine",
    "atorvastatin","simvastatin","rosuvastatin","pravastatin","fluvastatin",
    "warfarin","apixaban","rivaroxaban","dabigatran","edoxaban",
    "aspirin","clopidogrel","ticagrelor","prasugrel","dipyridamole",
    "furosemide","spironolactone","bumetanide","torasemide","eplerenone",
    "digoxin","amiodarone","flecainide","sotalol","dronedarone",
    "nitroglycerine","isosorbide","hydralazine","doxazosin","prazosin",
    "sacubitril","valsartan","ivabradine","empagliflozin","dapagliflozin",
    # Antibiotics
    "amoxicillin","ampicillin","co-amoxiclav","flucloxacillin",
    "penicillin","piperacillin","tazobactam","piperacillin-tazobactam",
    "ciprofloxacin","levofloxacin","moxifloxacin","ofloxacin",
    "metronidazole","tinidazole",
    "doxycycline","tetracycline","minocycline",
    "azithromycin","clarithromycin","erythromycin",
    "trimethoprim","nitrofurantoin","fosfomycin","co-trimoxazole",
    "ceftriaxone","cefuroxime","cephalexin","cefazolin","ceftazidime",
    "vancomycin","teicoplanin","linezolid","daptomycin","tigecycline",
    "meropenem","ertapenem","imipenem","doripenem",
    "gentamicin","amikacin","tobramycin",
    # Analgesics / Anti-inflammatory
    "paracetamol","acetaminophen",
    "ibuprofen","naproxen","diclofenac","celecoxib","meloxicam","indomethacin","etoricoxib",
    "morphine","oxycodone","hydromorphone","fentanyl","alfentanil","remifentanil",
    "codeine","dihydrocodeine","tramadol","buprenorphine","tapentadol",
    "prednisolone","dexamethasone","hydrocortisone","methylprednisolone","betamethasone",
    # Psychiatric / Neurological
    "sertraline","fluoxetine","paroxetine","citalopram","escitalopram","fluvoxamine",
    "venlafaxine","duloxetine","desvenlafaxine","mirtazapine","trazodone","agomelatine",
    "amitriptyline","nortriptyline","clomipramine","imipramine","dosulepin",
    "diazepam","lorazepam","clonazepam","alprazolam","temazepam","nitrazepam","oxazepam",
    "quetiapine","olanzapine","risperidone","aripiprazole","haloperidol","clozapine","amisulpride",
    "lithium","valproate","lamotrigine","carbamazepine","levetiracetam","phenytoin","topiramate",
    "donepezil","rivastigmine","galantamine","memantine",
    "levodopa","pramipexole","ropinirole","rasagiline","selegiline","entacapone",
    "sumatriptan","rizatriptan","zolmitriptan","propranolol",
    "pregabalin","gabapentin",
    "melatonin","zopiclone","zolpidem",
    # Respiratory
    "salbutamol","terbutaline","salmeterol","formoterol","indacaterol","olodaterol",
    "ipratropium","tiotropium","umeclidinium","glycopyrronium","aclidinium",
    "beclometasone","fluticasone","budesonide","ciclesonide","mometasone",
    "montelukast","zafirlukast","theophylline","aminophylline",
    "acetylcysteine","carbocisteine","dornase alfa",
    "roflumilast","nintedanib","pirfenidone",
    # Diabetes
    "metformin","gliclazide","glibenclamide","glimepiride","glipizide",
    "sitagliptin","saxagliptin","linagliptin","alogliptin","vildagliptin",
    "canagliflozin","ertugliflozin",
    "liraglutide","semaglutide","exenatide","dulaglutide","lixisenatide",
    "insulin","glargine","detemir","degludec","aspart","lispro","glulisine","isophane",
    "pioglitazone","acarbose","repaglinide",
    # Gastrointestinal
    "omeprazole","lansoprazole","pantoprazole","esomeprazole","rabeprazole",
    "ranitidine","famotidine","cimetidine",
    "ondansetron","metoclopramide","domperidone","prochlorperazine","cyclizine","granisetron",
    "loperamide","codeine phosphate",
    "lactulose","movicol","senna","bisacodyl","docusate","macrogol",
    "mesalazine","sulfasalazine","infliximab","adalimumab","vedolizumab","ustekinumab",
    "cholestyramine","colesevelam",
    # Thyroid / Endocrine
    "levothyroxine","liothyronine","carbimazole","propylthiouracil",
    "alendronate","risedronate","denosumab","strontium","teriparatide",
    "anastrozole","letrozole","exemestane","tamoxifen","fulvestrant",
    "testosterone","estradiol","progesterone","norethisterone","etonogestrel",
    "finasteride","dutasteride",
    # Renal / Rheumatology
    "allopurinol","febuxostat","colchicine","benzbromarone",
    "hydroxychloroquine","methotrexate","azathioprine","mycophenolate","leflunomide",
    "ciclosporin","tacrolimus","sirolimus",
    "rituximab","tocilizumab","etanercept","abatacept","certolizumab","golimumab",
    "belimumab","secukinumab","ixekizumab","baricitinib","tofacitinib",
    # Anticoagulation / Haematology
    "heparin","enoxaparin","dalteparin","fondaparinux","tinzaparin",
    "erythropoietin","epoetin","darbepoetin",
    "ferrous sulphate","ferrous fumarate","iron sucrose","ferric carboxymaltose",
    "folic acid","hydroxocobalamin","cyanocobalamin",
    "filgrastim","lenograstim","pegfilgrastim",
    # Miscellaneous
    "calcium carbonate","calcium acetate","sevelamer","lanthanum",
    "vitamin d","cholecalciferol","alfacalcidol","calcitriol",
    "bisoprolol","carvedilol",
    "sildenafil","tadalafil","vardenafil",
]

_NLP_DIAGNOSES = [
    # Cardiovascular
    "hypertension","essential hypertension","secondary hypertension","resistant hypertension",
    "heart failure","congestive heart failure","cardiac failure","systolic heart failure",
    "diastolic heart failure","heart failure with reduced ejection fraction",
    "atrial fibrillation","atrial flutter","supraventricular tachycardia","ventricular tachycardia",
    "ventricular fibrillation","complete heart block","sick sinus syndrome",
    "myocardial infarction","ST elevation myocardial infarction","STEMI","NSTEMI",
    "angina","stable angina","unstable angina","Prinzmetal angina",
    "acute coronary syndrome","ACS",
    "stroke","ischaemic stroke","haemorrhagic stroke","subarachnoid haemorrhage",
    "transient ischaemic attack","TIA",
    "deep vein thrombosis","DVT","pulmonary embolism","PE",
    "peripheral vascular disease","peripheral arterial disease",
    "aortic stenosis","mitral regurgitation","aortic regurgitation","mitral stenosis",
    "cardiomyopathy","dilated cardiomyopathy","hypertrophic cardiomyopathy","restrictive cardiomyopathy",
    "pericarditis","endocarditis","myocarditis","cardiac tamponade",
    # Respiratory
    "asthma","brittle asthma","exercise-induced asthma",
    "chronic obstructive pulmonary disease","COPD","emphysema","chronic bronchitis",
    "pneumonia","community-acquired pneumonia","hospital-acquired pneumonia","aspiration pneumonia",
    "pulmonary fibrosis","idiopathic pulmonary fibrosis","IPF",
    "pleural effusion","pneumothorax","haemothorax","haemopneumothorax",
    "pulmonary oedema","cardiogenic pulmonary oedema","acute respiratory distress syndrome","ARDS",
    "pulmonary hypertension","cor pulmonale",
    "sleep apnoea","obstructive sleep apnoea","OSA",
    "bronchiectasis","cystic fibrosis",
    "COVID-19","SARS-CoV-2","influenza",
    "sarcoidosis","hypersensitivity pneumonitis","mesothelioma",
    # Metabolic / Endocrine
    "type 2 diabetes","type 1 diabetes","diabetes mellitus","gestational diabetes",
    "hypothyroidism","hyperthyroidism","thyrotoxicosis","thyroid storm",
    "Grave's disease","Hashimoto's thyroiditis","autoimmune thyroiditis",
    "hypercholesterolaemia","dyslipidaemia","hyperlipidaemia","hypertriglyceridaemia",
    "obesity","morbid obesity","metabolic syndrome",
    "Cushing's syndrome","Addison's disease","primary adrenal insufficiency",
    "hyperparathyroidism","hypoparathyroidism",
    "hypokalaemia","hyperkalaemia","hyponatraemia","hypernatraemia",
    "hypomagnesaemia","hypocalcaemia","hypercalcaemia",
    "acromegaly","hypopituitarism","diabetes insipidus","SIADH",
    # Renal
    "chronic kidney disease","CKD","acute kidney injury","AKI","acute tubular necrosis",
    "nephrotic syndrome","nephritic syndrome","proteinuria",
    "glomerulonephritis","IgA nephropathy","membranous nephropathy",
    "polycystic kidney disease","renal artery stenosis","renal cell carcinoma",
    "urinary tract infection","UTI","cystitis","pyelonephritis","prostatitis",
    # Gastrointestinal
    "peptic ulcer disease","gastric ulcer","duodenal ulcer","H pylori",
    "Crohn's disease","ulcerative colitis","inflammatory bowel disease","IBD",
    "irritable bowel syndrome","IBS",
    "gastro-oesophageal reflux","GORD","GERD","Barrett's oesophagus","oesophagitis",
    "cirrhosis","alcoholic liver disease","non-alcoholic fatty liver disease","NAFLD","NASH",
    "pancreatitis","acute pancreatitis","chronic pancreatitis",
    "cholecystitis","cholelithiasis","gallstones","cholangitis","primary sclerosing cholangitis",
    "diverticulitis","diverticular disease","diverticulosis",
    "appendicitis","bowel obstruction","volvulus","intussusception",
    "coeliac disease","malabsorption","short bowel syndrome",
    "hepatitis","hepatitis B","hepatitis C","autoimmune hepatitis",
    # Musculoskeletal
    "rheumatoid arthritis","osteoarthritis","psoriatic arthritis","reactive arthritis",
    "gout","pseudogout","calcium pyrophosphate deposition",
    "osteoporosis","osteopenia","osteomalacia","Paget's disease",
    "systemic lupus erythematosus","SLE","lupus nephritis",
    "ankylosing spondylitis","fibromyalgia","polymyalgia rheumatica",
    "Sjogren's syndrome","systemic sclerosis","scleroderma",
    "polymyositis","dermatomyositis",
    # Neurological
    "epilepsy","seizure disorder","generalised epilepsy","focal epilepsy","status epilepticus",
    "Parkinson's disease","Parkinsonism","Lewy body dementia",
    "Alzheimer's disease","dementia","vascular dementia","frontotemporal dementia",
    "multiple sclerosis","MS","relapsing remitting MS","primary progressive MS",
    "migraine","cluster headache","tension headache","trigeminal neuralgia",
    "peripheral neuropathy","diabetic neuropathy","Charcot-Marie-Tooth",
    "Guillain-Barré syndrome","myasthenia gravis","motor neurone disease","ALS",
    "Bell's palsy","carpal tunnel syndrome","sciatica","spinal stenosis",
    "meningitis","encephalitis","brain abscess","subdural haematoma","extradural haematoma",
    "normal pressure hydrocephalus","Huntington's disease","cerebellar ataxia",
    # Psychiatric
    "depression","major depressive disorder","treatment-resistant depression",
    "bipolar disorder","bipolar affective disorder","mania","hypomania",
    "anxiety","generalised anxiety disorder","GAD","panic disorder","social anxiety disorder",
    "schizophrenia","schizoaffective disorder","psychosis","first episode psychosis",
    "PTSD","post-traumatic stress disorder",
    "obsessive-compulsive disorder","OCD","body dysmorphic disorder",
    "eating disorder","anorexia nervosa","bulimia nervosa","ARFID",
    "ADHD","attention deficit hyperactivity disorder","autism spectrum disorder",
    "alcohol use disorder","substance misuse","opiate dependence",
    # Infections
    "sepsis","septic shock","bacteraemia","SIRS",
    "cellulitis","erysipelas","necrotising fasciitis","abscess",
    "tuberculosis","TB","latent TB","multi-drug resistant TB",
    "HIV","AIDS","opportunistic infection",
    "Lyme disease","brucellosis","malaria","typhoid",
    "COVID-19","SARS-CoV-2","influenza","RSV",
    "hepatitis B","hepatitis C",
    "infective endocarditis",
    # Cancer / Haematology
    "breast cancer","lung cancer","colorectal cancer","colon cancer","rectal cancer",
    "prostate cancer","ovarian cancer","cervical cancer","endometrial cancer",
    "lymphoma","Hodgkin lymphoma","non-Hodgkin lymphoma","diffuse large B-cell lymphoma",
    "leukaemia","chronic lymphocytic leukaemia","CLL","acute myeloid leukaemia","AML",
    "acute lymphoblastic leukaemia","ALL","chronic myeloid leukaemia","CML",
    "multiple myeloma","myelodysplastic syndrome","MDS",
    "melanoma","basal cell carcinoma","squamous cell carcinoma",
    "hepatocellular carcinoma","cholangiocarcinoma","pancreatic cancer",
    "bladder cancer","kidney cancer","thyroid cancer","gastric cancer",
    "brain tumour","glioblastoma","glioma","meningioma",
    "anaemia","iron deficiency anaemia","pernicious anaemia","aplastic anaemia",
    "thrombocytopenia","thrombophilia","antiphospholipid syndrome",
    # Other
    "chronic fatigue syndrome","fibromyalgia","sarcoidosis",
    "psoriasis","eczema","dermatitis","urticaria","angioedema",
    "glaucoma","macular degeneration","diabetic retinopathy","cataracts",
    "hypothyroidism","hyperthyroidism",
]


def _run_nlp_extractor(text: str) -> dict:
    """Rule-based clinical NLP entity extractor using regex + curated medical vocabulary."""
    entities: list[dict] = []
    seen_spans: list[tuple] = []

    def no_overlap(s: int, e: int) -> bool:
        return all(e <= a or s >= b for a, b in seen_spans)

    # ── DATES ──────────────────────────────────────────────────────────────
    date_patterns = [
        r'\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b',
        r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{4}\b',
        r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?,?\s+\d{4}\b',
        r'\b\d{4}[-\/]\d{2}[-\/]\d{2}\b',
        r'\btoday\b|\byesterday\b|\btomorrow\b',
        r'\b(?:last|this|next)\s+(?:week|month|year|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',
        r'\b\d+\s+(?:days?|weeks?|months?|years?)\s+ago\b',
        r'\b(?:in|since|from)\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
    ]
    for pat in date_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if no_overlap(m.start(), m.end()):
                entities.append({"type": "DATE", "text": m.group(), "start": m.start(), "end": m.end(), "confidence": 0.95})
                seen_spans.append((m.start(), m.end()))

    # ── DOSAGES ────────────────────────────────────────────────────────────
    dosage_patterns = [
        r'\b\d+(?:\.\d+)?\s*(?:mg|mcg|µg|micrograms?|g|ml|mL|L|mmol|units?|IU|mEq|mg\/kg|mcg\/kg|mg\/mL|µg\/kg)\b',
        r'\b\d+\s*(?:micrograms?|milligrams?|grams?)\b',
        r'\b(?:once|twice|three\s+times|four\s+times)\s+(?:daily|a\s+day|per\s+day)\b',
        r'\b(?:BD|TDS|QDS|OD|PRN|QID|TID|BID|OM|ON|stat|STAT|nocte)\b',
        r'\b\d+\s+(?:tablet|capsule|puff|drop|patch|vial|ampoule|sachet)s?\b',
        r'\b(?:loading dose|maintenance dose|starting dose|initial dose)\b',
        r'\b\d+(?:\.\d+)?%\s+(?:solution|cream|ointment|gel|drops?|lotion|infusion)\b',
    ]
    for pat in dosage_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if no_overlap(m.start(), m.end()):
                entities.append({"type": "DOSAGE", "text": m.group(), "start": m.start(), "end": m.end(), "confidence": 0.92})
                seen_spans.append((m.start(), m.end()))

    # ── VITAL SIGNS ────────────────────────────────────────────────────────
    vital_patterns = [
        r'\bBP\s*:?\s*\d{2,3}\s*\/\s*\d{2,3}\b',
        r'\b(?:blood\s+pressure)\s*:?\s*\d{2,3}\s*\/\s*\d{2,3}\b',
        r'\b(?:HR|heart\s+rate|pulse\s+rate|pulse)\s*:?\s*\d{2,3}\s*(?:bpm|\/min)?\b',
        r'\bSpO2\s*:?\s*\d{2,3}\s*%?\b',
        r'\b(?:O2\s+sat(?:uration)?|oxygen\s+saturation)\s*:?\s*\d{2,3}\s*%?\b',
        r'\b(?:temp(?:erature)?)\s*:?\s*\d{2}(?:\.\d)?\s*°?\s*[CF]?\b',
        r'\b(?:RR|respiratory\s+rate)\s*:?\s*\d{1,2}\b',
        r'\bGCS\s*:?\s*\d{1,2}(?:\/15)?\b',
        r'\bBMI\s*:?\s*\d{2}(?:\.\d+)?\b',
        r'\b(?:weight|Wt)\s*:?\s*\d+(?:\.\d+)?\s*kg\b',
        r'\b(?:height|Ht)\s*:?\s*\d+(?:\.\d+)?\s*(?:cm|m)\b',
    ]
    for pat in vital_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if no_overlap(m.start(), m.end()):
                entities.append({"type": "VITAL_SIGN", "text": m.group(), "start": m.start(), "end": m.end(), "confidence": 0.96})
                seen_spans.append((m.start(), m.end()))

    # ── LAB VALUES ─────────────────────────────────────────────────────────
    lab_patterns = [
        r'\b(?:HbA1c|haemoglobin\s+A1c)\s*:?\s*\d+(?:\.\d+)?\s*%?\b',
        r'\b(?:Hb|haemoglobin)\s*:?\s*\d+(?:\.\d+)?\s*(?:g\/dL|g\/L)?\b',
        r'\b(?:Na|sodium)\s*:?\s*\d{2,3}\s*(?:mmol\/L)?\b',
        r'\b(?:K|potassium)\s*:?\s*\d(?:\.\d)?\s*(?:mmol\/L)?\b',
        r'\b(?:Cr|creatinine)\s*:?\s*\d+(?:\.\d+)?\s*(?:µmol\/L|umol\/L|mg\/dL)?\b',
        r'\b(?:eGFR|GFR)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:WBC|white\s+(?:blood\s+)?cell\s+count)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:Hct|haematocrit)\s*:?\s*\d+(?:\.\d+)?%?\b',
        r'\b(?:PLT|platelets?)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:ALT|AST|ALP|GGT|bilirubin)\s*:?\s*\d+(?:\.\d+)?\s*(?:U\/L|IU\/L|µmol\/L)?\b',
        r'\b(?:TSH|free\s+T4|T3)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:CRP|ESR|procalcitonin)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:troponin|BNP|NT-proBNP)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:INR|APTT|PT)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:cholesterol|LDL|HDL|triglycerides?)\s*:?\s*\d+(?:\.\d+)?\s*(?:mmol\/L)?\b',
        r'\b(?:glucose|blood\s+glucose|fasting\s+glucose)\s*:?\s*\d+(?:\.\d+)?\s*(?:mmol\/L|mg\/dL)?\b',
        r'\b(?:urea|BUN|uric\s+acid)\s*:?\s*\d+(?:\.\d+)?\b',
        r'\b(?:albumin|total\s+protein)\s*:?\s*\d+(?:\.\d+)?\s*(?:g\/L|g\/dL)?\b',
        r'\b(?:calcium|phosphate|magnesium)\s*:?\s*\d+(?:\.\d+)?\s*(?:mmol\/L)?\b',
        r'\b(?:ferritin|iron|TIBC|transferrin\s+saturation)\s*:?\s*\d+(?:\.\d+)?\b',
    ]
    for pat in lab_patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            if no_overlap(m.start(), m.end()):
                entities.append({"type": "LAB_VALUE", "text": m.group(), "start": m.start(), "end": m.end(), "confidence": 0.94})
                seen_spans.append((m.start(), m.end()))

    # ── MEDICATIONS ────────────────────────────────────────────────────────
    for med in sorted(_NLP_MEDICATIONS, key=len, reverse=True):
        pat = r'\b' + re.escape(med) + r'\b'
        for m in re.finditer(pat, text, re.IGNORECASE):
            if no_overlap(m.start(), m.end()):
                entities.append({"type": "MEDICATION", "text": m.group(), "start": m.start(), "end": m.end(), "confidence": 0.90})
                seen_spans.append((m.start(), m.end()))

    # ── DIAGNOSES ──────────────────────────────────────────────────────────
    for diag in sorted(_NLP_DIAGNOSES, key=len, reverse=True):
        pat = r'\b' + re.escape(diag) + r'\b'
        for m in re.finditer(pat, text, re.IGNORECASE):
            if no_overlap(m.start(), m.end()):
                entities.append({"type": "DIAGNOSIS", "text": m.group(), "start": m.start(), "end": m.end(), "confidence": 0.88})
                seen_spans.append((m.start(), m.end()))

    entities.sort(key=lambda x: x["start"])

    counts: dict[str, int] = {}
    for e in entities:
        counts[e["type"]] = counts.get(e["type"], 0) + 1

    return {"entities": entities, "counts": counts, "total": len(entities)}


# ── Voice Clinical Notes ──────────────────────────────────────────────────────

def _format_clinical_note(transcript: str) -> str:
    """Format a voice transcript into a structured clinical note using NLP entity extraction."""
    from datetime import datetime

    # Strip filler words common in dictation
    fillers = r'\b(um|uh|er|ah|hmm|so|like|you know|sort of|kind of|basically|right|okay so|and so)\b'
    text = re.sub(fillers, '', transcript, flags=re.IGNORECASE)
    text = re.sub(r'\s{2,}', ' ', text).strip()

    # Split into sentences (handle lack of punctuation in speech-to-text)
    # Split on ". " or "? " or "! " or common verbal full-stops like ", so " / ", and "
    raw_sents = re.split(r'(?<=[.!?])\s+|(?<=\n)', text)
    sentences = [s.strip() for s in raw_sents if len(s.strip()) > 3]

    # Extract entities from full text
    nlp = _run_nlp_extractor(text)
    def ents(t): return list(dict.fromkeys(e['text'] for e in nlp['entities'] if e['type'] == t))
    meds   = ents('MEDICATION')
    diags  = ents('DIAGNOSIS')
    vitals = ents('VITAL_SIGN')
    labs   = ents('LAB_VALUE')
    doses  = ents('DOSAGE')

    # Keyword patterns for section classification (use alternation groups, not char classes)
    PC = re.compile(r'\b(presenting|presented|presents|complaining|complaint|came in|brought in|attending|attended|referr(?:ed|al)?|admitted|c/o|chief complaint)\b', re.I)
    HX = re.compile(r'\b(background|history of|known|past medical|pmh|previous|chronic|suffered|diagnosed with|has a history|long.?standing)\b', re.I)
    EX = re.compile(r'\b(examin(?:ation|ed|es)?|on exam(?:ination)?|inspection|auscultation|palpation|found on|on observation|looks|appears|clinically)\b', re.I)
    IX = re.compile(r'\b(bloods?(?:\s+(?:test|show|result))|blood\s+test|ecg|x.?ray|ct\s+scan|mri|ultrasound|imaging|scan(?:ned)?|result(?:s)?|showed|pending|investig(?:ations?|ated)|fbc|u&e|lft|tfts?|troponin|cultures?)\b', re.I)
    AS = re.compile(r'\b(impression|assessment|working\s+diagnosis|likely|probable|suspect|rule\s+out|differential|my\s+(?:working\s+)?impression|diagnosis is|consistent with)\b', re.I)
    PL = re.compile(r'\b(plan(?:ning)?(?:\s+for)?|for\s+(?:serial|urgent|routine|review)|refer(?:ral)?|discharge|prescrib(?:e|ing)|start(?:ing)?|stop(?:ping)?|continue|follow.?up|review|arrange|request|monitor|titrat(?:e|ing)?|commence)\b', re.I)

    # Classify sentences into sections
    sections: dict[str, list[str]] = {
        'PRESENTING COMPLAINT': [],
        'HISTORY':              [],
        'EXAMINATION':          [],
        'INVESTIGATIONS':       [],
        'ASSESSMENT':           [],
        'PLAN':                 [],
        'OTHER':                [],
    }

    vital_lower = [v.lower() for v in vitals]
    lab_lower   = [l.lower() for l in labs]

    for sent in sentences:
        sl = sent.lower()
        has_vital = any(v in sl for v in vital_lower)
        has_lab   = any(l in sl for l in lab_lower)

        if AS.search(sent):
            sections['ASSESSMENT'].append(sent)
        elif PL.search(sent) and not EX.search(sent):
            sections['PLAN'].append(sent)
        elif IX.search(sent) or has_lab:
            sections['INVESTIGATIONS'].append(sent)
        elif EX.search(sent) or has_vital:
            sections['EXAMINATION'].append(sent)
        elif PC.search(sent):
            sections['PRESENTING COMPLAINT'].append(sent)
        elif HX.search(sent):
            sections['HISTORY'].append(sent)
        else:
            # Fallback: first unclassified sentence → PC; rest → History
            if not sections['PRESENTING COMPLAINT']:
                sections['PRESENTING COMPLAINT'].append(sent)
            else:
                sections['OTHER'].append(sent)

    # Promote orphaned vital-containing sentences in OTHER to EXAMINATION
    for s in list(sections['OTHER']):
        if any(v in s.lower() for v in vital_lower) or any(l in s.lower() for l in lab_lower):
            sections['INVESTIGATIONS' if any(l in s.lower() for l in lab_lower) else 'EXAMINATION'].append(s)
            sections['OTHER'].remove(s)

    # Build formatted output
    now = datetime.now()
    lines = [
        "CLINICAL NOTE",
        f"Date: {now.strftime('%-d %B %Y')}",
        f"Time: {now.strftime('%H:%M')}",
        "",
    ]

    section_order = ['PRESENTING COMPLAINT', 'HISTORY', 'EXAMINATION', 'INVESTIGATIONS', 'ASSESSMENT', 'PLAN']
    for section in section_order:
        sents = sections[section]
        if sents:
            lines.append(f"{section}:")
            for s in sents:
                # Capitalise first letter
                lines.append(f"  {s[0].upper() + s[1:] if s else ''}")
            lines.append("")

    if sections['OTHER']:
        lines.append("ADDITIONAL NOTES:")
        for s in sections['OTHER']:
            lines.append(f"  {s}")
        lines.append("")

    # Structured medication list (deduplicated, from NLP)
    if meds:
        lines.append("MEDICATIONS MENTIONED:")
        for m in meds:
            # Try to find associated dose immediately after the med name in text
            idx = text.lower().find(m.lower())
            dose_context = ""
            if idx >= 0:
                after = text[idx + len(m):idx + len(m) + 30]
                dose_m = re.search(r'\s*(\d+\s*(?:mg|mcg|g|ml)\s*(?:BD|TDS|QDS|OD|PRN|once daily|twice daily)?)', after, re.I)
                if dose_m:
                    dose_context = f" {dose_m.group(1).strip()}"
            lines.append(f"  - {m.title()}{dose_context}")
        lines.append("")

    # Diagnoses mentioned
    if diags:
        lines.append("DIAGNOSES / CONDITIONS:")
        for d in diags:
            lines.append(f"  - {d.title()}")
        lines.append("")

    result = '\n'.join(lines).rstrip()
    return result


@app.route("/voice-notes")
def voice_notes():
    return render_template("voice_notes.html")


@app.route("/voice-notes/format", methods=["POST"])
def voice_notes_format():
    try:
        data = request.get_json(force=True) or {}
        transcript = data.get("transcript", "").strip()
        if not transcript:
            return jsonify({"ok": False, "error": "No transcript provided"}), 400
        note = _format_clinical_note(transcript)
        return jsonify({"ok": True, "note": note})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/nlp-extractor")
def nlp_extractor():
    return render_template("nlp_extractor.html")


@app.route("/nlp-extractor/run", methods=["POST"])
def nlp_extractor_run():
    try:
        data = request.get_json(force=True) or {}
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"ok": False, "error": "No text provided"}), 400
        result = _run_nlp_extractor(text)
        return jsonify({"ok": True, **result})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST"])
def contact():
    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    subject = request.form.get("subject", "Message from drnealaggarwal.info").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, message]):
        flash("All fields are required.", "error")
        return redirect(url_for("about") + "#contact")

    try:
        gmail_user = os.environ.get("GMAIL_USER", "dr.neal.aggarwal@gmail.com")
        gmail_pass = os.environ.get("GMAIL_APP_PASS", "")

        body = (
            f"From:    {name} <{email}>\n"
            f"Subject: {subject}\n"
            f"{'─'*48}\n\n"
            f"{message}"
        )

        msg = MIMEMultipart()
        msg["From"]    = gmail_user
        msg["To"]      = "dr.neal.aggarwal@gmail.com"
        msg["Reply-To"] = email
        msg["Subject"] = f"[drnealaggarwal.info] {subject}"
        msg.attach(MIMEText(body, "plain"))

        if gmail_pass:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(gmail_user, gmail_pass)
                smtp.send_message(msg)

        flash("Message sent — I'll be in touch.", "ok")
    except Exception:
        flash("Something went wrong. Please email me directly at dr.neal.aggarwal@gmail.com.", "error")

    return redirect(url_for("about") + "#contact")


@app.route("/sw.js")
def service_worker():
    from flask import send_from_directory
    return send_from_directory(BASE / "static", "sw.js", mimetype="application/javascript")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
