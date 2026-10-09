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
  const isPrivacy = config.pageType === "privacy";
  const isHome = config.pageType === "home";
  document.title = isHome ? text.appName : (isPrivacy ? text.privacyTitle : text.supportTitle) + " | " + text.appName;
  document.querySelector('meta[name="description"]').content = text.appName + " — " + (isHome ? text.homeIntro : isPrivacy ? text.privacyIntro : text.supportIntro);
  document.querySelectorAll("[data-support-text]").forEach(element => {
   const value = text[element.dataset.supportText];
   if (typeof value === "string") element.textContent = value;
  });
  document.querySelectorAll("[data-page-locale]").forEach(element => { element.hidden = element.dataset.pageLocale !== code; });
  const inquiryNote = document.querySelector("[data-inquiry-note]");
  if (inquiryNote) inquiryNote.textContent = code === "ja" ? "相談に不要な氏名、金額、個人情報は記載しないでください。" : ({en:"Please omit names, amounts, and personal information that are unnecessary for your inquiry.",es:"No incluyas nombres, importes ni datos personales que no sean necesarios para tu consulta.",ko:"문의에 필요하지 않은 이름, 금액, 개인정보는 적지 마세요.","zh-Hans":"请勿提供与咨询无关的姓名、金额或个人信息。","zh-Hant":"請勿提供與諮詢無關的姓名、金額或個人資訊。"})[code];
  const privacyContact = document.querySelector("[data-privacy-contact]");
  if (privacyContact) privacyContact.textContent = code === "ja" ? "本ポリシーに関するお問い合わせはサポートページをご利用ください。お問い合わせ内容は対応のために使用します。" : ({en:"Use the support page for questions about this policy. Information you submit is used to respond to your inquiry.",es:"Usa la página de soporte para consultar esta política. La información enviada se utiliza para responder a tu consulta.",ko:"이 정책에 관한 문의는 지원 페이지를 이용해 주세요. 보내 주신 정보는 문의 응답에 사용됩니다.","zh-Hans":"如对本政策有疑问，请使用支持页面。您提供的信息用于回复咨询。","zh-Hant":"如對本政策有疑問，請使用支援頁面。您提供的資訊用於回覆諮詢。"})[code];
  const faqList = document.querySelector("[data-support-faqs]");
  if (faqList) {
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
  }
  document.querySelectorAll("[data-support-link]").forEach(link => {
   const target = link.dataset.supportLink;
   const path = "/" + config.slug + "/" + (target === "privacy" || target === "support" ? target + "/" : "");
   const url = new URL(path, location.href);
   url.searchParams.set("lang", code);
   link.href = url.href;
  });
  const email = document.querySelector("[data-support-email]");
  if (email) {
  const fields = ["appVersion", "device", "osVersion", "issue", "steps"];
  const body = [text.appName, ...fields.map(key => text[key] + ": ")].join("\n\n");
  email.href = "mailto:" + config.email + "?subject=" + encodeURIComponent(text.appName + " / " + text.contactTitle) + "&body=" + encodeURIComponent(body);
  }
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

