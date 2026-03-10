// Reading-progress bar
(function () {
  const bar = document.querySelector('.progress-bar');
  if (!bar) return;
  window.addEventListener('scroll', function () {
    const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    bar.style.width = (scrollTop / docHeight * 100) + '%';
  });
})();

// Video toggle buttons
(function () {
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.video-toggle');
    if (!btn) return;
    var targetId = btn.getAttribute('data-target');
    var wrapper = document.getElementById(targetId);
    if (!wrapper) return;
    var isOpen = wrapper.classList.toggle('visible');
    btn.classList.toggle('open', isOpen);
    btn.innerHTML = isOpen ? '&#9660; Hide Animation' : '&#9654; Watch Chapter Animation';
  });
})();
