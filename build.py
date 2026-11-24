#!/usr/bin/env python3
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'engine'))
from engine import Site, fmt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site')
f = lambda n: fmt(n, ',')

THEME = """
/* VOICE: plain-spoken English buyer's guide for international investors
   IDEA: a coastal survey sheet: simplified map of Batumi's shoreline with district pins
   PICTURE: schematic coastline map, district markers, price rows
   COLOUR and TYPE: white ground, cobalt dominant, pale sky support, tomato-red accent; Archivo + Inter
   LAYOUT: full-width bands, 1240px content, 10px corners */
:root{color-scheme:light;--bg:#fff;--ink:#121a2e;--ink2:#2c3650;--mute:#55607a;--sea:#1f4fbf;--sea2:#2a62d9;--aqua:#eef3ff;--line:#dbe3f5;--line2:#b9c6e6;--coral:#e8483b;
--tint1:#e8efff;--tint2:#f7f9ff;--radius:10px;--btn-radius:8px;--bar-radius:3px;--head-font:Archivo,system-ui,sans-serif;--body-font:Inter,system-ui,sans-serif;--head-weight:800;--foot-bg:#0f1d45;--foot-ink:#d6def5}
"""

SRC = {
 'gt_aug': ('Galt &amp; Taggart: Batumi prices and sales by district, Jan–Aug 2026 (International Investment)', 'https://internationalinvestment.biz/en/business/9099-batumi-real-estate-trends-prices-and-sales-by-district.html'),
 'gt_sales': ('Galt &amp; Taggart: Batumi sales and buyer mix, Jan–Aug 2026 (International Investment)', 'https://internationalinvestment.biz/en/business/9064-batumi-real-estate-market-sales-growth-galt-taggart.html'),
 'gt_kob': ('Galt &amp; Taggart: eight months of 2026 incl. Kobuleti and buyer nationalities (Homesoverseas)', 'https://www.homesoverseas.ru/eng/news/Bolee_70_kvartir_prodannyh_v_Batumi_v_2026_godu_priobreli_inostrancy'),
 'ii_2026': ('Georgia real estate 2026: prices and yields in Tbilisi and Batumi (International Investment)', 'https://internationalinvestment.biz/en/real-estate/8910-georgia-real-estate-2026-prices-and-yields-in-tbilisi-and-batumi.html'),
 'ii_2025': ('Batumi market in 2025 by district (International Investment)', 'https://internationalinvestment.biz/en/real-estate/7391-rynok-nedvizhimosti-batumi-v-2025-godu-rost-prodazh-i-snizhenie-dohodnosti-arendy.html'),
 'tbc': ('TBC Capital: Batumi average price 2019–2025 (International Investment)', 'https://internationalinvestment.biz/en/business/7220-batumi-housing-market-prices-rose-by-17-in-2025-tbc-capital-report.html'),
 'investor': ('Investor.ge: Batumi residential real estate snapshot, 2026', 'https://www.investor.ge/2026/04/20/sector-snapshot-batumi-residential-real-estate/'),
 'oversupply': ('Batumi housing market: sales growth and oversupply risks (International Investment)', 'https://internationalinvestment.biz/en/real-estate/8149-batumi-housing-market-sales-growth-and-risks-of-oversupply.html'),
 'gpg_buy': ('Global Property Guide: buying costs in Georgia', 'https://www.globalpropertyguide.com/asia/georgia/buying-guide'),
 'madloba_buy': ('Madloba: buying property in Georgia as a foreigner', 'https://madloba.info/en/faq/housing/buying-property-in-georgia-as-a-foreigner/'),
 'madloba_rent': ('Madloba: tax on renting out an apartment (Tax Code art. 81)', 'https://madloba.info/en/faq/work-business-taxes/tax-on-renting-out-an-apartment-in-georgia/'),
 'madloba_tax': ('Madloba: taxes in Georgia and small business status', 'https://madloba.info/faq/work-business-taxes/taxes-and-vat-in-georgia/'),
 'madloba_poa': ('Madloba: power of attorney for a transaction in Georgia', 'https://madloba.info/en/blog/laws-of-georgia/doverennost-ne-grazhdaninu-gruzii'),
 'madloba_rp': ('Madloba: residence permit processing times', 'https://madloba.info/en/faq/residence-and-citizenship/check-residence-permit-status-georgia/'),
 'chambers': ('Chambers Real Estate 2026: Georgia', 'https://practiceguides.chambers.com/practice-guides/real-estate-2026/georgia'),
 'eig': ('EIG Law: real estate residence permit threshold from 1 March 2026', 'https://eiglaw.com/georgia-to-increase-real-estate-investment-threshold-for-residence-permits-effective-march-1-2026/'),
 'visaatlas': ('VisaAtlas: short-term residence for property owners', 'https://visaatlas.org/visas/georgia/short-term-residence-real-estate'),
 'sda': ('Public Service Development Agency: residence permits', 'https://sda.gov.ge/en/products/migration-residence-permits/'),
 'andersen': ('Andersen Georgia: tax on selling a home', 'https://ge.andersen.com/georgia-property-tax/'),
 'sova': ('SOVA: property tax threshold raised to GEL 100,000', 'https://sovanews.tv/en/2026/09/30/georgian-parliament-approves-abolition-of-40000-gel-property-tax-threshold/amp/'),
 'korter_frames': ('Korter: black, white and green frame explained', 'https://korter.ge/en/new-projects-tbilisi-black-frame'),
 'safebuy': ('SafeBuy: checking new developments in the registry', 'https://safebuy.ge/properties/new-developments'),
 'eurasia': ('Eurasia Travel: Old and New Boulevard', 'https://eurasia.travel/georgia/batumi/boulevard/'),
 'prian': ('Prian: Georgian coast beyond Batumi', 'https://prian.info/pub/beachfront-real-estate-in-georgia-beyond-batumi-emerging-hotspots-for-apartment-purchases.html'),
 'geoln': ('Geoln: Makhinjauri district', 'https://geoln.com/georgia/batumi-makhinjauri'),
 'civil': ('Civil.ge: Eagle Hills projects in Gonio and Krtsanisi', 'https://civil.ge/archives/711355'),
 'korter_kob': ('Korter: Kobuleti developments and transport', 'https://korter.ge/en/alliance-renaissance-kobuleti'),
 'hs_yield': ('Homesoverseas: Batumi yields fell from 8.8% (2024) to 7.1% (early 2026), Galt &amp; Taggart', 'https://www.homesoverseas.ru/eng/articles/14899'),
 'napr': ('National Agency of Public Registry', 'https://napr.gov.ge'),
 'rs': ('Revenue Service of Georgia', 'https://www.rs.ge'),
}

