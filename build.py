"""Builds the website from src/template.html (home), pages.py (subpages) and src/styles.css.

  python3 build.py              -> prod/     the full static site for www.resolvedcx.com
  SITE_URL=https://x.github.io/resolvedcx-website python3 build.py
                                -> prod/     a preview copy for that address (hidden from search engines)
  python3 build.py --preview    -> preview/index.html, a single-file version used for Claude previews

Standard-library Python only; nothing to install.
"""
import re, json, os, shutil, sys, html, datetime
from urllib.parse import urlparse
R = os.path.dirname(os.path.abspath(__file__)) + '/'
sys.path.insert(0, R)
import importlib, pages
importlib.reload(pages)

T = open(R + 'src/template.html').read()
M = json.load(open(R + 'static/i/manifest.json'))
# Pages from the old Squarespace site, sent to their closest new equivalent
OLD_URLS = {'/home/': '/', '/solutions/': '/services/customer-support/', '/team/': '/#story', '/contact-us/': '/#contact',
            '/blog/': '/', '/blog/how-to-know-when-to-outsource-1/': '/', '/blog/h92cukvb73ioozng72gxsg6wbj96jk/': '/',
            '/case-studies/': '/', '/case-studies/hubble/': '/', '/case-studies/cheers/': '/', '/case-studies/willow/': '/'}

# ---- settings to fill in before launch --------------------------------------------
FORM_ENDPOINT = 'https://formsubmit.co/ajax/michael@resolvedcx.com'   # FormSubmit relays each inquiry to this inbox
GA_ID = ''           # Google Analytics 4 ID, e.g. G-XXXXXXX (nothing loads while empty)
# -------------------------------------------------------------------------------------

SITE = os.environ.get('SITE_URL', '').rstrip('/') or pages.SITE
PREVIEW = urlparse(SITE).netloc.lower() not in ('www.resolvedcx.com', 'resolvedcx.com')   # previews are hidden from search engines
if not PREVIEW: SITE = pages.SITE                    # the live site always uses https://www.resolvedcx.com
BASE = urlparse(SITE).path.rstrip('/')          # e.g. /resolvedcx-website on GitHub Pages
TODAY = datetime.date.today().isoformat()
LOGO_SYMBOL = open(R + 'src/logo_symbol.html').read().strip()

FONTS = '\n'.join(l for l in T.split('\n')[:5] if 'fonts.g' in l)
RESET = '\n/* Base reset (the Artifact preview supplies this; production needs it) */\nbody{margin:0}\nimg{max-width:100%}\n[hidden]{display:none!important}\n.leader img,.ceo img{height:auto}\n[id]{scroll-margin-top:84px}\n'
CSS = open(R + 'src/styles.css').read() + RESET
MAIN = re.search(r'<main id="top">(.*?)</main>', T, re.S).group(1)
LEGAL = {m.group(1): m.group(0) for m in re.finditer(r'<article class="legal" id="(\w+)" hidden>.*?</article>', T, re.S)}
CONTACT = re.search(r'  <section class="block" id="contact".*?</section>', MAIN, re.S).group(0)
CHECK = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3.5 8.5l3 3 6-7" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# ------------------------------------------------------------------ home main edits
main = MAIN
main = main.replace('''  <section class="block" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Who we work with</p>''', '''  <section class="block" id="industries" style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <div>
          <p class="eyebrow">Who we work with</p>''', 1)
for label, slug in pages.INDUSTRY_LINK.items():
    main = re.sub(r'(<div class="ind"><h3>' + re.escape(label) + r'</h3>.*?</span>)(</div>)',
                  lambda m: m.group(1) + f'<a class="more" href="@page:{slug}">Learn more →</a>' + m.group(2), main, count=1, flags=re.S)
tiers = re.search(r'      <div class="tiers">.*?</div>\n', main).group(0)
main = main.replace(tiers, tiers + pages.SERVICE_LINKS + '\n', 1)
quote_anchor = '''  <section class="block" style="padding-top:0">
    <div class="wrap">
      <figure class="quote">'''
assert quote_anchor in main
# Results section removed (Michael, Sept 2026)
main = main.replace('<a class="btn btn-primary" href="#contact">Apply to join</a>', '<a class="btn btn-primary" href="@page:careers">See open roles</a>')
assert '@page:careers' in main

