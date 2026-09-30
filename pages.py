"""SUBPAGE CONTENT: the service, industry and careers pages.
Edit the text inside the quotes. Home page text lives in src/template.html.
Links use tokens resolved per build target:
  @page:<slug>   -> another subpage
  @home:<id>     -> an anchor on the home page
  @img:<name>|<alt>|<sizes>|<class>   -> responsive <img>
"""

SITE = 'https://www.resolvedcx.com'


ARROW = '<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

SERVICE_LINKS = f'''
      <div class="more-links">
        <a href="@page:customer-support"><div>Customer support<span>Email, chat, phone and social</span></div>{ARROW}</a>
        <a href="@page:virtual-assistants"><div>Virtual assistants<span>Dedicated, recruited and managed</span></div>{ARROW}</a>
        <a href="@page:back-office"><div>Back office &amp; finance<span>Orders, bookkeeping, business development</span></div>{ARROW}</a>
      </div>'''

LEADERS = '''
      <div class="leaders compact">
        <div class="leader"><img src="@team:michael" alt="Portrait of Michael Feinberg"><span class="nm">Michael Feinberg</span><span class="ti">CEO</span></div>
        <div class="leader"><img src="@team:ruvel" alt="Portrait of Ruvel Batu"><span class="nm">Ruvel Batu</span><span class="ti">Philippines Country Director</span></div>
        <div class="leader"><img src="@team:jessa" alt="Portrait of Jessa Cura"><span class="nm">Jessa Cura</span><span class="ti">Operations Manager</span></div>
        <div class="leader"><img src="@team:ianchu" alt="Portrait of Ian Levi Chu"><span class="nm">Ian Levi Chu</span><span class="ti">Senior Manager</span></div>
        <div class="leader"><img src="@team:realm" alt="Portrait of Realm Pajarito"><span class="nm">Realm Pajarito</span><span class="ti">Human Resources Manager</span></div>
        <div class="leader"><img src="@team:jessatrigo" alt="Portrait of Jessa Trigo"><span class="nm">Jessa Trigo</span><span class="ti">Customer Service Manager</span></div>
        <div class="leader"><img src="@team:iannovido" alt="Portrait of Ian Novido"><span class="nm">Ian Novido</span><span class="ti">Account Manager</span></div>
      </div>
      <p class="team-more"><a href="@home:people">Meet the whole team →</a></p>'''

def logos(names):
    alts = {'podium':'Podium','tunecore':'TuneCore','prose':'Prose','bambee':'Bambee','fellow':'Fellow','firstleaf':'Firstleaf','pattern':'Pattern','agelessrx':'AgelessRx','andie':'Andie','twentyeight':'Twentyeight Health','dutch':'Dutch','wholier':'Wholier'}
    return '<div class="logo-strip">' + ''.join(f'<img src="@logo:{n}" alt="{alts[n]}" loading="lazy">' for n in names) + '</div>'

def hero(crumb_label, crumb_parent, eyebrow, h1, lede, right, cta='Talk to Michael', cta_href='@contact', how=True):
    parent = f'<a href="@home:{crumb_parent[0]}">{crumb_parent[1]}</a> <span aria-hidden="true">/</span> ' if crumb_parent else ''
    return f'''
  <section class="sub-hero">
    <div class="wrap">
      <div>
        <nav class="crumbs" aria-label="Breadcrumb"><a href="@home:top">Home</a> <span aria-hidden="true">/</span> {parent}<span>{crumb_label}</span></nav>
        <p class="eyebrow" style="margin-top:18px">{eyebrow}</p>
        <h1>{h1}</h1>
        <p class="lede">{lede}</p>
        <div class="ctas"><a class="btn btn-primary" href="{cta_href}">{cta} {ARROW}</a>{'<a class="btn btn-ghost" href="@home:how">How it works</a>' if how else ''}</div>
      </div>
      {right}
    </div>
  </section>'''

def panel(title, items):
    return '<div class="panel"><h2>' + title + '</h2><ul>' + ''.join(f'<li>{i}</li>' for i in items) + '</ul></div>'

def section(eyebrow, h2, intro, body, pad_top=True):
    st = '' if pad_top else ' style="padding-top:0"'
    return f'''
  <section class="block"{st}>
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">{eyebrow}</p><h2>{h2}</h2></div><p>{intro}</p></div>
      {body}
    </div>
  </section>'''

def features(items):
    return '<div class="feature-grid">' + ''.join(f'<div class="feature"><h3>{h}</h3><p>{p}</p></div>' for h, p in items) + '</div>'

def faq(items):
    return '<div class="faq-list">' + ''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(items)) + '</div>'