S = Site(domain='https://batumi-real-estate.com', lang='en', out=OUT, utm='batumi-real-estate', theme_css=THEME,
         fonts_href='https://fonts.googleapis.com/css2?family=Archivo:wght@700;800&amp;family=Inter:wght@400;600;700&amp;display=swap',
         logo='Batumi<span>/</span>Real Estate',
         nav=[('', 'Home'), ('areas/', 'Areas'), ('prices/', 'Prices'), ('how-to-buy/', 'How to buy'), ('costs-and-taxes/', 'Costs &amp; taxes'),
              ('residence-permit/', 'Residence'), ('rental-yields/', 'Rental yields'), ('faq/', 'FAQ')],
         labels=dict(home='Home', updated='Last updated', sources='Sources', crumbs='Breadcrumb', nav='Sections', facts_label='Key figures',
                     sources_note='Every figure carries its period and the study it comes from. Analysts measure different market segments, so compare numbers only within one source.',
                     draft='Draft for review. Sample listings are placeholders; every other figure is sourced.',
                     disclaimer='This guide is general information, not legal or tax advice.',
                     submit='Send request', form_draft='Draft: the form is not connected yet, nothing was sent.'),
         footer_blurb='<b>Batumi/Real Estate</b> is an independent English guide to buying property in Batumi, part of the <a href="{BRIK}">Brik</a> project.',
         footer_cols=[('Buying', [('how-to-buy/', 'How to buy'), ('buying-remotely/', 'Buying remotely'), ('costs-and-taxes/', 'Costs &amp; taxes'), ('residence-permit/', 'Residence permit')]),
                      ('Market', [('areas/', 'Areas'), ('prices/', 'Prices'), ('rental-yields/', 'Rental yields'), ('faq/', 'FAQ')]),
                      ('About', [('about/', 'About'), ('contact/', 'Contact'), ('privacy/', 'Privacy')])],
         updated='November 2026', sources=SRC)

AREAS = [  # Galt & Taggart, primary market turnkey, Jan–Aug 2026
 ('Old Batumi', 'old-batumi', 3224, 839), ('Gonio–Kvariati', 'gonio-kvariati', 2657, 196), ('Alley of Heroes', 'alley-of-heroes', 2255, 2485),
 ('Makhinjauri', 'makhinjauri', 1998, 779), ('New Boulevard', 'new-boulevard', 1798, 4417), ('Kobuleti', 'kobuleti', 1734, 401)]

def area_rows(link=True, hl=None):
    return S.rows([(n, f'{f(s)} sales, Jan–Aug 2026', p, f'${f(p)}/m²', ('areas/' if link else None)) for n, _, p, s in AREAS], 3300, hl)