# ------------------------------------------------------------------ header / footer
NAV = [('Services', '@home:services'), ('Industries', '@home:industries'), ('How it works', '@home:how'),
       ('Our story', '@home:story'), ('Careers', '@page:careers'), ('FAQ', '@home:faq')]
HEADER = f'''<header class="nav">
  <div class="wrap">
    <a class="logo" href="@home:top" aria-label="ResolvedCX home">
      <svg viewBox="0 0 918 293" aria-hidden="true" focusable="false"><use href="#rcx-logo" width="918" height="293"/></svg><span class="vh">ResolvedCX</span>
    </a>
    <nav class="nav-links" aria-label="Primary">
      {''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)}
    </nav>
    <a class="btn btn-primary" href="@contact">Talk to us</a>
    <button type="button" class="menu-btn" id="menu-btn" aria-expanded="false" aria-controls="mobile-menu" aria-label="Open menu"><span></span><span></span></button>
  </div>
  <nav class="mobile-menu" id="mobile-menu" aria-label="Mobile" hidden>
    {''.join(f'<a href="{h}">{t}</a>' for t, h in NAV)}<a href="@contact">Contact</a>
  </nav>
</header>'''
FOOTER = f'''<footer>
  <div class="wrap">
    <a class="logo" href="@home:top" aria-label="ResolvedCX home" style="font-size:18px">
      <svg viewBox="0 0 918 293" aria-hidden="true" focusable="false"><use href="#rcx-logo" width="918" height="293"/></svg><span class="vh">ResolvedCX</span>
    </a>
    <nav aria-label="Footer">
      <a href="@page:customer-support">Customer support</a><a href="@page:virtual-assistants">Virtual assistants</a><a href="@page:back-office">Back office</a><a href="@page:ecommerce">Ecommerce</a><a href="@page:health-wellness">Health &amp; wellness</a><a href="@page:software">Software</a><a href="@page:careers">Careers</a><a href="@legal:privacy">Privacy</a><a href="@legal:terms">Terms</a><a href="@legal:security">Security</a><a class="social" href="https://www.linkedin.com/company/resolvedcx/" target="_blank" rel="noopener"><svg viewBox="0 0 16 16" aria-hidden="true"><path fill="currentColor" d="M3.6 5.6H1.2V14h2.4V5.6zM2.4 1.6a1.4 1.4 0 100 2.8 1.4 1.4 0 000-2.8zM14.8 9.3c0-2.3-.5-4-3.2-4-1.3 0-2.1.7-2.5 1.3v-1H6.8V14h2.4V9.8c0-1.1.2-2.2 1.6-2.2 1.3 0 1.4 1.3 1.4 2.3V14h2.4V9.3z"/></svg>LinkedIn</a>
    </nav>
    <span>Brooklyn, NY · Remote across the Philippines and Latin America<br>© 2026 Customer Service Excellence LLC, d/b/a ResolvedCX</span>
  </div>
</footer>'''

# ------------------------------------------------------------------ images
SIZES = {
    'band': '100vw', 'canopy': '(max-width:700px) 100vw, 780px', 'why': '(max-width:860px) 100vw, 440px',
    'vet': '(max-width:860px) 100vw, 480px', 'story': '(max-width:860px) 100vw, 480px', 'careers': '(max-width:860px) 100vw, 520px',
}
SMALL = '(max-width:700px) 50vw, 390px'

def rimg(p, name, alt, sizes=None, eager=False, extra=''):
    m = M[name]; ws = m['widths']; big = ws[-1]
    h = round(m['h'] * big / m['w'])
    mid = ws[len(ws) // 2]
    srcset = ', '.join(f'{p}i/{name}-{w}.webp {w}w' for w in ws)
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{p}i/{name}-{mid}.webp" srcset="{srcset}" sizes="{sizes or SIZES.get(name, SMALL)}" '
            f'width="{big}" height="{h}" alt="{alt}" {load} decoding="async"{extra}>')

def strip_img(p, name, hidden):
    m = M[name]; a, b = m['widths']
    h = 260
    aria = ' aria-hidden="true"' if hidden else ''
    return f'<img src="{p}i/{name}-{a}.webp" srcset="{p}i/{name}-{a}.webp 1x, {p}i/{name}-{b}.webp 2x" width="{a}" height="{h}" alt=""{aria} loading="lazy" decoding="async">'

