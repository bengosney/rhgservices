import initSlider from "./sliders";
//import initPreloads from "./pre-load";

Array.from(document.getElementsByClassName("slider")).map((e) => initSlider(e, 2500));

//initPreloads();
