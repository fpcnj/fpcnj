#!/usr/bin/env python3
"""Emit static HTML pages for First Presbyterian Church Palisades Park."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://fpcpp.org"
DONATE = "https://www.zeffy.com/en-US/donation-form/offering-to-first-presbyterian-church"
CONTACT_EMAIL = "pastordavidpeng@gmail.com"
PHONE = "(201) 771-3379"
ADDRESS = "50 W Palisades Blvd, Palisades Park, NJ 07650"
CHURCH = "First Presbyterian Church Palisades Park"

NAV = [
    ("index.html", "Home"),
    ("about.html", "About"),
    ("services.html", "Services"),
    ("congregation.html", "Congregation"),
    ("programs.html", "Programs"),
    ("contact.html", "Contact"),
    ("donate.html", "Donate"),
]


def json_ld() -> str:
    return """{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Church",
      "@id": "https://fpcpp.org/#church",
      "name": "First Presbyterian Church Palisades Park",
      "alternateName": ["FPC Palisades Park", "First Presbyterian Church"],
      "url": "https://fpcpp.org/",
      "logo": "https://fpcpp.org/image/icon-512.png",
      "image": "https://fpcpp.org/image/hero-front.jpg",
      "email": "pastordavidpeng@gmail.com",
      "telephone": "+1-201-771-3379",
      "foundingDate": "1909",
      "address": {
        "@type": "PostalAddress",
        "streetAddress": "50 W Palisades Blvd",
        "addressLocality": "Palisades Park",
        "addressRegion": "NJ",
        "postalCode": "07650",
        "addressCountry": "US"
      }
    },
    {
      "@type": "WebSite",
      "@id": "https://fpcpp.org/#website",
      "url": "https://fpcpp.org/",
      "name": "First Presbyterian Church Palisades Park",
      "description": "A multilingual Presbyterian congregation in Palisades Park, New Jersey, worshiping since 1909.",
      "publisher": { "@id": "https://fpcpp.org/#church" }
    }
  ]
}"""


def head(title: str, description: str, path: str, image: str, current: str) -> str:
    url = f"{ORIGIN}/{path}" if path else f"{ORIGIN}/"
    og_image = f"{ORIGIN}/image/{image}"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="canonical" href="{url}">
  <link rel="alternate" type="text/plain" href="{ORIGIN}/llms.txt" title="LLM site summary">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta name="theme-color" content="#1a2744">
  <meta name="color-scheme" content="light">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{CHURCH}">
  <meta property="og:locale" content="en_US">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_image}">
  <meta property="og:image:alt" content="{CHURCH}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{og_image}">
  <link rel="icon" href="favicon.ico">
  <link rel="icon" href="image/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="image/favicon-32.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="image/apple-touch-icon.png">
  <link rel="manifest" href="site.webmanifest">
  <link rel="stylesheet" href="css/site.css">
  <script type="application/ld+json">
{json_ld()}
  </script>
</head>
<body data-page="{current}">
  <a class="skip" href="#main">Skip to content</a>
"""


def nav(current_file: str) -> str:
    links = []
    for href, title in NAV:
        current = ' is-current" aria-current="page"' if href == current_file else '"'
        links.append(f'        <a class="nav-link{current} href="{href}">{title}</a>')
    return f"""  <header class="site-header">
    <div class="wrap header-bar">
      <a class="brand" href="index.html">
        <img class="brand-mark" src="image/favicon.svg" width="40" height="40" alt="">
        <span class="brand-text">
          <span class="brand-kicker">Established 1909</span>
          <span class="brand-name">First Presbyterian Church</span>
        </span>
      </a>
      <button class="nav-toggle" type="button" data-nav-toggle aria-expanded="false" aria-controls="site-nav">Menu</button>
      <nav id="site-nav" class="site-nav" data-site-nav data-current="{current_id(current_file)}" aria-label="Primary">
{chr(10).join(links)}
      </nav>
    </div>
  </header>
"""