def images(s, p):
    s = re.sub(r'<img src="img/(\w+)\.jpg" alt="([^"]*)"( loading="lazy")?>',
               lambda m: rimg(p, m.group(1), m.group(2), eager=(m.group(1) == 'band')), s)
    s = re.sub(r'<img src="strip/(\w+)\.jpg" alt=""( aria-hidden="true")? loading="lazy">',
               lambda m: strip_img(p, m.group(1), bool(m.group(2))), s)
    s = re.sub(r'<img src="team/(\w+)\.png" alt="([^"]*)"( loading="lazy")?>',
               lambda m: f'<img src="{p}i/{m.group(1)}-320.webp" srcset="{p}i/{m.group(1)}-160.webp 160w, {p}i/{m.group(1)}-320.webp 320w" sizes="140px" width="320" height="320" alt="{m.group(2)}" loading="lazy" decoding="async">', s)
    s = re.sub(r'<img src="@team:(\w+)" alt="([^"]*)">',
               lambda m: f'<img src="{p}i/{m.group(1)}-320.webp" srcset="{p}i/{m.group(1)}-160.webp 160w, {p}i/{m.group(1)}-320.webp 320w" sizes="140px" width="320" height="320" alt="{m.group(2)}" loading="lazy" decoding="async">', s)
    s = re.sub(r'<img src="@img:([^|]+)\|([^|]*)\|([^|]*)\|([^"]*)">', lambda m: rimg(p, m.group(1), m.group(2), m.group(3) or None), s)
    s = re.sub(r'src="@logo:(\w+)"', lambda m: f'src="{p}logos/{m.group(1)}.{"svg" if m.group(1) == "agelessrx" else "png"}"', s)
    s = s.replace('src="logos/', f'src="{p}logos/')
    assert 'img/' not in re.sub(r'\bi/', '', s).replace('logos/', ''), [x for x in re.findall(r'src="[^"]*img/[^"]*"', s)][:3]
    return s

# ------------------------------------------------------------------ links
def links(s, target, on_home):
    def page(slug): return ('#pg-' + slug) if target == 'preview' else pages.PAGES[slug]['path']
    def home(anchor):
        if target == 'preview': return '#' + anchor
        if anchor == 'top': return '/' if not on_home else '#top'
        return ('#' + anchor) if on_home else '/#' + anchor
    def legal(x): return ('#' + x) if target == 'preview' else f'/{x}/'
    s = re.sub(r'@page:([\w-]+)', lambda m: page(m.group(1)), s)
    s = re.sub(r'@home:([\w-]+)', lambda m: home(m.group(1)), s)
    s = re.sub(r'@legal:([\w-]+)', lambda m: legal(m.group(1)), s)
    s = s.replace('@contact', '#contact')
    if target == 'prod':
        # legacy hash links inside legal articles / main
        for x in ('privacy', 'terms', 'security'):
            s = s.replace(f'href="#{x}"', f'href="/{x}/"')
        if not on_home:
            for a in ('why', 'services', 'how', 'story', 'faq', 'results', 'industries', 'people', 'vetting'):
                s = s.replace(f'href="#{a}"', f'href="/#{a}"')
            s = s.replace('href="#top"', 'href="/"')
    assert '@page:' not in s and '@home:' not in s and '@legal:' not in s
    return s

