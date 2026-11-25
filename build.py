#!/usr/bin/env python3
"""Build a small static academic website from the shared bibliography."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
DIST = ROOT
# GitHub Pages serves the prebuilt files directly from the repository root.
# Rebuilding writes only the four HTML pages and the empty .nojekyll marker.
(DIST / ".nojekyll").write_text("")
DATA = json.loads((ROOT / "content.json").read_text())
PUBS = DATA["publications"]
e = lambda value: escape(str(value), quote=True)

def link(url, label, cls=""):
    external = ' target="_blank" rel="noopener noreferrer"' if url.startswith("https:") else ""
    return f'<a href="{e(url)}" class="{e(cls)}"{external}>{e(label)}</a>'

def author_names(authors):
    rendered = []
    for author in authors:
        equal = author.endswith("*")
        name = author.rstrip("*")
        name = f"<strong>{e(name)}</strong>" if name == "Nitin Bisht" else e(name)
        rendered.append(name + ("<sup>*</sup>" if equal else ""))
    return ", ".join(rendered)

def publication(p, summary=False):
    paper_links = " ".join(link(v["url"],v["label"]) for v in p.get("links",[]))
    subtitle = e(p["venue"])
    if p.get("note"):
        subtitle += f'<span class="meta-separator">·</span><span class="paper-note">{e(p["note"])}</span>'
    desc = f'<p class="paper-summary">{e(p["summary"])}</p>' if summary and p.get("summary") else ""
    searchable = " ".join([p["title"]," ".join(p["authors"]),p["venue"],p.get("tags","")])
    return f'''<article class="publication" id="paper-{e(p['id'])}" data-kind="{e(p['type'])}" data-search="{e(searchable)}">
      <h3>{e(p["title"])}</h3>
      <p class="authors">{author_names(p["authors"])}</p>
      <p class="paper-meta"><span>{subtitle}</span>{f'<span class="paper-links">{paper_links}</span>' if paper_links else ''}</p>
      {desc}
    </article>'''

def publication_list(kind, summary=False):
    return "".join(publication(p,summary) for p in PUBS if p["type"]==kind)

def heading(title, extra=""):
    return f'<div class="section-heading"><h2>{e(title)}</h2>{extra}</div>'

def row(title, place, date, description=""):
    return f'''<article class="record">
      <div class="record-heading"><h3>{e(title)}</h3><span class="record-date">{e(date)}</span></div>
      <p class="institution">{e(place)}</p>
      {f'<p>{e(description)}</p>' if description else ''}
    </article>'''

def sidebar():
    return f'''<aside class="profile" aria-label="Profile">
      <a class="profile-name" href="/">Nitin Bisht</a>
      <a class="portrait-link" href="/" aria-label="Nitin Bisht home"><img class="portrait" src="/nitin-bisht.jpg" width="200" height="200" alt="Nitin Bisht"></a>
      <div class="profile-details">
      <p class="profile-role">PhD candidate<br><a href="https://www.uts.edu.au/" target="_blank" rel="noopener noreferrer">University of Technology Sydney</a></p>
      <p class="profile-role">Visiting Researcher<br><a href="https://www.eduhk.hk/" target="_blank" rel="noopener noreferrer">The Education University of Hong Kong</a></p>
      <div class="profile-links">{link("mailto:"+DATA["email"],"Mail")}{link(DATA["linkedin"],"LinkedIn")}{link("/nitin-bisht-cv.pdf","CV")}</div>
      <div class="profile-block"><h2>About me</h2><p>I am a PhD candidate at UTS and a Visiting Researcher at EdUHK. Expected PhD completion: April 2027.</p></div>
      <div class="profile-block"><h2>Research interests</h2><p>Uncertainty quantification, statistical risk control, continual learning, recommender systems, and large language models.</p></div>
      <div class="profile-block"><h2>Scholarships</h2><p>ARC Discovery PhD Fellowship and IRS Scholarship, University of Technology Sydney.</p></div>
      </div>
    </aside>'''

def page(slug, title, content, description):
    nav = []
    for path,label in [("","Home"),("publications","Detailed Publications"),("talks","Talks & Others"),("cv","CV")]:
        href = "/"+(path+".html" if path else "")
        current=' aria-current="page"' if path==slug else ""
        nav.append(f'<a href="{href}"{current}>{label}</a>')
    doc=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#163e60">
<meta property="og:title" content="{e(title)} · Nitin Bisht">
<meta property="og:description" content="{e(description)}">
<meta property="og:type" content="website">
<title>{e(title)} · Nitin Bisht</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/style.css">
<script defer src="/site.js"></script>
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="site-shell">
{sidebar()}
<div class="content-column">
<nav class="top-nav" aria-label="Main navigation">{"".join(nav)}</nav>
<main id="main" tabindex="-1" class="{e(slug or 'home')}-page">{content}</main>
<footer class="site-footer"><span>© 2026 Nitin Bisht</span><span>Updated {e(DATA["updated"])}</span></footer>
</div>
</div>
</body>
</html>'''
    dest = DIST / (f"{slug}.html" if slug else "index.html")
    dest.write_text(doc)

profile = f'<p class="research-profile">{e(DATA["profile"])}</p>'
intro = """<p>I am a PhD candidate in Artificial Intelligence at the University of Technology Sydney and a visiting researcher at The Education University of Hong Kong. I expect to complete my PhD in April 2027.</p>"""
selected_ids=["align","care","frag","mida"]
selected="".join(publication(next(p for p in PUBS if p["id"]==pid),True) for pid in selected_ids)
home=f'''

<div class="introduction">{intro}{profile}</div>

<section>{heading("Recent updates")}
<ul class="news-list">
<li><span class="news-date">Nov 2026</span><span>Winner of the <a href="/cv.html#awards">2026 FEIT HDR Excellence Award (Individual)</a>, University of Technology Sydney.</span></li>
<li><span class="news-date">Nov 2026</span><span>Invited talk on <a href="/talks.html">Managing Uncertainty in Personalized Recommendation</a> at the STFG Workshop, IEEE ICDM 2026.</span></li>
<li><span class="news-date">WSDM 2027</span><span><a href="/publications.html#paper-frag">FRAG</a> accepted for oral presentation.</span></li>
<li><span class="news-date">September 2026</span><span><a href="/publications.html#paper-mida">MIDA</a> accepted by IEEE TKDE. Co-first author with Linjiang Guo.</span></li>
<li><span class="news-date">NeurIPS 2026</span><span><a href="/publications.html#paper-align">ALIGN-Rec</a> accepted.</span></li>
</ul></section>
<section>{heading("Selected work",'<a class="section-link" href="/publications.html">All publications</a>')}
{selected}
</section>
<section class="contact-section">{heading("Contact")}<p>For research and professional enquiries, contact me at <a href="mailto:{e(DATA['email'])}">{e(DATA['email'])}</a>.</p></section>
'''
page("","Home",home,DATA["profile"])

publications=f'''
<header class="page-header"><h1>Publications</h1>
<p class="page-intro">Peer-reviewed papers, preprints, and manuscripts.</p></header>
<div class="publication-tools">
<div class="publication-jumps"><a href="#peer-reviewed">Peer-reviewed publications</a><a href="#preprints">Preprints and manuscripts</a></div>
<label for="publication-search">Search publications</label>
<div class="search-row"><input id="publication-search" type="search" placeholder="Title, author, venue or topic" autocomplete="off"><button id="clear-search" type="button" hidden>Clear</button></div>
<p class="search-status" id="search-status" role="status" aria-live="polite"></p>
</div>
<section id="peer-reviewed" class="publication-section">{heading("Peer-reviewed publications")}
{publication_list("reviewed")}
</section>
<section id="preprints" class="publication-section">{heading("Preprints and manuscripts")}
{publication_list("preprint")}
</section>
<p class="empty-results" id="empty-results" hidden>No matching publications. Try another title, author, venue or topic.</p>
<p class="equal-note"><sup>*</sup> Equal contribution.</p>
'''
page("publications","Publications",publications,"Publications and preprints by Nitin Bisht on statistical machine learning, recommender systems and large language models.")

training = f'''<section>{heading("Professional development")}
{row("Technical Alignment Research Accelerator (TARA)","Participant · Hong Kong cohort","Sep–Dec 2026 · In progress","Technical AI safety training based on the ARENA curriculum, covering transformer architectures, mechanistic interpretability, reinforcement learning, and model evaluation.")}
<p>{link("https://www.taraprogram.org/","Programme")}</p></section>'''

talks=f'''
<p class="page-intro">Invited talks, teaching, academic service, and professional development.</p>
<section class="section-card"><h2>Talks</h2>
<ul class="activity-list"><li><strong>November 2026.</strong> <em>Managing Uncertainty in Personalized Recommendation.</em> Invited talk, STFG Workshop, IEEE ICDM 2026. {link("https://icdm-2026-workshop.netlify.app/#nitin-bisht","Programme")}</li></ul>
</section>
<section class="section-card"><h2>Others</h2>
<div class="subsection"><h3>Reviewer</h3><p class="activity-context">NeurIPS · ICML · ICLR · AAAI · KDD · WWW (The Web Conference)</p></div>
<div class="subsection"><h3>Teaching</h3><p class="activity-context">Academic Tutor (casual), University of Technology Sydney, 2024–2026.</p>
<ul class="activity-list"><li>48024 Programming 2</li><li>41181 Information Security and Management</li></ul>
<p class="activity-context">Tutored 200+ students and led deployment of a student-support system serving 500+ students, reducing support response times to 20 minutes.</p></div>
<div class="subsection"><h3>Professional development</h3>
<ul class="activity-list"><li><strong>{link("https://www.taraprogram.org/","Technical Alignment Research Accelerator (TARA)")}.</strong> Participant, Hong Kong cohort. September–December 2026 (in progress).</li></ul>
<p class="activity-context">ARENA-based technical AI safety training in transformers, mechanistic interpretability, reinforcement learning, and model evaluation.</p></div>
</section>
'''
page("talks","Talks & Others",talks,"Invited talks, teaching and academic service by Nitin Bisht.")

education = row("PhD candidate in Artificial Intelligence","University of Technology Sydney","Expected completion: April 2027","Thesis: Advanced Statistical Approaches for Robust Recommender Systems.")
education += row("Medical Imaging and Informatics","IIT Kharagpur","","Thesis: Early Detection of Oral Cancer. Combined thermal imaging and clinical data for classification. DAAD KOSPIE exchange at Leibniz University Hannover.")
experience = row("Visiting Researcher","The Education University of Hong Kong","Jan 2026–present","Research on statistical risk control for sequential knowledge editing in large language models, alongside reliable recommendation and model adaptation.")
experience += row("Research Intern","L3S Research Center, Hannover","Oct 2022–Mar 2023","Used a gene-interaction network to constrain a PyTorch model trained on RNA sequencing data from patients with B-cell precursor acute lymphoblastic leukemia, identifying genes and expression thresholds associated with leukemia subtypes.")
experience += row("Software Developer","Zorang (GSPANN), Gurugram","Jul–Nov 2023","Automated classification and summarization of scanned documents in Python, reducing processing time by 90%. Wrote a scraper to categorize products and recover missing SKU data.")
experience += row("Academic Tutor (casual)","University of Technology Sydney","2024–2026","Tutored 200+ students in 48024 Programming 2 and 41181 Information Security and Management. Led deployment of a student-support system serving 500+ students, reducing support response times to 20 minutes.")
awards = """<ul class="compact-list"><li><strong>2026</strong> · Winner, FEIT HDR Excellence Award (Individual), University of Technology Sydney.</li><li><strong>2023</strong> · ARC Discovery PhD Fellowship and IRS Scholarship, University of Technology Sydney.</li><li><strong>2023</strong> · Leibniz AI &amp; Security Fellowship, L3S Research Center.</li><li><strong>2022</strong> · DAAD Fellowship, German Academic Exchange Service.</li><li><strong>2020</strong> · Foundation for Excellence Scholarship and TITAN Merit Scholarship.</li></ul>"""
cv=f'''
<header class="page-header"><h1>Curriculum vitae</h1></header>
<div class="cv-downloads">
<a class="primary-link" href="/nitin-bisht-cv.pdf" download>CV · PDF</a>
</div>
<section>{heading("Research profile")}{profile}
<p>10+ peer-reviewed publications, including NeurIPS, ICML, AAAI, SIGIR, WSDM, CIKM, and IEEE TKDE.</p></section>
<section>{heading("Education")}{education}</section>
<section>{heading("Research and professional experience")}{experience}</section>
<section>{heading("Peer-reviewed publications")}{publication_list("reviewed")}<p class="equal-note"><sup>*</sup> Equal contribution.</p></section>
<section>{heading("Preprints and manuscripts")}{publication_list("preprint")}</section>
<section>{heading("Invited talks")}<p><strong>Managing Uncertainty in Personalized Recommendation.</strong> STFG Workshop, IEEE ICDM 2026. Invited talk, 12 November 2026. {link("https://icdm-2026-workshop.netlify.app/#nitin-bisht","Programme")}</p></section>
{training}
<section id="awards">{heading("Fellowships and awards")}{awards}</section>
<section>{heading("Academic service")}<p>Reviewer for ICLR, ICML, NeurIPS, KDD, AAAI, and WWW (The Web Conference).</p></section>
<section>{heading("Technical skills")}
<dl class="skills-list"><div><dt>Programming</dt><dd>Python, C++, Java, Git</dd></div><div><dt>ML and data</dt><dd>PyTorch, scikit-learn, NumPy, pandas, OpenCV</dd></div><div><dt>Methods</dt><dd>Conformal prediction, statistical risk control, recommendation, retrieval-augmented generation, knowledge editing, machine unlearning, and parameter-efficient adaptation.</dd></div></dl>
</section>
<section>{heading("References")}<p>References available upon request.</p></section>
'''
page("cv","Curriculum vitae",cv,"Nitin Bisht's academic CV, research and engineering experience, publications, talks, teaching and awards.")
print("Built Home, Publications, Talks and CV.")

