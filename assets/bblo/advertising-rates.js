/* Dated launch offer expires at midnight Eastern after February 6, 2027. */
(() => {
  document.querySelectorAll('[data-ad-intro]').forEach(element => {
    const expires = Date.parse(element.dataset.introEnd);
    if (Number.isFinite(expires) && Date.now() >= expires) element.hidden = true;
  });
})();
