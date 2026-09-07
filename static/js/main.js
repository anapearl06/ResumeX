function toast(message, type = '') {
  const el = document.createElement('div');
  el.className = 'toast ' + type;
  el.setAttribute('role', 'status');

  const icons = {
    success: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;flex-shrink:0"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="m9 11 3 3L22 4"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;flex-shrink:0"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    default: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px;flex-shrink:0"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
  };

  el.innerHTML = icons[type] || icons.default;
  el.appendChild(document.createTextNode(' '));
  el.appendChild(document.createTextNode(message));
  document.body.appendChild(el);

  setTimeout(() => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(8px)';
    setTimeout(() => el.remove(), 200);
  }, 2800);
}

async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    headers: options.body instanceof FormData ? {} : { 'Content-Type': 'application/json' },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
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