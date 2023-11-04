const initSlider = (slider: Element, duration: number) => {
    let mouseOver: boolean = false;
    const select = (selector: string) => slider.querySelector<HTMLInputElement>(selector);
    const lightboxSelector = ".lightbox input:checked";
    const initTimer = () =>
        setInterval(() => {
            const next = select("input:checked ~ input") || select("input:first-child");
            if (document.querySelectorAll(lightboxSelector).length == 0 && !mouseOver && next) {
                next.checked = true;
            }
        }, duration);

    slider.addEventListener("mouseover", () => (mouseOver = true), true);
    slider.addEventListener("mouseout", () => (mouseOver = false), true);

    return initTimer();
};

export default initSlider;
