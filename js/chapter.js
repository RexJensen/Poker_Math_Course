/* ===== Shared Chapter JavaScript ===== */

// --- Quiz functionality ---
function initQuizzes() {
  document.querySelectorAll('.quiz-box').forEach(quiz => {
    const options = quiz.querySelectorAll('.quiz-option');
    const feedback = quiz.querySelector('.quiz-feedback');
    let answered = false;

    options.forEach(opt => {
      opt.addEventListener('click', () => {
        if (answered) return;
        answered = true;
        const isCorrect = opt.dataset.correct === 'true';
        opt.classList.add(isCorrect ? 'correct' : 'incorrect');

        if (!isCorrect) {
          options.forEach(o => {
            if (o.dataset.correct === 'true') o.classList.add('correct');
          });
        }

        if (feedback) {
          feedback.classList.add('show', isCorrect ? 'correct' : 'incorrect');
          feedback.textContent = isCorrect
            ? (feedback.dataset.correct || 'Correct!')
            : (feedback.dataset.incorrect || 'Not quite. See the correct answer highlighted above.');
        }
      });
    });
  });
}

// --- Poker card rendering ---
function card(rank, suit) {
  const suitSymbols = { s: '\u2660', h: '\u2665', d: '\u2666', c: '\u2663' };
  const isRed = suit === 'h' || suit === 'd';
  return `<span class="poker-card ${isRed ? 'red' : 'black'}">${rank}${suitSymbols[suit]}</span>`;
}

// --- Simple bar chart on canvas ---
function drawBarChart(canvasId, labels, values, opts = {}) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const pad = { top: 30, right: 20, bottom: 50, left: 60 };
  const chartW = W - pad.left - pad.right;
  const chartH = H - pad.top - pad.bottom;

  const maxVal = opts.maxVal || Math.max(...values) * 1.15;
  const minVal = opts.minVal !== undefined ? opts.minVal : Math.min(0, ...values);
  const range = maxVal - minVal;

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#161b22';
  ctx.fillRect(0, 0, W, H);

  // Grid lines
  ctx.strokeStyle = '#30363d';
  ctx.lineWidth = 0.5;
  for (let i = 0; i <= 4; i++) {
    const y = pad.top + (chartH * i / 4);
    ctx.beginPath();
    ctx.moveTo(pad.left, y);
    ctx.lineTo(W - pad.right, y);
    ctx.stroke();
    ctx.fillStyle = '#8b949e';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'right';
    const val = maxVal - (range * i / 4);
    ctx.fillText(val.toFixed(opts.decimals || 1), pad.left - 8, y + 4);
  }

  // Bars
  const barW = chartW / labels.length * 0.7;
  const gap = chartW / labels.length * 0.3;
  const zeroY = pad.top + chartH * (maxVal / range);

  values.forEach((v, i) => {
    const x = pad.left + (chartW / labels.length) * i + gap / 2;
    const barH = (v / range) * chartH;
    const y = v >= 0 ? zeroY - barH : zeroY;

    ctx.fillStyle = v >= 0 ? (opts.posColor || '#2ea043') : (opts.negColor || '#c9382a');
    ctx.fillRect(x, y, barW, Math.abs(barH));

    // Label
    ctx.fillStyle = '#8b949e';
    ctx.font = '11px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(labels[i], x + barW / 2, H - pad.bottom + 18);
  });

  // Title
  if (opts.title) {
    ctx.fillStyle = '#e6edf3';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(opts.title, W / 2, 18);
  }
}

// --- Normal distribution PDF ---
function normalPDF(x, mu, sigma) {
  const exp = -0.5 * Math.pow((x - mu) / sigma, 2);
  return (1 / (sigma * Math.sqrt(2 * Math.PI))) * Math.exp(exp);
}

// --- Draw normal distribution curve ---
function drawNormalCurve(canvasId, mu, sigma, opts = {}) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  const pad = { top: 20, right: 20, bottom: 40, left: 50 };

  ctx.clearRect(0, 0, W, H);
  ctx.fillStyle = '#161b22';
  ctx.fillRect(0, 0, W, H);

  const xMin = mu - 4 * sigma;
  const xMax = mu + 4 * sigma;
  const yMax = normalPDF(mu, mu, sigma) * 1.15;

  // Shaded region
  if (opts.shadeFrom !== undefined && opts.shadeTo !== undefined) {
    ctx.fillStyle = 'rgba(46, 160, 67, 0.3)';
    ctx.beginPath();
    const fromPx = pad.left + ((opts.shadeFrom - xMin) / (xMax - xMin)) * (W - pad.left - pad.right);
    ctx.moveTo(fromPx, H - pad.bottom);
    for (let px = fromPx; px <= pad.left + ((opts.shadeTo - xMin) / (xMax - xMin)) * (W - pad.left - pad.right); px++) {
      const x = xMin + ((px - pad.left) / (W - pad.left - pad.right)) * (xMax - xMin);
      const y = normalPDF(x, mu, sigma);
      const yPx = H - pad.bottom - (y / yMax) * (H - pad.top - pad.bottom);
      ctx.lineTo(px, yPx);
    }
    const toPx = pad.left + ((opts.shadeTo - xMin) / (xMax - xMin)) * (W - pad.left - pad.right);
    ctx.lineTo(toPx, H - pad.bottom);
    ctx.closePath();
    ctx.fill();
  }

  // Curve
  ctx.strokeStyle = opts.color || '#e05347';
  ctx.lineWidth = 2;
  ctx.beginPath();
  for (let px = pad.left; px <= W - pad.right; px++) {
    const x = xMin + ((px - pad.left) / (W - pad.left - pad.right)) * (xMax - xMin);
    const y = normalPDF(x, mu, sigma);
    const yPx = H - pad.bottom - (y / yMax) * (H - pad.top - pad.bottom);
    if (px === pad.left) ctx.moveTo(px, yPx);
    else ctx.lineTo(px, yPx);
  }
  ctx.stroke();

  // Axis
  ctx.strokeStyle = '#30363d';
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(pad.left, H - pad.bottom);
  ctx.lineTo(W - pad.right, H - pad.bottom);
  ctx.stroke();

  // Labels
  ctx.fillStyle = '#8b949e';
  ctx.font = '11px sans-serif';
  ctx.textAlign = 'center';
  for (let s = -3; s <= 3; s++) {
    const v = mu + s * sigma;
    const px = pad.left + ((v - xMin) / (xMax - xMin)) * (W - pad.left - pad.right);
    ctx.fillText(v.toFixed(0), px, H - pad.bottom + 16);
  }

  if (opts.title) {
    ctx.fillStyle = '#e6edf3';
    ctx.font = 'bold 13px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(opts.title, W / 2, 15);
  }
}

// --- Cumulative normal distribution (approximation) ---
function normalCDF(x) {
  const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741;
  const a4 = -1.453152027, a5 = 1.061405429, p = 0.3275911;
  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x) / Math.sqrt(2);
  const t = 1.0 / (1.0 + p * x);
  const y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);
  return 0.5 * (1.0 + sign * y);
}

// --- Format percentage ---
function pct(v, d = 1) {
  return (v * 100).toFixed(d) + '%';
}

// --- Init on DOM ready ---
document.addEventListener('DOMContentLoaded', () => {
  initQuizzes();

  // Reading progress bar
  const bar = document.querySelector('.progress-bar');
  if (bar) {
    window.addEventListener('scroll', () => {
      const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
      const docHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      bar.style.width = (scrollTop / docHeight * 100) + '%';
    });
  }
});
