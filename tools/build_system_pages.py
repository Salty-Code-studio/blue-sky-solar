#!/usr/bin/env python3
"""Generates the six system landing pages from one template.

Run from anywhere:  python3 tools/build_system_pages.py
Header, mobile nav, footer and sticky CTA are copied from index.html at build time.
"""
import html, json, re, sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://blueskysolarbonaire.com"
E = lambda s: html.escape(s, quote=False)
A = lambda s: html.escape(s, quote=True)

COST = "It depends on how much power you use and what you want to fix. We give a free consultation and a custom quote. Material prices move with purchase and transport costs, so ask for the current figure."

# ---------------------------------------------------------------- data
SYSTEMS = {}

SYSTEMS["hybrid"] = dict(
    slug="hybrid-solar-bonaire", name="Hybrid solar", goal="backup",
    title="Hybrid Solar with Battery on Bonaire | Blue Sky Solar",
    desc="Hybrid solar with a battery on Bonaire. Cut your WEB bill and keep the lights on in an outage. Drone design, own crew, monitoring app. Free roof design.",
    service="Hybrid solar and battery systems",
    photo="irene-roof", photo_alt="Solar panels on a red roof in Bonaire",
    photo2="irene-shed", photo2_alt="Hybrid inverter and battery setup in a shed",
    h1="Hybrid solar on Bonaire.", h1b="Your lights stay on when WEB goes down.",
    lead="Panels make power by day. A battery keeps some for later. The grid stays connected as your backup.",
    wa="Hi Blue Sky, I would like a hybrid solar system with a battery on Bonaire.",
    card="Sun by day, battery at night, grid only when you need it.",
    diagram=dict(w=680, h=250, nodes=[
        ("p", 10, 95, 150, "Panels", "make the power", "sun"),
        ("i", 255, 95, 170, "Hybrid inverter", "manages the flow", ""),
        ("h", 520, 15, 150, "Your home", "runs first", ""),
        ("b", 520, 95, 150, "Battery", "stores the extra", ""),
        ("g", 520, 175, 150, "WEB grid", "backup", ""),
    ], edges=[("p", "i", 0), ("i", "h", 0), ("i", "b", 1), ("i", "g", 1)],
    label="Diagram: panels feed a hybrid inverter, which feeds your home, a battery and the WEB grid."),
    how_h="Sun by day. Battery at night. Grid as the safety net.",
    how_intro="A hybrid system is solar and a battery working with the grid. Here is what happens through the day.",
    how=[("Panels feed the house first", "Your panels power the home while the sun is up. What you do not use goes into the battery."),
         ("The battery holds the rest", "When the sun goes down, the battery takes over. You draw less from WEB."),
         ("The grid is still there", "If the battery runs low, the house pulls from WEB. If WEB drops out, you keep your power.")],
    fit_h="Who a hybrid fits.",
    fit=["You want a lower bill and power that survives an outage.",
         "WEB cuts and spikes have cost you comfort or damaged equipment.",
         "You already have panels and want to add a battery. Louis and Irene did exactly that, adding a battery to their ten panels.",
         "You want to keep the grid as a safety net instead of leaving it."],
    facts=[("Payback", "Usually 4 to 5 years"), ("Works in a blackout", "Yes"), ("Battery", "Yes"),
           ("Grid connection", "Kept as backup"), ("Roofs", "Sloped, flat, tile, corrugated"), ("Install", "Typically two days")],
    bn_h="Outages are normal here. Your home should not notice.",
    bn_p="Bonaire has over 3,000 sunshine hours a year. It also has WEB outages and power spikes. A hybrid system turns the first into a fix for the second.",
    bn=[("Heat", "Panels, inverters and batteries work in high heat. We plan the battery space with that in mind."),
        ("Salt air", "Salt reaches everything on the coast. Every system we build has to handle it."),
        ("Sun", "Over 3,000 sunshine hours a year give the battery plenty to fill from."),
        ("WEB outages", "The battery keeps the house running while WEB is down.")],
    proc_note=["The design drawing shows where the panels go. The battery space is part of the quote.",
               "Typical install takes two days. Our own electricians do the work.",
               "You see battery level, solar output and grid use on your phone."],
    proof=dict(big="Air-con all day. Only the fixed fee left.",
               quote="“We now use the air conditioning during the day without worries.”",
               cite="Louis and Irene, nine years on Bonaire. They added a battery to ten existing panels and now pay only the fixed monthly fee.",
               extra="“What I gained is independence.”", extra_cite="Ferry Maat, radio DJ. His WEB bill went from $350 a month to a few dollars."),
    faq=[("Does hybrid solar keep my power on when WEB goes down?", "Yes. A hybrid system has a battery, so you have power during outages."),
         ("How long does a hybrid take to pay back?", "Usually 4 to 5 years. Grid tied pays back faster, at around 2 years, but it gives no backup in an outage."),
         ("Can I add a battery to the panels I already have?", "Often yes. Louis and Irene had ten panels and added a battery for blackouts. Tell us what you have and we will look at it."),
         ("Will I still pay WEB anything?", "The grid stays connected. Louis and Irene now pay only the fixed monthly fee."),
         ("How do I see what the system is doing?", "We set up the monitoring app with you before we leave. Battery level, solar output and grid use show on your phone."),
         ("What does a hybrid system cost?", COST)],
    cta_h="Keep the lights on. Pay less.", cta_p="Get a free drone photo and design drawing of your roof. Remco calls you back within one business day.",
)