def current_id(filename: str) -> str:
    return {
        "index.html": "home",
        "about.html": "about",
        "services.html": "services",
        "congregation.html": "congregation",
        "programs.html": "programs",
        "contact.html": "contact",
        "donate.html": "donate",
    }[filename]


def footer() -> str:
    return f"""  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <h2>First Presbyterian Church</h2>
        <p>Palisades Park, New Jersey</p>
        <p>{ADDRESS}</p>
        <p><a href="tel:+12017713379">{PHONE}</a></p>
        <p>Office: <a href="mailto:fpcmaster1@gmail.com">fpcmaster1@gmail.com</a></p>
        <p>Pastor: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
      </div>
      <div>
        <h3>Visit</h3>
        <ul class="list-plain">
          <li><a href="about.html">About</a></li>
          <li><a href="services.html">Services</a></li>
          <li><a href="congregation.html">Congregation</a></li>
          <li><a href="programs.html">Programs</a></li>
          <li><a href="contact.html">Contact</a></li>
          <li><a href="donate.html">Donate</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap copyright">
      <p>© 1896–2026 First Presbyterian Church Palisades Park. Content and identity reference <a href="https://fpcpp.org">fpcpp.org</a>.</p>
      <p>Worship in English, Mandarin, Korean, and Spanish. All are welcome.</p>
    </div>
  </footer>
  <script src="js/site.js"></script>
</body>
</html>
"""


HOME = """  <main id="main">
    <section class="hero">
      <div class="photo-frame hero-frame">
        <img src="image/hero-front.jpg" width="1400" height="875" alt="First Presbyterian Church Palisades Park in spring, with cherry blossoms and a cross on the roof" fetchpriority="high">
      </div>
      <div class="wrap hero-copy">
        <p class="kicker">Established 1909 · Palisades Park, NJ</p>
        <h1>A house of prayer for every language in town</h1>
        <p class="lede">First Presbyterian Church Palisades Park has worshiped, served, and gathered neighbors here for more than a century. English, Mandarin, Korean, and Spanish congregations share one sanctuary at 50 W Palisades Blvd.</p>
        <div class="actions">
          <a class="btn btn-gold" href="services.html">Sunday services</a>
          <a class="btn btn-ghost" href="https://www.zeffy.com/en-US/donation-form/offering-to-first-presbyterian-church" data-donate-link target="_blank" rel="noopener noreferrer">Donate</a>
          <a class="btn btn-ghost" href="contact.html">Contact</a>
        </div>
      </div>
    </section>
    <section class="section section-cream">
      <div class="wrap">
        <p class="verse">“I was glad when they said to me, ‘Let us go to the house of the Lord!’” — Psalm 122:1</p>
        <p class="muted">A word the church still keeps on the door: this house is open daily for prayer and meditation.</p>
      </div>
    </section>
    <section class="section">
      <div class="wrap grid grid-2">
        <article class="card">
          <img src="image/campus-front.jpg" width="1200" height="750" alt="White clapboard sanctuary, bell tower, and church sign on Palisades Boulevard" loading="lazy">
          <div class="card-body">
            <h2>Since 1909</h2>
            <p>Founded as Union Chapel in 1897 and chartered as First Presbyterian Church in 1909, this congregation has been a beacon in Palisades Park through the Edsall family’s gifts, the Depression, war years, and a multi-ethnic revival since the 1980s.</p>
            <p><a href="about.html">Read our history</a></p>
          </div>
        </article>
        <article class="card">
          <img src="image/worship.jpg" width="1200" height="750" alt="Congregation standing in the sanctuary during worship, flags of many nations overhead" loading="lazy">
          <div class="card-body">
            <h2>Four languages, one church</h2>
            <p>Sunday worship is offered in Mandarin, English, Korean, and Spanish. The doors stay open to the community. People of every language are welcome to share the gospel and the love of God.</p>
            <p><a href="congregation.html">Meet the congregation</a></p>
          </div>
        </article>
      </div>
    </section>
    <section class="section section-cream">
      <div class="wrap">
        <h2>Look to Jesus and lead people to the Lord</h2>
        <p>Our mission is to proclaim the love of Jesus Christ in Palisades Park and beyond — a refuge of joy, peace, love, and spiritual healing, and a household where gifts are used for ministry.</p>
        <div class="grid grid-3" style="margin-top:20px">
          <article class="card">
            <img src="image/kids.jpg" width="800" height="500" alt="Children gathered for a church program" loading="lazy">
            <div class="card-body">
              <h3>TCCC &amp; VBS</h3>
              <p>Touch Community Christian Center and Vacation Bible School have served more than 200 families with after-school care, music, language, arts, and faith.</p>
            </div>
          </article>
          <article class="card">
            <img src="image/fair.jpg" width="800" height="500" alt="Outdoor church fair tents on the grounds" loading="lazy">
            <div class="card-body">
              <h3>Twelve programs</h3>
              <p>The church co-hosts community service, missions, AWANA, prayer, and partner congregations under one roof.</p>
            </div>
          </article>
          <article class="card">
            <img src="image/fellowship.jpg" width="800" height="500" alt="Fellowship hall with tables, bookshelves, and a cross" loading="lazy">
            <div class="card-body">
              <h3>Pastor David Peng</h3>
              <p>Rev. David Peng, the thirteenth pastor, was called in 2000 and ordained and installed on May 2, 2004. He still shepherds this multilingual house of prayer.</p>
            </div>
          </article>
        </div>
        <div class="actions">
          <a class="btn btn-navy" href="programs.html">See programs</a>
          <a class="btn btn-gold" href="{DONATE}" data-donate-link target="_blank" rel="noopener noreferrer">Give today</a>
        </div>
      </div>
    </section>
  </main>
""".replace("{DONATE}", DONATE)

