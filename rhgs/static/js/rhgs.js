Array.from(document.getElementsByClassName("slider")).map(e=>{let t;return t=!1,e.addEventListener("mouseover",()=>t=!0,!0),e.addEventListener("mouseout",()=>t=!1,!0),setInterval(()=>{let r=e.querySelector("input:checked ~ input")||e.querySelector("input:first-child");0==document.querySelectorAll(".lightbox input:checked").length&&!t&&r&&(r.checked=!0)},2500)});
//# sourceMappingURL=rhgs.js.map