SYSTEMS["offgrid"] = dict(
    slug="off-grid-solar-bonaire", name="Off-grid solar", goal="offgrid",
    title="Off-Grid Solar on Bonaire | Blue Sky Solar",
    desc="Off-grid solar on Bonaire for remote sites and full independence. Panels charge batteries that power your whole home. Free roof design from a local crew.",
    service="Off-grid solar and battery systems",
    photo="install", photo_alt="Blue Sky Solar technician wiring Victron inverters",
    photo2="techroom", photo2_alt="Technical room with Victron inverters and EG4 batteries",
    h1="Off-grid solar on Bonaire.", h1b="Your home runs on its own.",
    lead="No grid line and no WEB bill. Your panels charge your batteries and the batteries power everything.",
    wa="Hi Blue Sky, I would like an off-grid solar system on Bonaire.",
    card="Panels charge your batteries and your home runs on its own.",
    diagram=dict(w=680, h=140, nodes=[
        ("p", 5, 40, 140, "Panels", "roof or frame", "sun"),
        ("b", 195, 40, 140, "Batteries", "hold the power", ""),
        ("i", 385, 40, 140, "Inverter", "makes it usable", ""),
        ("h", 575, 40, 100, "Home", "all of it", ""),
    ], edges=[("p", "b", 0), ("b", "i", 0), ("i", "h", 0)],
    label="Diagram: panels charge batteries, an inverter turns that into household power, and your home runs on it."),
    how_h="Sun in. Batteries hold it. Everything runs.",
    how_intro="Off-grid means the system is the whole supply. It has to be sized to how you really live.",
    how=[("Panels charge the batteries", "The panels sit on the roof, or on a ground frame if the roof is not the right one. All that sun goes into storage."),
         ("The batteries run everything", "Your home draws from the battery bank. We design the bank around your daily use."),
         ("Nothing comes from the grid", "There is no WEB line to lean on. That is why the design drawing comes with the quote.")],
    fit_h="Who off-grid fits.",
    fit=["Your site is remote and the grid is far away or not there.",
         "You want full independence from WEB, its bill and its outages.",
         "You are ready to size the system to your real use. We size the panels and batteries around how much you use each day.",
         "You have space for a battery room. Mario on our crew builds them."],
    facts=[("Payback", "Usually 4 to 5 years"), ("Grid use", "0 kWh"), ("Battery", "Runs everything"),
           ("Mounting", "Roof or ground frame"), ("Roofs", "Sloped, flat, tile, corrugated"), ("Install", "Typically two days")],
    bn_h="Built for a place with no second chance.",
    bn_p="When you are off-grid there is no fallback. The system has to cope with Bonaire's conditions every single day.",
    bn=[("Heat", "Batteries and inverters sit in a hot climate. The battery room is planned for it."),
        ("Salt air", "Salt air is hard on equipment. Every system we build has to handle it."),
        ("Sun", "Over 3,000 sunshine hours a year are the fuel for the whole system."),
        ("WEB outages", "You have no WEB line to lose. Outages stop being your problem.")],
    proc_note=["The design drawing comes with your quote. We size it around how much you use each day.",
               "Typical install takes two days. Battery room work is done by our own crew.",
               "Remote monitoring and service help when the site is far from town."],
    proof=dict(big="Two months in. Every kind of weather.",
               quote="“The fully off-grid system has now been operational for two months and has performed exceptionally well under all weather conditions.”",
               cite="Remco Vinck, June 2026",
               extra="", extra_cite=""),
    faq=[("Can a whole home run off-grid on Bonaire?", "Yes. Off-grid means fully independent of the grid. The batteries power everything."),
         ("How long does off-grid take to pay back?", "Usually 4 to 5 years, the same range as a hybrid system."),
         ("What if my roof is not suitable?", "Panels can also go on a ground frame or another structure on your property. The drone photo shows us the options."),
         ("How does it handle bad weather?", "One customer wrote that his fully off-grid system performed exceptionally well under all weather conditions after two months."),
         ("Can you watch an off-grid system for me?", "We set up the monitoring app with you before we leave. We also offer remote monitoring and service for remote sites and vacation homes."),
         ("What does an off-grid system cost?", COST)],
    cta_h="Done with the grid? Let's design the way out.", cta_p="Get a free drone photo and design drawing. We size the batteries around how you live.",
)