MAP = '''<svg class="scene" viewBox="0 0 600 500" role="img" aria-label="Schematic map of the Batumi coast: Kobuleti to the north, then Makhinjauri, Old Batumi, New Boulevard, the airport and Gonio–Kvariati near the Turkish border">
<defs><linearGradient id="bsea" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1f4fbf"/><stop offset="1" stop-color="#5d86e3"/></linearGradient>
<pattern id="grid" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#ffffff" stroke-opacity=".12"/></pattern></defs>
<rect width="600" height="500" rx="10" fill="#f3f6ff"/>
<path d="M0 0 H262 C250 60 236 110 246 160 C254 196 230 214 212 232 C236 250 262 262 272 300 C282 350 288 410 300 500 H0Z" fill="url(#bsea)"/>
<path d="M0 0 H262 C250 60 236 110 246 160 C254 196 230 214 212 232 C236 250 262 262 272 300 C282 350 288 410 300 500 H0Z" fill="url(#grid)"/>
<path d="M262 0 C250 60 236 110 246 160 C254 196 230 214 212 232 C236 250 262 262 272 300 C282 350 288 410 300 500" fill="none" stroke="#e8483b" stroke-width="3"/>
<path d="M360 0 C420 80 470 120 600 110 V0Z" fill="#dfe7fb"/><path d="M380 500 C430 420 500 380 600 390 V500Z" fill="#dfe7fb"/>
<path d="M400 160 l40 -60 l40 60Z M450 170 l50 -80 l50 80Z" fill="#c9d6f5"/>
<g font-family="Inter,system-ui,sans-serif" font-size="15" font-weight="700" fill="#121a2e">
 <path d="M300 22 l10 -14 l10 14" fill="none" stroke="#121a2e" stroke-width="2.5"/><text x="328" y="24">Kobuleti ~ north</text>
 <circle cx="252" cy="120" r="9" fill="#fff" stroke="#e8483b" stroke-width="4"/><text x="272" y="125">Makhinjauri</text>
 <circle cx="216" cy="232" r="11" fill="#e8483b"/><text x="238" y="237">Old Batumi</text>
 <circle cx="262" cy="290" r="9" fill="#fff" stroke="#e8483b" stroke-width="4"/><text x="284" y="295">New Boulevard</text>
 <rect x="282" y="346" width="16" height="16" rx="3" fill="#121a2e"/><text x="308" y="360" font-weight="600">Airport</text>
 <circle cx="292" cy="430" r="9" fill="#fff" stroke="#e8483b" stroke-width="4"/><text x="314" y="435">Gonio–Kvariati</text>
 <path d="M300 482 H600" stroke="#121a2e" stroke-width="2" stroke-dasharray="6 6"/><text x="420" y="476" font-weight="600" font-size="13">Turkish border</text>
 <text x="40" y="250" fill="#fff" font-size="18">Black Sea</text>
</g>
<text x="16" y="490" font-family="Inter,sans-serif" font-size="11" fill="#ffffff" fill-opacity=".85">Schematic, not to scale</text>
</svg>'''

def form():
    opts = ''.join(f'<option>{n}</option>' for n, *_ in AREAS)
    return S.lead_form(f'''<label>Name<input name="name" autocomplete="name" required></label>
<label>WhatsApp, Telegram or email<input name="contact" required></label>
<label>Budget<select name="budget"><option>Under $80,000</option><option>$80,000–150,000</option><option>$150,000–300,000</option><option>Over $300,000</option></select></label>
<label>Area<select name="area"><option>Not sure yet</option>{opts}</select></label>
<label>Goal<select name="goal"><option>Rental income</option><option>Holiday home</option><option>Residence permit</option><option>Moving to Batumi</option></select></label>''')

CTA = lambda c, t='Browse Batumi listings on Brik', x='Apartments from developers, agencies and owners, with filters by area, price and size.': S.cta(c, t, x, 'Open listings')

# ---------------- pages ----------------
S.page('', 'Batumi real estate — prices, areas and buying as a foreigner',
 'An English guide to Batumi real estate: prices by area, how foreigners buy, taxes, residence permits and rental yields, with sourced 2026 data.', None, f'''
<section class="hero band"><div class="wrap">
 <div><h1>Batumi real estate: what it costs and how foreigners buy</h1>
 <p class="lede">Foreigners can buy apartments in Georgia on the same terms as Georgian citizens, with no visa or residence needed. In Batumi, more than seven in ten buyers in surveyed new developments were foreign in the first eight months of 2026.</p>
 <div class="ctas"><a class="btn" href="#areas">Compare areas</a>{S.a("how-to-buy/", "How buying works", "btn ghost")}</div></div>
 {MAP}
</div></section>
{S.facts([('$1,408', 'average price per m² in new developments', 'September 2026, Colliers'), ('72%', 'of buyers in surveyed new projects were foreign', 'Jan–Aug 2026, Galt &amp; Taggart'), ('7.1%', 'gross rental yield, before costs and tax', 'June 2026, Galt &amp; Taggart'), ('$150,000', 'minimum property value for a residence permit', 'since 1 March 2026')])}
<section class="band" id="areas"><div class="wrap">
 <h2>Price per m² by area</h2>
 <p>Average price of turnkey apartments on the primary market, January–August 2026, Galt &amp; Taggart. New Boulevard sells the most; Old Batumi costs the most.</p>
 {area_rows()}
 <p class="sub" style="margin-top:14px">{S.a("areas/", "What each area is like")} · {S.a("prices/", "How prices have moved since 2019")}</p>
</div></section>
<section class="band alt"><div class="wrap two">
 <div><h2>Who buys in Batumi</h2><p>Among developers surveyed by Galt &amp; Taggart for January–August 2026, Georgian citizens made 28% of purchases. The largest foreign groups were buyers from Ukraine, Russia and Belarus (19%), Europe (17%) and Israel (12%).</p>
 <p>Foreign demand is why Batumi behaves differently from Tbilisi, where buyers are mostly local.</p></div>
 <div><h2>Listings from Brik</h2><p>A live selection of Batumi apartments will appear here once the feed is connected. Meanwhile, the full catalogue is on the main site.</p><a class="btn" href="{S.brik('home-listings')}">See Batumi listings</a></div>
</div></section>
<section class="band"><div class="wrap">
 <h2>Six steps to buy</h2>
 <ol class="steps">
  <li><h3>Choose area and type</h3><p>Decide between resale and new build, and what the apartment is for. {S.a("areas/", "Areas")}</p></li>
  <li><h3>Check the registry</h3><p>The Public Registry shows the owner and any mortgage or arrest on the property.</p></li>
  <li><h3>Sign a preliminary agreement</h3><p>Price, timeline, deposit and when the deposit is refundable.</p></li>
  <li><h3>Open a bank account</h3><p>Payments usually go through a Georgian bank, which may ask where the money comes from.</p></li>
  <li><h3>Sign the sale contract</h3><p>At a notary or a Public Service Hall, in front of a registrar.</p></li>
  <li><h3>Register ownership</h3><p>Ownership passes when the registry records it, usually within one to several working days. {S.a("how-to-buy/", "Full guide")}</p></li>
 </ol>
</div></section>
<section class="band alt" id="lead"><div class="wrap two">
 <div><h2>Get a shortlist</h2><p>Tell us your budget, area and goal. A Brik agent will send matching apartments and answer questions about the purchase. Your request goes to the Brik team only; see the {S.a("privacy/", "privacy notice")}.</p>
 <p class="sub">Content is reviewed by Brik's partners in Georgia. {S.a("about/", "About this guide")}</p></div>
 {form()}
</div></section>''', srcs=['ii_2026', 'gt_aug', 'gt_kob', 'gt_sales', 'madloba_buy', 'eig'])

