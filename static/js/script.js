const images = [
  "/static/img/imagem-1.png",
  "/static/img/imagem-2.png",
  "/static/img/imagem-3.png"
];

let current = 0;
const bg1 = document.getElementById("background1");
const bg2 = document.getElementById("background2");

let activeLayer = bg1;
let inactiveLayer = bg2;

// Função para alternar entre camadas com fade para ficar bem babadeiro
function changeBackground() {
  if (!images.length || !bg1 || !bg2) return;

  inactiveLayer.style.backgroundImage = `url(${images[current]})`;
  inactiveLayer.style.opacity = 1;
  activeLayer.style.opacity = 0;

  [activeLayer, inactiveLayer] = [inactiveLayer, activeLayer];
  current = (current + 1) % images.length;
}

window.addEventListener("DOMContentLoaded", () => {
  if (!bg1 || !bg2) return;

  // Primeira imagem
  bg1.style.backgroundImage = `url(${images[current]})`;
  bg1.style.opacity = 1;
  bg2.style.opacity = 0;
  current++;

  setInterval(changeBackground, 10000);

  const form = document.getElementById("reviewForm");
  const result = document.getElementById("result");
  const ratingDisplay = document.getElementById("ratingDisplay");
  const reviewInput = document.getElementById("reviewInput");
  const restartBtn = document.getElementById("restartBtn");

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const text = reviewInput.value.trim();

      if (!text) return;

      ratingDisplay.innerHTML = "Analyzing...";
      result.classList.remove("hidden");
      ratingDisplay.classList.remove("hidden");

      try {
        const response = await fetch("/predict", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text })
        });

        const data = await response.json();

        if (data.rating) {
          const stars = "⭐".repeat(data.rating);
          const labels = [
            "one star 😕",
            "two stars 😐",
            "three stars 🙂",
            "four stars 😄",
            "five stars! 🎉"
          ];

          const label = labels[data.rating - 1] || "unrated 🤔";
          ratingDisplay.innerHTML = `${stars}, ${label}`;
        } else {
          ratingDisplay.innerHTML = "Could not rate your review.";
        }

        restartBtn.classList.remove("hidden");
      } catch (error) {
        console.error("Error:", error);
        ratingDisplay.innerHTML = "Something went wrong 😓";
      }
    });
  }

  if (restartBtn) {
    restartBtn.addEventListener("click", () => {
      reviewInput.value = "";
      ratingDisplay.innerHTML = "";
      result.classList.add("hidden");
      ratingDisplay.classList.add("hidden");
      restartBtn.classList.add("hidden");
      reviewInput.focus();
    });
  }
});