SYSTEMS["gridtied"] = dict(
    slug="grid-tied-solar-bonaire", name="Grid tied solar", goal="bill",
    title="Grid Tied Solar on Bonaire | Blue Sky Solar",
    desc="Grid tied solar on Bonaire: the lowest cost way to cut your WEB bill, with payback around 2 years. Free drone roof design and a local install crew.",
    service="Grid tied solar systems",
    photo="gridtied", photo_alt="Fronius grid tied inverter on a wall",
    photo2="villa-roof", photo2_alt="Solar panels on a villa roof by the water",
    h1="Grid tied solar on Bonaire.", h1b="The fastest way to cut your WEB bill.",
    lead="Solar covers your daytime use. The grid fills the rest. No battery means the lowest cost way in.",
    wa="Hi Blue Sky, I would like a grid tied solar system to lower my bill on Bonaire.",
    card="Solar covers your daytime use and the grid fills the rest.",
    diagram=dict(w=680, h=230, nodes=[
        ("p", 10, 20, 150, "Panels", "daytime power", "sun"),
        ("i", 255, 20, 170, "Inverter", "grid tied", ""),
        ("h", 520, 20, 150, "Your home", "uses it live", ""),
        ("g", 255, 150, 170, "WEB grid", "fills the gap", ""),
    ], edges=[("p", "i", 0), ("i", "h", 0), ("g", "h", 0)],
    label="Diagram: panels feed an inverter and then your home. The WEB grid supplies the rest, especially at night."),
    how_h="Simple on purpose.",
    how_intro="A grid tied system has no battery. That keeps it cheap and keeps the payback short.",
    how=[("Panels power your day", "While the sun is up, your panels run the home. Less of your bill is WEB power."),
         ("The grid covers the night", "After dark, and whenever the panels cannot keep up, you draw from WEB like you always did."),
         ("No battery to buy", "Skipping the battery is why this is the lowest cost way to cut the bill.")],
    fit_h="Who grid tied fits.",
    fit=["You want the quickest payback. It is around 2 years.",
         "You use most of your power in the daytime.",
         "Your main problem is the bill, not the blackouts.",
         "You can live without backup power. If you cannot, look at hybrid instead."],
    facts=[("Payback", "About 2 years"), ("Works in a blackout", "No"), ("Battery", "None"),
           ("Entry cost", "The lowest of the three"), ("Roofs", "Sloped, flat, tile, corrugated"), ("Install", "Typically two days")],
    bn_h="Sun does the heavy lifting here.",
    bn_p="Bonaire gets over 3,000 sunshine hours a year. A grid tied system turns that straight into a smaller bill, with nothing in between.",
    bn=[("Heat", "Hot days are sunny days. The equipment is chosen to take the heat."),
        ("Salt air", "Salt air reaches the roof too. Every system we build has to handle it."),
        ("Sun", "Over 3,000 sunshine hours mean your panels work most of the year."),
        ("WEB outages", "Be aware: a grid tied system gives no backup in an outage.")],
    proc_note=["The design drawing shows every panel. You see the layout before you sign.",
               "Typical install takes two days. No battery room to build.",
               "The app shows what the panels produce while you are at work or on the beach."],
    proof=dict(big="A date. A price. Then delivered.",
               quote="“It’s so refreshing to find a company on Bonaire that sets a date, a price and then delivers what they promise.”",
               cite="Rob Wiens, October 2026, on working with our crew.",
               extra="", extra_cite=""),
    faq=[("Does grid tied solar work in a blackout?", "No. A grid tied system gives no backup during outages. If you want power in an outage, choose hybrid."),
         ("How long does grid tied take to pay back?", "Around 2 years. It is the fastest payback of our systems."),
         ("Why choose grid tied over hybrid?", "Grid tied is the lowest cost way to cut the bill. Hybrid adds a battery and outage power, and pays back in about 4 to 5 years."),
         ("Do I need a battery?", "No. Solar works during the day and the grid supplies the rest."),
         ("How long does the install take?", "Typically two days on site."),
         ("What does a grid tied system cost?", COST)],
    cta_h="Smaller bill. Quicker payback.", cta_p="Get a free drone photo and design drawing. You see every panel before you sign.",
)