AREA_TXT = {
 'Old Batumi': ('The historic centre around Europe Square and the old part of the seafront boulevard. Few new projects fit here, so prices are the highest in the city: some sold above $5,000 per m² in August 2026.',
                'Buyers who want to live centrally without a car, or want a long-term asset in the most established location.',
                'Older buildings need a structural and services check; new builds are rare and expensive; summer crowds.', ['gt_aug', 'eurasia']),
 'New Boulevard': ('Part of "New Batumi", the southern extension of the seafront where most high-rise towers and aparthotels have gone up. About 3 km from the airport. It had 4,417 sales in the first eight months of 2026, roughly 40% of all registered sales in Batumi.',
                   'Investors who want a furnished unit to let, and buyers who want a sea-view new build below Old Batumi prices.',
                   'Hundreds of near-identical studios compete for tenants and resale buyers. Check whether the unit is registered as residential or as a hotel room.', ['gt_sales', 'gt_aug']),
 'Alley of Heroes': ('A district of high-rise, business and premium residential complexes. Second only to New Boulevard by sales (2,485 in January–August 2026), at about $450 more per m².',
                     'Buyers who want a newer, higher-spec building closer to the centre than New Boulevard.',
                     'Prices vary widely between projects; compare within the district rather than with the average.', ['gt_aug', 'ii_2025']),
 'Makhinjauri': ('A former settlement north of the centre that is now part of the city, with a quieter, suburban feel. Both residential complexes and aparthotels are being built. It grew fastest of Batumi\'s submarkets in 2026.',
                 'People who want to live by the sea away from the busy centre, including families.',
                 'Commute time to the centre; rental demand is more seasonal than downtown.', ['gt_aug', 'gt_sales', 'geoln']),
 'Gonio–Kvariati': ('A resort suburb about 15 km south of the centre, by the Turkish border. Premium complexes have pushed the average above most city districts. A large Eagle Hills master-planned project was announced for Gonio in 2025.',
                    'Buyers looking for a resort-style second home who will not commute daily.',
                    'Only 196 sales in eight months, so resale can take longer; new large-scale supply could shift prices.', ['gt_aug', 'prian', 'civil']),
 'Kobuleti': ('A separate resort town north of Batumi, in its own municipality, which Galt &amp; Taggart includes in its Batumi review. High-rise projects are going up along the main avenue near the sea, and buses run frequently to Batumi.',
              'Buyers with a smaller budget who want a seaside apartment for summer use or seasonal letting.',
              'Stronger seasonality than Batumi; many projects still under construction; fewer services in winter.', ['gt_kob', 'korter_kob']),
}
blocks = ''
for n, slug, p, s in AREAS:
    about, who, watch, _ = AREA_TXT[n]
    blocks += (f'<section class="band{" alt" if AREAS.index((n, slug, p, s)) % 2 else ""}" id="{slug}"><div class="wrap two"><div class="prose"><h2>{n}</h2>'
               f'<p><b>${f(p)}/m²</b> average, turnkey primary market · <b>{f(s)}</b> sales, Jan–Aug 2026</p><p>{about}</p></div>'
               f'<div class="prose"><h3>Suits</h3><p>{who}</p><h3>Watch for</h3><p>{watch}</p></div></div></section>')
S.page('areas/', 'Batumi areas compared — where to buy an apartment',
 'Old Batumi, New Boulevard, Alley of Heroes, Makhinjauri, Gonio–Kvariati and Kobuleti compared: price per m², sales and who each area suits.',
 [('areas/', 'Areas')], f'''
<section class="band"><div class="wrap"><h2>At a glance</h2><p>Jump to an area: ''' + ' · '.join(f'<a href="#{slug}">{n}</a>' for n, slug, *_ in AREAS) + f'''.</p>{area_rows(link=False)}</div></section>
{blocks}{CTA('areas')}''', h1='Batumi areas: where to buy',
 lede='Average new-build prices differ almost twofold across Batumi: from $1,734 per m² in Kobuleti to $3,224 in Old Batumi (Galt &amp; Taggart, January–August 2026).',
 srcs=sorted({k for v in AREA_TXT.values() for k in v[3]}))

