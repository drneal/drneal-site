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
            if stripped and not stripped.startswith("![") and not stripped.startswith("<"):
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
        extensions=["fenced_code", "tables", "toc", "attr_list"],
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


@app.route("/archive")
def archive():
    posts = load_posts()
    return render_template("archive.html", posts=posts)


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


# ── Drug Interaction Checker ─────────────────────────────────────────────────

_DRUG_ALIASES: dict[str, str] = {
    "acetaminophen": "paracetamol", "tylenol": "paracetamol",
    "advil": "ibuprofen", "nurofen": "ibuprofen", "brufen": "ibuprofen",
    "voltaren": "diclofenac", "voltarol": "diclofenac",
    "coumadin": "warfarin",
    "lasix": "furosemide", "frusemide": "furosemide",
    "zocor": "simvastatin",
    "lipitor": "atorvastatin",
    "crestor": "rosuvastatin",
    "glucophage": "metformin",
    "lanoxin": "digoxin",
    "cordarone": "amiodarone",
    "plavix": "clopidogrel",
    "eliquis": "apixaban",
    "xarelto": "rivaroxaban",
    "pradaxa": "dabigatran",
    "prozac": "fluoxetine",
    "zoloft": "sertraline",
    "lexapro": "escitalopram",
    "celexa": "citalopram",
    "effexor": "venlafaxine",
    "cymbalta": "duloxetine",
    "seroquel": "quetiapine",
    "risperdal": "risperidone",
    "zyprexa": "olanzapine",
    "depakote": "valproate", "depakene": "valproate",
    "sodium valproate": "valproate", "semisodium valproate": "valproate",
    "tegretol": "carbamazepine",
    "lamictal": "lamotrigine",
    "neurontin": "gabapentin",
    "lyrica": "pregabalin",
    "diflucan": "fluconazole",
    "flagyl": "metronidazole",
    "rifadin": "rifampicin", "rifampin": "rifampicin",
    "sandimmun": "ciclosporin", "cyclosporine": "ciclosporin",
    "ciclosporine": "ciclosporin", "cyclosporin": "ciclosporin",
    "imuran": "azathioprine",
    "zyloprim": "allopurinol",
    "nitro": "nitroglycerine", "gtn": "nitroglycerine",
    "glyceryl trinitrate": "nitroglycerine",
    "viagra": "sildenafil",
    "cialis": "tadalafil",
    "prilosec": "omeprazole",
    "nexium": "esomeprazole",
    "clexane": "enoxaparin", "lovenox": "enoxaparin",
    "zithromax": "azithromycin",
    "biaxin": "clarithromycin",
    "cipro": "ciprofloxacin",
    "asa": "aspirin", "acetylsalicylic acid": "aspirin",
    "ms contin": "morphine", "oramorph": "morphine",
    "oxycontin": "oxycodone",
    "ultram": "tramadol",
    "colcrys": "colchicine",
    "inderal": "propranolol", "avlocardyl": "propranolol",
    "cardizem": "diltiazem",
    "calan": "verapamil", "isoptin": "verapamil",
    "slo-phyllin": "theophylline",
}