ABOUT = """  <main id="main">
    <section class="section">
      <div class="wrap split">
        <div>
          <p class="kicker">About</p>
          <h1>History of First Presbyterian Church</h1>
          <p>First Presbyterian Church Palisades Park and Touch Community Christian Center. Centennial brief historical timeline, 1909 to now. Address: 50 West Palisades Blvd., Palisades Park, NJ 07650.</p>
          <p class="muted">Drawn from the church history compiled with Pastor David Peng (June 26, 2025) and the public identity at fpcpp.org.</p>
        </div>
        <div class="photo-frame">
          <img src="image/historic.jpg" width="1200" height="900" alt="Historic photograph of the Palisades Park Presbyterian sanctuary and bell tower" fetchpriority="high">
        </div>
      </div>
    </section>
    <section class="section section-cream">
      <div class="wrap timeline">
        <h2>1896–1909: Origin</h2>
        <p>On December 14, 1896, residents of Palisades Park gathered at the home of the town’s first mayor, John S. Edsall, to establish the Union Association and found Union Chapel, with 43 initial members. John and Henry Brinkerhoff donated land at 219 Grand Avenue. The Women’s Aid Society, founded January 5, 1897 by Mrs. Paul Gantert with Mrs. John Edsall as president, raised funds for construction. The contract was signed October 21, 1897 for $1,620. Groundbreaking was November 28; the chapel was dedicated March 6, 1898.</p>
        <h2>1909–1934: Church founded</h2>
        <p>Between February and April 1909 the congregation voted to join the Presbyterian denomination and became First Presbyterian Church. From 1911 to 1912 the Women’s Aid Society raised $1,600 for a lot at Palisades Boulevard and Hillside Avenue. Samuel S. Edsall’s 1911 will began “In the name of God, Amen,” and gave $2,000 to the church and $2,000 to the borough for the poor. The new church was dedicated March 19, 1916. A manse followed in 1921–22. Membership reached 282 at its 1930 peak.</p>
        <h2>1935–1959: Challenges and expansion</h2>
        <p>Under Rev. Janvier J. Louderbough the roof was repaired and the Edsall family gave a Meneely commemorative bell tower in memory of Samuel, Isabella Christie, John S., and Samuel S. Edsall. Mrs. A.W. Knapp funded the first organ in 1942. Elder Frank Wheeler, ordained in 1909, kept the books and Sunday School for about forty years. Architect Carl Mattberg volunteered the 1957 expansion design. A $25,000 loan in 1958 finished classrooms, the pastor’s study, and fellowship hall for the 50th anniversary in 1959. The fireplace became the “Altar of Beautiful Ashes”; Brinkerhoff chairs remain in the sanctuary.</p>
        <h2>1960–1985: Renewal</h2>
        <p>After lean years, 23 Taiwanese members joined in 1983. On May 25 the first bilingual worship was held. Pastor Chu-Yih Huang, led to the unused Presbyterian building on a weekday walk, was welcomed by Elder Mike Kelly. Rev. William A. Carhart (1983–1986) stabilized the church and raised $9,000 for a second organ in 1984.</p>
        <h2>1986–now: Multilingual worship</h2>
        <p>A mission study (1999–2001) launched English worship in 2001, then Mandarin, Korean, and Spanish services. In 2005 the church founded Touch Community Christian Center (TCCC). By 2008 TCCC had served over 200 families; VBS had grown from one week of morning sessions to six full weeks; an annual charity concert began on the first Saturday of December; and short-term mission teams went yearly to sister churches in Taiwan. Ten percent of tithes go to outside missions.</p>
        <div class="photo-frame" style="margin-top:24px">
          <img src="image/campus-side.jpg" width="1400" height="900" alt="Side view of the church campus along Palisades Boulevard" loading="lazy">
        </div>
      </div>
    </section>
    <section class="section">
      <div class="wrap split">
        <div>
          <h2>The dream</h2>
          <p>Our church has a dream. With the gifts of multiple languages God gives us, we will spearhead a community church by reaching out to the un-churched in and beyond the community and build up a core of committed disciples of Jesus Christ.</p>
          <p>We infuse evangelical zeal and rely on the Holy Spirit so people can grow into spiritual maturity and use the gifts God gave them. With the Spirit’s empowering, Christians can work as one team, one family, and one body of Christ for the glorification of God.</p>
          <p>It is our mission to offer this church as a refuge where people find joy, peace, love, and spiritual healing through prayer and meditation — and to proclaim the love of Jesus Christ by bringing the gospel and serving spiritual and social needs.</p>
        </div>
        <div class="photo-frame">
          <img src="image/prayer-sign.jpg" width="1000" height="700" alt="Painted sign: This church open daily for prayer and meditation" loading="lazy">
        </div>
      </div>
    </section>
  </main>
"""