def faq_section(items):
    return f'''
  <section class="block" style="padding-top:0">
    <div class="wrap faq">
      <div><p class="eyebrow">FAQ</p><h2>Common questions.</h2></div>
      {faq(items)}
    </div>
  </section>'''

F_PRICING = ('How does pricing work?', "We bill hourly per person under a simple statement of work sized to your needs. You're billed only for hours worked, and you can add or reduce people as your needs change, with no long-term commitment.")
F_SPEED = ('How quickly can people start?', 'Once we have your training materials, we can generally onboard new agents within a week.')
F_TOOLS = ('Which tools do they use?', 'Yours. Our team works inside your helpdesk (Zendesk, Gorgias, Freshdesk, Intercom and others), your ecommerce platform and your Slack.')
F_HOURS = ('What hours can you cover?', "Our team works overnight shifts in the Philippines, so they're online during US business hours. Tell us the coverage you need and we'll build a schedule around it.")
F_QUALITY = ('How do you measure quality?', 'Every account has an experienced ResolvedCX manager overseeing quality. QA is tailored to each client: we agree what gets reviewed and how often, and can run regular reviews of each agent\'s tickets if you want them. Your data stays in your own helpdesk, and we provide reporting on request.')


import re as _re, os as _os
_R = _os.path.dirname(_os.path.abspath(__file__)) + '/'
_VET = open(_R + 'src/vet_block.html').read()
_VET = _re.sub(r'\s*<figure class="side-photo">.*?</figure>', '', _VET, flags=_re.S)
_GRID = _re.search(r'<div class="people-grid">.*?\n      </div>', open(_R + 'src/grid_block.html').read(), _re.S).group(0)
LIFE = section('Life at ResolvedCX', 'A team that likes working together.', 'We bring everyone together in person, and it shows in how long people stay.', _GRID, pad_top=False)

