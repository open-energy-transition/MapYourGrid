---
hide:
  - navigation
  - toc
  - footer
---

<div id="gridinspector-root">
  <iframe
    src="https://mapyourgrid.dynartio.com/gridinspector/"
    class="iframestyle" allow="fullscreen">
  </iframe>
</div>

<style>

body:has(#gridinspector-root) {
  overflow: hidden;
}

body:has(#gridinspector-root) .md-main,
body:has(#gridinspector-root) .md-main__inner,
body:has(#gridinspector-root) .md-content,
body:has(#gridinspector-root) .md-content__inner {
  padding: 0 !important;
  margin: 0 !important;
  max-width: none !important;
  height: 100%;
}

body:has(#gridinspector-root) .md-typeset h1, 
body:has(#gridinspector-root) .md-content__inner > h1 {
  display: none !important;
}

#gridinspector-root {
  position: fixed;
  top: 5.8rem;      
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
}


/* Make iframe fill the viewport completely */
.iframestyle {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

@media (max-width: 1080px){
 .iframestyle {
   width: 104vw;
 }
}
</style>

<script>
document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector(".md-header");
  const banner = document.querySelector(".md-banner");
  let topOffset = 0;
  if (header) topOffset += header.getBoundingClientRect().height;
  if (banner) topOffset += banner.getBoundingClientRect().height;
  document.getElementById("gridinspector-root").style.top = topOffset + "px";
});
</script>

