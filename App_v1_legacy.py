"""
╔══════════════════════════════════════════════════════════════════════╗
║        AI RESUME ANALYSER — Pro Edition                              ║
║  · Real-world weighted skill scoring                                 ║
║  · Market demand integration                                         ║
║  · Skill gap radar chart                                             ║
║  · Career roadmap timeline                                           ║
║  · ATS compatibility checker                                         ║
║  · Salary benchmark display                                          ║
║  · Rich admin dashboard with 6 charts                                ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import base64, random, time, datetime, io, os, re, sqlite3, json
import plotly.express as px
import plotly.graph_objects as go

from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
import spacy
from streamlit_tags import st_tags
import nltk
nltk.download('stopwords', quiet=True)

from Courses import (
    ds_course, web_course, android_course,
    ios_course, uiux_course, resume_videos, interview_videos
)

# ══════════════════════════════════════════════════
# PAGE CONFIG  ─ must be first Streamlit call
# ══════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Resume Analyser Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════
# GLOBAL CUSTOM CSS  — dark editorial theme
# ══════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #0d0f1a; }
section[data-testid="stSidebar"] { background: #090b14 !important; border-right: 1px solid #1e2235; }
section[data-testid="stSidebar"] * { color: #c8cfe0 !important; }

.hero-banner {
    background: linear-gradient(135deg,#0d0f1a 0%,#141728 50%,#0d0f1a 100%);
    border: 1px solid #1e2235; border-radius: 16px;
    padding: 48px 40px; margin-bottom: 32px; position: relative; overflow: hidden;
}
.hero-banner::before {
    content:''; position:absolute; top:-80px; right:-80px;
    width:300px; height:300px;
    background:radial-gradient(circle,rgba(99,102,241,.15) 0%,transparent 70%); border-radius:50%;
}
.hero-title {
    font-family:'DM Serif Display',serif; font-size:3rem;
    background:linear-gradient(135deg,#e2e8f0,#6366f1,#ec4899);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; line-height:1.1; margin:0 0 12px;
}
.hero-sub { color:#8892a4; font-size:1.05rem; font-weight:300; margin:0; }

.stat-card {
    background:#141728; border:1px solid #1e2235; border-radius:12px;
    padding:20px 24px; text-align:center; transition:border-color .2s;
}
.stat-card:hover { border-color:#6366f1; }
.stat-number { font-family:'DM Serif Display',serif; font-size:2.2rem; color:#6366f1; margin:0; }
.stat-label  { color:#8892a4; font-size:.82rem; margin:4px 0 0; letter-spacing:.08em; text-transform:uppercase; }

.section-card {
    background:#141728; border:1px solid #1e2235; border-radius:14px;
    padding:28px 32px; margin-bottom:24px;
}
.section-title {
    font-family:'DM Serif Display',serif; font-size:1.4rem; color:#e2e8f0;
    margin:0 0 20px; padding-bottom:12px; border-bottom:1px solid #1e2235;
}

.skill-pill { display:inline-block; padding:4px 12px; border-radius:999px; font-size:.78rem; margin:3px; font-weight:500; }
.pill-have  { background:rgba(99,102,241,.15); color:#818cf8; border:1px solid rgba(99,102,241,.3); }
.pill-need  { background:rgba(236,72,153,.12); color:#f472b6; border:1px solid rgba(236,72,153,.25); }

.check-row { display:flex; align-items:flex-start; gap:12px; padding:10px 0; border-bottom:1px solid #1a1e30; }
.check-row:last-child { border-bottom:none; }
.check-icon { font-size:1.1rem; flex-shrink:0; margin-top:1px; }
.check-text { color:#c8cfe0; font-size:.92rem; line-height:1.4; }
.check-tip  { color:#6b7280; font-size:.80rem; margin-top:2px; }

.salary-badge {
    background:linear-gradient(135deg,rgba(99,102,241,.2),rgba(236,72,153,.15));
    border:1px solid rgba(99,102,241,.3); border-radius:10px; padding:16px 20px; margin-bottom:12px;
}
.salary-role  { color:#c8cfe0; font-weight:600; font-size:.95rem; }
.salary-range { color:#818cf8; font-size:1.1rem; font-weight:700; margin-top:4px; }
.salary-meta  { color:#6b7280; font-size:.78rem; margin-top:2px; }

.stButton > button {
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    color:#fff !important; border:none !important; border-radius:8px !important;
    font-weight:500 !important; padding:10px 28px !important;
}
.stProgress > div > div > div > div { background:linear-gradient(90deg,#6366f1,#ec4899) !important; }
div[data-testid="stMetric"] { background:#141728; border:1px solid #1e2235; border-radius:10px; padding:14px 18px; }
div[data-testid="stMetric"] label { color:#8892a4 !important; }
div[data-testid="stMetric"] div   { color:#e2e8f0 !important; }
[data-testid="stFileUploader"] { border:2px dashed #1e2235 !important; border-radius:12px !important; background:#0d0f1a !important; }
[data-testid="stFileUploader"]:hover { border-color:#6366f1 !important; }
.stTabs [data-baseweb="tab-list"] { background:#141728; border-radius:10px; padding:4px; gap:4px; }
.stTabs [data-baseweb="tab"]      { background:transparent; color:#8892a4; border-radius:8px; font-size:.88rem; }
.stTabs [aria-selected="true"]    { background:#6366f1 !important; color:#fff !important; }
div[data-testid="stExpander"]     { background:#141728; border:1px solid #1e2235; border-radius:12px; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════
DB_PATH = "resume_pro.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            ID                  INTEGER PRIMARY KEY AUTOINCREMENT,
            Name                TEXT,
            Email_ID            TEXT,
            resume_score        INTEGER,
            ats_score           INTEGER,
            Timestamp           TEXT,
            Page_no             TEXT,
            Predicted_Field     TEXT,
            User_level          TEXT,
            Actual_skills       TEXT,
            Recommended_skills  TEXT,
            Recommended_courses TEXT,
            skills_count        INTEGER
        )
    """)
    conn.commit(); conn.close()