_DRUG_INTERACTIONS: list[dict] = [
    # ── CONTRAINDICATED ─────────────────────────────────────────────────────────
    {
        "drugs": ["selegiline", "sertraline"], "severity": "CONTRAINDICATED",
        "mechanism": "MAOI + SSRI: dual serotonergic stimulation causing serotonin syndrome.",
        "effect": "Potentially fatal serotonin syndrome: hyperthermia, rigidity, clonus, rhabdomyolysis, seizures.",
        "recommendation": "Do not co-prescribe. Allow ≥14 days washout after stopping MAOI before starting SSRI.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["selegiline", "fluoxetine"], "severity": "CONTRAINDICATED",
        "mechanism": "MAOI + SSRI. Fluoxetine's active metabolite has a 1–2 week half-life, extending the washout requirement.",
        "effect": "Potentially fatal serotonin syndrome.",
        "recommendation": "Allow ≥5 weeks washout after stopping fluoxetine before starting any MAOI.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["selegiline", "venlafaxine"], "severity": "CONTRAINDICATED",
        "mechanism": "MAOI + SNRI: dual serotonergic stimulation.",
        "effect": "Potentially fatal serotonin syndrome.",
        "recommendation": "Contraindicated. ≥14 days washout after stopping MAOI.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["selegiline", "tramadol"], "severity": "CONTRAINDICATED",
        "mechanism": "Tramadol inhibits serotonin and noradrenaline reuptake; combined with MAO inhibition causes serotonin syndrome.",
        "effect": "Serotonin syndrome; also lowers seizure threshold.",
        "recommendation": "Contraindicated. Use alternative analgesia (e.g., paracetamol, codeine).",
        "onset": "Hours"
    },
    {
        "drugs": ["rasagiline", "sertraline"], "severity": "CONTRAINDICATED",
        "mechanism": "Selective MAO-B inhibitor + SSRI: serotonin syndrome.",
        "effect": "Serotonin syndrome.",
        "recommendation": "Contraindicated. Use alternative antidepressant (e.g., mirtazapine).",
        "onset": "Hours to days"
    },
    {
        "drugs": ["rasagiline", "tramadol"], "severity": "CONTRAINDICATED",
        "mechanism": "MAO-B inhibitor + tramadol serotonin reuptake inhibition.",
        "effect": "Serotonin syndrome; seizures.",
        "recommendation": "Contraindicated. Use alternative analgesia.",
        "onset": "Hours"
    },
    {
        "drugs": ["sildenafil", "nitroglycerine"], "severity": "CONTRAINDICATED",
        "mechanism": "Both increase cGMP via the nitric oxide pathway; additive smooth muscle vasodilation.",
        "effect": "Severe, potentially fatal hypotension.",
        "recommendation": "Contraindicated within 24 hours of sildenafil. Never co-prescribe as regular medications.",
        "onset": "Minutes"
    },
    {
        "drugs": ["tadalafil", "nitroglycerine"], "severity": "CONTRAINDICATED",
        "mechanism": "Additive cGMP-mediated vasodilation. Tadalafil half-life is 17–35 hours.",
        "effect": "Severe hypotension.",
        "recommendation": "Contraindicated within 48 hours of tadalafil.",
        "onset": "Minutes"
    },
    {
        "drugs": ["sildenafil", "isosorbide"], "severity": "CONTRAINDICATED",
        "mechanism": "PDE5 inhibitor + nitrate: additive vasodilation via cGMP pathway.",
        "effect": "Severe hypotension.",
        "recommendation": "Contraindicated.",
        "onset": "Minutes to hours"
    },
    {
        "drugs": ["tadalafil", "isosorbide"], "severity": "CONTRAINDICATED",
        "mechanism": "PDE5 inhibitor + nitrate.",
        "effect": "Severe hypotension.",
        "recommendation": "Contraindicated.",
        "onset": "Minutes to hours"
    },
    {
        "drugs": ["linezolid", "sertraline"], "severity": "CONTRAINDICATED",
        "mechanism": "Linezolid is a reversible, non-selective MAO inhibitor; combined with SSRIs causes serotonin syndrome.",
        "effect": "Serotonin syndrome.",
        "recommendation": "Avoid. Use alternative antibiotic. If linezolid essential, discontinue SSRI ≥2 weeks beforehand.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["linezolid", "fluoxetine"], "severity": "CONTRAINDICATED",
        "mechanism": "Linezolid MAO inhibition + SSRI with long-acting active metabolite.",
        "effect": "Serotonin syndrome.",
        "recommendation": "Contraindicated. ≥5 weeks washout after fluoxetine.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["linezolid", "venlafaxine"], "severity": "CONTRAINDICATED",
        "mechanism": "Linezolid MAO inhibition + SNRI.",
        "effect": "Serotonin syndrome.",
        "recommendation": "Contraindicated.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["linezolid", "tramadol"], "severity": "CONTRAINDICATED",
        "mechanism": "Linezolid MAO inhibition + tramadol serotonin/noradrenaline reuptake inhibition.",
        "effect": "Serotonin syndrome.",
        "recommendation": "Contraindicated. Use alternative analgesia.",
        "onset": "Hours"
    },
    # ── MAJOR ────────────────────────────────────────────────────────────────────
    {
        "drugs": ["warfarin", "amiodarone"], "severity": "MAJOR",
        "mechanism": "Amiodarone inhibits CYP2C9 (primary warfarin metabolising enzyme) and CYP3A4.",
        "effect": "INR increases 2–3× within days to weeks; major haemorrhage risk.",
        "recommendation": "Reduce warfarin dose by 30–50% on starting amiodarone. Monitor INR every 3–5 days until stable, then weekly for 4–6 weeks.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["warfarin", "metronidazole"], "severity": "MAJOR",
        "mechanism": "Metronidazole inhibits CYP2C9 and may directly inhibit warfarin metabolism.",
        "effect": "Elevated INR; bleeding risk.",
        "recommendation": "Monitor INR during and for 7–10 days after metronidazole. Empirical warfarin dose reduction of ~25% often needed.",
        "onset": "2–7 days"
    },
    {
        "drugs": ["warfarin", "fluconazole"], "severity": "MAJOR",
        "mechanism": "Fluconazole inhibits CYP2C9 (major) and CYP3A4 (minor).",
        "effect": "Marked INR elevation; serious bleeding risk.",
        "recommendation": "Check INR on day 3 of fluconazole. Empirical warfarin dose reduction 30–50% often required.",
        "onset": "2–4 days"
    },
    {
        "drugs": ["warfarin", "aspirin"], "severity": "MAJOR",
        "mechanism": "Additive: COX-1 antiplatelet inhibition + anticoagulant + GI mucosal damage.",
        "effect": "Major bleeding, particularly GI haemorrhage.",
        "recommendation": "Avoid unless dual antithrombotic therapy is specifically indicated (ACS with AF). Always add PPI.",
        "onset": "Immediate"
    },
    {
        "drugs": ["warfarin", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "NSAIDs inhibit platelet aggregation and cause GI mucosal damage; potential CYP2C9 competition.",
        "effect": "Significantly increased GI and systemic bleeding risk.",
        "recommendation": "Avoid. Use paracetamol. If NSAID essential, monitor INR closely and add PPI.",
        "onset": "Days"
    },
    {
        "drugs": ["warfarin", "naproxen"], "severity": "MAJOR",
        "mechanism": "NSAID: antiplatelet + gastric mucosal damage.",
        "effect": "Increased bleeding risk.",
        "recommendation": "Avoid. Paracetamol preferred.",
        "onset": "Days"
    },
    {
        "drugs": ["warfarin", "diclofenac"], "severity": "MAJOR",
        "mechanism": "NSAID + CYP2C9 inhibition by diclofenac.",
        "effect": "Increased bleeding risk.",
        "recommendation": "Avoid. Paracetamol preferred.",
        "onset": "Days"
    },
    {
        "drugs": ["warfarin", "carbamazepine"], "severity": "MAJOR",
        "mechanism": "Carbamazepine is a potent CYP2C9/CYP3A4 inducer, accelerating warfarin clearance.",
        "effect": "Reduced anticoagulation; thrombosis risk.",
        "recommendation": "Monitor INR closely on starting carbamazepine; warfarin dose may need to increase significantly.",
        "onset": "1–2 weeks"
    },
    {
        "drugs": ["warfarin", "rifampicin"], "severity": "MAJOR",
        "mechanism": "Rifampicin is one of the most potent CYP enzyme inducers (CYP2C9, CYP3A4, CYP1A2).",
        "effect": "Dramatic reduction in warfarin effect; INR may fall to sub-therapeutic levels.",
        "recommendation": "Warfarin dose may need to double or more. Monitor INR very frequently. Consider alternative anticoagulation.",
        "onset": "Days to 2 weeks"
    },
    {
        "drugs": ["digoxin", "amiodarone"], "severity": "MAJOR",
        "mechanism": "Amiodarone inhibits P-glycoprotein, reducing digoxin renal excretion and altering volume of distribution.",
        "effect": "Digoxin toxicity: nausea, bradycardia, AV block, ventricular arrhythmias.",
        "recommendation": "Reduce digoxin dose by 50% on starting amiodarone. Monitor digoxin level and ECG closely.",
        "onset": "Days"
    },
    {
        "drugs": ["digoxin", "verapamil"], "severity": "MAJOR",
        "mechanism": "Verapamil inhibits P-glycoprotein, reducing digoxin renal clearance; additive AV nodal depression.",
        "effect": "Digoxin toxicity and bradycardia/AV block.",
        "recommendation": "Reduce digoxin dose by 33–50%. Monitor ECG and digoxin levels.",
        "onset": "Days"
    },
    {
        "drugs": ["digoxin", "diltiazem"], "severity": "MAJOR",
        "mechanism": "Diltiazem reduces digoxin clearance and has additive AV nodal effects.",
        "effect": "Elevated digoxin levels; bradycardia; AV block.",
        "recommendation": "Monitor digoxin levels and ECG. Reduce digoxin dose accordingly.",
        "onset": "Days"
    },
    {
        "drugs": ["methotrexate", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "NSAIDs reduce renal prostaglandin synthesis, decreasing GFR and methotrexate renal excretion; may also displace methotrexate from plasma proteins.",
        "effect": "Methotrexate toxicity: pancytopenia, mucositis, hepatotoxicity, nephrotoxicity.",
        "recommendation": "Avoid NSAIDs in patients on methotrexate. Use paracetamol. If unavoidable, monitor FBC and renal function closely.",
        "onset": "Days"
    },
    {
        "drugs": ["methotrexate", "naproxen"], "severity": "MAJOR",
        "mechanism": "NSAID-mediated reduction in methotrexate renal clearance.",
        "effect": "Methotrexate toxicity.",
        "recommendation": "Avoid. Use paracetamol.",
        "onset": "Days"
    },
    {
        "drugs": ["methotrexate", "trimethoprim"], "severity": "MAJOR",
        "mechanism": "Both are antifolates; additive inhibition of dihydrofolate reductase.",
        "effect": "Severe pancytopenia, megaloblastic anaemia.",
        "recommendation": "Avoid. If unavoidable, folinic acid rescue and close FBC monitoring.",
        "onset": "Days"
    },
    {
        "drugs": ["methotrexate", "co-trimoxazole"], "severity": "MAJOR",
        "mechanism": "Co-trimoxazole = trimethoprim (antifolate) + sulfamethoxazole (reduces methotrexate renal excretion).",
        "effect": "Severe antifolate toxicity: pancytopenia, mucositis.",
        "recommendation": "Avoid. If essential, folinic acid prophylaxis and close FBC monitoring required.",
        "onset": "Days"
    },
    {
        "drugs": ["lithium", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "NSAIDs reduce renal prostaglandin synthesis, decreasing GFR and lithium renal excretion.",
        "effect": "Lithium toxicity: tremor, ataxia, confusion, renal failure, cardiac arrhythmias.",
        "recommendation": "Avoid NSAIDs in patients on lithium. Use paracetamol. If NSAID unavoidable, reduce lithium dose and monitor levels closely.",
        "onset": "Days"
    },
    {
        "drugs": ["lithium", "naproxen"], "severity": "MAJOR",
        "mechanism": "NSAID: reduced GFR → reduced lithium excretion.",
        "effect": "Lithium toxicity.",
        "recommendation": "Avoid. Use paracetamol.",
        "onset": "Days"
    },
    {
        "drugs": ["lithium", "diclofenac"], "severity": "MAJOR",
        "mechanism": "NSAID: reduced lithium excretion.",
        "effect": "Lithium toxicity.",
        "recommendation": "Avoid.",
        "onset": "Days"
    },
    {
        "drugs": ["lithium", "ramipril"], "severity": "MAJOR",
        "mechanism": "ACE inhibitors reduce aldosterone-mediated sodium reabsorption, causing compensatory lithium retention in the proximal tubule.",
        "effect": "Lithium toxicity even at previously therapeutic doses.",
        "recommendation": "Monitor lithium levels closely when starting or changing ACE inhibitor dose. Consider empirical 50% lithium dose reduction.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["lithium", "lisinopril"], "severity": "MAJOR",
        "mechanism": "ACE inhibitor: sodium depletion → compensatory lithium reabsorption.",
        "effect": "Lithium toxicity.",
        "recommendation": "Monitor lithium levels closely.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["lithium", "furosemide"], "severity": "MAJOR",
        "mechanism": "Loop diuretics cause sodium depletion, triggering compensatory lithium reabsorption in the proximal tubule.",
        "effect": "Lithium toxicity.",
        "recommendation": "Monitor lithium levels closely. Ensure adequate dietary sodium intake.",
        "onset": "Days"
    },
    {
        "drugs": ["morphine", "diazepam"], "severity": "MAJOR",
        "mechanism": "Additive CNS and respiratory depression (opioid receptor agonism + GABA-A positive allosteric modulation).",
        "effect": "Respiratory depression, coma, death. This combination accounts for a large proportion of opioid overdose deaths.",
        "recommendation": "Avoid where possible. If co-prescribed (palliative care), use lowest doses, monitor respiratory rate closely, and have naloxone available.",
        "onset": "Hours"
    },
    {
        "drugs": ["oxycodone", "diazepam"], "severity": "MAJOR",
        "mechanism": "Additive opioid + benzodiazepine respiratory depression.",
        "effect": "Respiratory depression, sedation.",
        "recommendation": "Avoid where possible. Naloxone should be accessible if co-prescribed.",
        "onset": "Hours"
    },
    {
        "drugs": ["codeine", "diazepam"], "severity": "MAJOR",
        "mechanism": "Additive respiratory depression (opioid + benzodiazepine).",
        "effect": "Respiratory depression.",
        "recommendation": "Avoid. If necessary, lowest doses and close monitoring.",
        "onset": "Hours"
    },
    {
        "drugs": ["tramadol", "sertraline"], "severity": "MAJOR",
        "mechanism": "Tramadol inhibits serotonin and noradrenaline reuptake; combined with SSRIs substantially raises synaptic serotonin.",
        "effect": "Serotonin syndrome: agitation, confusion, hyperthermia, tachycardia, clonus, rigidity.",
        "recommendation": "Avoid if possible. If co-prescribed, use lowest tramadol dose and monitor for serotonin syndrome signs.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["tramadol", "fluoxetine"], "severity": "MAJOR",
        "mechanism": "Serotonin syndrome + fluoxetine inhibits CYP2D6 (tramadol metabolic activation).",
        "effect": "Serotonin syndrome.",
        "recommendation": "Avoid. Use alternative analgesia.",
        "onset": "Hours"
    },
    {
        "drugs": ["tramadol", "citalopram"], "severity": "MAJOR",
        "mechanism": "Serotonin syndrome (SSRI + tramadol serotonin reuptake inhibition).",
        "effect": "Serotonin syndrome.",
        "recommendation": "Avoid.",
        "onset": "Hours"
    },
    {
        "drugs": ["tramadol", "escitalopram"], "severity": "MAJOR",
        "mechanism": "Serotonin syndrome (SSRI + tramadol).",
        "effect": "Serotonin syndrome.",
        "recommendation": "Avoid.",
        "onset": "Hours"
    },
    {
        "drugs": ["tramadol", "venlafaxine"], "severity": "MAJOR",
        "mechanism": "Serotonin syndrome (SNRI + tramadol); also additive seizure risk.",
        "effect": "Serotonin syndrome; seizures.",
        "recommendation": "Avoid. Use alternative analgesia.",
        "onset": "Hours"
    },
    {
        "drugs": ["metoprolol", "verapamil"], "severity": "MAJOR",
        "mechanism": "Additive AV nodal depression: beta-blockade + rate-limiting calcium channel blockade.",
        "effect": "Severe bradycardia, complete heart block.",
        "recommendation": "Avoid. Use dihydropyridine CCB (amlodipine) instead of verapamil if both rate control and BP control are needed.",
        "onset": "Hours"
    },
    {
        "drugs": ["bisoprolol", "verapamil"], "severity": "MAJOR",
        "mechanism": "Additive AV nodal depression.",
        "effect": "Bradycardia, heart block.",
        "recommendation": "Avoid. Use amlodipine if CCB required.",
        "onset": "Hours"
    },
    {
        "drugs": ["atenolol", "verapamil"], "severity": "MAJOR",
        "mechanism": "Additive AV nodal depression.",
        "effect": "Bradycardia, heart block.",
        "recommendation": "Avoid.",
        "onset": "Hours"
    },
    {
        "drugs": ["propranolol", "verapamil"], "severity": "MAJOR",
        "mechanism": "Additive AV nodal depression.",
        "effect": "Bradycardia, heart block.",
        "recommendation": "Avoid.",
        "onset": "Hours"
    },
    {
        "drugs": ["metoprolol", "diltiazem"], "severity": "MAJOR",
        "mechanism": "Additive AV nodal depression (beta-blocker + rate-limiting CCB).",
        "effect": "Severe bradycardia, heart block.",
        "recommendation": "Avoid. Use amlodipine instead of diltiazem if CCB needed.",
        "onset": "Hours"
    },
    {
        "drugs": ["bisoprolol", "diltiazem"], "severity": "MAJOR",
        "mechanism": "Additive AV nodal depression.",
        "effect": "Bradycardia, heart block.",
        "recommendation": "Avoid. Use amlodipine.",
        "onset": "Hours"
    },
    {
        "drugs": ["amiodarone", "sotalol"], "severity": "MAJOR",
        "mechanism": "Additive QTc prolongation via multiple mechanisms (IKr blockade + multiple ion channel effects).",
        "effect": "Torsades de pointes; ventricular fibrillation.",
        "recommendation": "Avoid combination. ECG monitoring mandatory in specialist settings.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["amiodarone", "azithromycin"], "severity": "MAJOR",
        "mechanism": "Additive QTc prolongation (both prolong cardiac repolarisation via IKr blockade).",
        "effect": "Torsades de pointes.",
        "recommendation": "Avoid. Use doxycycline or co-amoxiclav as alternative to azithromycin.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["amiodarone", "clarithromycin"], "severity": "MAJOR",
        "mechanism": "Additive QTc prolongation; clarithromycin also inhibits CYP3A4 (amiodarone metabolism), raising amiodarone levels.",
        "effect": "Torsades de pointes.",
        "recommendation": "Avoid. Use alternative antibiotic.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["amiodarone", "haloperidol"], "severity": "MAJOR",
        "mechanism": "Additive QTc prolongation.",
        "effect": "Torsades de pointes.",
        "recommendation": "Avoid. If necessary, baseline ECG and regular QTc monitoring.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["amiodarone", "ciprofloxacin"], "severity": "MAJOR",
        "mechanism": "Additive QTc prolongation (fluoroquinolone IKr blockade).",
        "effect": "Torsades de pointes.",
        "recommendation": "Avoid. Use alternative antibiotic.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["haloperidol", "azithromycin"], "severity": "MAJOR",
        "mechanism": "Additive QTc prolongation.",
        "effect": "Torsades de pointes.",
        "recommendation": "Avoid. Use alternative antibiotic.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["simvastatin", "amiodarone"], "severity": "MAJOR",
        "mechanism": "Amiodarone inhibits CYP3A4 (simvastatin metabolism); simvastatin has concentration-dependent myopathy.",
        "effect": "Myopathy; rhabdomyolysis.",
        "recommendation": "Simvastatin dose must not exceed 20 mg/day with amiodarone. Switch to pravastatin or rosuvastatin (less CYP3A4-dependent).",
        "onset": "Weeks to months"
    },
    {
        "drugs": ["simvastatin", "clarithromycin"], "severity": "MAJOR",
        "mechanism": "Clarithromycin inhibits CYP3A4, markedly raising simvastatin acid levels.",
        "effect": "Myopathy; rhabdomyolysis.",
        "recommendation": "Suspend simvastatin for the duration of the clarithromycin course. Restart after completion.",
        "onset": "Days"
    },
    {
        "drugs": ["atorvastatin", "clarithromycin"], "severity": "MAJOR",
        "mechanism": "Clarithromycin inhibits CYP3A4 (atorvastatin metabolism).",
        "effect": "Elevated atorvastatin levels; myopathy risk.",
        "recommendation": "Suspend atorvastatin during clarithromycin course or switch to pravastatin/rosuvastatin.",
        "onset": "Days"
    },
    {
        "drugs": ["simvastatin", "ciclosporin"], "severity": "MAJOR",
        "mechanism": "Ciclosporin inhibits both OATP1B1 transporter (hepatic uptake) and CYP3A4, markedly increasing simvastatin bioavailability.",
        "effect": "Severe myopathy; rhabdomyolysis.",
        "recommendation": "Avoid simvastatin in patients on ciclosporin. Use pravastatin (lower OATP1B1 dependence) at low doses.",
        "onset": "Weeks"
    },
    {
        "drugs": ["simvastatin", "fluconazole"], "severity": "MAJOR",
        "mechanism": "Fluconazole inhibits CYP3A4, raising simvastatin levels markedly.",
        "effect": "Myopathy; rhabdomyolysis.",
        "recommendation": "Suspend simvastatin during fluconazole course.",
        "onset": "Days"
    },
    {
        "drugs": ["spironolactone", "ramipril"], "severity": "MAJOR",
        "mechanism": "Both raise serum potassium: aldosterone antagonist + reduced aldosterone synthesis via ACE inhibition.",
        "effect": "Hyperkalaemia: cardiac arrhythmias, cardiac arrest.",
        "recommendation": "Monitor potassium at baseline, 1–2 weeks, then monthly. Acceptable in heart failure if eGFR >30 and K+ <5.0 mmol/L at baseline.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["spironolactone", "lisinopril"], "severity": "MAJOR",
        "mechanism": "Dual hyperkalaemia (aldosterone antagonist + ACE inhibitor).",
        "effect": "Hyperkalaemia.",
        "recommendation": "Monitor potassium at 1–2 weeks and monthly.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["allopurinol", "azathioprine"], "severity": "MAJOR",
        "mechanism": "Allopurinol inhibits xanthine oxidase, the enzyme responsible for inactivating azathioprine's active metabolite (6-mercaptopurine), causing accumulation.",
        "effect": "Severe bone marrow suppression: pancytopenia, agranulocytosis.",
        "recommendation": "Avoid if at all possible. If essential, reduce azathioprine dose by 75% and monitor FBC very frequently.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["valproate", "lamotrigine"], "severity": "MAJOR",
        "mechanism": "Valproate inhibits glucuronidation of lamotrigine, approximately doubling plasma lamotrigine levels.",
        "effect": "Lamotrigine toxicity (ataxia, diplopia, dizziness); elevated Stevens-Johnson syndrome risk with rapid dose escalation.",
        "recommendation": "Halve the standard starting lamotrigine dose and titrate at half the usual rate when adding to valproate.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["carbamazepine", "lamotrigine"], "severity": "MAJOR",
        "mechanism": "Carbamazepine induces lamotrigine glucuronidation, reducing lamotrigine levels 40–50%.",
        "effect": "Subtherapeutic lamotrigine levels; worsened seizure control.",
        "recommendation": "Higher lamotrigine doses required when co-prescribed with carbamazepine. Monitor seizure control carefully.",
        "onset": "Weeks"
    },
    {
        "drugs": ["ramipril", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "NSAIDs reduce renal prostaglandin synthesis (reduces GFR) and antagonise ACE inhibitor antihypertensive effect. With a concurrent diuretic, this constitutes the 'triple whammy' — a leading cause of drug-induced AKI.",
        "effect": "Acute kidney injury; loss of blood pressure control.",
        "recommendation": "Avoid. Use paracetamol. If NSAID essential, stop ACE inhibitor temporarily and monitor renal function.",
        "onset": "Days"
    },
    {
        "drugs": ["lisinopril", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "NSAID reduces GFR and antagonises ACE inhibitor. With diuretic = triple whammy.",
        "effect": "Acute kidney injury.",
        "recommendation": "Avoid. Use paracetamol.",
        "onset": "Days"
    },
    {
        "drugs": ["theophylline", "ciprofloxacin"], "severity": "MAJOR",
        "mechanism": "Ciprofloxacin inhibits CYP1A2, the primary enzyme metabolising theophylline.",
        "effect": "Theophylline toxicity: tachycardia, nausea, vomiting, seizures, arrhythmias.",
        "recommendation": "Reduce theophylline dose by 30–50% during ciprofloxacin. Monitor levels. Use alternative antibiotic if possible.",
        "onset": "Days"
    },
    {
        "drugs": ["theophylline", "clarithromycin"], "severity": "MAJOR",
        "mechanism": "Clarithromycin inhibits CYP1A2 and CYP3A4 (theophylline metabolism).",
        "effect": "Theophylline toxicity.",
        "recommendation": "Monitor theophylline levels closely. Consider alternative antibiotic.",
        "onset": "Days"
    },
    {
        "drugs": ["apixaban", "aspirin"], "severity": "MAJOR",
        "mechanism": "Additive anticoagulant + antiplatelet bleeding risk.",
        "effect": "Major bleeding including intracranial haemorrhage.",
        "recommendation": "Avoid unless dual antithrombotic therapy is specifically indicated (ACS/stent + AF). Add PPI.",
        "onset": "Immediate"
    },
    {
        "drugs": ["rivaroxaban", "aspirin"], "severity": "MAJOR",
        "mechanism": "Additive anticoagulant + antiplatelet bleeding risk.",
        "effect": "Major bleeding.",
        "recommendation": "Avoid unless clinically indicated. Add PPI.",
        "onset": "Immediate"
    },
    {
        "drugs": ["apixaban", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "NSAIDs: antiplatelet + GI mucosal damage; additive with DOAC anticoagulation.",
        "effect": "GI haemorrhage.",
        "recommendation": "Avoid NSAIDs in patients on DOACs. Use paracetamol.",
        "onset": "Days"
    },
    {
        "drugs": ["rivaroxaban", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "Additive bleeding risk (DOAC + NSAID).",
        "effect": "GI haemorrhage.",
        "recommendation": "Avoid NSAIDs with DOACs.",
        "onset": "Days"
    },
    {
        "drugs": ["colchicine", "clarithromycin"], "severity": "MAJOR",
        "mechanism": "Clarithromycin inhibits both P-glycoprotein (colchicine efflux) and CYP3A4 (colchicine metabolism), dramatically raising colchicine plasma levels.",
        "effect": "Colchicine toxicity: myopathy, bone marrow suppression, multi-organ failure. Fatal cases reported.",
        "recommendation": "Contraindicated in renal/hepatic impairment. In normal renal/hepatic function, use the lowest colchicine dose for the shortest duration.",
        "onset": "Days"
    },
    {
        "drugs": ["colchicine", "ciclosporin"], "severity": "MAJOR",
        "mechanism": "Ciclosporin inhibits P-glycoprotein and CYP3A4 (colchicine clearance).",
        "effect": "Colchicine toxicity.",
        "recommendation": "Avoid. Use alternative gout therapy.",
        "onset": "Days"
    },
    {
        "drugs": ["ciclosporin", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "NSAIDs reduce renal prostaglandins; ciclosporin has direct nephrotoxicity — combination markedly increases AKI risk.",
        "effect": "Acute kidney injury.",
        "recommendation": "Avoid. Use paracetamol.",
        "onset": "Days"
    },
    {
        "drugs": ["tacrolimus", "ibuprofen"], "severity": "MAJOR",
        "mechanism": "Additive nephrotoxicity (calcineurin inhibitor + NSAID).",
        "effect": "Acute kidney injury.",
        "recommendation": "Avoid. Use paracetamol.",
        "onset": "Days"
    },
    # ── MODERATE ──────────────────────────────────────────────────────────────────
    {
        "drugs": ["clopidogrel", "omeprazole"], "severity": "MODERATE",
        "mechanism": "Omeprazole inhibits CYP2C19, which activates clopidogrel (prodrug → active thiol metabolite).",
        "effect": "Reduced antiplatelet activity of clopidogrel; potential increased cardiovascular events.",
        "recommendation": "Use pantoprazole or esomeprazole (less CYP2C19 inhibition) instead of omeprazole as the PPI.",
        "onset": "Days"
    },
    {
        "drugs": ["quetiapine", "azithromycin"], "severity": "MODERATE",
        "mechanism": "Additive QTc prolongation.",
        "effect": "Torsades de pointes risk.",
        "recommendation": "Baseline ECG. Monitor QTc. Use alternative antibiotic if feasible.",
        "onset": "Hours to days"
    },
    {
        "drugs": ["gabapentin", "morphine"], "severity": "MODERATE",
        "mechanism": "Additive CNS and respiratory depression.",
        "effect": "Excessive sedation, respiratory depression.",
        "recommendation": "Use lowest effective doses. Monitor for respiratory depression. Avoid in patients with COPD.",
        "onset": "Hours"
    },
    {
        "drugs": ["pregabalin", "oxycodone"], "severity": "MODERATE",
        "mechanism": "Additive CNS depression (gabapentinoid + opioid).",
        "effect": "Sedation, cognitive impairment, respiratory depression.",
        "recommendation": "Lowest effective doses. Counsel on driving. Monitor closely.",
        "onset": "Hours"
    },
    {
        "drugs": ["pregabalin", "morphine"], "severity": "MODERATE",
        "mechanism": "Additive CNS and respiratory depression.",
        "effect": "Respiratory depression.",
        "recommendation": "Start low. Monitor.",
        "onset": "Hours"
    },
    {
        "drugs": ["furosemide", "ibuprofen"], "severity": "MODERATE",
        "mechanism": "NSAIDs antagonise the renal prostaglandin-dependent mechanism of loop diuretics.",
        "effect": "Reduced diuretic efficacy; fluid retention; AKI risk.",
        "recommendation": "Avoid NSAIDs in patients requiring diuretic therapy. Use paracetamol.",
        "onset": "Days"
    },
    {
        "drugs": ["sertraline", "ibuprofen"], "severity": "MODERATE",
        "mechanism": "SSRIs deplete platelet serotonin (reducing platelet aggregation); NSAIDs add independent antiplatelet and mucosal effects.",
        "effect": "3–15× increased risk of upper GI bleeding.",
        "recommendation": "Add PPI cover if both drugs are necessary.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["fluoxetine", "ibuprofen"], "severity": "MODERATE",
        "mechanism": "SSRI platelet depletion + NSAID antiplatelet/mucosal effects.",
        "effect": "Increased GI bleeding risk.",
        "recommendation": "Add PPI cover.",
        "onset": "Days to weeks"
    },
    {
        "drugs": ["simvastatin", "amlodipine"], "severity": "MODERATE",
        "mechanism": "Amlodipine weakly inhibits CYP3A4, modestly increasing simvastatin exposure.",
        "effect": "Slightly increased myopathy risk.",
        "recommendation": "Simvastatin dose should not exceed 20 mg/day when co-prescribed with amlodipine.",
        "onset": "Weeks"
    },
    {
        "drugs": ["levothyroxine", "warfarin"], "severity": "MODERATE",
        "mechanism": "Thyroid hormones increase catabolism of vitamin K-dependent clotting factors.",
        "effect": "Elevated INR when levothyroxine dose is increased or a hypothyroid patient achieves euthyroidism.",
        "recommendation": "Monitor INR whenever levothyroxine dose changes.",
        "onset": "Weeks"
    },
    {
        "drugs": ["carbamazepine", "valproate"], "severity": "MODERATE",
        "mechanism": "Carbamazepine induces valproate metabolism; valproate inhibits carbamazepine epoxide hydrolase, raising the toxic carbamazepine-10,11-epoxide metabolite.",
        "effect": "Reduced valproate levels; carbamazepine toxicity (diplopia, ataxia, dizziness) from raised epoxide.",
        "recommendation": "Monitor both drug levels. Specialist epilepsy supervision recommended.",
        "onset": "Weeks"
    },
    {
        "drugs": ["metformin", "ibuprofen"], "severity": "MODERATE",
        "mechanism": "NSAIDs reduce GFR; metformin accumulates in renal impairment with lactic acidosis risk.",
        "effect": "Metformin accumulation and risk of lactic acidosis, particularly in CKD.",
        "recommendation": "Use paracetamol instead. Monitor renal function if NSAID unavoidable.",
        "onset": "Days"
    },
    {
        "drugs": ["enoxaparin", "aspirin"], "severity": "MODERATE",
        "mechanism": "Additive anticoagulant + antiplatelet bleeding risk.",
        "effect": "Increased bleeding.",
        "recommendation": "Often co-prescribed intentionally in ACS — acceptable with clear clinical indication and PPI cover.",
        "onset": "Hours"
    },
    {
        "drugs": ["ramipril", "furosemide"], "severity": "MODERATE",
        "mechanism": "Furosemide-induced volume depletion sensitises patients to first-dose ACE inhibitor hypotension.",
        "effect": "Symptomatic first-dose hypotension.",
        "recommendation": "Start ACE inhibitor at lowest dose. Consider stopping furosemide 24h before initiating ACE inhibitor in volume-depleted patients.",
        "onset": "Hours (first dose)"
    },
]


def _check_drug_interactions(drug_list: list[str]) -> dict:
    """Check a list of drug name strings for known clinically significant interactions."""

    # Build symmetric lookup: frozenset({drug_a, drug_b}) → interaction
    ix_lookup: dict[frozenset, dict] = {}
    for ix in _DRUG_INTERACTIONS:
        key = frozenset(ix["drugs"])
        if key not in ix_lookup:
            ix_lookup[key] = ix

    # Normalise each drug name: lowercase, strip dose/frequency, resolve aliases
    _med_lower = [m.lower() for m in _NLP_MEDICATIONS]

    def _normalise(raw: str) -> str | None:
        name = raw.strip().lower()
        # Strip trailing dose / frequency info
        name = re.sub(r'\s+\d[\d.]*\s*(mg|mcg|g|ml|mL|units?|IU|%)\S*', '', name)
        name = re.sub(
            r'\s+(od|bd|tds|qds|prn|nocte|stat|once\s+daily|twice\s+daily|'
            r'three\s+times|four\s+times)\b.*', '', name, flags=re.I
        )
        name = name.strip()
        # Check aliases
        name = _DRUG_ALIASES.get(name, name)
        # Exact match
        if name in _med_lower:
            return name
        # Partial match: name is a substring of a known drug (handles brand-ish substrings)
        for med in _med_lower:
            if name and (name in med or med in name) and len(name) >= 4:
                return med
        return None

    recognised: list[str] = []
    unrecognised: list[str] = []
    for raw in drug_list:
        norm = _normalise(raw)
        if norm and norm not in recognised:
            recognised.append(norm)
        elif not norm:
            clean = raw.strip()
            if clean and clean not in unrecognised:
                unrecognised.append(clean)

    # Check all unique pairs
    interactions_found: list[dict] = []
    sev_counts = {"CONTRAINDICATED": 0, "MAJOR": 0, "MODERATE": 0, "MINOR": 0}

    for i in range(len(recognised)):
        for j in range(i + 1, len(recognised)):
            key = frozenset([recognised[i], recognised[j]])
            if key in ix_lookup:
                ix = ix_lookup[key]
                interactions_found.append({
                    **ix,
                    "drug_a": recognised[i],
                    "drug_b": recognised[j],
                })
                sev = ix["severity"]
                if sev in sev_counts:
                    sev_counts[sev] += 1

    # Sort by severity
    _sev_order = {"CONTRAINDICATED": 0, "MAJOR": 1, "MODERATE": 2, "MINOR": 3}
    interactions_found.sort(key=lambda x: _sev_order.get(x["severity"], 4))

    return {
        "drugs_detected": recognised,
        "drugs_unrecognised": unrecognised,
        "interactions": interactions_found,
        "severity_counts": sev_counts,
        "total": len(interactions_found),
    }


@app.route("/drug-checker")
def drug_checker():
    return render_template("drug_checker.html")


@app.route("/drug-checker/run", methods=["POST"])
def drug_checker_run():
    try:
        data = request.get_json(force=True) or {}
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"ok": False, "error": "No medications provided"}), 400

        # Extract medications from text using NLP extractor
        nlp_result = _run_nlp_extractor(text)
        drug_list = [e["text"] for e in nlp_result["entities"] if e["type"] == "MEDICATION"]

        # Also parse line-by-line (handles plain lists and bullet-point lists)
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        for line in lines:
            # Strip bullets / numbers: "- warfarin 5mg" → "warfarin 5mg"
            line = re.sub(r'^[\-\•\*\d\.]+\s*', '', line).strip()
            if line and line not in drug_list:
                drug_list.append(line)

        result = _check_drug_interactions(drug_list)
        return jsonify({"ok": True, **result})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


# ── LLM Agent Trace Visualiser ───────────────────────────────────────────────

def _parse_agent_trace(raw: dict | list) -> dict:
    """Normalise Claude API, OpenAI, or generic messages-array traces into a unified structure."""

    # Detect format and extract messages list
    if isinstance(raw, list):
        msgs = raw
        model = "unknown"
    elif isinstance(raw, dict):
        if "messages" in raw:
            msgs = raw["messages"]
            model = raw.get("model", raw.get("id", "unknown"))
        elif "role" in raw:          # single Anthropic response object
            msgs = [raw]
            model = raw.get("model", "unknown")
        elif "choices" in raw:       # OpenAI Chat Completion response
            msgs = [c.get("message", {}) for c in raw.get("choices", [])]
            model = raw.get("model", "unknown")
        else:
            raise ValueError("Unrecognised trace format — expected messages array, Anthropic response, or OpenAI response.")
    else:
        raise ValueError("Trace must be a JSON object or array.")

    steps = []
    total_input = 0
    total_output = 0
    tool_counts: dict[str, int] = {}

    for i, msg in enumerate(msgs):
        role    = msg.get("role", "unknown")
        content = msg.get("content", "")
        usage   = msg.get("usage", {})

        # Token counts — Anthropic uses input_tokens/output_tokens;
        # OpenAI uses prompt_tokens/completion_tokens at the top level
        inp = usage.get("input_tokens", usage.get("prompt_tokens", 0))
        out = usage.get("output_tokens", usage.get("completion_tokens", 0))
        total_input  += inp
        total_output += out

        blocks = []

        # Normalise content to a list of typed blocks
        if isinstance(content, str) and content:
            blocks.append({"type": "text", "text": content})
        elif isinstance(content, list):
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get("type", "text")

                if btype == "text":
                    blocks.append({"type": "text", "text": block.get("text", "")})

                elif btype == "thinking":
                    blocks.append({"type": "thinking", "text": block.get("thinking", "")})

                elif btype == "tool_use":
                    name = block.get("name", "")
                    tool_counts[name] = tool_counts.get(name, 0) + 1
                    blocks.append({
                        "type": "tool_use",
                        "id": block.get("id", ""),
                        "name": name,
                        "input": block.get("input", {}),
                    })

                elif btype == "tool_result":
                    rc = block.get("content", "")
                    if isinstance(rc, list):
                        rc = "\n".join(
                            c.get("text", "") for c in rc
                            if isinstance(c, dict) and c.get("type") == "text"
                        )
                    blocks.append({
                        "type": "tool_result",
                        "tool_use_id": block.get("tool_use_id", ""),
                        "content": rc,
                        "is_error": block.get("is_error", False),
                    })

        # Handle OpenAI tool_calls field (parallel to content)
        for tc in msg.get("tool_calls", []):
            fn   = tc.get("function", {})
            args = fn.get("arguments", {})
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except Exception:
                    args = {"raw": args}
            name = fn.get("name", "")
            tool_counts[name] = tool_counts.get(name, 0) + 1
            blocks.append({
                "type": "tool_use",
                "id": tc.get("id", ""),
                "name": name,
                "input": args,
            })

        # OpenAI tool response messages (role == "tool")
        if role == "tool":
            blocks.append({
                "type": "tool_result",
                "tool_use_id": msg.get("tool_call_id", ""),
                "content": content if isinstance(content, str) else str(content),
                "is_error": False,
            })

        steps.append({
            "index": i,
            "role": role,
            "blocks": blocks,
            "input_tokens": inp,
            "output_tokens": out,
        })

    return {
        "steps": steps,
        "model": model,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "total_tokens": total_input + total_output,
        "total_steps": len(steps),
        "tool_counts": tool_counts,
    }


@app.route("/agent-trace")
def agent_trace():
    return render_template("agent_trace.html")


@app.route("/agent-trace/parse", methods=["POST"])
def agent_trace_parse():
    try:
        data = request.get_json(force=True) or {}
        raw  = data.get("trace")
        if raw is None:
            return jsonify({"ok": False, "error": "No trace provided"}), 400
        result = _parse_agent_trace(raw)
        return jsonify({"ok": True, **result})
    except Exception as exc:
        return jsonify({"ok": False, "error": str(exc)}), 500


@app.route("/binaural")
def binaural():
    return render_template("binaural.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        return render_template("contact.html")

    name    = request.form.get("name", "").strip()
    email   = request.form.get("email", "").strip()
    subject = request.form.get("subject", "Message from drnealaggarwal.info").strip()
    message = request.form.get("message", "").strip()

    if not all([name, email, message]):
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("contact"))

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

        flash("Message sent — I'll be in touch.", "success")
    except Exception:
        flash("Something went wrong. Please email me directly at dr.neal.aggarwal@gmail.com.", "error")

    return redirect(url_for("contact"))


@app.route("/sw.js")
def service_worker():
    from flask import send_from_directory
    return send_from_directory(BASE / "static", "sw.js", mimetype="application/javascript")


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
