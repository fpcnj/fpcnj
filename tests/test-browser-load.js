"use strict";

var assert = require("assert");
var fs = require("fs");
var path = require("path");
var vm = require("vm");

var sitePath = path.join(__dirname, "..", "js", "site.js");
var code = fs.readFileSync(sitePath, "utf8");

var window = {};
var sandbox = {
  window: window,
  console: console
};

vm.runInNewContext(code, sandbox, { filename: "site.js" });

assert.strictEqual(typeof sandbox.module, "undefined", "no module global");
assert.strictEqual(typeof sandbox.require, "undefined", "no require global");
assert.ok(window.FpcSite, "FpcSite attached to window");
assert.strictEqual(typeof window.FpcSite.ChurchSite, "function");
assert.strictEqual(typeof window.FpcSite.SiteApp, "function");

var site = window.FpcSite.ChurchSite.defaults();
var app = new window.FpcSite.SiteApp(site);
assert.strictEqual(app.site.donateUrl, window.FpcSite.DONATE_URL);
assert.ok(app.nav.pageTitles().indexOf("Contact") !== -1);

console.log("PASS browser-like script load (window, no Node globals)");