def insert_data(name, email, res_score, ats_score, timestamp, no_pages,
                field, level, skills, rec_skills, courses):
    conn = get_conn()
    conn.execute("""
        INSERT INTO user_data
        (Name,Email_ID,resume_score,ats_score,Timestamp,Page_no,
         Predicted_Field,User_level,Actual_skills,Recommended_skills,
         Recommended_courses,skills_count)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
    """, (name, email, res_score, ats_score, timestamp, str(no_pages),
          field, level, str(skills), str(rec_skills), str(courses), len(skills)))
    conn.commit(); conn.close()

# ══════════════════════════════════════════════════
# PDF UTILITIES
# ══════════════════════════════════════════════════
def pdf_reader(path):
    rm   = PDFResourceManager()
    buf  = io.StringIO()
    conv = TextConverter(rm, buf, laparams=LAParams())
    interp = PDFPageInterpreter(rm, conv)
    with open(path, 'rb') as fh:
        for page in PDFPage.get_pages(fh, caching=True, check_extractable=True):
            interp.process_page(page)
    text = buf.getvalue(); conv.close(); buf.close()
    return text

def count_pages(path):
    n = 0
    with open(path, 'rb') as fh:
        for _ in PDFPage.get_pages(fh): n += 1
    return n

def show_pdf(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{b64}" '
        f'width="100%" height="750" type="application/pdf"></iframe>',
        unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# REAL-WORLD RECOMMENDATION ENGINE
# ══════════════════════════════════════════════════
FIELD_PROFILES = {
    "Data Science & ML": {
        "keywords": {'tensorflow','keras','pytorch','machine learning','deep learning',
                     'scikit-learn','data science','nlp','xgboost','pandas','numpy',
                     'matplotlib','seaborn','data mining','data analytics'},
        "core_skills": [
            ("Python",10),("Machine Learning",10),("SQL",9),("Statistics",9),
            ("Data Visualization",8),("Pandas / NumPy",8),("Scikit-learn",7),
            ("TensorFlow / PyTorch",7),("Feature Engineering",6),("A/B Testing",6),
            ("Big Data (Spark)",5),("MLOps",5),("NLP",5),("Cloud (AWS/GCP)",5),("Git",4),
        ],
        "nice_to_have": ["Docker","Kubernetes","Airflow","dbt","Tableau","Power BI","R"],
        "salaries": [
            ("Data Analyst",       "₹4L – ₹10L / yr",  "$55k – $90k / yr"),
            ("Data Scientist",     "₹8L – ₹22L / yr",  "$90k – $140k / yr"),
            ("ML Engineer",        "₹12L – ₹30L / yr", "$120k – $180k / yr"),
            ("Senior DS / Lead",   "₹25L – ₹55L / yr", "$150k – $220k / yr"),
        ],
        "roadmap": [
            ("Month 1–2",  "Master Python, Pandas, NumPy & SQL basics"),
            ("Month 3–4",  "Statistics, probability, EDA & visualisation"),
            ("Month 5–6",  "Supervised & unsupervised ML with Scikit-learn"),
            ("Month 7–8",  "Deep Learning — TensorFlow / PyTorch"),
            ("Month 9–10", "Kaggle competitions & end-to-end pipelines"),
            ("Month 11–12","MLOps, cloud deployment & portfolio polish"),
        ],
        "ats_keywords": ["machine learning","data science","python","sql","tensorflow",
                         "model","analysis","pipeline","feature","accuracy"],
        "courses": ds_course,
    },
    "Web Development": {
        "keywords": {'react','django','node js','node.js','php','laravel','wordpress',
                     'javascript','angular','angular js','c#','html','css','typescript',
                     'graphql','rest api','bootstrap','vue','next.js','fastapi'},
        "core_skills": [
            ("HTML / CSS",10),("JavaScript",10),("React / Vue / Angular",9),
            ("Node.js / Django",8),("REST API Design",8),("Git & CI/CD",7),
            ("TypeScript",7),("SQL / NoSQL DB",7),("Testing (Jest/Pytest)",6),
            ("Docker Basics",6),("Cloud Deploy",5),("GraphQL",4),
            ("Performance Opt.",5),("Accessibility",4),("Security Basics",5),
        ],
        "nice_to_have": ["Redis","WebSockets","Microservices","Kubernetes","Terraform"],
        "salaries": [
            ("Junior Frontend Dev",  "₹3L – ₹8L / yr",   "$50k – $80k / yr"),
            ("Full-Stack Developer", "₹7L – ₹20L / yr",  "$85k – $130k / yr"),
            ("Backend Engineer",     "₹8L – ₹22L / yr",  "$90k – $140k / yr"),
            ("Senior Web Engineer",  "₹20L – ₹45L / yr", "$130k – $200k / yr"),
        ],
        "roadmap": [
            ("Week 1–4",   "HTML, CSS, JavaScript fundamentals"),
            ("Week 5–8",   "React / Vue — components, state, hooks"),
            ("Week 9–12",  "Node.js + Express + REST API"),
            ("Week 13–16", "Databases — PostgreSQL & MongoDB"),
            ("Week 17–20", "Auth, testing & Docker basics"),
            ("Week 21–24", "Full-stack project + cloud deployment"),
        ],
        "ats_keywords": ["javascript","react","node","api","frontend","backend","fullstack",
                         "html","css","database","agile","git"],
        "courses": web_course,
    },
    "Android Development": {
        "keywords": {'android','android development','flutter','kotlin','xml','kivy',
                     'java','sdk','firebase','gradle','jetpack'},
        "core_skills": [
            ("Kotlin",10),("Android SDK",10),("Jetpack Compose",9),("MVVM Architecture",8),
            ("REST APIs (Retrofit)",8),("Firebase",7),("Room Database",7),("Git",7),
            ("Unit Testing",6),("Play Store Publish",6),("Coroutines/Flow",6),
            ("Hilt DI",5),("Flutter (bonus)",5),("CI/CD",4),("Material Design",5),
        ],
        "nice_to_have": ["React Native","Compose Multiplatform","ML Kit","ARCore"],
        "salaries": [
            ("Junior Android Dev",  "₹3L – ₹8L / yr",   "$55k – $85k / yr"),
            ("Android Developer",   "₹7L – ₹18L / yr",  "$80k – $125k / yr"),
            ("Senior Android Dev",  "₹15L – ₹35L / yr", "$120k – $175k / yr"),
            ("Android Tech Lead",   "₹28L – ₹55L / yr", "$160k – $220k / yr"),
        ],
        "roadmap": [
            ("Month 1", "Kotlin language fundamentals"),
            ("Month 2", "Android SDK — activities, fragments, layouts"),
            ("Month 3", "Jetpack Compose + ViewModel + LiveData"),
            ("Month 4", "Retrofit, Room, Hilt DI"),
            ("Month 5", "Firebase, testing, Play Store submission"),
            ("Month 6", "Publish a real app + open-source contributions"),
        ],
        "ats_keywords": ["kotlin","android","jetpack","firebase","mvvm","sdk",
                         "compose","retrofit","gradle","mobile"],
        "courses": android_course,
    },
    "iOS Development": {
        "keywords": {'ios','ios development','swift','cocoa','cocoa touch','xcode',
                     'objective-c','storekit','swiftui','core data','uikit'},
        "core_skills": [
            ("Swift",10),("SwiftUI / UIKit",10),("Xcode",9),("Core Data",8),
            ("REST APIs (URLSession)",8),("MVVM Pattern",7),("App Store Publish",7),
            ("Git",7),("Testing (XCTest)",6),("Combine Framework",6),
            ("Instruments",5),("Core Animation",5),("Push Notifications",5),
            ("In-App Purchases",4),("ARKit (bonus)",4),
        ],
        "nice_to_have": ["React Native","Flutter","Firebase","CloudKit","Metal"],
        "salaries": [
            ("Junior iOS Dev",       "₹4L – ₹9L / yr",   "$60k – $90k / yr"),
            ("iOS Developer",        "₹8L – ₹20L / yr",  "$90k – $135k / yr"),
            ("Senior iOS Developer", "₹18L – ₹40L / yr", "$130k – $185k / yr"),
            ("iOS Tech Lead",        "₹32L – ₹60L / yr", "$170k – $230k / yr"),
        ],
        "roadmap": [
            ("Month 1", "Swift — optionals, closures, protocols"),
            ("Month 2", "UIKit fundamentals — table views, auto-layout"),
            ("Month 3", "SwiftUI + Combine + MVVM"),
            ("Month 4", "Core Data, URLSession, authentication"),
            ("Month 5", "Testing, Instruments, App Store submission"),
            ("Month 6", "Ship a real app + portfolio + open source"),
        ],
        "ats_keywords": ["swift","ios","xcode","uikit","swiftui","objective-c",
                         "apple","mobile","core data","app store"],
        "courses": ios_course,
    },
    "UI/UX Design": {
        "keywords": {'ux','adobe xd','figma','zeplin','balsamiq','ui','prototyping',
                     'wireframes','photoshop','illustrator','after effects','indesign',
                     'user research','user experience','interaction design'},
        "core_skills": [
            ("Figma",10),("User Research",10),("Wireframing",9),("Prototyping",9),
            ("Visual Design",8),("Usability Testing",8),("Design Systems",7),
            ("Adobe XD / Sketch",7),("Information Architecture",7),("Accessibility",6),
            ("Interaction Design",6),("Motion Design",5),("Front-end basics",5),
            ("Data-driven Design",5),("Stakeholder Communication",6),
        ],
        "nice_to_have": ["After Effects","Principle","Lottie","HTML/CSS","Miro","FigJam"],
        "salaries": [
            ("Junior UX Designer",    "₹3L – ₹7L / yr",   "$45k – $75k / yr"),
            ("UX / Product Designer", "₹7L – ₹18L / yr",  "$75k – $120k / yr"),
            ("Senior UX Designer",    "₹14L – ₹32L / yr", "$110k – $160k / yr"),
            ("Design Lead / Head",    "₹25L – ₹55L / yr", "$150k – $220k / yr"),
        ],
        "roadmap": [
            ("Week 1–3",   "Design principles, typography, colour theory"),
            ("Week 4–6",   "Figma fundamentals — frames, components, auto-layout"),
            ("Week 7–10",  "User research — interviews, surveys, personas"),
            ("Week 11–14", "Wireframing, information architecture, flow maps"),
            ("Week 15–18", "Prototyping, usability testing, iteration"),
            ("Week 19–24", "End-to-end case studies for portfolio"),
        ],
        "ats_keywords": ["figma","ux","user experience","design","prototype","research",
                         "wireframe","accessibility","ui","product"],
        "courses": uiux_course,
    },
}

ALL_SKILLS = set()
for p in FIELD_PROFILES.values():
    ALL_SKILLS |= p["keywords"]
    ALL_SKILLS |= {s.lower() for s, _ in p["core_skills"]}
    ALL_SKILLS |= {s.lower() for s in p.get("nice_to_have", [])}
ALL_SKILLS |= {'git','github','docker','kubernetes','aws','azure','gcp','linux',
               'agile','scrum','jira','postgresql','mongodb','redis','r','python',
               'java','c++','bash','terraform','jenkins','sql'}

@st.cache_resource
def load_nlp():
    try:    return spacy.load("en_core_web_sm")
    except OSError:
        st.error("Run: python -m spacy download en_core_web_sm"); st.stop()

def extract_skills(text):
    # Remove unicode icons
    clean = re.sub(r'[\uf000-\uf8ff]', ' ', text)
    # Fix jammed words like "PythonMachine LearningDeep Learning"
    clean = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', clean)
    tl = clean.lower()
    found = []
    for skill in sorted(ALL_SKILLS, key=len, reverse=True):
        if re.search(r'\b' + re.escape(skill) + r'\b', tl):
            found.append(skill)
    return list(dict.fromkeys(found))

def extract_email(text):
    # Strip unicode icon characters before scanning
    clean = re.sub(r'[\uf000-\uf8ff]', ' ', text)
    m = re.findall(r'[\w\.\-]+@[\w\.\-]+\.\w+', clean)
    return m[0] if m else "Not found"

def extract_phone(text):
    # Strip unicode icon characters
    clean = re.sub(r'[\uf000-\uf8ff]', ' ', text)
    m = re.findall(r'(\+?\d[\d\s\-\(\)]{7,}\d)', clean)
    if m:
        # Remove all spaces inside the number
        return re.sub(r'\s+', '', m[0].strip())
    return "Not found"

def extract_name(text):
    BLACKLIST = {
        'resume','curriculum','vitae','cv','page','objective','summary',
        'profile','address','phone','email','contact','linkedin','github',
        'skills','education','experience','projects','certifications',
        'achievements','hobbies','interests','references','declaration',
        'india','usa','uk','australia','canada','germany','france','china',
        'python','java','react','sql','html','css','javascript','android',
        'swift','kotlin','figma','aws','docker','git','tableau','excel',
        'bachelor','master','engineer','developer','designer','analyst',
        'fresher','student','intern','manager','lead','senior','junior',
        'university','college','institute','school','department',
        'scientist','founder','consultant','instructor','teacher',
        'researcher','architect','specialist','coordinator','director',
        'ios','mobile','web','data','science','machine','learning',
        'technology','solutions','llc','inc','ltd','pvt','corp',
        'international','national','global','languages','chines',
    }

    clean = re.sub(r'[\uf000-\uf8ff]', '', text)
    full_spaced = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', clean)

    # ── Strategy 1: line-by-line scan (single-column resumes) ──
    lines = [l.strip() for l in full_spaced.splitlines() if l.strip()]
    for line in lines[:20]:
        if re.search(r'[\d@|•/\\:_+#,]', line): continue
        if re.search(r'http|www|\.com|\.in|\.io', line, re.IGNORECASE): continue
        words = line.split()
        if not (2 <= len(words) <= 4): continue
        if not all(w[0].isupper() for w in words if w): continue
        if any(w.lower().strip('-') in BLACKLIST for w in words): continue
        if not all(re.match(r"^[A-Za-z\-']+$", w) for w in words): continue
        return line

    # ── Strategy 2: two-column resume — name before page-break + ALL CAPS title ──
    m = re.search(r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s+[A-Z\s]{4,}\x0c', full_spaced)
    if m:
        candidate = m.group(1).strip()
        words = candidate.split()
        if not any(w.lower() in BLACKLIST for w in words):
            return candidate

    # ── Strategy 3: name before ALL-CAPS title anywhere in text ──
    matches = re.findall(r'\b([A-Z][a-z]{1,20}\s+[A-Z][a-z]{1,20})\s+(?:[A-Z]{2,}\s*){2,}', full_spaced)
    for candidate in matches:
        words = candidate.strip().split()
        if any(w.lower() in BLACKLIST for w in words): continue
        if all(re.match(r"^[A-Za-z\-']+$", w) for w in words):
            return candidate.strip()

    return "Candidate"
def parse_resume(path):
    text  = pdf_reader(path); pages = count_pages(path)
    return {"name": extract_name(text), "email": extract_email(text),
            "mobile_number": extract_phone(text), "skills": extract_skills(text),
            "no_of_pages": pages, "_raw": text}

# ── Scoring ──────────────────────────────────────
def score_skills_for_field(user_skills_lower, field_name):
    core    = FIELD_PROFILES[field_name]["core_skills"]
    total_w = sum(w for _, w in core); earned = 0
    matched = []; missing = []
    for skill, weight in core:
        if any(skill.lower() in s or s in skill.lower() for s in user_skills_lower):
            earned += weight; matched.append(skill)
        else:
            missing.append((skill, weight))
    return (round((earned/total_w)*100),
            matched,
            [s for s, _ in sorted(missing, key=lambda x: -x[1])])

def detect_field(user_skills_lower):
    best_field, best_score = None, 0
    for field, profile in FIELD_PROFILES.items():
        overlap = sum(
            1 for kw in profile["keywords"]
            if any(kw in s or s in kw for s in user_skills_lower)
        )
        if overlap > best_score:
            best_score, best_field = overlap, field
    return best_field if best_score > 0 else None

def resume_section_score(text):
    checks = [
        ("Objective / Summary",
         ["objective","summary","career goal","professional summary","about me","profile"],
         "A strong summary boosts recruiter attention by 40%", 15),
        ("Work Experience",
         ["experience","employment","work history","professional experience",
          "internship","intern","worked at"],
         "Use bullet points with quantified achievements", 20),
        ("Education",
         ["education","degree","university","college","bachelor","master",
          "phd","mba","b.tech","graduated","school"],
         "Include GPA if above 3.5 / 8.0", 15),
        ("Skills Section",
         ["skills","technical skills","core competencies","expertise",
          "key skills","technologies","tools"],
         "Dedicated skills section is critical for ATS", 15),
        ("Projects",
         ["project","portfolio","built","developed","created","capstone","thesis"],
         "Showcase 2–3 impactful projects with GitHub links", 15),
        ("Achievements",
         ["achievement","award","winner","honor","recognition","percentile","gpa","rank"],
         "Quantify: 'increased sales by 30%' beats 'improved sales'", 10),
        ("Certifications",
         ["certification","certified","certificate","credential","coursera","ibm","udemy"],
         "Certifications validate skills and boost credibility", 5),
        ("Hobbies / Interests",
         ["hobbies","interests","activities","volunteer","extracurricular","additional"],
         "Shows personality — keep to 1–2 relevant interests", 5),
    ]
    score = 0; result = []; tl = text.lower()
    for label, kws, tip, pts in checks:
        found = any(k in tl for k in kws)
        if found: score += pts
        result.append({"label": label, "found": found, "tip": tip, "pts": pts})
    return score, result

def ats_score(text, field_name):
    if not field_name or field_name not in FIELD_PROFILES: return 50
    kws  = FIELD_PROFILES[field_name]["ats_keywords"]
    tl   = text.lower()
    hits = sum(1 for k in kws if k in tl)
    return min(100, round((hits / len(kws)) * 100))

def get_yt_title(url):
    try:
        import urllib.request, json as _j
        vid = None
        for pat in [r'v=([^&]+)', r'youtu\.be/([^?]+)']:
            m = re.search(pat, url)
            if m: vid = m.group(1); break
        if not vid: return url
        api = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
        with urllib.request.urlopen(api, timeout=4) as r:
            return _j.loads(r.read()).get("title", url)
    except Exception:
        return url

def get_download_link(df, fname, label):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{fname}">{label}</a>'

# ══════════════════════════════════════════════════
# CHART HELPERS
# ══════════════════════════════════════════════════
COLORS = ["#6366f1","#ec4899","#10b981","#f59e0b","#3b82f6","#8b5cf6","#ef4444"]
BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#c8cfe0"),
    margin=dict(t=40, b=20, l=20, r=20),
)

def radar_chart(user_lower, field):
    core = FIELD_PROFILES[field]["core_skills"][:10]
    labels = [s for s,_ in core]
    user_v = [w if any(s.lower() in us or us in s.lower() for us in user_lower) else 0
              for s,w in core]
    ideal_v = [w for _,w in core]
    labels += [labels[0]]; user_v += [user_v[0]]; ideal_v += [ideal_v[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=ideal_v, theta=labels, fill='toself', name='Market Ideal',
        fillcolor='rgba(99,102,241,.12)', line=dict(color='#6366f1', width=2, dash='dot')))
    fig.add_trace(go.Scatterpolar(r=user_v, theta=labels, fill='toself', name='Your Skills',
        fillcolor='rgba(236,72,153,.18)', line=dict(color='#ec4899', width=2)))
    fig.update_layout(**BASE_LAYOUT, height=380,
        polar=dict(bgcolor='rgba(20,23,40,.6)',
            radialaxis=dict(visible=True, range=[0,10], color='#3a3f5c', gridcolor='#1e2235'),
            angularaxis=dict(color='#3a3f5c', gridcolor='#1e2235')),
        legend=dict(bgcolor='rgba(0,0,0,0)', font_color='#8892a4'))
    return fig

def gauge(score, label):
    colour = "#10b981" if score>=75 else "#f59e0b" if score>=50 else "#ef4444"
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score, domain=dict(x=[0,1], y=[0,1]),
        gauge=dict(axis=dict(range=[0,100], tickcolor='#3a3f5c', tickfont_color='#8892a4'),
            bar=dict(color=colour, thickness=0.3), bgcolor='rgba(20,23,40,.8)', borderwidth=0,
            steps=[dict(range=[0,50],  color='rgba(239,68,68,.08)'),
                   dict(range=[50,75], color='rgba(245,158,11,.08)'),
                   dict(range=[75,100],color='rgba(16,185,129,.08)')],
            threshold=dict(line=dict(color=colour, width=3), value=score)),
        number=dict(font=dict(size=42, color=colour, family="DM Serif Display")),
        title=dict(text=label, font=dict(size=13, color="#8892a4"))))
    fig.update_layout(**BASE_LAYOUT, height=260)
    return fig

