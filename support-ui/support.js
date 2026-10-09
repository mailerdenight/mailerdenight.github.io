"use strict";
(() => {
 const node = document.getElementById("support-page-config");
 if (!node) return;
 const config = JSON.parse(node.textContent);
 const locales = Object.keys(config.locales);
 const selector = document.getElementById("language-selector");
 const storageKey = "mailerdenight-support-language";
 let active = config.defaultLocale || "ja";
 function localeFrom(value) {
  if (typeof value !== "string") return null;
  const lower = value.replaceAll("_", "-").toLowerCase();
  const exact = locales.find(code => code.toLowerCase() === lower);
  if (exact) return exact;
  if (lower.startsWith("zh")) {
   const traditional = /(?:^|-)(hant|tw|hk|mo)(?:-|$)/.test(lower);
   const preferred = traditional ? "zh-Hant" : "zh-Hans";
   return locales.includes(preferred) ? preferred : null;
  }
  return locales.find(code => code.split("-")[0].toLowerCase() === lower.split("-")[0]) || null;
 }
 function storedLocale() {
  try { return localeFrom(localStorage.getItem(storageKey)); } catch { return null; }
 }
 function chooseLocale() {
  const query = localeFrom(new URLSearchParams(location.search).get("lang"));
  const languages = navigator.languages || [navigator.language];
  return query || storedLocale() || languages.map(localeFrom).find(Boolean) || active;
 }
 function render(code) {
  const text = config.locales[code];
  if (!text) return;
  active = code;
  document.documentElement.lang = code;
  document.title = text.supportTitle + " | " + text.appName;
  document.querySelector('meta[name="description"]').content = text.appName + " — " + text.supportIntro;
  document.querySelectorAll("[data-support-text]").forEach(element => {
   const value = text[element.dataset.supportText];
   if (typeof value === "string") element.textContent = value;
  });
  const faqList = document.querySelector("[data-support-faqs]");
  faqList.replaceChildren();
  for (const faq of text.faqs || []) {
   const article = document.createElement("article");
   article.className = "faq-item";
   const heading = document.createElement("h3");
   heading.textContent = faq.question;
   const answer = document.createElement("p");
   answer.textContent = faq.answer;
   article.append(heading, answer);
   faqList.append(article);
  }
  document.querySelectorAll("[data-support-link]").forEach(link => {
   const path = link.dataset.supportLink === "privacy" ? "/" + config.slug + "/privacy/" : "/" + config.slug + "/";
   const url = new URL(path, location.href);
   url.searchParams.set("lang", code);
   link.href = url.href;
  });
  const email = document.querySelector("[data-support-email]");
  const fields = ["appVersion", "device", "osVersion", "issue", "steps"];
  const body = [text.appName, ...fields.map(key => text[key] + ": ")].join("\n\n");
  email.href = "mailto:" + config.email + "?subject=" + encodeURIComponent(text.appName + " / " + text.contactTitle) + "&body=" + encodeURIComponent(body);
  document.querySelector("[data-support-nav]").setAttribute("aria-label", text.navLabel);
  selector.value = code;
  selector.setAttribute("aria-label", text.language);
 }
 selector.addEventListener("change", () => {
  const code = selector.value;
  if (!config.locales[code]) return;
  try { localStorage.setItem(storageKey, code); } catch {}
  const url = new URL(location.href);
  url.searchParams.set("lang", code);
  try { history.replaceState(null, "", url.href); } catch {}
  render(code);
 });
 window.addEventListener("popstate", () => render(chooseLocale()));
 render(chooseLocale());
})();
