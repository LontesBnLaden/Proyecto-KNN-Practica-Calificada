const kValue = document.querySelector("#kValue");
const kOutput = document.querySelector("#kOutput");
const heroK = document.querySelector("#heroK");

kValue.addEventListener("input", () => {
  kOutput.value = `${kValue.value} vecinos`;
  kOutput.textContent = `${kValue.value} vecinos`;
  heroK.textContent = kValue.value;
});

document.querySelector("#clientForm").addEventListener("submit", (event) => {
  event.preventDefault();

  const resultBox = document.querySelector("#clientResult");
  resultBox.innerHTML = "<span>Resultado</span><strong>Calculando...</strong>";

  fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      practice: "client",
      attention: document.querySelector("#attention").value,
      responseTime: document.querySelector("#responseTime").value,
      k: kValue.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) throw new Error(data.error);
      resultBox.innerHTML =
        `<span>Resultado</span><strong>${data.prediction}</strong>`;
    })
    .catch((error) => {
      resultBox.innerHTML =
        `<span>Resultado</span><strong>Error: ${error.message}</strong>`;
    });
});

document.querySelector("#investmentForm").addEventListener("submit", (event) => {
  event.preventDefault();

  const resultBox = document.querySelector("#investmentResult");
  resultBox.innerHTML = "<span>Resultado</span><strong>Calculando...</strong>";

  fetch("/api/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      practice: "investment",
      profit: document.querySelector("#profit").value,
      risk: document.querySelector("#risk").value,
      k: kValue.value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) throw new Error(data.error);
      resultBox.innerHTML =
        `<span>Resultado</span><strong>${data.prediction}</strong>`;
    })
    .catch((error) => {
      resultBox.innerHTML =
        `<span>Resultado</span><strong>Error: ${error.message}</strong>`;
    });
});

const menuButton = document.querySelector(".menu-button");
const navLinks = document.querySelector(".nav-links");

menuButton.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  menuButton.setAttribute("aria-expanded", String(isOpen));
});

navLinks.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    menuButton.setAttribute("aria-expanded", "false");
  });
});