SERVICES = """  <main id="main">
    <section class="section">
      <div class="wrap split">
        <div>
          <p class="kicker">Services</p>
          <h1>Worship in four languages</h1>
          <p>Sunday worship at First Presbyterian Church Palisades Park is offered in Mandarin, English, Korean, and Spanish. The sanctuary on 50 W Palisades Blvd is a shared house of prayer. All are welcome.</p>
          <p>Flags of the nations hang over the pews. The church keeps a simple invitation on a worn plaque: this church is open daily for prayer and meditation.</p>
        </div>
        <div class="photo-frame">
          <img src="image/sanctuary.jpg" width="1400" height="875" alt="Sanctuary pews facing the cross, lanterns, and screens during an evening gathering" fetchpriority="high">
        </div>
      </div>
    </section>
    <section class="section section-cream">
      <div class="wrap">
        <h2>Sunday schedule</h2>
        <p class="muted">Times follow the multilingual worship pattern the church has kept since 2004. Clergy for each language hour are announced in the bulletin; this page does not invent names.</p>
        <div class="schedule" style="margin-top:16px">
          <article>
            <h3>Mandarin worship</h3>
            <p>Sunday 10:00 a.m. – 12:00 p.m.</p>
          </article>
          <article>
            <h3>English worship</h3>
            <p>Sunday 12:00 p.m. – 2:00 p.m.</p>
          </article>
          <article>
            <h3>Korean worship</h3>
            <p>Sunday 2:00 p.m. – 4:00 p.m.</p>
          </article>
          <article>
            <h3>Spanish worship</h3>
            <p>Sunday 4:00 p.m. – 6:00 p.m.</p>
          </article>
        </div>
        <div class="pill-row" aria-label="Worship languages">
          <span class="pill">Mandarin</span>
          <span class="pill">English</span>
          <span class="pill">Korean</span>
          <span class="pill">Spanish</span>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="wrap split">
        <div class="photo-frame">
          <img src="image/worship.jpg" width="1400" height="875" alt="Standing congregation and piano during a multilingual service" loading="lazy">
        </div>
        <div>
          <h2>How we gather</h2>
          <p>English worship was established in May 2001 for the second generation and the wider town. Mandarin worship grew from the earlier Taiwanese-Mandarin bilingual service. Korean worship began in July 2003 when Crystal Presbyterian Church was welcomed. A Hispanic congregation was received in 2004.</p>
          <p>Come as you are. Parking and the front stair meet Palisades Boulevard. If you are visiting, <a href="contact.html">write us</a> and we will help you find the hour that fits your language.</p>
          <div class="actions">
            <a class="btn btn-navy" href="contact.html">Plan a visit</a>
            <a class="btn btn-gold" href="donate.html" data-donate-link>Support worship</a>
          </div>
        </div>
      </div>
    </section>
  </main>
"""