SYSTEMS["heater"] = dict(
    slug="solar-water-heater-bonaire", name="Solar water heater", goal="", proc_titles=["Free advice at your place", "Our own crew installs", "Hot water from the sun"],
    title="Solar Water Heater on Bonaire | Blue Sky Solar",
    desc="Sunpad solar water heater on Bonaire. A 150 litre tank heats to 85°C and gives up to 380 litres at 40°C, with no electricity needed. Ask for a free quote.",
    service="Solar water heater installation",
    photo="heater", photo_alt="Sunpad solar water heater on a tiled roof",
    photo2="villa-pool", photo2_alt="Pool and terrace of a solar powered villa on Bonaire",
    h1="Solar water heater on Bonaire.", h1b="Hot showers without electricity.",
    lead="A Sunpad heats a 150 litre tank to 85°C using only the sun. It gives you up to 380 litres of water at 40°C.",
    wa="Hi Blue Sky, I would like a Sunpad solar water heater on Bonaire.",
    card="Sunpad heats a 150 litre tank to 85°C. No electricity needed.",
    diagram=dict(w=680, h=140, nodes=[
        ("s", 5, 40, 190, "The sun", "even on cloudy days", "sun"),
        ("t", 245, 40, 190, "150 litre tank", "heats to 85°C", ""),
        ("h", 485, 40, 190, "Hot water", "up to 380 L at 40°C", ""),
    ], edges=[("s", "t", 0), ("t", "h", 0)],
    label="Diagram: sun heats a 150 litre Sunpad tank to 85 degrees, which gives up to 380 litres of water at 40 degrees."),
    how_h="The sun heats the tank. You open the tap.",
    how_intro="No app and no power bill for hot water. The Sunpad does one job.",
    how=[("The sun does the heating", "The Sunpad works on sunshine. It keeps working on cloudy days."),
         ("The tank holds the heat", "A 150 litre tank heats up to 85°C."),
         ("One tank, a lot of showers", "That hot water gives you up to 380 litres at 40°C, a comfortable shower temperature.")],
    fit_h="Who a solar water heater fits.",
    fit=["You pay to heat water and want that part of the bill gone.",
         "You want hot water that needs no electricity to make.",
         "You prefer low maintenance and little to worry about.",
         "You have a roof with sun. Sloped, flat, tile and corrugated sheet roofs all work for our crew."],
    facts=[("Tank", "150 litres"), ("Heats to", "85°C"), ("Hot water", "Up to 380 L at 40°C"),
           ("Electricity needed", "None"), ("Cloudy days", "Still works"), ("Maintenance", "Low")],
    bn_h="Bonaire is a hot water machine.",
    bn_p="With over 3,000 sunshine hours a year, a roof gets plenty of sun. A Sunpad puts that to work without using any electricity.",
    bn=[("Heat", "The Sunpad exists to make heat, so Bonaire's climate suits it."),
        ("Salt air", "Salt air is part of life on the coast. Every system we install has to handle it."),
        ("Sun", "Over 3,000 sunshine hours a year. The Sunpad also works on cloudy days."),
        ("WEB outages", "No electricity needed, so an outage does not stop the Sunpad from heating.")],
    proc_note=["We look at your roof and your hot water use, and advise where the Sunpad goes.",
               "Our own crew installs it.",
               "We walk you through how it works before we leave."],
    proof=dict(big="Rated 5.0 from 46 reviews.",
               quote="“Doen wat ze beloven. Vakmensen die gewoon hun werk doen.”",
               cite="Ruben van der Ploeg, July 2026. In English: they do what they promise. Tradespeople who simply do their job.",
               extra="", extra_cite=""),
    faq=[("How much hot water does a Sunpad give?", "The Sunpad has a 150 litre tank that heats to 85°C. It gives you up to 380 litres of water at 40°C."),
         ("Does a solar water heater need electricity?", "No. The Sunpad needs no electricity."),
         ("Does it work on cloudy days?", "Yes. It still works on cloudy days."),
         ("How much maintenance does it need?", "Low maintenance."),
         ("Can you fit it on my roof?", "Most likely. We install on sloped, flat, tile and corrugated sheet roofs."),
         ("What does a solar water heater cost?", "It depends on what you want to fix. We give a free consultation and a custom quote. Material prices move with purchase and transport costs, so ask for the current figure.")],
    cta_h="Hot water from the sun.", cta_p="Ask for a free consultation. Remco calls you back within one business day.",
)