hist = [(2019, 838), (2020, 839), (2021, 844), (2022, 897), (2023, 1125), (2024, 1197), (2025, 1395)]
S.page('prices/', 'Batumi property prices 2026 — by area and over time',
 'Batumi apartment prices in 2026: average price per m² by area, the trend since 2019 and the latest figures from Colliers, Galt & Taggart and TBC Capital.',
 [('prices/', 'Prices')], f'''
<section class="band"><div class="wrap"><h2>Average price per m², 2019–2025</h2>
 <p>TBC Capital's all-transaction average for Batumi rose from $838 in 2019 to $1,395 in 2025, with most of the increase from 2023 onwards.</p>
 {S.rows([(str(y), 'TBC Capital, all transactions', v, f'${f(v)}', None) for y, v in hist], 1500, '2025')}
</div></section>
<section class="band alt"><div class="wrap"><h2>Latest figures</h2>
 <table class="stack"><thead><tr><th>Measure</th><th class="n">Value</th><th>Period and source</th></tr></thead><tbody>
 <tr><td>New developments, weighted average</td><td class="n">$1,408/m²</td><td>September 2026, Colliers; +5.2% year on year</td></tr>
 <tr><td>Completed apartments, primary market</td><td class="n">$1,960/m²</td><td>June 2026; +9.8% year on year</td></tr>
 <tr><td>Newer projects, resale market</td><td class="n">$1,497/m²</td><td>June 2026; +6.5% year on year</td></tr>
 <tr><td>Turnkey primary market, 2025</td><td class="n">$1,865/m²</td><td>Galt &amp; Taggart; +9.4% year on year</td></tr>
 </tbody></table>
 <p style="margin-top:16px">Galt &amp; Taggart expects primary-market price growth in Batumi to slow to 4–6% a year. It also flags a large pipeline of aparthotel supply, which could weigh on rents.</p>
</div></section>
<section class="band"><div class="wrap"><h2>By area</h2><p>Turnkey primary market, January–August 2026, Galt &amp; Taggart.</p>{area_rows()}</div></section>
{CTA('prices')}''', h1='Batumi property prices',
 lede='New developments in Batumi averaged $1,408 per m² in September 2026 (Colliers). Turnkey apartments cost more, from $1,734 to $3,224 per m² depending on the area.',
 srcs=['ii_2026', 'tbc', 'investor', 'gt_aug', 'gt_kob', 'oversupply'])

S.page('how-to-buy/', 'How to buy property in Batumi as a foreigner — step by step',
 'How foreigners buy an apartment in Batumi: who can buy, registry checks, contracts, payment, registration and buying off-plan.',
 [('how-to-buy/', 'How to buy')], f'''
<section class="band"><div class="wrap two">
 <div class="prose"><h2>Who can buy</h2><p>Foreign individuals and companies can own apartments, houses and commercial property in Georgia on the same terms as citizens. The exception is agricultural land, which the constitution reserves for the state, municipalities and Georgian citizens. You do not need a visa, residence permit or local partner to buy.</p>
 <h2>What you need</h2><ul class="txt"><li>Your passport.</li><li>A sale contract, in Georgian and usually bilingual.</li><li>Proof of paying the registration fee (tariff on napr.gov.ge).</li><li>A power of attorney with a notarised Georgian translation if someone signs for you.</li></ul></div>
 <div class="prose"><h2>Resale or off-plan?</h2><p>Turnkey primary-market apartments averaged $1,865 per m² in December 2025; resale was about $1,450. New builds are often sold with developer instalments, but you take on the risk of delays.</p>
 <p>Off-plan units are sold in stages of finish: <b>black frame</b> (walls, windows, entrance door only), <b>white frame</b> (services installed, walls plastered, rough screed) and <b>green frame</b> (ready for decorative finishing). What each includes varies by developer, so check the contract.</p></div>
</div></section>
<section class="band alt"><div class="wrap"><h2>The process</h2>
 <ol class="steps">
  <li><h3>Check the registry</h3><p>Get an extract from the National Agency of Public Registry: owner, area, mortgage, arrest or other encumbrances.</p></li>
  <li><h3>Check the developer</h3><p>For off-plan: the developer owns the land, the land is not pledged, the building permit matches the project, and earlier projects were delivered.</p></li>
  <li><h3>Preliminary agreement</h3><p>Price, deposit, deadlines, penalties for delay and how the deposit is refunded. Have a lawyer read it.</p></li>
  <li><h3>Bank and payment</h3><p>Pay by bank transfer to the seller's account, never in cash through an intermediary. Link off-plan payments to construction stages.</p></li>
  <li><h3>Sale contract</h3><p>Signed at a notary or a Public Service Hall in front of a registrar.</p></li>
  <li><h3>Registration</h3><p>Ownership passes only when the registry records it, usually within one to several working days.</p></li>
 </ol>
 <div class="note">There is no state scheme that protects off-plan buyers' money in Georgia. The contract, the payment schedule and the developer's track record are your protection.</div>
 {S.related([('buying-remotely/', 'Buying without travelling'), ('costs-and-taxes/', 'Costs &amp; taxes'), ('residence-permit/', 'Residence permit')])}
</div></section>
{CTA('how-to-buy')}''', h1='How to buy property in Batumi',
 lede='A foreigner needs only a passport to buy an apartment in Batumi. The sale is registered with the Public Registry, usually within one to several working days, and ownership passes at that moment.',
 srcs=['madloba_buy', 'chambers', 'korter_frames', 'safebuy', 'napr', 'gt_kob'])