CONGREGATION = """  <main id="main">
    <section class="section">
      <div class="wrap split">
        <div>
          <p class="kicker">Congregation</p>
          <h1>One body, many languages</h1>
          <p>This congregation has belonged to Palisades Park since Union Chapel. It peaked at 282 members in 1930, walked through lean decades, and opened again in the 1980s as a multi-ethnic house of prayer. We are growing again today.</p>
          <p>Rev. David Peng is the thirteenth pastor. Called as an inquirer on October 1, 2000 from a United Methodist background, he was ordained and installed on May 2, 2004. Under his leadership the church kept four Sunday services and founded ministries that still mark the town.</p>
        </div>
        <div class="photo-frame">
          <img src="image/congregation.jpg" width="1400" height="875" alt="The congregation filling the sanctuary under international flags" fetchpriority="high">
        </div>
      </div>
    </section>
    <section class="section section-cream">
      <div class="wrap">
        <h2>How the family gathered</h2>
        <ul class="list-plain">
          <li><strong>1982–1983.</strong> Pastor Chu-Yih Huang found the unused Presbyterian building on a Spirit-led walk. Elder Mike Kelly opened the door. In March 1983, 23 members of the former Formosan Presbyterian Church joined. Bilingual worship began May 25, 1983 under Rev. William A. Carhart.</li>
          <li><strong>1987–1988.</strong> Pastor Gretchen Janssen, the only woman to serve as presiding pastor in the church’s first century, completed a mission study so the congregation would reflect the town’s ethnic picture and could call a bilingual pastor.</li>
          <li><strong>1989–1999.</strong> Rev. Jack Chiang of Canada served as the twelfth pastor, renovating the building and leading youth.</li>
          <li><strong>2000–now.</strong> Rev. David Peng. English worship (2001); Mandarin worship; Korean worship with Crystal Presbyterian Church and Rev. Victor Moon (2003); Hispanic congregation under Pastor Teresa Delgato (2004).</li>
        </ul>
        <p>Between 2000 and 2008 average attendance grew from 54 to 109, and children’s ministry from 2 to 28. The budget grew with the work. Ten percent of tithes go outward.</p>
      </div>
    </section>
    <section class="section">
      <div class="wrap grid grid-2">
        <div class="photo-frame">
          <img src="image/campus-back.jpg" width="1200" height="800" alt="Rear view of the church buildings and grounds" loading="lazy">
        </div>
        <div class="photo-frame">
          <img src="image/bulletin.jpg" width="1200" height="800" alt="Church bulletin and worship notes" loading="lazy">
        </div>
      </div>
      <div class="wrap" style="margin-top:24px">
        <h2>Pastors of this pulpit</h2>
        <p>The church remembers a line of shepherds, including Rev. George Brinton Hassey (1954–1959), Rev. John Edward Bauer (1961–1980), Rev. William A. Carhart (1983–1986), Pastor Gretchen Janssen (1987–1988), Rev. Jack Chiang (1989–1999), and Rev. David Peng (2000–now). Earlier years include Rev. Janvier J. Louderbough, who led the wartime roof repair and received the Edsall bell.</p>
        <p><a href="about.html">Read the full timeline</a> · <a href="contact.html">Write Pastor David Peng</a></p>
      </div>
    </section>
  </main>
"""