SYSTEMS["ev"] = dict(
    slug="ev-charging-bonaire", name="EV charging", goal="",
    title="EV Charging on Bonaire, Solar Powered | Blue Sky Solar",
    desc="EV charging on Bonaire at home, at your business or at public locations, powered by solar. Own install crew and a free consultation. Ask for your quote.",
    service="Solar powered EV charger installation",
    photo="ev", photo_alt="Blue EV charger on a wall",
    photo2="install", photo2_alt="Blue Sky Solar technician wiring Victron inverters",
    h1="EV charging on Bonaire.", h1b="Drive on your own sunshine.",
    lead="Fit a charger at home, at your business or at a public location. Power it with solar.",
    wa="Hi Blue Sky, I would like a solar powered EV charger on Bonaire.",
    card="A charger at home, at your business or for your guests.",
    diagram=dict(w=680, h=140, nodes=[
        ("p", 5, 40, 140, "Panels", "make the power", "sun"),
        ("i", 195, 40, 140, "Inverter", "converts it", ""),
        ("c", 385, 40, 140, "EV charger", "wall mounted", ""),
        ("v", 575, 40, 100, "Your EV", "", ""),
    ], edges=[("p", "i", 0), ("i", "c", 0), ("c", "v", 0)],
    label="Diagram: solar panels feed an inverter, which feeds an EV charger, which charges your electric vehicle."),
    how_h="Sun goes in. Kilometres come out.",
    how_intro="An EV charger is only as good as the power behind it. Ours run on solar.",
    how=[("Panels make the power", "Solar panels on your roof or a frame produce the electricity."),
         ("The charger delivers it", "A charger on your wall or in your car park hands that power to the vehicle."),
         ("You plug in", "Park, plug in, leave. You can check how the system is doing from the monitoring app.")],
    fit_h="Who solar EV charging fits.",
    fit=["You drive electric at home and want to charge from your own roof.",
         "You run a business and want chargers for staff, customers or guests.",
         "You manage a public location and want charging powered by solar.",
         "You want one crew for the panels and the charger."],
    facts=[("Where", "Home, business or public"), ("Powered by", "Solar"), ("Installed by", "Our own crew"),
           ("Monitoring", "App set up before we leave"), ("Quote", "Free consultation, custom"), ("Roofs", "Sloped, flat, tile, corrugated")],
    bn_h="A sunny island is the right place to plug in.",
    bn_p="Bonaire has over 3,000 sunshine hours a year. That is a lot of fuel to put in a car.",
    bn=[("Heat", "Chargers and inverters work outdoors in high heat. We plan the install with that in mind."),
        ("Salt air", "Salt air reaches wall boxes and cables too. Every system we build has to handle it."),
        ("Sun", "Over 3,000 sunshine hours a year to charge from."),
        ("WEB outages", "Outages and spikes are a real pain point on Bonaire. Your own solar gives you a supply of your own.")],
    proc_note=["We fly the roof and draw the panel layout. The charger location is part of the plan.",
               "Our own electricians install. Typical solar installs take two days.",
               "We set up the app with you before we leave."],
    proof=dict(big="Rated 5.0 from 46 reviews.",
               quote="",
               cite="",
               extra="Reviews keep mentioning the same things: dates that hold, tidy installs and a crew that enjoys the work.", extra_cite=""),
    faq=[("Where can you install an EV charger?", "At home, at your business or at public locations."),
         ("Is the charger powered by solar?", "Yes. Our EV charging is powered by solar."),
         ("Can I offer charging to guests or customers?", "Yes. A charger at your business or for your guests is something we install."),
         ("Who installs it?", "Our own crew. We also set up the monitoring app with you before we leave."),
         ("Do I need new panels?", "Tell us what you have in your free consultation. We size the solar side around what you want to fix."),
         ("What does EV charging cost?", "It depends on your setup and your goal. We give a free consultation and a custom quote. Material prices move with purchase and transport costs, so ask for the current figure.")],
    cta_h="Charge from your own roof.", cta_p="Tell us where the car parks. We design the solar and the charger together.",
)

