!function(){var e=(e,t)=>{const r=t=>e.querySelector(t),o=()=>setInterval((()=>{const e=r("input:checked ~ input")||r("input:first-child");e?e.checked=!0:clearInterval(n)}),t);let n=o();e.addEventListener("mouseover",(()=>clearInterval(n)),!0),e.addEventListener("mouseout",(()=>n=o()),!0)};var t=()=>{let e;const t=document.createElement("link");t.rel="prefetch",t.onload=()=>t.removeAttribute("href"),document.head.appendChild(t);document.querySelectorAll("a[href]").forEach((r=>{r.origin==window.location.origin&&(["mouseover","touchstart"].forEach((o=>{r.addEventListener(o,(()=>(r=>{clearTimeout(e),e=setTimeout((()=>t.href=r.href),50)})(r)),!0)})),["mouseout","touchend"].forEach((e=>{r.addEventListener(e,(()=>t.removeAttribute("href")),!0)})))}))};Array.from(document.getElementsByClassName("slider")).map((t=>e(t,2500))),t()}();
//# sourceMappingURL=rhgs.js.map
