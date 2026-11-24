const kValue = document.querySelector("#kValue");
const kOutput = document.querySelector("#kOutput");
const heroK = document.querySelector("#heroK");

function formatDetails(data) {
  const neighbors = data.neighbors
    .map((neighbor, index) =>
      `${index + 1}. ${neighbor.label} (dist. ${neighbor.distance})`
    )
    .join("<br>");

  return `
    <p><strong>Confianza:</strong> ${data.confidence}%</p>
    <p><strong>Exactitud del modelo:</strong> ${data.training_accuracy}%</p>
    <p><strong>Vecinos encontrados:</strong><br>${neighbors}</p>
  `;
}

function updateChart(chart, practice, point, prediction) {
  chart.src = `/api/plot/${practice}?x=${encodeURIComponent(point[0])}` +
    `&y=${encodeURIComponent(point[1])}` +
    `&prediction=${encodeURIComponent(prediction)}&cache=${Date.now()}`;
}

kValue.addEventListener("input", () => {
  kOutput.value = `${kValue.value} vecinos`;
  kOutput.textContent = `${kValue.value} vecinos`;
  heroK.textContent = kValue.value;
});

document.querySelector("#clientForm").addEventListener("submit", (event) => {
  event.preventDefault();

  const resultBox = document.querySelector("#clientResult");
  const detailsBox = document.querySelector("#clientDetails");
  const submitButton = event.submitter;
  resultBox.innerHTML = "<span>Resultado</span><strong>Calculando...</strong>";
  submitButton.disabled = true;

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
      detailsBox.innerHTML = formatDetails(data);
      updateChart(
        document.querySelector("#clientChart"),
        "client",
        data.point,
        data.prediction,
      );
    })
    .catch((error) => {
      resultBox.innerHTML =
        `<span>Resultado</span><strong>Error: ${error.message}</strong>`;
      detailsBox.innerHTML = "";
    })
    .finally(() => {
      submitButton.disabled = false;
    });
});

document.querySelector("#investmentForm").addEventListener("submit", (event) => {
  event.preventDefault();

  const resultBox = document.querySelector("#investmentResult");
  const detailsBox = document.querySelector("#investmentDetails");
  const submitButton = event.submitter;
  resultBox.innerHTML = "<span>Resultado</span><strong>Calculando...</strong>";
  submitButton.disabled = true;

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
      detailsBox.innerHTML = formatDetails(data);
      updateChart(
        document.querySelector("#investmentChart"),
        "investment",
        data.point,
        data.prediction,
      );
    })
    .catch((error) => {
      resultBox.innerHTML =
        `<span>Resultado</span><strong>Error: ${error.message}</strong>`;
      detailsBox.innerHTML = "";
    })
    .finally(() => {
      submitButton.disabled = false;
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