SYSTEMS["commercial"] = dict(
    slug="commercial-solar-bonaire", name="Commercial and custom solar", goal="",
    title="Commercial Solar on Bonaire | Blue Sky Solar",
    desc="Commercial and custom solar on Bonaire: large facilities, villas, boats and remote sites. Drone design, battery rooms, remote monitoring and local service.",
    service="Commercial and custom solar systems",
    photo="villa-roof", photo_alt="Solar panels on a villa roof by the water",
    photo2="techroom", photo2_alt="Victron and EG4 equipment in a technical room",
    h1="Commercial solar on Bonaire.", h1b="Bring us the hard roof.",
    lead="Large facilities, rental villas, boats and remote sites. We design around your building, then service it on island.",
    wa="Hi Blue Sky, I would like a commercial or custom solar system on Bonaire.",
    card="Larger buildings, villas, boats and remote sites.",
    diagram=dict(w=680, h=230, nodes=[
        ("p", 5, 20, 170, "Panels", "roof, frame or shade roof", "sun"),
        ("e", 255, 20, 170, "Inverters, batteries", "in one tech room", ""),
        ("s", 510, 20, 165, "Your site", "building, boat, remote", ""),
        ("m", 255, 150, 170, "Monitoring app", "we see it too", ""),
    ], edges=[("p", "e", 0), ("e", "s", 0), ("e", "m", 0)],
    label="Diagram: panels on roofs or frames feed inverters and batteries in a technical room. They power your site and report to a monitoring app."),
    how_h="Custom does not mean complicated.",
    how_intro="Bigger or stranger jobs get the same simple path. We start with the roof and work out from there.",
    how=[("We fly the site", "A drone photo shows every roof area. Small, awkward roofs and ground frames go on the same drawing."),
         ("Equipment goes in one place", "For one customer with a challenging roof and many small areas, all the equipment fit in a small technical room. Mario builds battery rooms when you need one."),
         ("We keep watching", "Remote monitoring and service means we can look after a site you do not visit every day.")],
    fit_h="Who custom and commercial fits.",
    fit=["You run a large commercial facility.",
         "You own a boat or a remote site that needs its own power.",
         "You manage a vacation home or rental villa, perhaps from abroad.",
         "Your roof is awkward. Many small areas, shade structures or no good roof at all."],
    facts=[("Scope", "Facilities, villas, boats, remote sites"), ("Roofs", "Sloped, flat, tile, corrugated"),
           ("Mounting", "Ground frames and structures possible"), ("Design", "Drone photo and drawing"),
           ("Monitoring", "Remote, for vacation homes too"), ("Service", "On island")],
    bn_h="Built for work that has to keep working.",
    bn_p="A business cannot afford a system that struggles in Bonaire's conditions. We design for them from the first drawing.",
    bn=[("Heat", "Equipment rooms get hot. We plan the space and choose gear that handles high heat."),
        ("Salt air", "Salt air is a daily fact on the coast and on boats. Every system we build has to handle it."),
        ("Sun", "Over 3,000 sunshine hours a year give a large roof a lot to work with."),
        ("WEB outages", "Outages and power spikes are a real pain point on Bonaire. We design with that in mind.")],
    proc_note=["The drawing covers every usable roof area, frame and shade roof on the site.",
               "Our own electricians and construction crew do the work. A typical install takes two days.",
               "Remote monitoring is set up with you before we leave."],
    proof=dict(big="Rated 5.0 from 46 reviews.",
               quote="",
               cite="",
               extra="Paul van der Wal, November 2026, needed a solution for a challenging roof with many small areas. All the equipment was fitted in a small technical room.", extra_cite=""),
    faq=[("What kinds of sites do you cover?", "Large commercial facilities, boats, remote sites and vacation homes."),
         ("Can you handle a difficult roof?", "Yes. We install on sloped, flat, tile and corrugated sheet roofs, and we can build ground frames and structures."),
         ("Can you look after a site I am not at?", "Yes. We offer remote monitoring and service for vacation homes. We also set up the monitoring app with you before we leave."),
         ("Do you build battery rooms?", "Yes. Mario on our crew builds battery rooms."),
         ("Who does the work?", "Our own crew: electricians, construction and warehouse, working from our base on Kaya Industria Pariba."),
         ("What does a custom system cost?", "It depends on consumption and your goal. We give a free consultation and a custom quote. Material prices move with purchase and transport costs, so ask for the current figure.")],
    cta_h="Bring us the hard roof.", cta_p="Get a free drone photo and design drawing. Remco calls you back within one business day.",
)

ORDER = ["hybrid", "offgrid", "gridtied", "heater", "ev", "commercial"]
SHORTNAME = dict(hybrid="Hybrid", offgrid="Off-grid", gridtied="Grid tied", heater="Solar water heater", ev="EV charging", commercial="Custom and commercial")
FAQ_TOPIC = dict(hybrid="hybrid solar", offgrid="off-grid solar", gridtied="grid tied solar", heater="solar water heaters", ev="EV charging", commercial="commercial solar")

# ---------------------------------------------------------------- pieces
def pic(name, alt, eager=False, w=None, h=None):
    attrs = f' width="{w}" height="{h}"' if w else ""
    ld = ' fetchpriority="high"' if eager else ' loading="lazy"'
    return f'<picture><source srcset="img/{name}.webp" type="image/webp"><img src="img/{name}.jpg" alt="{A(alt)}"{attrs}{ld}></picture>'

ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

