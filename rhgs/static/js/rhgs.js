!function(){var e=(e,t)=>{const n=t=>e.querySelector(t),r=()=>setInterval((()=>{const e=n("input:checked ~ input")||n("input:first-child");e&&(e.checked=!0)}),t);let s=r();e.addEventListener("mouseover",(()=>clearInterval(s)),!0),e.addEventListener("mouseout",(()=>s=r()),!0)};Array.from(document.getElementsByClassName("slider")).map((t=>e(t,2500)))}();
//# sourceMappingURL=rhgs.js.map
