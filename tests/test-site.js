"use strict";

var assert = require("assert");
var fs = require("fs");
var path = require("path");
var vm = require("vm");

var root = path.join(__dirname, "..");
var sitePath = path.join(root, "js", "site.js");
var shipped = require(sitePath);

var ZEFFY =
  "https://www.zeffy.com/en-US/donation-form/offering-to-first-presbyterian-church";
var PASTOR = "pastordavidpeng@gmail.com";
var NAMED = ["About", "Services", "Congregation", "Programs", "Contact", "Donate"];

function runAssertions(api, label) {
  assert.ok(api, label + ": missing API");
  assert.strictEqual(typeof api.ChurchSite, "function", label + ": ChurchSite");
  assert.strictEqual(typeof api.Navigation, "function", label + ": Navigation");
  assert.strictEqual(typeof api.ContactSender, "function", label + ": ContactSender");

  var site = api.ChurchSite.defaults();
  assert.strictEqual(site.contactEmail, PASTOR, label + ": contact email");
  assert.strictEqual(site.donateUrl, ZEFFY, label + ": donate URL");
  assert.ok(
    String(site.mailEndpoint).indexOf(PASTOR) !== -1,
    label + ": mail endpoint includes pastor email"
  );

  var nav = new api.Navigation(site);
  var titles = nav.pageTitles();
  NAMED.forEach(function (title) {
    assert.ok(titles.indexOf(title) !== -1, label + ": nav missing " + title);
  });
  var named = nav.namedPages().map(function (p) {
    return p.title;
  });
  NAMED.forEach(function (title) {
    assert.ok(named.indexOf(title) !== -1, label + ": named page missing " + title);
  });

  var captured = [];
  var sender = new api.ContactSender(site, function (request) {
    captured.push(request);
    return Promise.resolve({ ok: true });
  });
  return sender
    .send({
      name: "Test Neighbor",
      email: "neighbor@example.com",
      message: "Peace to the house."
    })
    .then(function () {
      assert.strictEqual(captured.length, 1, label + ": transport called once");
      var request = captured[0];
      var blob = JSON.stringify(request);
      assert.ok(blob.indexOf(PASTOR) !== -1, label + ": payload includes pastor email");
      assert.ok(
        String(request.url).indexOf(PASTOR) !== -1,
        label + ": request URL includes pastor email"
      );
      assert.strictEqual(request.body.to, PASTOR, label + ": body.to");
      assert.strictEqual(request.method, "POST", label + ": POST");
      console.log("PASS " + label);
    });
}

function loadInWindowSandbox() {
  var code = fs.readFileSync(sitePath, "utf8");
  var window = {};
  var sandbox = { window: window, console: console };
  vm.runInNewContext(code, sandbox);
  assert.ok(sandbox.window.FpcSite, "window.FpcSite after classic script load");
  return sandbox.window.FpcSite;
}

function main() {
  return runAssertions(shipped, "require(js/site.js)")
    .then(function () {
      return runAssertions(loadInWindowSandbox(), "vm window load of js/site.js");
    })
    .then(function () {
      console.log("All site unit assertions passed.");
    });
}

main().catch(function (err) {
  console.error(err && err.stack ? err.stack : err);
  process.exit(1);
});