S.page('costs-and-taxes/', 'Costs and taxes of buying in Batumi — 2026 rules',
 'What it costs to buy property in Batumi and the taxes an owner pays in 2026: property tax with the new GEL 100,000 threshold, 5% on rent, and tax on resale.',
 [('costs-and-taxes/', 'Costs &amp; taxes')], f'''
<section class="band"><div class="wrap"><h2>One-off costs when buying</h2>
 <table class="stack"><thead><tr><th>Item</th><th>Typical cost</th><th>Notes</th></tr></thead><tbody>
 <tr><td>Transfer or stamp tax</td><td class="k">none</td><td>Georgia has no separate property transfer tax.</td></tr>
 <tr><td>Registration fee</td><td class="k">fixed tariff</td><td>Depends on how fast you need it; see napr.gov.ge.</td></tr>
 <tr><td>Notary and translation</td><td class="k">by tariff</td><td>When the contract or a power of attorney is notarised.</td></tr>
 <tr><td>Agent's commission</td><td class="k">usually 3–5%</td><td>Usually paid by the seller; depends on the agreement.</td></tr>
 <tr><td>Total buyer costs</td><td class="k">0.6–1.1%</td><td>Global Property Guide estimate for a typical purchase.</td></tr>
 </tbody></table></div></section>
<section class="band alt"><div class="wrap"><h2>Owner's taxes in 2026</h2>
 <table class="stack"><thead><tr><th>Tax</th><th>Rate</th><th>When it applies</th></tr></thead><tbody>
 <tr><td>Property tax</td><td class="k">0% or 0.8–1%</td><td>From 1 October 2026, none if your family's income last year was GEL 100,000 or less. Above that, 0.8–1% of market value. The old GEL 40,000 threshold and the 0.05–0.2% rate were abolished.</td></tr>
 <tr><td>Residential rent</td><td class="k">5%</td><td>On gross rent, with no deductions, when a home is let for living in (Tax Code art. 81). The general income tax rate is 20%.</td></tr>
 <tr><td>Sale after 2+ years</td><td class="k">0%</td><td>Gains on a home owned for more than two years are exempt.</td></tr>
 <tr><td>Sale within 2 years</td><td class="k">5%</td><td>On the gain, for apartments.</td></tr>
 <tr><td>Short-term letting as a sole trader</td><td class="k">1% of turnover</td><td>With small business status and turnover up to GEL 500,000 a year. Ask the Revenue Service whether it fits your letting.</td></tr>
 </tbody></table>
 <div class="note">Many sites still quote the old GEL 40,000 property-tax threshold. Check current rules with the Revenue Service (rs.ge) or a tax adviser, and check how your home country taxes income from Georgia.</div>
</div></section>
{CTA('costs')}''', h1='Costs and taxes',
 lede='Buying costs in Georgia are low: there is no transfer tax and total buyer costs are usually 0.6–1.1% of the price. Owners pay 5% on residential rent, and property tax only above a family income of GEL 100,000.',
 srcs=['gpg_buy', 'ii_2026', 'sova', 'madloba_rent', 'andersen', 'madloba_tax', 'rs', 'napr'])

need = ''.join(f'<tr><td>{n}</td><td class="n">{f(p)}</td><td class="n">{-(-150000 // p)} m²</td></tr>' for n, _, p, _ in AREAS)
S.page('residence-permit/', 'Georgian residence permit through property — $150,000 rule',
 'Georgia\'s property-based residence permit since 1 March 2026: the $150,000 threshold, valuation, family members, processing time and the floor area needed in each Batumi area.',
 [('residence-permit/', 'Residence permit')], f'''
{S.facts([('$150,000', 'minimum market value of non-agricultural property', 'since 1 March 2026; was $100,000'), ('1 year', 'permit term, renewable while you own the property', 'EIG Law'), ('up to 30 days', 'standard processing; faster for a higher fee', 'Madloba, October 2026')], three=True)}
<section class="band"><div class="wrap two">
 <div class="prose"><h2>Conditions</h2><ul class="txt"><li>You own non-agricultural property in Georgia registered in the Public Registry.</li><li>Its market value is at least $150,000, confirmed by a licensed valuer. The contract price is not what counts.</li><li>Several properties can be combined.</li><li>Your spouse and children can be included.</li></ul>
 <p>The permit is not automatic. The Public Service Development Agency decides, and the first application is usually made in person at a Public Service Hall.</p></div>
 <div class="prose"><h2>Limits</h2><ul class="txt"><li>This short-term permit does not lead to permanent residence.</li><li>Holders who qualified under the old $100,000 rule can keep renewing on the old terms while they keep that property.</li><li>A separate investment residence permit requires at least $300,000.</li><li>State fees depend on processing speed; see sda.gov.ge.</li></ul></div>
</div></section>
<section class="band alt"><div class="wrap"><h2>Floor area needed for $150,000</h2><p>At each area's average turnkey price (Galt &amp; Taggart, January–August 2026). The valuation of the actual unit decides.</p>
 <table><thead><tr><th>Area</th><th class="n">$/m²</th><th class="n">Area needed</th></tr></thead><tbody>{need}</tbody></table></div></section>
{CTA('residence', 'Batumi apartments from $150,000', 'Properties whose value may qualify for a residence permit.')}''', h1='Residence permit through property',
 lede='Since 1 March 2026, owning property in Georgia worth at least $150,000 lets you apply for a one-year renewable residence permit. In Batumi that means roughly 47 to 87 m² at average new-build prices.',
 srcs=['eig', 'madloba_rp', 'visaatlas', 'sda', 'gt_aug', 'gt_kob'])

