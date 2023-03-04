const initSlider = (slider: Element, duration: number) => {
    const select = (selector: string) => slider.querySelector<HTMLInputElement>(selector);
    const initTimer = () =>
        setInterval(() => {
            const next = select("input:checked ~ input") || select("input:first-child");
            if (next) {
                next.checked = true;
            } else {
                clearInterval(timer);
            }
        }, duration);

    let timer = initTimer();

    slider.addEventListener("mouseover", () => clearInterval(timer), true);
    slider.addEventListener("mouseout", () => (timer = initTimer()), true);
};

export default initSlider;