PROGRAMS = """  <main id="main">
    <section class="section">
      <div class="wrap split">
        <div>
          <p class="kicker">Programs</p>
          <h1>Ministry that stays in the neighborhood</h1>
          <p>First Presbyterian Church Palisades Park co-hosts worship and community programs under one roof. fpcpp.org names twelve co-hosted programs, short-term missions, VBS, and charity concerts among the fruit of this house.</p>
          <p>Ten percent of every gift goes directly to outside missions and community care.</p>
        </div>
        <div class="photo-frame">
          <img src="image/tent.jpg" width="1400" height="875" alt="White event tent on the church grounds" fetchpriority="high">
        </div>
      </div>
    </section>
    <section class="section section-cream">
      <div class="wrap grid grid-2">
        <article class="card">
          <img src="image/kids.jpg" width="1000" height="625" alt="Children in a church program" loading="lazy">
          <div class="card-body">
            <h2>Touch Community Christian Center</h2>
            <p>TCCC was established in September 2005 as a subdivision of the church. It offers after-school academic enrichment — music, Chinese, English, math, arts and crafts, and exploration of Christian faith — because many parents work late. By 2008 it had reached more than 200 families. Frank Huang served as the first TCCC director; Eric Wu served as youth director.</p>
          </div>
        </article>
        <article class="card">
          <img src="image/facepainting.jpg" width="1000" height="625" alt="Child receiving face painting at a church gathering" loading="lazy">
          <div class="card-body">
            <h2>Vacation Bible School</h2>
            <p>VBS — fondly called Very Best Summer — began in 2001 as one week of three-hour mornings. It grew into morning-and-afternoon days and then a six-week program inside the TCCC framework, a joyful open door for the children of Palisades Park.</p>
          </div>
        </article>
        <article class="card">
          <img src="image/fair.jpg" width="1000" height="625" alt="Community fair on the church lawn" loading="lazy">
          <div class="card-body">
            <h2>Missions and the charity concert</h2>
            <p>From 2006 the church has sent a short-term mission team each year to sister churches in Taiwan, including Taipei Cheh-Feng Street Church, Longtan Presbyterian Church, and Tailan Liberty Church. Since 2003, a charity concert on the first Saturday of December raises gifts for the homeless, missionaries, and evangelistic work.</p>
          </div>
        </article>
        <article class="card">
          <img src="image/fellowship.jpg" width="1000" height="625" alt="Fellowship room used for classes and meetings" loading="lazy">
          <div class="card-body">
            <h2>Co-hosted programs</h2>
            <p>Alongside FPC worship, the building has hosted partner works named in the church’s own program list: CPC, Mission Church, Love Church, LJPC, New Jerusalem, New Wine Church, go4Jesus, InterCP, CJK FAN, Rising Well Ministry, AWANA, and harmonica class.</p>
          </div>
        </article>
      </div>
    </section>
    <section class="section">
      <div class="wrap">
        <h2>A campus still serving</h2>
        <p>117 years of worship, fellowship, and community service continue from this corner of Palisades Boulevard. If you want to volunteer, enroll a child, or bring a partner ministry, <a href="contact.html">contact the church</a>.</p>
        <div class="actions">
          <a class="btn btn-navy" href="contact.html">Talk with us</a>
          <a class="btn btn-gold" href="{DONATE}" data-donate-link target="_blank" rel="noopener noreferrer">Fund the work</a>
        </div>
      </div>
    </section>
  </main>
""".replace("{DONATE}", DONATE)