def skill_gap_bar(user_lower, field):
    core = FIELD_PROFILES[field]["core_skills"][:12]
    labels = [s for s,_ in core]
    user_v  = [w if any(s.lower() in us or us in s.lower() for us in user_lower) else 0
                for s,w in core]
    ideal_v = [w for _,w in core]
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Market Demand', x=labels, y=ideal_v,
                         marker_color='rgba(99,102,241,.35)', marker_line_width=0))
    fig.add_trace(go.Bar(name='Your Level',    x=labels, y=user_v,
                         marker_color='#ec4899', marker_line_width=0))
    fig.update_layout(**BASE_LAYOUT, barmode='overlay', height=320,
        xaxis=dict(tickangle=-30, gridcolor='#1e2235'),
        yaxis=dict(gridcolor='#1e2235', range=[0,11]),
        legend=dict(bgcolor='rgba(0,0,0,0)'))
    return fig

def roadmap_chart(field):
    steps = FIELD_PROFILES[field]["roadmap"]
    fig   = go.Figure()
    for i, (period, task) in enumerate(steps):
        c = COLORS[i % len(COLORS)]
        fig.add_trace(go.Scatter(
            x=[i], y=[0], mode='markers+text',
            marker=dict(size=20, color=c, line=dict(color='#0d0f1a', width=3)),
            text=[str(i+1)], textposition='middle center',
            textfont=dict(color='#fff', size=10),
            hovertext=f"<b>{period}</b><br>{task}", hoverinfo='text', showlegend=False))
        fig.add_annotation(x=i, y=0.38 if i%2==0 else -0.38,
            text=f"<b>{period}</b><br><span style='font-size:10px;color:#8892a4'>{task}</span>",
            showarrow=True, arrowhead=0, arrowcolor=c, arrowwidth=1,
            ay=-55 if i%2==0 else 55,
            font=dict(size=10, color='#c8cfe0'),
            bgcolor='rgba(20,23,40,.85)', bordercolor=c, borderwidth=1, borderpad=6)
    fig.add_shape(type='line', x0=-.3, x1=len(steps)-.7, y0=0, y1=0,
                  line=dict(color='#1e2235', width=2))
    fig.update_layout(**BASE_LAYOUT, height=320,
        xaxis=dict(visible=False, range=[-.5, len(steps)-.5]),
        yaxis=dict(visible=False, range=[-1, 1]))
    return fig

