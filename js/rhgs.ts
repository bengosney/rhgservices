import initSlider from "./sliders";
Array.from(document.querySelectorAll("[data-slider]")).map((e) => initSlider(e, 2500));