CONTACT = f"""  <main id="main">
    <section class="section">
      <div class="wrap split">
        <div>
          <p class="kicker">Contact</p>
          <h1>Write the church</h1>
          <p>Ask us anything, plan a visit, or send a word to Pastor David Peng. Submitting this form sends email to <strong>{CONTACT_EMAIL}</strong>.</p>
          <form class="form" data-contact-form novalidate>
            <label>Name
              <input type="text" name="name" autocomplete="name" required>
            </label>
            <label>Email
              <input type="email" name="email" autocomplete="email" required>
            </label>
            <label>Phone <span class="muted">(optional)</span>
              <input type="tel" name="phone" autocomplete="tel">
            </label>
            <label>Message
              <textarea name="message" required></textarea>
            </label>
            <div class="hp" aria-hidden="true">
              <label>Website <input type="text" name="website" tabindex="-1" autocomplete="off"></label>
            </div>
            <button class="btn btn-navy" type="submit">Send message</button>
            <p class="form-status" data-contact-status role="status"></p>
          </form>
        </div>
        <aside class="contact-aside">
          <h2>Find us</h2>
          <p>{ADDRESS}</p>
          <p>Call <a href="tel:+12017713379">{PHONE}</a></p>
          <p>Church office: <a href="mailto:fpcmaster1@gmail.com">fpcmaster1@gmail.com</a></p>
          <p>Pastor: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>
          <div class="photo-frame" style="margin:16px 0">
            <img src="image/campus-front.jpg" width="1000" height="625" alt="Church exterior and sign on Palisades Boulevard" loading="lazy">
          </div>
          <p>Checks may be mailed payable to FPC at the church address. Online giving is on the <a href="donate.html">Donate</a> page.</p>
        </aside>
      </div>
    </section>
  </main>
"""

DONATE_PAGE = f"""  <main id="main">
    <section class="section">
      <div class="wrap split">
        <div>
          <p class="kicker">Donate</p>
          <h1>Offering to First Presbyterian Church</h1>
          <p>Every gift — large or small — helps fund daily operations, community programs, and the care of this 117-year house of prayer. Tax-deductible gifts support FPC ministries and the campus renewal described at fpcpp.org.</p>
          <p>Ten percent of every gift goes directly to outside missions and community care.</p>
          <div class="actions">
            <a class="btn btn-gold" href="{DONATE}" data-donate-link target="_blank" rel="noopener noreferrer">Give securely on Zeffy</a>
            <a class="btn btn-navy" href="contact.html">Ask about giving</a>
          </div>
        </div>
        <div class="photo-frame">
          <img src="image/campus-front.jpg" width="1400" height="875" alt="First Presbyterian Church Palisades Park campus" fetchpriority="high">
        </div>
      </div>
    </section>
    <section class="section section-cream">
      <div class="wrap">
        <h2>Three ways to give</h2>
        <div class="grid grid-3" style="margin-top:16px">
          <article class="card">
            <div class="card-body">
              <h3>1. Zeffy</h3>
              <p>Give online through the church’s offering form. 100% of the gift supports FPC ministries and renovation.</p>
              <p><a href="{DONATE}" data-donate-link target="_blank" rel="noopener noreferrer">Open the Zeffy offering form</a></p>
            </div>
          </article>
          <article class="card">
            <div class="card-body">
              <h3>2. Check</h3>
              <p>Please write payable checks to FPC. Mail to:</p>
              <p>50 W Palisades Blvd., Palisades Park, NJ 07650</p>
            </div>
          </article>
          <article class="card">
            <div class="card-body">
              <h3>3. Offering box</h3>
              <p>Place cash or check in the offering box at the church entrance when you come to worship or prayer.</p>
            </div>
          </article>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="wrap split">
        <div class="photo-frame">
          <img src="image/historic.jpg" width="1200" height="900" alt="Historic church building, the campus we still keep" loading="lazy">
        </div>
        <div>
          <h2>Renewing a sacred home</h2>
          <p>From the Edsall sanctuary and bell tower through a beautiful multi-ethnic revival, this campus has carried worship for generations. The public renovation appeal at fpcpp.org names urgent care for sanctuary, parsonage, grounds, and aging systems so the church can keep serving Palisades Park.</p>
          <p>Weekly worship in four languages, twelve programs, VBS, short-term missions to Taiwan, and charity concerts all depend on this house remaining open.</p>
        </div>
      </div>
    </section>
  </main>
"""

