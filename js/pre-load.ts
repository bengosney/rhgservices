const initPreloads = () => {
    let timer: NodeJS.Timer | undefined;

    const link: HTMLLinkElement = document.createElement("link");
    link.rel = "prefetch";
    link.onload = () => link.removeAttribute("href");
    document.head.appendChild(link);

    const preload = (element: HTMLAnchorElement) => {
        clearTimeout(timer);
        timer = setTimeout(() => (link.href = element.href), 50);
    };

    document.querySelectorAll<HTMLAnchorElement>("a[href]").forEach((element) => {
        if (element.origin == window.location.origin) {
            ["mouseover", "touchstart"].forEach((event) => {
                element.addEventListener(event, () => preload(element), true);
            });
            ["mouseout", "touchend"].forEach((event) => {
                element.addEventListener(event, () => link.removeAttribute("href"), true);
            });
        }
    });
};

export default initPreloads;