# ------------------------------------------------------------------ script
JS = r'''
(function(){
  var b=document.getElementById('menu-btn'), m=document.getElementById('mobile-menu');
  if(b&&m){
    function set(open){m.hidden=!open;b.setAttribute('aria-expanded',open?'true':'false');b.setAttribute('aria-label',open?'Close menu':'Open menu');}
    b.addEventListener('click',function(){set(m.hidden);});
    m.addEventListener('click',function(e){if(e.target.tagName==='A') set(false);});
  }
})();
/*ROUTER*/
(function(){
  function fmt(tz){try{return new Intl.DateTimeFormat('en-US',{hour:'numeric',minute:'2-digit',timeZone:tz}).format(new Date());}catch(e){return '';}}
  var ny=document.getElementById('clk-ny'), mn=document.getElementById('clk-mnl');
  function tick(){var a=fmt('America/New_York'), c=fmt('Asia/Manila'); if(a&&ny){ny.innerHTML=a.replace(/ (AM|PM)/,'<small>$1</small>');} if(c&&mn){mn.innerHTML=c.replace(/ (AM|PM)/,'<small>$1</small>');}}
  if(ny||mn){tick(); setInterval(tick,15000);}

  var list=document.getElementById('tickets');
  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if(list&&!reduce){
    var pool=[['email','Charged twice for my last order','Email'],['chat','Is the discount code still active?','Chat'],['phone','Need to pause my subscription for a month','Phone'],['social','DM: "My order says delivered but it isn’t here"','Social'],['email','How do I start a return for a gift?','Email'],['chat','Can you change my shipping address?','Chat']];
    var icons={}; list.querySelectorAll('.ch').forEach(function(el){icons[el.title.toLowerCase()]=el.innerHTML;});
    var n=48218, p=0;
    function setStatus(li,s){var el=li.querySelector('.status'); el.className='status '+s+(s==='resolved'?' just':''); el.textContent=s.charAt(0).toUpperCase()+s.slice(1);}
    setInterval(function(){
      var items=Array.prototype.slice.call(list.children);
      var pend=items.filter(function(li){return li.querySelector('.status.pending');});
      var open=items.filter(function(li){return li.querySelector('.status.open');});
      if(pend.length){setStatus(pend[0],'resolved'); var mt=pend[0].querySelector('.meta'); mt.textContent=mt.textContent.replace(/[^·]+$/,' '+(1+Math.floor(Math.random()*4))+'m');}
      if(open.length){setStatus(open[0],'pending');}
      var first=list.firstElementChild;
      if(first&&first.querySelector('.status.resolved')){
        list.removeChild(first);
        var t=pool[p++%pool.length], li=document.createElement('li'); li.className='ticket';
        li.innerHTML='<span class="ch" title="'+t[2]+'">'+(icons[t[0]]||'')+'</span><span class="msg"></span><span class="status open">Open</span><span class="meta"></span>';
        li.querySelector('.msg').textContent=t[1]; li.querySelector('.meta').textContent='#'+(n++)+' · '+t[2]+' · just now';
        list.appendChild(li);
      }
    },2600);
  }

  var btn=document.getElementById('copy');
  if(btn){btn.addEventListener('click',function(){
    var el=document.getElementById('email'), txt=el.textContent;
    function fallback(){var r=document.createRange();r.selectNodeContents(el);var s=window.getSelection();s.removeAllRanges();s.addRange(r);btn.textContent='Selected';}
    try{navigator.clipboard.writeText(txt).then(function(){btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy';},1800);},fallback);}catch(e){fallback();}
  });}

  // Contact form: posts to FORM_ENDPOINT (FormSubmit), which emails the inquiry to michael@resolvedcx.com.
  var FORM_ENDPOINT='/*ENDPOINT*/';
  var form=document.getElementById('form'), note=document.getElementById('form-note'), t0=Date.now();
  if(form){form.addEventListener('submit',function(e){
    e.preventDefault();
    var name=document.getElementById('f-name').value.trim(), email=document.getElementById('f-email').value.trim();
    if(!name||!/.+@.+\..+/.test(email)){note.textContent='Add your name and a valid work email so we can reach you.';note.hidden=false;return;}
    var hp=document.getElementById('f-web');
    function done(){note.textContent='Thanks, '+name.split(' ')[0]+'. Michael will get back to you within one business day.'; form.reset(); if(window.gtag) gtag('event','generate_lead');}
    if((hp&&hp.value)||Date.now()-t0<2500){done();return;}
    if(!FORM_ENDPOINT){note.textContent='Thanks, '+name.split(' ')[0]+'. This form isn’t connected yet, so please email michael@resolvedcx.com for now.';note.hidden=false;return;}
    var company=document.getElementById('f-company').value.trim();
    var data={Name:name,Email:email,Company:company,'Interested in':document.getElementById('f-type').value,Message:document.getElementById('f-msg').value.trim(),'Sent from':location.href,
      _subject:'Website inquiry: '+name+(company?' ('+company+')':''),_replyto:email,_template:'table'};
    note.textContent='Sending…'; note.hidden=false;
    var btn=form.querySelector('button[type=submit]'); if(btn) btn.disabled=true;
    fetch(FORM_ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
      .then(function(r){return r.json();})
      .then(function(j){if(!j||String(j.success)!=='true') throw new Error('fail'); done();})
      .catch(function(){note.textContent='That didn’t go through. Please email michael@resolvedcx.com instead.';})
      .then(function(){if(btn) btn.disabled=false;});
  });}
})();
'''
ROUTER = r'''
(function(){
  var VIEWS=/*VIEWS*/;
  var main=document.getElementById('top');
  function route(){
    var h=(location.hash||'').slice(1), view=VIEWS[h]?h:null, target=null;
    if(!view&&h&&h!=='top'){
      // an anchor inside a subpage (e.g. #apply on Careers): open that subpage, then scroll to it
      target=document.getElementById(h);
      var host=target&&target.closest('[data-view]');
      if(host) view=host.id;
    }
    main.hidden=!!view;
    Object.keys(VIEWS).forEach(function(k){var el=document.getElementById(k); if(el) el.hidden=(k!==view);});
    document.title=view?VIEWS[view]+' \u00b7 ResolvedCX':'ResolvedCX';
    if(target&&h!==view){setTimeout(function(){target.scrollIntoView();},0);}
    else if(view){window.scrollTo(0,0);}
    else if(h&&h!=='top'){var t=document.getElementById(h); if(t) setTimeout(function(){t.scrollIntoView();},0);}
  }
  window.addEventListener('hashchange',route); route();
})();
'''