PAGES = [
    {
        "file": "index.html",
        "title": "First Presbyterian Church Palisades Park",
        "description": "First Presbyterian Church Palisades Park — a multilingual Presbyterian congregation at 50 W Palisades Blvd, Palisades Park, NJ. Worship in English, Mandarin, Korean, and Spanish since 1909.",
        "path": "",
        "image": "hero-front.jpg",
        "body": HOME,
    },
    {
        "file": "about.html",
        "title": "About · First Presbyterian Church Palisades Park",
        "description": "History and mission of First Presbyterian Church Palisades Park and Touch Community Christian Center, from Union Chapel (1897) and the 1909 charter to today’s multilingual congregation.",
        "path": "about.html",
        "image": "historic.jpg",
        "body": ABOUT,
    },
    {
        "file": "services.html",
        "title": "Services · First Presbyterian Church Palisades Park",
        "description": "Sunday worship times in Mandarin, English, Korean, and Spanish at First Presbyterian Church, 50 W Palisades Blvd, Palisades Park, NJ 07650.",
        "path": "services.html",
        "image": "sanctuary.jpg",
        "body": SERVICES,
    },
    {
        "file": "congregation.html",
        "title": "Congregation · First Presbyterian Church Palisades Park",
        "description": "Meet the multilingual congregation of First Presbyterian Church Palisades Park and Pastor David Peng, thirteenth pastor since 2000.",
        "path": "congregation.html",
        "image": "congregation.jpg",
        "body": CONGREGATION,
    },
    {
        "file": "programs.html",
        "title": "Programs · First Presbyterian Church Palisades Park",
        "description": "TCCC, Vacation Bible School, short-term missions to Taiwan, charity concerts, and twelve co-hosted community programs at First Presbyterian Church Palisades Park.",
        "path": "programs.html",
        "image": "kids.jpg",
        "body": PROGRAMS,
    },
    {
        "file": "contact.html",
        "title": "Contact · First Presbyterian Church Palisades Park",
        "description": "Contact First Presbyterian Church Palisades Park and Pastor David Peng at 50 W Palisades Blvd, Palisades Park, NJ 07650. Phone (201) 771-3379.",
        "path": "contact.html",
        "image": "campus-front.jpg",
        "body": CONTACT,
    },
    {
        "file": "donate.html",
        "title": "Donate · First Presbyterian Church Palisades Park",
        "description": "Give an offering to First Presbyterian Church Palisades Park through Zeffy, mailed check, or the sanctuary offering box.",
        "path": "donate.html",
        "image": "campus-front.jpg",
        "body": DONATE_PAGE,
    },
]


def main() -> None:
    for page in PAGES:
        html = (
            head(page["title"], page["description"], page["path"], page["image"], current_id(page["file"]))
            + nav(page["file"])
            + page["body"]
            + footer()
        )
        dest = ROOT / page["file"]
        dest.write_text(html, encoding="utf-8")
        print(f"wrote {dest.name} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