def diagram(d):
    nodes = {n[0]: n for n in d["nodes"]}
    H = 56
    out = [f'<svg class="flow-svg" viewBox="0 0 {d["w"]} {d["h"]}" role="img" aria-label="{A(d["label"])}">',
           '<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1673d4"/></marker></defs>']
    for a, b, both in d["edges"]:
        na, nb = nodes[a], nodes[b]
        ax, ay, aw = na[1], na[2], na[3]
        bx, by, bw = nb[1], nb[2], nb[3]
        if abs(ax + aw / 2 - (bx + bw / 2)) < 30:  # vertical
            x1 = x2 = ax + aw / 2
            if by > ay:
                y1, y2 = ay + H, by
            else:
                y1, y2 = ay, by + H
        else:
            if bx > ax:
                x1, x2 = ax + aw, bx
            else:
                x1, x2 = ax, bx + bw
            y1, y2 = ay + H / 2, by + H / 2
        ms = ' marker-start="url(#ah)"' if both else ""
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#1673d4" stroke-width="2.5" marker-end="url(#ah)"{ms}/>')
    for id_, x, y, w, label, sub, kind in d["nodes"]:
        fill, stroke = ("#fdf0d3", "#f4a52a") if kind == "sun" else ("#e6f0fb", "#1673d4")
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{H}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
        ty = y + (24 if sub else 34)
        out.append(f'<text x="{x + w / 2}" y="{ty}" text-anchor="middle" font-family="Outfit,sans-serif" font-weight="600" font-size="17" fill="#062f4c">{E(label)}</text>')
        if sub:
            out.append(f'<text x="{x + w / 2}" y="{y + 43}" text-anchor="middle" font-family="Figtree,sans-serif" font-size="13" fill="#5a6773">{E(sub)}</text>')
    out.append("</svg>")
    return "\n".join(out)

def jsonld(s, url):
    prov = {"@type": "LocalBusiness", "name": "Blue Sky Solar Bonaire", "url": SITE, "telephone": "+5997841782",
            "email": "info@blueskysolarbonaire.com",
            "address": {"@type": "PostalAddress", "streetAddress": "Kaya Industria Pariba 50", "addressLocality": "Kralendijk", "addressRegion": "Bonaire", "addressCountry": "BQ"},
            "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "bestRating": "5", "reviewCount": "46"}}
    service = {"@context": "https://schema.org", "@type": "Service", "name": s["service"] + " on Bonaire", "serviceType": s["service"],
               "description": s["desc"], "url": url, "areaServed": {"@type": "Place", "name": "Bonaire"}, "provider": prov}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Systems", "item": SITE + "/systems/"},
        {"@type": "ListItem", "position": 3, "name": s["name"], "item": url}]}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in s["faq"]]}
    return "\n".join('<script type="application/ld+json">\n' + json.dumps(o, ensure_ascii=False, indent=2) + "\n</script>" for o in (service, crumbs, faq))

def proof_html(s):
    p = s["proof"]
    parts = [f'<div class="proof-big">{E(p["big"])}</div><div class="proof-side">']
    if p["quote"]:
        parts.append(f'<figure class="q"><blockquote>{E(p["quote"])}</blockquote><figcaption>{E(p["cite"])}</figcaption></figure>')
    if p["extra"] and p["extra_cite"]:
        parts.append(f'<figure class="q"><blockquote>{E(p["extra"])}</blockquote><figcaption>{E(p["extra_cite"])}</figcaption></figure>')
    elif p["extra"]:
        parts.append(f'<p class="proof-note">{E(p["extra"])}</p>')
    if "5.0" not in p["big"]:
        parts.append('<p class="proof-note">Blue Sky Solar is rated 5.0 from 46 reviews.</p>')
    parts.append('<a class="more" href="results.html">Read every customer story ' + ARROW + '</a></div>')
    return "".join(parts)

def build(key, shell):
    s = SYSTEMS[key]
    url = f'{SITE}/{s["slug"]}/'
    assert 140 <= len(s["desc"]) <= 160, (key, len(s["desc"]))
    assert len(s["title"]) <= 62, (key, len(s["title"]))
    wa = "https://wa.me/5997841782?text=" + quote(s["wa"])
    goal_href = f'contact.html?goal={s["goal"]}#quote' if s["goal"] else 'contact.html#quote'
    head, foot = shell["head"], shell["foot"]
    old = 'href="#quote">Free roof design'
    assert old in shell["sticky"]
    sticky = shell["sticky"].replace(old, f'href="{goal_href}">Free roof design')
    others = [k for k in ORDER if k != key]
    def thumb(k):
        o = SYSTEMS[k]
        return pic(o["photo"], o["photo_alt"])
    cards = "".join(
        f'<a class="other-card rv" href="{SYSTEMS[k]["slug"]}.html"><div class="other-img">{thumb(k)}</div><div class="other-body"><b>{E(SHORTNAME[k])}</b><span>{E(SYSTEMS[k]["card"])}</span><i>See the page</i></div></a>'
        for k in others)
    how = "".join(f'<div class="how-item"><h3>{E(t)}</h3><p>{E(p)}</p></div>' for t, p in s["how"])
    fit = "".join(f"<li>{E(x)}</li>" for x in s["fit"])
    facts = "".join(f"<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>" for a, b in s["facts"])
    bn = "".join(f'<div class="bn-item"><h3>{E(a)}</h3><p>{E(b)}</p></div>' for a, b in s["bn"])
    proc_titles = s.get("proc_titles") or ["Drone photo and design drawing", "Our own crew installs", "Monitoring before we leave"]
    proc = "".join(f'<div class="proc-item rv"><h3>{E(t)}</h3><p>{E(n)}</p></div>' for t, n in zip(proc_titles, s["proc_note"]))
    faq = "".join(f"<details><summary>{E(q)}<i></i></summary><p>{E(a)}</p></details>" for q, a in s["faq"])
    og_img = f'{SITE}/img/{s["photo"]}.jpg'
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{E(s["title"])}</title>
<meta name="description" content="{A(s["desc"])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Blue Sky Solar Bonaire">
<meta property="og:title" content="{A(s["title"])}">
<meta property="og:description" content="{A(s["desc"])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/BSS-Brandmark-FC.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=Figtree:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/site.css">
<link rel="stylesheet" href="css/system-page.css">
{jsonld(s, url)}
</head>
<body>

