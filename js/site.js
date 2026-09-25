(function (root) {
  "use strict";

  var CONTACT_EMAIL = "pastordavidpeng@gmail.com";
  var DONATE_URL =
    "https://www.zeffy.com/en-US/donation-form/offering-to-first-presbyterian-church";
  var MAIL_ENDPOINT = "https://formsubmit.co/ajax/" + CONTACT_EMAIL;

  function ChurchSite(options) {
    options = options || {};
    this.name = options.name || "First Presbyterian Church Palisades Park";
    this.shortName = options.shortName || "FPC Palisades Park";
    this.address =
      options.address || "50 W Palisades Blvd, Palisades Park, NJ 07650";
    this.phone = options.phone || "(201) 696-1813";
    this.contactEmail = options.contactEmail || CONTACT_EMAIL;
    this.donateUrl = options.donateUrl || DONATE_URL;
    this.mailEndpoint = options.mailEndpoint || MAIL_ENDPOINT;
    this.origin = options.origin || "https://fpcpp.org";
    this.pages = (options.pages || ChurchSite.pageCatalog()).slice();
  }

  ChurchSite.pageCatalog = function () {
    return [
      { id: "home", title: "Home", href: "index.html" },
      { id: "about", title: "About", href: "about.html" },
      { id: "services", title: "Services", href: "services.html" },
      { id: "congregation", title: "Congregation", href: "congregation.html" },
      { id: "programs", title: "Programs", href: "programs.html" },
      { id: "contact", title: "Contact", href: "contact.html" },
      { id: "donate", title: "Donate", href: "donate.html" }
    ];
  };

  ChurchSite.defaults = function () {
    return new ChurchSite();
  };

  ChurchSite.prototype.pageById = function (id) {
    var i;
    for (i = 0; i < this.pages.length; i += 1) {
      if (this.pages[i].id === id) return this.pages[i];
    }
    return null;
  };

  function Navigation(site) {
    this.site = site || ChurchSite.defaults();
  }

  Navigation.prototype.pageTitles = function () {
    return this.site.pages.map(function (page) {
      return page.title;
    });
  };

  Navigation.prototype.namedPages = function () {
    return this.site.pages.filter(function (page) {
      return page.id !== "home";
    });
  };

  Navigation.prototype.currentFromPath = function (path) {
    var file = String(path || "").split("/").pop() || "index.html";
    if (!file || file === "") file = "index.html";
    var i;
    for (i = 0; i < this.site.pages.length; i += 1) {
      if (this.site.pages[i].href === file) return this.site.pages[i].id;
    }
    return "home";
  };

  Navigation.prototype.compose = function (currentId) {
    var items = [];
    var i;
    var page;
    var current;
    for (i = 0; i < this.site.pages.length; i += 1) {
      page = this.site.pages[i];
      current = page.id === currentId ? " is-current" : "";
      items.push(
        '<a class="nav-link' +
          current +
          '" href="' +
          page.href +
          '">' +
          page.title +
          "</a>"
      );
    }
    return items.join("");
  };

  Navigation.prototype.hydrate = function (doc) {
    var nav = doc.querySelector("[data-site-nav]");
    if (!nav) return;
    var path = (doc.location && doc.location.pathname) || "";
    var currentId =
      (nav.getAttribute("data-current") || this.currentFromPath(path));
    if (!nav.querySelector("a.nav-link")) {
      nav.innerHTML = this.compose(currentId);
    }
    var links = nav.querySelectorAll("a[href]");
    var i;
    var href;
    for (i = 0; i < links.length; i += 1) {
      href = links[i].getAttribute("href") || "";
      if (href.split("/").pop() === (this.site.pageById(currentId) || {}).href) {
        links[i].className +=
          links[i].className.indexOf("is-current") === -1 ? " is-current" : "";
        links[i].setAttribute("aria-current", "page");
      }
    }
  };

  Navigation.prototype.bindToggle = function (doc) {
    var btn = doc.querySelector("[data-nav-toggle]");
    var nav = doc.querySelector("[data-site-nav]");
    if (!btn || !nav) return;
    btn.addEventListener("click", function () {
      var open = nav.className.indexOf("is-open") !== -1;
      if (open) {
        nav.className = nav.className.replace(/\bis-open\b/g, "").replace(/\s+/g, " ").trim();
        btn.setAttribute("aria-expanded", "false");
      } else {
        nav.className = (nav.className + " is-open").trim();
        btn.setAttribute("aria-expanded", "true");
      }
    });
  };

  function defaultTransport(request) {
    return fetch(request.url, {
      method: request.method,
      headers: request.headers,
      body: JSON.stringify(request.body)
    }).then(function (res) {
      if (!res.ok) {
        throw new Error("Contact send failed");
      }
      return res.json().catch(function () {
        return { ok: true };
      });
    });
  }

  function ContactSender(site, transport) {
    this.site = site || ChurchSite.defaults();
    this.transport = transport || defaultTransport;
  }

  ContactSender.prototype.buildRequest = function (fields) {
    fields = fields || {};
    var name = String(fields.name || "").trim();
    var email = String(fields.email || "").trim();
    var message = String(fields.message || "").trim();
    var phone = String(fields.phone || "").trim();
    if (!name || !email || !message) {
      throw new Error("Name, email, and message are required.");
    }
    return {
      url: this.site.mailEndpoint,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json"
      },
      body: {
        _subject: "First Presbyterian Church Palisades Park — website contact",
        _template: "table",
        _captcha: "false",
        to: this.site.contactEmail,
        name: name,
        email: email,
        phone: phone,
        message: message
      }
    };
  };

  ContactSender.prototype.send = function (fields) {
    var request = this.buildRequest(fields);
    return this.transport(request);
  };

  function SiteApp(site) {
    this.site = site || ChurchSite.defaults();
    this.nav = new Navigation(this.site);
    this.contact = new ContactSender(this.site);
  }

  SiteApp.prototype.bindDonate = function (doc) {
    var links = doc.querySelectorAll("[data-donate-link]");
    var i;
    for (i = 0; i < links.length; i += 1) {
      links[i].setAttribute("href", this.site.donateUrl);
      if (links[i].tagName === "A") {
        links[i].setAttribute("target", "_blank");
        links[i].setAttribute("rel", "noopener noreferrer");
      }
    }
  };

  SiteApp.prototype.bindContact = function (doc) {
    var form = doc.querySelector("[data-contact-form]");
    if (!form) return;
    var status = doc.querySelector("[data-contact-status]");
    var sender = this.contact;
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var honey = form.querySelector("[name='website']");
      if (honey && honey.value) return;
      var payload = {
        name: (form.querySelector("[name='name']") || {}).value,
        email: (form.querySelector("[name='email']") || {}).value,
        phone: (form.querySelector("[name='phone']") || {}).value,
        message: (form.querySelector("[name='message']") || {}).value
      };
      if (status) {
        status.textContent = "Sending…";
        status.className = "form-status is-pending";
      }
      try {
        sender
          .send(payload)
          .then(function () {
            form.reset();
            if (status) {
              status.textContent =
                "Thank you. Your message is on its way to the pastor.";
              status.className = "form-status is-ok";
            }
          })
          .catch(function () {
            if (status) {
              status.textContent =
                "The message could not be sent. Please call the church at (201) 696-1813.";
              status.className = "form-status is-err";
            }
          });
      } catch (err) {
        if (status) {
          status.textContent =
            "Please fill in your name, email, and message before sending.";
          status.className = "form-status is-err";
        }
      }
    });
  };

  SiteApp.prototype.bindVideoNotice = function (doc) {
    doc = doc || root.document;
    if (!doc || typeof doc.querySelector !== "function") return this;
    var loc = (typeof location !== "undefined") ? location : (root.location || null);
    if (!loc || loc.protocol !== "file:") return this;
    var frame = doc.querySelector('.video-frame iframe[src*="youtube.com/embed/"]');
    if (!frame || typeof frame.closest !== "function") return this;
    var stage = frame.closest(".video-stage");
    var wrap = stage ? stage.querySelector(".wrap") : null;
    if (!wrap) return this;
    var src = frame.getAttribute("src") || "";
    var id = src.split("/embed/")[1] || "";
    id = id.split("?")[0].split("&")[0];
    var note = doc.createElement("p");
    note.className = "video-note";
    var link = id ? ' You can also <a href="https://youtu.be/' + id + '" target="_blank" rel="noopener">watch on YouTube</a> directly.' : "";
    note.innerHTML = "Heads up: this page was opened as a local file, so YouTube blocks the embedded player (Error 153). Serve the site over http(s) — e.g. run <code>python3 -m http.server</code> in the site folder — or open the live site." + link;
    wrap.appendChild(note);
    return this;
  };

  SiteApp.prototype.mount = function (doc) {
    doc = doc || root.document;
    if (!doc) return this;
    this.nav.hydrate(doc);
    this.nav.bindToggle(doc);
    this.bindDonate(doc);
    this.bindContact(doc);
    this.bindVideoNotice(doc);
    return this;
  };

  var api = {
    CONTACT_EMAIL: CONTACT_EMAIL,
    DONATE_URL: DONATE_URL,
    MAIL_ENDPOINT: MAIL_ENDPOINT,
    ChurchSite: ChurchSite,
    Navigation: Navigation,
    ContactSender: ContactSender,
    SiteApp: SiteApp
  };

  root.FpcSite = api;

  if (typeof document !== "undefined") {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", function () {
        new SiteApp().mount(document);
      });
    } else {
      new SiteApp().mount(document);
    }
  }

  if (typeof module !== "undefined" && module.exports) {
    module.exports = api;
  }
})(typeof window !== "undefined" ? window : typeof globalThis !== "undefined" ? globalThis : this);