S.page('rental-yields/', 'Batumi rental yields 2026 — what an apartment earns',
 'Gross rental yields in Batumi in 2026, rent per m², short-term letting rates, tax on rental income, and what to check in an aparthotel management contract.',
 [('rental-yields/', 'Rental yields')], f'''
{S.facts([('7.1%', 'gross yield, before costs and tax', 'June 2026, Galt &amp; Taggart'), ('$10.6–12.3', 'monthly rent per m² across areas', 'Q2 2026, Galt &amp; Taggart'), ('$65 / $54', 'average nightly rate, high / low season', '2026, International Investment')], three=True)}
<section class="band"><div class="wrap two">
 <div class="prose"><h2>A worked example</h2><p>A 40 m² apartment at average rents brings in about $424–492 a month, or $5,100–5,900 a year before costs. After utilities, repairs, management, vacancy and 5% tax, the net yield is lower than the 7.1% gross figure.</p>
 <p>Gross yields have fallen from 8.8% in 2024. In large complexes with hundreds of similar studios, competition for guests and resale buyers is strong.</p></div>
 <div class="prose"><h2>Long-term or nightly?</h2><table class="stack"><thead><tr><th></th><th>Long-term</th><th>Nightly</th></tr></thead><tbody>
 <tr><td class="k">Income</td><td>Steady, lower in peak season</td><td>Higher in summer, drops sharply in winter</td></tr>
 <tr><td class="k">Effort</td><td>Low</td><td>Cleaning, check-ins, platforms, or a management company</td></tr>
 <tr><td class="k">Tax</td><td>5% on gross rent if let for living in</td><td>Depends on the set-up; many register as a sole trader</td></tr></tbody></table></div>
</div></section>
<section class="band alt"><div class="wrap"><h2>Aparthotels and management contracts</h2>
 <p>Many complexes sell units with a management agreement: the operator lets the unit and splits income with the owner. Before buying, ask for the operator's share, who pays for repairs and furniture, the contract term and how to exit early. A developer's projected yield is a forecast, not a guarantee.</p>
 <div class="note">Check in the registry extract whether the unit is registered as a residence or as a non-residential hotel room. It changes how rental income is taxed.</div>
 {S.related([('costs-and-taxes/', 'All taxes'), ('areas/', 'Compare areas')])}
</div></section>
{CTA('yields', 'Apartments to let in Batumi', 'Furnished units in areas with strong rental demand.')}''', h1='Rental yields in Batumi',
 lede='Batumi apartments earned a gross yield of about 7.1% a year in June 2026 (Galt &amp; Taggart). Individuals pay 5% on residential rent; nightly letting and hotel-room units follow different rules.',
 srcs=['ii_2026', 'hs_yield', 'oversupply', 'madloba_rent', 'madloba_tax', 'rs'])

S.page('buying-remotely/', 'Buying property in Batumi without travelling — power of attorney',
 'How to buy an apartment in Batumi remotely: power of attorney, apostille and translation, paying safely and what your representative should check.',
 [('buying-remotely/', 'Buying remotely')], f'''
<section class="band"><div class="wrap two">
 <div class="prose"><h2>How it works</h2><p>You can buy through a representative holding your power of attorney. You sign it before a notary in your country; in Georgia it is translated into Georgian and the translation is notarised.</p>
 <p>Documents from most countries need an apostille. Russian powers of attorney do not, because Russia and Georgia are both parties to the Minsk Convention.</p>
 <h2>Scope the power carefully</h2><ul class="txt"><li>Name the specific property, or limit the price and area.</li><li>Say whether the representative may sign the preliminary agreement, the sale contract, or both.</li><li>Do not grant the right to receive your money unless you mean to.</li></ul></div>
 <div class="prose"><h2>Paying safely</h2><ul class="check"><li>Pay by bank transfer directly to the seller's account.</li><li>Ask for the registry extract before any deposit and again just before signing.</li><li>Get the signed contract and the new registry extract once ownership is registered.</li><li>Use a representative who is independent of the seller or developer.</li></ul>
 <div class="note">Some buyers watch a video viewing before signing. A video call shows the flat, but not the building's services or the land title; the registry check still matters.</div></div>
</div></section>
<section class="band alt"><div class="wrap">{S.related([('how-to-buy/', 'Full buying process'), ('costs-and-taxes/', 'Costs'), ('contact/', 'Ask a question')])}</div></section>
{CTA('remote')}''', h1='Buying in Batumi without travelling',
 lede='You do not need to be in Georgia to buy. A representative can sign for you under a notarised power of attorney, translated into Georgian; the sale is registered in the same way.',
 srcs=['madloba_poa', 'madloba_buy', 'napr'])

