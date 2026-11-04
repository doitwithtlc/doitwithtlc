"""Direct native CRM capture replaces the general and presenter email-draft paths."""
from pathlib import Path
import runpy,re
REPO=Path(__file__).resolve().parents[1]
n=runpy.run_path(str(REPO/'scripts/build-membership-benefits.py'))
sec,page,embed=n['sec'],n['page'],n['n']['embed']
body=sec('<p class="eyebrow">Talk with The Liaison Companies</p><h1>Tell us what you’re building.<br><em>Let’s find the next step.</em></h1><p class="lead">Need brand representation, event management, bilingual outreach, content support or information about BBLO? Share your goals and the details that will help Carmen review your request.</p>','hero')
body+=sec('<h2>Start the conversation.</h2><p>Your submission goes directly into TLC’s CRM for review. Carmen receives an internal alert and a follow-up task. We’ll contact you about your inquiry; submitting does not confirm availability, services or an agreement.</p>'+embed('MFNV2rDc8OXIGmKnHplC','TLC general inquiry form'),'intake-section')
page('/inquire/','Contact TLC | General Inquiry &amp; Project Request','Send your brand representation, event management, bilingual outreach, content or BBLO inquiry directly to TLC for review.',body)
body=sec('<p class="eyebrow">Present at BBLO</p><h1>Bring something useful.<br><em>Help a business move forward.</em></h1><p class="lead">Propose a practical presentation, workshop or conversation for local business owners. Tell us what attendees will learn, how they can use it and why you’re the right person to share it.</p>','hero')
body+=sec('<div class="grid three"><article class="card"><h2>Make it practical.</h2><p>Give attendees a useful takeaway and room to ask questions.</p></article><article class="card"><h2>Know the audience.</h2><p>Shape your topic for local owners and professionals across industries and business stages.</p></article><article class="card"><h2>Plan it together.</h2><p>BBLO reviews the topic, format, experience and availability before confirming a presentation.</p></article></div>')
body+=sec('<h2>Submit your presentation application.</h2><p>Your application is saved privately in BBLO’s CRM review funnel. Carmen receives an internal alert and a review task. Submission does not approve a topic or reserve a date; we’ll follow up after review.</p>'+embed('bsvdmVndVtnY9FU6RCUj','BBLO presenter application form'),'intake-section')
page('/bblo/present/','Apply to Present at BBLO | Workshops &amp; Business Learning | TLC','Propose a useful presentation or workshop for BBLO business owners. Submit your topic, experience, learning outcomes and availability for review.',body)
