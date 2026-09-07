function toast(message, type = '') {
  const el = document.createElement('div');
  el.className = 'toast ' + type;
  el.textContent = message;
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 3000);
}

async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    headers: options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' },
    ...options,
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || 'Something went wrong');
  return data;
}

function esc(str) {
  if (!str) return '';
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

function matchRing(id, score, color) {
  color = color || '#18181B';
  const el = document.getElementById(id);
  if (!el) return;
  var r = 30, c = 2 * Math.PI * r, offset = c - (score / 100) * c;
  el.innerHTML =
    '<svg width="72" height="72" viewBox="0 0 72 72">' +
    '<circle class="ring-bg" cx="36" cy="36" r="' + r + '"/>' +
    '<circle class="ring-fill" cx="36" cy="36" r="' + r + '" stroke="' + color + '" stroke-dasharray="' + c + '" stroke-dashoffset="' + c + '"/>' +
    '</svg>' +
    '<div class="ring-text">' + score + '%</div>';
  requestAnimationFrame(function() {
    requestAnimationFrame(function() {
      el.querySelector('.ring-fill').style.strokeDashoffset = offset;
    });
  });
}
