const initSlider = (slider: Element, duration: number) => {
    const select = (selector: string) => slider.querySelector<HTMLInputElement>(selector);

    const nextSlide = () => select("input:checked ~ input") || select("input:first-child");

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

    let startEvent: TouchEvent | undefined = undefined;
    slider.addEventListener("touchstart", (e) => (startEvent = e as TouchEvent), true);
    slider.addEventListener(
        "touchend",
        (e) => {
            const endEvent = e as TouchEvent;
            if (startEvent) {
                const timeDiff = endEvent.timeStamp - startEvent.timeStamp;
                const { touches } = startEvent;
                const { changedTouches } = endEvent;
                const xDiff = changedTouches[0].screenX - touches[0].screenX;
                const yDiff = changedTouches[0].screenY - touches[0].screenY;

                if (timeDiff <= 500 && Math.abs(xDiff) > Math.abs(yDiff * 1.5) && Math.abs(xDiff) > 100) {
                    if (xDiff > 0) {
                        nextSlide()?.checked;
                    }
                }
            }
        },
        true,
    );
};

export default initSlider;
