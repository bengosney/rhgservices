var e;e=(e,t)=>{let r=!1,n=t=>e.querySelector(t);return e.addEventListener("mouseover",()=>r=!0,!0),e.addEventListener("mouseout",()=>r=!1,!0),setInterval(()=>{let e=n("input:checked ~ input")||n("input:first-child");0==document.querySelectorAll(".lightbox input:checked").length&&!r&&e&&(e.checked=!0)},t)},Array.from(document.getElementsByClassName("slider")).map(t=>e(t,2500));//# sourceMappingURL=rhgs.js.map

//# sourceMappingURL=rhgs.js.map