PAGES = {
 'customer-support': {
  'path': '/services/customer-support/', 'kind': 'service',
  'title': 'Outsourced Customer Support: Email, Chat, Phone & Social | ResolvedCX',
  'desc': 'Dedicated, work-from-home customer support agents in the Philippines for email, chat, phone and social. Managed, QA-scored and billed hourly with no long-term commitment.',
  'name': 'Customer support', 'parent': ('services', 'Services'),
  'service_type': 'Outsourced customer support',
  'body': lambda: hero('Customer support', ('services','Services'), 'Outsourced customer support',
        'Customer support teams that work inside your helpdesk.',
        'Dedicated agents in the Philippines answer your customers by email, chat, phone and social, in your brand\'s voice, during your hours. Each team is run by an experienced ResolvedCX manager, with QA set up around your standards.',
        panel('Every team includes', ['Agents screened for writing, speaking and typing, then trained on your brand','An experienced ResolvedCX manager and team leads','QA tailored to your standards and schedule','Reporting on request, while your data stays in your helpdesk','Hourly billing with no long-term commitment']))
   + section('Channels', 'Every channel your customers use.', 'Start with one channel or hand us the whole queue. We staff to your volume and your peak hours.',
        features([('Email &amp; tickets','Order status, returns, exchanges, subscriptions and account questions, answered accurately and in your tone.'),('Live chat','Fast answers while customers are still on your site, staffed to your busiest hours.'),('Phone','Inbound calls handled by agents screened for clear, confident spoken English.'),('Social','Replies to comments and DMs, with problems escalated to your team before they spread.')]))
   + section('How we run it', 'Managed like it\'s your own team.', 'You stay in control of policy and tone. We handle hiring, scheduling, coaching and coverage.',
        features([('Tier 1 and Tier 2','Frontline agents handle the volume; experienced Tier 2 agents take escalations and complex cases.'),('Inside your stack','Agents work in your helpdesk and your Slack, so escalations take minutes and nothing lives in a separate system.'),('Quality on your terms','QA built around your standards and reviewed as often as you want, with reporting whenever you ask for it.'),('Scale when you need to','Add agents for a launch or the holidays and scale back down after, billed only for hours worked.')]), pad_top=False)
   + _VET
   + section('Your managers', 'The people running your team.', 'Our leadership team in the Philippines runs day-to-day operations for every account.', LEADERS, pad_top=False)
   + faq_section([F_PRICING, F_SPEED, F_HOURS, F_TOOLS, F_QUALITY]),
 },
 'virtual-assistants': {
  'path': '/services/virtual-assistants/', 'kind': 'service',
  'title': 'Virtual Assistants in the Philippines, Recruited and Managed | ResolvedCX',
  'desc': 'Dedicated virtual assistants in the Philippines for scheduling, inbox management, research and admin. Recruited, screened and managed by ResolvedCX, billed hourly.',
  'name': 'Virtual assistants', 'parent': ('services', 'Services'),
  'service_type': 'Virtual assistant staffing',
  'body': lambda: hero('Virtual assistants', ('services','Services'), 'Virtual assistants',
        'A dedicated assistant, without the hiring headache.',
        'We recruit, screen and manage full-time remote assistants in the Philippines who work your hours and your way. You get a consistent person who learns your business, and we handle the rest.',
        panel('What assistants typically handle', ['Calendar and scheduling','Inbox triage and follow-ups','Research, lists and data entry','Travel, vendors and day-to-day admin','Reporting and spreadsheet upkeep']))
   + section('How it works', 'Hired to your profile, managed by us.', 'Tell us what you need done. We find the right person and stay responsible for them.',
        features([('Recruited to your brief','We source candidates against the skills and hours you need, using the same screening we use for our support agents.'),('Screened properly','Written and spoken English, typing and practical exercises before anyone reaches you.'),('Managed day to day','Your assistant has a ResolvedCX manager behind them, so you are not managing them alone.'),('Simple billing','Hourly, under a short statement of work, with no long-term commitment.')]))
   + section('Who we are', 'Backed by a team of about 350.', 'Your assistant is supported by the same managers who run support for our clients.', LEADERS, pad_top=False)
   + faq_section([F_PRICING, ('Will I work with the same person every day?', 'Yes. A virtual assistant is dedicated to you, so they learn your preferences, tools and contacts over time.'), F_HOURS]),
 },
 'back-office': {
  'path': '/services/back-office/', 'kind': 'service',
  'title': 'Back-Office, Bookkeeping & Business Development Support | ResolvedCX',
  'desc': 'Remote back-office teams in the Philippines for order processing, refunds, invoicing, bookkeeping support and business development. Managed by ResolvedCX, billed hourly.',
  'name': 'Back office & finance', 'parent': ('services', 'Services'),
  'service_type': 'Back-office outsourcing',
  'body': lambda: hero('Back office &amp; finance', ('services','Services'), 'Back office, finance and growth',
        'The work behind every resolved ticket.',
        'Order edits, refunds, invoicing, bookkeeping and sales support pile up behind customer service. We staff dedicated remote teams for that work, managed the same way as our support teams.',
        panel('Common back-office work', ['Order edits, refunds and fraud checks','Invoicing and accounts receivable follow-up','Bookkeeping support alongside your accountant','Data entry and reporting','Lead research, list building and CRM upkeep']))
   + section('Services', 'Three kinds of back-office team.', 'Most clients start with one and add the others as they see how the model works.',
        features([('Operations','Order processing, returns, refunds, fraud checks, data entry and the one-off processes unique to your business.'),('Finance','Routine bookkeeping, invoicing and collections support, working to your accountant\'s direction.'),('Business development','Lead research, list building, CRM hygiene and outreach support that keep your sales team selling.'),('Customer support, too','When you\'re ready, the same managers can run your support queue. See <a href="@page:customer-support">customer support</a>.')]))
   + faq_section([F_PRICING, F_SPEED, F_HOURS]),
 },
 'ecommerce': {
  'path': '/industries/ecommerce/', 'kind': 'industry',
  'title': 'Ecommerce & DTC Customer Service Outsourcing | ResolvedCX',
  'desc': 'Customer service teams for ecommerce and DTC brands: order status, returns, subscriptions and holiday peaks. Trusted by brands like Prose, Fellow, Firstleaf and Pattern.',
  'name': 'Ecommerce &amp; DTC', 'parent': ('industries', 'Industries'),
  'service_type': 'Ecommerce customer service outsourcing',
  'body': lambda: hero('Ecommerce &amp; DTC', ('industries','Industries'), 'Ecommerce &amp; DTC',
        'Support that keeps up with your growth and your holidays.',
        'We\'ve run customer service for consumer brands since 2017. Our agents handle the order, shipping, returns and subscription questions that make up most of your queue, and scale with your peaks.',
        panel('What we handle', ['Where-is-my-order and shipping issues','Returns, exchanges and refunds','Subscription changes, pauses and cancellations, including win-backs','Product questions in your brand\'s voice','Holiday and launch surges']))
   + section('Brands we support', 'Consumer brands that grew with us.', 'Some have been with us for six years or more.', logos(['prose','fellow','firstleaf','pattern','andie']))
   + faq_section([('Can you scale up for the holidays?', 'Yes. Add agents ahead of peak season and scale back in January. You\'re billed only for hours worked.'), F_TOOLS, F_PRICING]),
 },
 'health-wellness': {
  'path': '/industries/health-wellness/', 'kind': 'industry',
  'title': 'Customer Support for Health & Wellness Companies | ResolvedCX',
  'desc': 'Non-clinical member and customer support for health and wellness companies: accounts, billing, shipping and scheduling, with clinical questions routed to your licensed team.',
  'name': 'Health &amp; wellness', 'parent': ('industries', 'Industries'),
  'service_type': 'Member support outsourcing',
  'body': lambda: hero('Health &amp; wellness', ('industries','Industries'), 'Health &amp; wellness',
        'Member support that knows where its lane ends.',
        'We provide non-clinical support for health and wellness companies: account, billing, shipping and scheduling questions. Anything clinical goes straight to your licensed team, following the escalation rules you set.',
        panel('What we handle', ['Account access and profile updates','Billing, payments and subscription changes','Shipping and delivery of orders','Appointment scheduling and reminders','Escalating clinical questions to your team']))
   + section('Companies we support', 'Trusted by health and wellness brands.', 'Our agents work within your compliance program and your policies.', logos(['agelessrx','twentyeight','dutch']))
   + faq_section([('Do your agents give medical advice?', 'No. Our agents handle non-clinical support only and route anything clinical to your licensed staff, following the escalation rules you define.'), ('Can you follow our compliance requirements?', 'Yes. Agents work inside your systems under your policies, and we can agree client-specific confidentiality and data-protection terms. See our <a href="@legal:security">security page</a>.'), F_PRICING]),
 },
 'software': {
  'path': '/industries/software/', 'kind': 'industry',
  'title': 'SaaS & Software Customer Support Outsourcing | ResolvedCX',
  'desc': 'Customer and account support for SaaS and service businesses, with Tier 1 and Tier 2 agents trained on your product. Trusted by Bambee and TuneCore.',
  'name': 'Software &amp; services', 'parent': ('industries', 'Industries'),
  'service_type': 'SaaS customer support outsourcing',
  'body': lambda: hero('Software &amp; services', ('industries','Industries'), 'Software &amp; services',
        'Product-savvy support for software and service businesses.',
        'We train agents on your product and your policies so they can answer account, billing and how-to questions accurately, and hand clean escalations to your engineers.',
        panel('What we handle', ['Account and login help','Billing and plan changes','How-to and onboarding questions','Tier 2 troubleshooting and clean bug reports','Back-office tasks like invoicing and data entry']))
   + section('Companies we support', 'Software and services clients.', 'From HR services to music distribution.', logos(['bambee','tunecore']))
   + faq_section([('How do agents learn our product?', 'They train directly with your team, inside your tools. If you don\'t have documentation yet, we\'ll help you write it.'), F_QUALITY, F_PRICING]),
 },
 'careers': {
  'path': '/careers/', 'kind': 'careers',
  'title': 'Work-From-Home Customer Support Jobs in the Philippines | ResolvedCX Careers',
  'desc': 'Join ResolvedCX as a work-from-home Customer Support Coordinator in the Philippines. Paid training, performance bonuses and a supportive, fully remote team.',
  'name': 'Careers', 'parent': None,
  'body': lambda: hero('Careers', None, 'Careers at ResolvedCX',
        'Work from home, with a team behind you.',
        'We hire Customer Support Coordinators across the Philippines to support well-known US brands. Shifts run overnight in Manila, during US business hours.',
        '<figure><img src="@img:careers|ResolvedCX team members cheering at a company gathering|(max-width:900px) 100vw, 520px|"></figure>', cta='How to apply', cta_href='#apply', how=False)
   + section('What we offer', 'Why people stay.', 'Many of our coordinators have been with us for years.',
        features([('Competitive pay','With performance bonuses on top of your base pay.'),('Fully paid training','Learn our support standards and common tools like Zendesk and Shopify before you start on a client.'),('Room to grow','Move into Tier 2, team lead and management roles.'),('A real team','A team lead who has your back, and optional in-person events with hundreds of coworkers.')]))
   + LIFE
   + section('What we look for', 'Is this role for you?', 'You don\'t need to know our clients\' products. We\'ll train you.',
        panel('Requirements', ['At least one year of customer service experience','Experience with Zendesk or a similar helpdesk (Gorgias, Freshdesk, Intercom). Shopify is a plus','Strong written and spoken English across email, chat and phone','A reliable home setup (a dual-monitor setup helps)','Real empathy for customers and an eye for detail'])
        + '<p class="note-inline" id="apply">To apply, email your resume to <a href="mailto:careers@resolvedcx.com"><strong>careers@resolvedcx.com</strong></a>. ResolvedCX never charges applicants fees and only contacts applicants from an @resolvedcx.com address.</p>', pad_top=False),
 },
}

INDUSTRY_LINK = {'DTC &amp; ecommerce':'ecommerce','Health &amp; wellness':'health-wellness','Software &amp; services':'software'}