FAQ = [
 ('Can foreigners buy property in Batumi?', 'Yes, on the same terms as Georgian citizens. Only agricultural land is restricted.', 'how-to-buy/'),
 ('Do I need a visa or residence to buy?', 'No. A passport is enough.', 'how-to-buy/'),
 ('How much does an apartment cost?', 'New developments averaged $1,408 per m² in September 2026 (Colliers). Turnkey new builds range from $1,734 to $3,224 per m² by area.', 'prices/'),
 ('Which area sells the most?', 'New Boulevard: 4,417 sales in January–August 2026, about 40% of the city total.', 'areas/'),
 ('What rental yield can I expect?', 'About 7.1% gross (June 2026), before costs and tax.', 'rental-yields/'),
 ('What taxes will I pay?', 'No transfer tax. 5% on residential rent; no tax on a sale after two years of ownership; property tax only above a family income of GEL 100,000.', 'costs-and-taxes/'),
 ('Does buying give me residence?', 'Property worth at least $150,000 lets you apply for a one-year renewable residence permit. It is not automatic.', 'residence-permit/'),
 ('Can I buy without travelling?', 'Yes, through a representative with a notarised power of attorney translated into Georgian.', 'buying-remotely/'),
 ('Is off-plan safe?', 'There is no state guarantee for off-plan buyers. Check land ownership, the building permit and the developer\'s delivered projects, and tie payments to construction stages.', 'how-to-buy/'),
]
ldq = json.dumps({'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a, _ in FAQ]}, ensure_ascii=False)
S.page('faq/', 'Batumi real estate FAQ', 'Short answers about buying property in Batumi: rules for foreigners, prices, yields, taxes, residence and remote purchase.',
 [('faq/', 'FAQ')], '<section class="band"><div class="wrap">' + ''.join(f'<details><summary>{q}</summary><p>{a} {S.a(t, "Read more")}</p></details>' for q, a, t in FAQ) + '</div></section>' + CTA('faq'),
 h1='Frequently asked questions', lede='Short answers with links to the full pages. Figures as of November 2026.', srcs=['madloba_buy', 'ii_2026', 'gt_aug', 'sova', 'eig'],
 head_extra=f'\n<script type="application/ld+json">{ldq}</script>')

S.page('about/', 'About Batumi/Real Estate', 'Who writes this guide, where the data comes from and how it relates to the Brik property platform.', [('about/', 'About')], f'''
<section class="band"><div class="wrap two"><div class="prose"><h2>What this is</h2><p>Batumi/Real Estate is an English guide for people thinking of buying property in Batumi. It brings prices, areas, rules and taxes together in plain language.</p>
<p>The guide is part of <a href="{S.brik('about')}">Brik</a>, a property platform for Georgia. Listing links and the request form lead to Brik's catalogue and agency.</p>
<h2>How we work</h2><ul class="txt"><li>Every figure names its source and period.</li><li>We do not mix price series from different analysts in one comparison.</li><li>Legal and tax pages are reviewed by Brik's partners in Georgia.</li><li>This is general information, not legal advice.</li></ul></div>
<div class="prose"><h2>Authors</h2><div class="note">Draft: author and reviewer names, photos and experience go here.</div><h2>Spotted an error?</h2><p>Rules and prices change. Tell us via the {S.a("contact/", "contact page")}.</p></div></div></section>''',
 h1='About this guide', lede='An independent English guide to buying in Batumi, part of the Brik project.')

S.page('contact/', 'Contact — Batumi/Real Estate', 'Contact the Brik team about buying property in Batumi.', [('contact/', 'Contact')], f'''
<section class="band"><div class="wrap two"><div class="prose"><h2>Ask us</h2><p>A Brik agent can answer questions about areas, specific apartments and the buying process, and send a shortlist.</p><div class="note">Draft: phone, messengers, email and office address will be added before launch.</div></div>
{form()}</div></section>''', h1='Contact', lede='Ask a question or request a shortlist of Batumi apartments.')

S.page('privacy/', 'Privacy notice — Batumi/Real Estate', 'What data this site collects and how it is used.', [('privacy/', 'Privacy')], '''
<section class="band"><div class="wrap prose"><div class="note">Draft for legal review: the legal entity, address and contact for data requests will be added before launch.</div>
<h2>What we collect</h2><p>What you enter in the request form: name, contact details, budget, area, goal and your message.</p>
<h2>Why</h2><p>So a Brik agent can contact you and send apartments that match. We do not use it for anything else without your consent.</p>
<h2>Who sees it</h2><p>The Brik team. We do not sell your data or share it with third parties unless the law requires it.</p>
<h2>How long we keep it</h2><p>As long as needed to answer and support your purchase, or until you ask us to delete it.</p>
<h2>Your rights</h2><p>You can ask to see, correct or delete your data. The main Brik site has its own privacy notice.</p>
<h2>Analytics</h2><p>We may use web analytics. Links to Brik carry tags that show the visit came from this site.</p></div></section>''',
 h1='Privacy notice', lede='How we handle the data you send through the request form.')

S.finish()