{head}
<main>
<div class="wrap crumbs"><nav aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="systems.html">Systems</a><span>/</span><span aria-current="page">{E(s["name"])}</span></nav></div>

<section class="page-hero">
  <div class="wrap">
    <h1>{E(s["h1"])} <span>{E(s["h1b"])}</span></h1>
    <div>
      <p>{E(s["lead"])}</p>
      <div class="hero-actions">
        <a class="btn btn-sky" href="{goal_href}">Get a free roof design {ARROW}</a>
        <a class="btn btn-ghost" href="{A(wa)}">WhatsApp us</a>
      </div>
    </div>
  </div>
  <div class="wrap">
    <figure class="wide-photo rv">{pic(s["photo"], s["photo_alt"], eager=True, w=2400, h=1600)}</figure>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>{E(s["how_h"])}</h2>
      <p>{E(s["how_intro"])}</p>
    </div>
    <div class="how-grid">
      <div>
        <div class="how-list">{how}</div>
        <div class="flow rv">{diagram(s["diagram"])}</div>
      </div>
      <figure class="side-photo rv">{pic(s["photo2"], s["photo2_alt"])}</figure>
    </div>
  </div>
</section>

<section class="sec fits">
  <div class="wrap fit-grid">
    <div>
      <h2>{E(s["fit_h"])}</h2>
      <ul class="fit-list">{fit}</ul>
    </div>
    <div class="fit-facts rv">
      <h3>The key facts</h3>
      <dl class="kf">{facts}</dl>
    </div>
  </div>
</section>

<section class="sec bonaire">
  <div class="wrap">
    <div class="sec-head">
      <h2>{E(s["bn_h"])}</h2>
      <p>{E(s["bn_p"])}</p>
    </div>
    <div class="bn-grid">{bn}</div>
    <div class="brands"><span>We install</span><strong>Victron Energy</strong><strong>EG4</strong><strong>BSL Batt</strong><strong>Jinko</strong><strong>Fronius</strong><strong>Sunpad</strong></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <h2>From roof photo to switch on.</h2>
      <p>You see the layout before you sign. You meet the people who build it.</p>
    </div>
    <div class="proc">{proc}</div>
  </div>
</section>

<section class="sec proof">
  <div class="wrap proof-grid">{proof_html(s)}</div>
</section>

<section class="sec" id="faq">
  <div class="wrap">
    <div class="faq">
      <h2>Questions about {E(FAQ_TOPIC[key])}.</h2>
      <div>{faq}</div>
    </div>
  </div>
</section>

<section class="sec others">
  <div class="wrap">
    <div class="sec-head">
      <h2>Other systems.</h2>
      <p>Not the right fit? Here are the other five. The crew that builds this one builds them all.</p>
    </div>
    <div class="other-grid">{cards}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="cta-band rv">
      <div><h2>{E(s["cta_h"])}</h2><p>{E(s["cta_p"])}</p></div>
      <div class="hero-actions">
        <a class="btn btn-sky" href="{goal_href}">Get a free roof design {ARROW}</a>
        <a class="btn btn-light" href="{A(wa)}">WhatsApp us</a>
      </div>
    </div>
  </div>
</section>
</main>

{foot}

{sticky}

<script src="js/site.js" defer></script>
</body>
</html>
'''

def main():
    idx = (ROOT / "index.html").read_text(encoding="utf-8")
    head = idx[idx.index('<header id="top">'):idx.index("<main>")].rstrip()
    foot = idx[idx.index("<footer>"):idx.index("</footer>") + len("</footer>")]
    sticky = re.search(r'<div class="sticky-cta">.*?</div>', idx).group(0)
    shell = dict(head=head, foot=foot, sticky=sticky)
    for k in ORDER:
        out = ROOT / (SYSTEMS[k]["slug"] + ".html")
        out.write_text(build(k, shell), encoding="utf-8")
        print("wrote", out.name)

if __name__ == "__main__":
    sys.exit(main())
