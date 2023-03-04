Array.from(document.getElementsByClassName("slider")).map((slider) => {
    const select = (selector: string) => slider.querySelector<HTMLInputElement>(selector);
    const initTimer = () =>
        setInterval(() => {
            const n = select("input:checked ~ input") || select("input:first-child");
            n && (n.checked = true);
        }, 2500);

    let timer = initTimer();

    slider.addEventListener("mouseover", () => clearInterval(timer), true);
    slider.addEventListener("mouseout", () => (timer = initTimer()), true);
});