# ------------------------------------------------------------------ PREVIEW
def build_preview():
    p = ''
    views = {'privacy': 'Privacy Policy', 'terms': 'Terms of Use', 'security': 'Security'}
    arts = []
    cta = '''
  <section class="block" style="padding-top:0"><div class="wrap"><div class="contact" style="grid-template-columns:1fr;text-align:left">
    <div><p class="eyebrow" style="color:var(--sun)">Get started</p><h2 style="margin-top:12px">Let's build your team.</h2>
    <p class="sub">Tell us what you need covered and Michael will come back with a proposed team and plan.</p>
    <div class="ctas" style="margin-top:24px;display:flex;gap:12px;flex-wrap:wrap"><a class="btn" style="background:var(--sun);color:#2A1D00" href="#contact">Talk to Michael</a></div></div>
  </div></div></section>'''
    for slug, pg in pages.PAGES.items():
        views['pg-' + slug] = re.sub('<[^>]+>', '', html.unescape(pg['name']))
        body = pg['body']() + ('' if slug == 'careers' else cta)
        arts.append(f'<article class="page-view" id="pg-{slug}" data-view hidden>\n{body}\n</article>')
    legal = '\n'.join(v.replace(' hidden>', ' data-view hidden>', 1) for v in LEGAL.values())
    body = (open(R + 'src/logo_symbol.html').read() + '\n' + HEADER + '\n<main id="top">' + main + '</main>\n' + '\n'.join(arts) + '\n' + legal + '\n' + FOOTER)
    body = images(links(body, 'preview', True), p)
    js = JS.replace('/*ROUTER*/', ROUTER.replace('/*VIEWS*/', json.dumps(views))).replace('/*ENDPOINT*/', '')
    out = f'<title>ResolvedCX</title>\n{FONTS}\n<style>{CSS}</style>\n\n{body}\n\n<script>{js}</script>\n'
    os.makedirs(R + 'preview', exist_ok=True)
    open(R + 'preview/index.html', 'w').write(out)
    return out

# ------------------------------------------------------------------ PROD
ORG = {
    '@context': 'https://schema.org', '@type': 'Organization', '@id': SITE + '/#org',
    'name': 'ResolvedCX', 'legalName': 'Customer Service Excellence LLC', 'url': SITE + '/',
    'logo': SITE + '/apple-touch-icon.png', 'foundingDate': '2017',
    'description': 'Dedicated, work-from-home customer support teams in the Philippines for fast-growing brands.',
    'email': 'michael@resolvedcx.com',
    'address': {'@type': 'PostalAddress', 'addressLocality': 'Brooklyn', 'addressRegion': 'NY', 'addressCountry': 'US'},
    'areaServed': 'US', 'numberOfEmployees': {'@type': 'QuantitativeValue', 'value': 350},
    'sameAs': ['https://www.linkedin.com/company/resolvedcx/'],
    'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales', 'email': 'michael@resolvedcx.com'},
}
GA = '''<!-- Analytics: set GA_ID to your Google Analytics 4 measurement ID (G-XXXXXXX) to turn on tracking. Nothing loads while it is empty. -->
<script>
  window.GA_ID='';
  if(window.GA_ID){var s=document.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id='+window.GA_ID;document.head.appendChild(s);
    window.dataLayer=window.dataLayer||[];window.gtag=function(){dataLayer.push(arguments);};gtag('js',new Date());gtag('config',window.GA_ID);}
</script>'''

