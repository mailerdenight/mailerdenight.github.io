"use strict";
const search = document.getElementById("search");
const cards = [...document.querySelectorAll(".app")];
const filters = [...document.querySelectorAll("[data-filter]")];
let category = "";
function update() {
 const query = search.value.trim().normalize("NFKC").toLocaleLowerCase();
 let count = 0;
 for (const card of cards) {
  card.hidden = (category !== "" && card.dataset.category !== category) || !card.dataset.search.normalize("NFKC").toLocaleLowerCase().includes(query);
  if (!card.hidden) count++;
 }
 document.getElementById("count").textContent = count + "アプリ";
 document.getElementById("empty").hidden = count > 0;
}
search.addEventListener("input", update);
for (const filter of filters) filter.addEventListener("click", () => {
 category = filter.dataset.filter;
 for (const other of filters) other.setAttribute("aria-pressed", String(other === filter));
 update();
});
