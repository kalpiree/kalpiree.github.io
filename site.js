(() => {
  const input = document.getElementById("publication-search");
  if (!input) return;
  const clear = document.getElementById("clear-search");
  const status = document.getElementById("search-status");
  const empty = document.getElementById("empty-results");
  const papers = Array.from(document.querySelectorAll(".publication"));
  const sections = Array.from(document.querySelectorAll(".publication-section"));
  const normalize = value => value.toLowerCase().normalize("NFKD").replace(/[\u0300-\u036f]/g, "");
  function update() {
    const value = input.value.trim();
    const words = normalize(value).split(/\s+/).filter(Boolean);
    let count = 0;
    papers.forEach(paper => {
      const match = words.every(word => normalize(paper.dataset.search || "").includes(word));
      paper.hidden = !match;
      if (match) count++;
    });
    sections.forEach(section => {
      section.hidden = !Array.from(section.querySelectorAll(".publication")).some(paper => !paper.hidden);
    });
    clear.hidden = !value;
    empty.hidden = count > 0;
    status.textContent = value ? count + (count === 1 ? " matching paper" : " matching papers") : "";
  }
  input.addEventListener("input", update);
  clear.addEventListener("click", () => { input.value = ""; update(); input.focus(); });
  document.querySelectorAll(".publication-jumps a").forEach(a => {
    a.addEventListener("click", () => { input.value = ""; update(); });
  });
  update();
})();