GA = GA.replace("window.GA_ID='';", f"window.GA_ID='{GA_ID}';")

def head(title, desc, path, extra_ld=(), preload=None):
    url = SITE + path
    ROBOTS = 'noindex,nofollow' if PREVIEW else 'index,follow'
    ld = [ORG] + list(extra_ld)
    pre = f'\n<link rel="preload" as="image" href="{preload[0]}" imagesrcset="{preload[1]}" imagesizes="100vw" fetchpriority="high">' if preload else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="robots" content="{ROBOTS}">
<meta name="theme-color" content="#121833">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ResolvedCX">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="The ResolvedCX team with the headline Every ticket, resolved.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/og.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Familjen+Grotesk:wght@500;600;700&family=Public+Sans:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/site.css">{pre}
<script type="application/ld+json">{json.dumps(ld if len(ld) > 1 else ld[0], ensure_ascii=False)}</script>
{GA}
</head>
<body>
{LOGO_SYMBOL}
'''

def faq_ld(fragment):
    qs = re.findall(r'<summary>(.*?)</summary><p>(.*?)</p>', fragment, re.S)
    clean = lambda x: re.sub(r'\s+', ' ', html.unescape(re.sub('<[^>]+>', '', x))).strip()
    return {'@context': 'https://schema.org', '@type': 'FAQPage',
            'mainEntity': [{'@type': 'Question', 'name': clean(q), 'acceptedAnswer': {'@type': 'Answer', 'text': clean(a)}} for q, a in qs]}

def crumbs_ld(items):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList',
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + u} for i, (n, u) in enumerate(items)]}

def write(path, doc):
    fp = R + 'prod' + path + ('index.html' if path.endswith('/') else '')
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, 'w').write(rebase(doc))

def rebase(doc):
    if not BASE: return doc
    doc = re.sub(r'((?:href|src|action)=")/(?!/)', r'\1' + BASE + '/', doc)
    fix = lambda v: re.sub(r'(^|,\s*)/(?!/)', lambda n: n.group(1) + BASE + '/', v)
    return re.sub(r'((?:imagesrcset|srcset)=")([^"]*)"', lambda m: m.group(1) + fix(m.group(2)) + '"', doc)

def build_prod():
    P = R + 'prod/'
    if os.path.exists(P): shutil.rmtree(P)
    shutil.copytree(R + 'static', P, ignore=shutil.ignore_patterns('manifest.json'))
    os.makedirs(P + 'assets', exist_ok=True)
    open(P + 'assets/site.css', 'w').write(CSS.strip() + '\n')
    js = JS.replace('/*ROUTER*/', '').replace('/*ENDPOINT*/', FORM_ENDPOINT)
    open(P + 'assets/site.js', 'w').write(js.strip() + '\n')
    foot = '\n<script src="/assets/site.js" defer></script>\n</body>\n</html>\n'
    urls = []
    # home
    b = M['band']
    pre = (f"/i/band-{b['widths'][1]}.webp", ', '.join(f"/i/band-{w}.webp {w}w" for w in b['widths']))
    home_body = images(links(HEADER + '\n<main id="top">' + main + '</main>\n' + FOOTER, 'prod', True), '/')
    write('/', head('ResolvedCX | Outsourced Customer Support Teams in the Philippines',
                    'ResolvedCX builds dedicated, work-from-home customer support teams in the Philippines for fast-growing brands. About 350 people, 100+ clients since 2017, no long-term commitment.',
                    '/', [faq_ld(main)], pre) + home_body + foot)
    urls.append(('/', '1.0'))
    # subpages
    for slug, pg in pages.PAGES.items():
        body_main = pg['body']()
        if slug != 'careers':
            body_main += '\n' + CONTACT
        name = re.sub('<[^>]+>', '', html.unescape(pg['name']))
        crumbs = [('Home', '/')]
        if pg.get('parent'):
            crumbs.append((pg['parent'][1], '/#' + pg['parent'][0]))
        crumbs.append((name, pg['path']))
        lds = [crumbs_ld(crumbs)]
        if pg['kind'] in ('service', 'industry'):
            lds.append({'@context': 'https://schema.org', '@type': 'Service', 'name': name, 'serviceType': pg.get('service_type', name),
                        'description': pg['desc'], 'provider': {'@id': SITE + '/#org'}, 'areaServed': 'US', 'url': SITE + pg['path']})
        if '<details' in body_main:
            lds.append(faq_ld(body_main))
        page_body = images(links(HEADER + '\n<main id="page">' + body_main + '</main>\n' + FOOTER, 'prod', False), '/')
        write(pg['path'], head(pg['title'], pg['desc'], pg['path'], lds) + page_body + foot)
        urls.append((pg['path'], '0.8' if pg['kind'] != 'careers' else '0.6'))
    # legal
    ltitles = {'privacy': ('Privacy Policy | ResolvedCX', 'How ResolvedCX collects, uses and protects personal information.'),
               'terms': ('Terms of Use | ResolvedCX', 'The terms that govern use of the ResolvedCX website.'),
               'security': ('Security | ResolvedCX', 'How ResolvedCX protects client and customer data.')}
    for k, art in LEGAL.items():
        art_open = art.replace(f'<article class="legal" id="{k}" hidden>', f'<article class="legal" id="{k}">')
        b2 = images(links(HEADER + '\n<main id="page">' + art_open + '</main>\n' + FOOTER, 'prod', False), '/')
        b2 = b2.replace('href="#top"', 'href="/"')
        t, d = ltitles[k]
        write(f'/{k}/', head(t, d, f'/{k}/', [crumbs_ld([('Home', '/'), (t.split(' |')[0], f'/{k}/')])]) + b2 + foot)
        urls.append((f'/{k}/', '0.3'))
    # sitemap + robots
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>\n' for u, pr in urls) + '</urlset>\n'
    open(P + 'sitemap.xml', 'w').write(sm)
    open(P + 'robots.txt', 'w').write('User-agent: *\nDisallow: /\n' if PREVIEW else f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
    # 404
    nf = head('Page not found | ResolvedCX', 'This page does not exist.', '/404.html').replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="noindex">')
    nf_body = links(HEADER + '\n<main id="page"><section class="sub-hero"><div class="wrap" style="grid-template-columns:1fr"><div><p class="eyebrow">404</p><h1>That page isn\'t here.</h1><p class="lede">It may have moved when we rebuilt the site.</p><div class="ctas"><a class="btn btn-primary" href="/">Go to the home page</a></div></div></div></section></main>\n' + FOOTER, 'prod', False)
    open(P + '404.html', 'w').write(rebase(nf + nf_body + foot))
    # old Squarespace URLs -> new pages
    for old, new in OLD_URLS.items():
        dest = SITE + new
        doc = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>'
               f'<link rel="canonical" href="{dest}"><meta name="robots" content="noindex">'
               f'<meta http-equiv="refresh" content="0; url={BASE}{new}"><script>location.replace("{BASE}{new}")</script></head>'
               f'<body><a href="{BASE}{new}">Continue to ResolvedCX</a></body></html>')
        os.makedirs(P + old.strip('/'), exist_ok=True)
        open(P + old.strip('/') + '/index.html', 'w').write(doc)
    # drop image sizes no page uses
    used = set()
    for dp, _, fs in os.walk(P):
        for f in fs:
            if f.endswith('.html'): used |= set(re.findall(r'/i/([\w-]+\.webp)', open(os.path.join(dp, f)).read()))
    for f in os.listdir(P + 'i'):
        if f not in used: os.remove(P + 'i/' + f)
    return urls

if __name__ == '__main__':
    if '--preview' in sys.argv:
        print('preview bytes', len(build_preview()))
    else:
        urls = build_prod()
        print('built', len(urls), 'pages into prod/' + (f' (preview for {SITE})' if PREVIEW else ''))
