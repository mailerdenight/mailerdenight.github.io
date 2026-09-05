const filters = document.querySelectorAll('.filter');
const cards = document.querySelectorAll('.cut-card');

filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    filters.forEach((button) => button.classList.remove('active'));
    filter.classList.add('active');
    const type = filter.dataset.filter;
    cards.forEach((card) => {
      card.classList.toggle('hidden', type !== 'all' && card.dataset.type !== type);
    });
  });
});