# ══════════════════════════════════════════════════
# BOOT
# ══════════════════════════════════════════════════
os.makedirs("Uploaded_Resumes", exist_ok=True)
init_db()

# ── Sidebar ──────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:20px 0 10px;">
        <span style="font-size:2.2rem;">🎯</span>
        <div style="font-family:'DM Serif Display',serif;font-size:1.2rem;color:#e2e8f0;margin-top:6px;">Resume Analyser</div>
        <div style="font-size:.72rem;color:#4b5563;letter-spacing:.1em;margin-top:2px;">PRO EDITION</div>
    </div>""", unsafe_allow_html=True)
    st.markdown("---")
    mode = st.radio("", ["👤  Candidate", "🔐  Admin"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("""
    <div style="font-size:.78rem;color:#4b5563;padding:10px 0;">
        <b style="color:#6b7280;">How it works</b><br><br>
        1️⃣ Upload your PDF resume<br><br>
        2️⃣ AI scans skills & sections<br><br>
        3️⃣ Get field prediction, gap analysis,
        salary ranges &amp; curated courses<br><br>
        4️⃣ Track progress over time
    </div>""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">AI Resume Analyser</div>
    <p class="hero-sub">
        Real-world skill gap analysis &nbsp;·&nbsp; Market salary benchmarks &nbsp;·&nbsp;
        ATS compatibility &nbsp;·&nbsp; Career roadmaps
    </p>
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════
# CANDIDATE
# ══════════════════════════════════════════════════
if "👤" in mode:
    pdf_file = st.file_uploader("📄 Drop your resume here (PDF)", type=["pdf"],
        help="Text-based PDF works best. Scanned images may give incomplete results.")

    if pdf_file:
        save_path = os.path.join("Uploaded_Resumes", pdf_file.name)
        with open(save_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        with st.spinner("🔍 Analysing your resume…"):
            data = parse_resume(save_path); raw  = data["_raw"]
            load_nlp()

        field = detect_field({s.lower() for s in data["skills"]})
        sec_score, checks = resume_section_score(raw)
        skill_pct, matched_core, missing_core = (
            score_skills_for_field({s.lower() for s in data["skills"]}, field)
            if field else (0, [], []))
        ats  = ats_score(raw, field)
        pages = data["no_of_pages"]
        cand_level = "Fresher" if pages==1 else "Intermediate" if pages==2 else "Experienced"

        # KPI strip
        cols = st.columns(5)
        for col, num, lbl in zip(cols,
            [len(data["skills"]), f"{sec_score}%", f"{ats}%", pages, cand_level],
            ["Skills Detected","Resume Score","ATS Score","Pages","Experience Level"]):
            col.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div>'
                         f'<div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Profile", "📊 Skill Gap", "🗺️ Roadmap", "📚 Courses", "🎥 Videos"])

        # ── TAB 1: Profile ──────────────────────
        with tab1:
            col_a, col_b = st.columns([1.3, 1])
            with col_a:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">👤 Candidate Profile</div>', unsafe_allow_html=True)
                st.write(f"**Name:** {data['name']}")
                st.write(f"**Email:** {data['email']}")
                st.write(f"**Phone:** {data['mobile_number']}")
                st.write(f"**Pages:** {pages}  ·  **Level:** {cand_level}")
                if field: st.write(f"**Predicted Field:** {field}")
                st.markdown("---")
                st.markdown("**Skills found in your resume:**")
                pills = " ".join(f'<span class="skill-pill pill-have">{s.title()}</span>'
                                 for s in data["skills"][:30])
                st.markdown(pills or "_No skills detected._", unsafe_allow_html=True)
                if missing_core:
                    st.markdown("<br>**High-priority skills to add:**", unsafe_allow_html=True)
                    mp = " ".join(f'<span class="skill-pill pill-need">{s}</span>'
                                  for s in missing_core[:12])
                    st.markdown(mp, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_b:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">📈 Score Dashboard</div>', unsafe_allow_html=True)
                g1, g2 = st.columns(2)
                g1.plotly_chart(gauge(sec_score, "Resume Quality"), use_container_width=True)
                g2.plotly_chart(gauge(ats, "ATS Readiness"),        use_container_width=True)
                if field:
                    st.plotly_chart(gauge(skill_pct, f"Skill Match – {field}"),
                                    use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # Checklist
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">✅ Resume Section Checklist</div>', unsafe_allow_html=True)
            for ch in checks:
                icon  = "✅" if ch["found"] else "❌"
                colour= "#10b981" if ch["found"] else "#ef4444"
                pts   = f'+{ch["pts"]}pts' if ch["found"] else f'Missing ({ch["pts"]}pts)'
                st.markdown(f"""
                <div class="check-row">
                    <span class="check-icon">{icon}</span>
                    <div>
                        <div class="check-text"><b>{ch["label"]}</b>
                            <span style="color:{colour};font-size:.78rem;margin-left:8px;">{pts}</span>
                        </div>
                        <div class="check-tip">{ch["tip"]}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Salary benchmarks
            if field:
                st.markdown('<div class="section-card">', unsafe_allow_html=True)
                st.markdown(f'<div class="section-title">💰 Salary Benchmarks — {field}</div>',
                            unsafe_allow_html=True)
                sc1, sc2 = st.columns(2)
                for i, (role, inr, usd) in enumerate(FIELD_PROFILES[field]["salaries"]):
                    (sc1 if i%2==0 else sc2).markdown(f"""
                    <div class="salary-badge">
                        <div class="salary-role">{role}</div>
                        <div class="salary-range">🇮🇳 {inr}</div>
                        <div class="salary-meta">🌍 {usd}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with st.expander("📄 Preview uploaded resume"):
                show_pdf(save_path)

        # ── TAB 2: Skill Gap ────────────────────
        with tab2:
            if not field:
                st.info("No specific field detected. Add more technical keywords to your resume.")
            else:
                st.markdown(f"### Skill Gap Analysis for **{field}**")
                st.caption("Pink = your current level  ·  Purple = market demand")
                rc, bc = st.columns([1, 1])
                with rc:
                    st.plotly_chart(radar_chart({s.lower() for s in data["skills"]}, field),
                                    use_container_width=True)
                with bc:
                    st.plotly_chart(skill_gap_bar({s.lower() for s in data["skills"]}, field),
                                    use_container_width=True)

                rows = []
                for skill, w in FIELD_PROFILES[field]["core_skills"]:
                    match = any(skill.lower() in s or s in skill.lower()
                                for s in {x.lower() for x in data["skills"]})
                    rows.append({"Skill": skill, "Market Weight": w,
                                 "Status": "✅ Have" if match else "❌ Gap",
                                 "Priority": "HIGH" if w>=8 else "MEDIUM" if w>=6 else "LOW"})
                df_gap = pd.DataFrame(rows)
                st.markdown("#### Detailed Skill Breakdown")
                st.dataframe(
                    df_gap.style
                    .map(lambda v: "color:#10b981" if "Have" in str(v) else
                            ("color:#ef4444" if "Gap" in str(v) else ""), subset=["Status"])
                    .map(lambda v: "color:#f59e0b;font-weight:600" if v=="HIGH" else "",
                            subset=["Priority"]),
                    use_container_width=True, hide_index=True)

                nth = FIELD_PROFILES[field].get("nice_to_have", [])
                if nth:
                    st.markdown("#### 💡 Nice-to-Have (Differentiators)")
                    st.markdown(" ".join(f'<span class="skill-pill pill-have">{s}</span>'
                                         for s in nth), unsafe_allow_html=True)

        # ── TAB 3: Roadmap ──────────────────────
        with tab3:
            if not field:
                st.info("Add technical keywords to your resume to unlock your personalised roadmap.")
            else:
                st.markdown(f"### 🗺️ Career Roadmap — {field}")
                st.caption("Your path from current skills to market-ready.")
                st.plotly_chart(roadmap_chart(field), use_container_width=True)

                steps = FIELD_PROFILES[field]["roadmap"]
                cols  = st.columns(3)
                for i, (period, task) in enumerate(steps):
                    with cols[i%3]:
                        st.markdown(f"""
                        <div class="section-card" style="padding:16px 18px;margin-bottom:12px;">
                            <div style="color:{COLORS[i%len(COLORS)]};font-weight:700;
                                        font-size:.78rem;letter-spacing:.06em;margin-bottom:6px;">
                                {period}
                            </div>
                            <div style="color:#c8cfe0;font-size:.88rem;line-height:1.45;">{task}</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown("#### 🔎 ATS Keywords Status")
                kws = FIELD_PROFILES[field]["ats_keywords"]; tl = raw.lower()
                for kw in kws:
                    present = kw in tl
                    bc2 = "#10b981" if present else "#ef4444"
                    status  = "In resume ✓" if present else "Missing ✗"
                    st.markdown(
                        f'<span class="skill-pill" style="background:rgba(0,0,0,.3);'
                        f'border:1px solid {bc2};color:{bc2};">{kw} — {status}</span>',
                        unsafe_allow_html=True)

        # ── TAB 4: Courses ──────────────────────
        with tab4:
            course_list = FIELD_PROFILES[field]["courses"] if field else ds_course + web_course
            if field: st.markdown(f"### 🎓 Courses for {field}")
            n = st.slider("How many courses to show?", 3, 10, 5)
            random.shuffle(course_list)
            for i, (cname, clink) in enumerate(course_list[:n]):
                free_tag = ('&nbsp;<span style="background:#10b981;color:#fff;font-size:.7rem;'
                            'padding:1px 7px;border-radius:999px;font-weight:600;">FREE</span>'
                            if "[free]" in cname.lower() else "")
                st.markdown(f"""
                <div class="section-card" style="padding:14px 20px;margin-bottom:10px;">
                    <span style="color:#6366f1;font-weight:700;">{i+1:02d}</span>&nbsp;&nbsp;
                    <a href="{clink}" target="_blank" style="color:#818cf8;text-decoration:none;">
                        {cname}</a>{free_tag}
                </div>""", unsafe_allow_html=True)

        # ── TAB 5: Videos ───────────────────────
        with tab5:
            v1, v2 = st.columns(2)
            with v1:
                st.markdown("### ✍️ Resume Writing Tips")
                rvid = random.choice(resume_videos)
                st.caption(f"▶ {get_yt_title(rvid)}")
                st.video(rvid)
            with v2:
                st.markdown("### 🎤 Interview Preparation")
                ivid = random.choice(interview_videos)
                st.caption(f"▶ {get_yt_title(ivid)}")
                st.video(ivid)

        # ── Save ──────────────────────────────────
        ts = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
        insert_data(
            data['name'], data['email'], sec_score, ats, ts, pages,
            field or "Unknown", cand_level, data['skills'],
            missing_core[:8] if field else [],
            [c for c,_ in (FIELD_PROFILES[field]["courses"] if field else [])[:5]]
        )

# ══════════════════════════════════════════════════
# ADMIN
# ══════════════════════════════════════════════════
else:
    st.subheader("🔐 Admin Dashboard")
    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type='password')
        submitted = st.form_submit_button("Login")

    if submitted:
        if u == "admin" and p == "admin123":   # ← change before deploying
            st.success("Welcome, Admin! 👋")
            conn = get_conn()
            df   = pd.read_sql_query("SELECT * FROM user_data", conn)
            conn.close()

            if df.empty:
                st.info("No submissions yet.")
            else:
                df['resume_score'] = pd.to_numeric(df['resume_score'], errors='coerce')
                df['ats_score']    = pd.to_numeric(df['ats_score'],    errors='coerce')
                df['skills_count'] = pd.to_numeric(df['skills_count'], errors='coerce')

                k1,k2,k3,k4 = st.columns(4)
                k1.metric("Total Candidates",  len(df))
                k2.metric("Avg Resume Score",  f"{df['resume_score'].mean():.0f}%")
                k3.metric("Avg ATS Score",     f"{df['ats_score'].mean():.0f}%")
                k4.metric("Avg Skills / Resume",f"{df['skills_count'].mean():.1f}")

                st.markdown("---")

                r1c1, r1c2 = st.columns(2)
                with r1c1:
                    st.subheader("Field Distribution")
                    fc = df['Predicted_Field'].value_counts().reset_index()
                    fc.columns = ['Field','Count']
                    fig = px.pie(fc, values='Count', names='Field',
                                 color_discrete_sequence=COLORS, hole=0.45)
                    fig.update_layout(**BASE_LAYOUT)
                    st.plotly_chart(fig, use_container_width=True)

                with r1c2:
                    st.subheader("Experience Levels")
                    lc = df['User_level'].value_counts().reset_index()
                    lc.columns = ['Level','Count']
                    fig = px.bar(lc, x='Level', y='Count',
                                 color='Level', color_discrete_sequence=COLORS)
                    fig.update_layout(**BASE_LAYOUT,
                        xaxis=dict(gridcolor='#1e2235'),
                        yaxis=dict(gridcolor='#1e2235'))
                    st.plotly_chart(fig, use_container_width=True)

                r2c1, r2c2 = st.columns(2)
                with r2c1:
                    st.subheader("Resume Score Distribution")
                    fig = px.histogram(df, x='resume_score', nbins=10,
                                       color_discrete_sequence=['#6366f1'])
                    fig.update_layout(**BASE_LAYOUT,
                        xaxis=dict(gridcolor='#1e2235', title='Score (%)'),
                        yaxis=dict(gridcolor='#1e2235', title='Count'))
                    st.plotly_chart(fig, use_container_width=True)

                with r2c2:
                    st.subheader("ATS Score Distribution")
                    fig = px.histogram(df, x='ats_score', nbins=10,
                                       color_discrete_sequence=['#ec4899'])
                    fig.update_layout(**BASE_LAYOUT,
                        xaxis=dict(gridcolor='#1e2235', title='ATS Score (%)'),
                        yaxis=dict(gridcolor='#1e2235', title='Count'))
                    st.plotly_chart(fig, use_container_width=True)

                r3c1, r3c2 = st.columns(2)
                with r3c1:
                    st.subheader("Resume Score vs ATS Score")
                    fig = px.scatter(df, x='resume_score', y='ats_score',
                                     color='Predicted_Field', size='skills_count',
                                     hover_data=['Name'], color_discrete_sequence=COLORS)
                    fig.update_layout(**BASE_LAYOUT,
                        xaxis=dict(gridcolor='#1e2235', title='Resume Score'),
                        yaxis=dict(gridcolor='#1e2235', title='ATS Score'))
                    st.plotly_chart(fig, use_container_width=True)

                with r3c2:
                    st.subheader("Submissions Over Time")
                    df['date'] = pd.to_datetime(df['Timestamp'].str[:10], errors='coerce')
                    tl = df.groupby('date').size().reset_index(name='Count')
                    fig = px.line(tl, x='date', y='Count',
                                  color_discrete_sequence=['#10b981'], markers=True)
                    fig.update_layout(**BASE_LAYOUT,
                        xaxis=dict(gridcolor='#1e2235'),
                        yaxis=dict(gridcolor='#1e2235', title='Submissions'))
                    st.plotly_chart(fig, use_container_width=True)

                st.markdown("### 📋 Full Data Table")
                st.dataframe(df, use_container_width=True)
                st.markdown(
                    get_download_link(df, 'resume_data.csv', '⬇️ Download Full Report (CSV)'),
                    unsafe_allow_html=True)
        else:
            st.error("❌ Incorrect credentials.")
