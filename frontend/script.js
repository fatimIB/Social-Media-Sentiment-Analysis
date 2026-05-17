const API = 'http://127.0.0.1:8000';

const inp = document.getElementById('inputText');
inp.addEventListener('input', () => {
  document.getElementById('charCount').textContent = inp.value.length + ' characters';
});

window.addEventListener('DOMContentLoaded', () => {
  setTimeout(() => {
    document.getElementById('b1').style.width = '91%';
    document.getElementById('b2').style.width = '85%';
    document.getElementById('b3').style.width = '78%';
    document.getElementById('b4').style.width = '87%';
  }, 300);
});

new Chart(document.getElementById('distChart').getContext('2d'), {
  type: 'bar',
  data: {
    labels: ['Positive', 'Negative', 'Neutral'],
    datasets: [{
      data: [46, 36, 18],
      backgroundColor: ['#1D9E75', '#E24B4A', '#BA7517'],
      borderRadius: 7,
      borderSkipped: false
    }]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { callbacks: { label: c => ' ' + c.parsed.y + '%' } }
    },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 11, family: "'DM Sans'" }, color: '#9ca3af' }
      },
      y: {
        grid: { color: 'rgba(0,0,0,0.05)' },
        ticks: {
          font: { size: 11, family: "'DM Sans'" },
          color: '#9ca3af',
          callback: v => v + '%'
        },
        max: 60
      }
    }
  }
});

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

new Chart(document.getElementById('trendChart').getContext('2d'), {
  type: 'line',
  data: {
    labels: days,
    datasets: [
      {
        label: 'Positive',
        data: [58, 62, 60, 65, 63, 68, 62],
        borderColor: '#1D9E75',
        backgroundColor: 'rgba(29,158,117,0.07)',
        tension: 0.4,
        fill: true,
        pointRadius: 3,
        borderWidth: 2
      },
      {
        label: 'Negative',
        data: [24, 21, 23, 20, 22, 18, 21],
        borderColor: '#E24B4A',
        backgroundColor: 'transparent',
        tension: 0.4,
        pointRadius: 3,
        borderWidth: 2,
        borderDash: [5, 3]
      },
      {
        label: 'Neutral',
        data: [18, 17, 17, 15, 15, 14, 17],
        borderColor: '#BA7517',
        backgroundColor: 'transparent',
        tension: 0.4,
        pointRadius: 3,
        borderWidth: 2,
        borderDash: [2, 3]
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: {
        grid: { display: false },
        ticks: { font: { size: 11, family: "'DM Sans'" }, color: '#9ca3af' }
      },
      y: {
        grid: { color: 'rgba(0,0,0,0.05)' },
        ticks: {
          font: { size: 11, family: "'DM Sans'" },
          color: '#9ca3af',
          callback: v => v + '%'
        }
      }
    }
  }
});

const history = [];

function addToFeed(text, sentiment, conf) {
  history.unshift({ text, sentiment, conf });

  const colors = {
    Positive: '#1D9E75',
    Negative: '#E24B4A',
    Neutral: '#BA7517'
  };

  const bgs = {
    Positive: '#E1F5EE',
    Negative: '#FCEBEB',
    Neutral: '#FAEEDA'
  };

  const labels = {
    Positive: 'Positive',
    Negative: 'Negative',
    Neutral: 'Neutral'
  };

  document.getElementById('feed').innerHTML = history.slice(0, 5).map(h => `
    <div class="feed-item">
      <div class="feed-icon" style="background:${bgs[h.sentiment]}">
        <div class="feed-dot" style="background:${colors[h.sentiment]}"></div>
      </div>
      <div>
        <div class="feed-title">${labels[h.sentiment]} · ${(h.conf * 100).toFixed(0)}% confidence</div>
        <div class="feed-meta">${h.text.slice(0, 65)}${h.text.length > 65 ? '…' : ''}</div>
      </div>
    </div>
  `).join('');
}

async function runAnalysis() {
  const text = inp.value.trim();
  if (!text) return;

  const btn = document.getElementById('analyzeBtn');
  const box = document.getElementById('resultBox');

  btn.disabled = true;
  btn.textContent = 'Analyzing...';

  box.innerHTML = `<div style="padding:12px;font-size:12px;color:var(--muted)">Connecting to API...</div>`;

  document.getElementById('postsBox').style.display = 'none';
  document.getElementById('postsBox').innerHTML = '';

  try {
    const res = await fetch(API + '/analyze?query=' + encodeURIComponent(text));
    if (!res.ok) throw new Error('API error ' + res.status);

    const data = await res.json();
    const s = data.summary || {};

    const pos = parseFloat(s.positive_pct || 0);
    const neg = parseFloat(s.negative_pct || 0);
    const neu = parseFloat(s.neutral_pct || 0);

    const scores = { Positive: pos, Negative: neg, Neutral: neu };

    const dom = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];

    const colors = { Positive: '#1D9E75', Negative: '#E24B4A', Neutral: '#BA7517' };
    const bgs = { Positive: '#E1F5EE', Negative: '#FCEBEB', Neutral: '#FAEEDA' };
    const darks = { Positive: '#085041', Negative: '#791F1F', Neutral: '#633806' };
    const labels = { Positive: 'POSITIVE', Negative: 'NEGATIVE', Neutral: 'NEUTRAL' };

    box.innerHTML = `
      <div class="result-box">
        <div class="result-head">
          <span class="result-badge" style="background:${bgs[dom[0]]};color:${darks[dom[0]]}">${labels[dom[0]]}</span>
          <span style="font-size:12px;color:var(--muted)">${dom[1].toFixed(1)}% confidence · ${data.count || 0} posts analyzed</span>
        </div>

        <div class="score-bars">
          ${[['Positive', pos, '#1D9E75'], ['Neutral', neu, '#BA7517'], ['Negative', neg, '#E24B4A']].map(([n, v, c]) => `
            <div class="score-line">
              <span class="score-name">${n}</span>
              <div class="score-track"><div class="score-fill" style="width:0;background:${c}" data-w="${v}"></div></div>
              <span class="score-num">${v.toFixed(1)}%</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    setTimeout(() => {
      document.querySelectorAll('[data-w]').forEach(el => {
        el.style.width = el.dataset.w + '%';
      });
    }, 50);

    addToFeed(text, dom[0], dom[1] / 100);

    const results = data.results || [];
    const postsBox = document.getElementById('postsBox');

    if (results.length > 0) {
      const sentColors = { Positive: '#1D9E75', Negative: '#E24B4A', Neutral: '#BA7517' };
      const sentBgs = { Positive: '#E1F5EE', Negative: '#FCEBEB', Neutral: '#FAEEDA' };
      const sentDarks = { Positive: '#085041', Negative: '#791F1F', Neutral: '#633806' };
      const sentLabels = { Positive: 'Positive', Negative: 'Negative', Neutral: 'Neutral' };

      postsBox.style.display = 'block';

      postsBox.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px">
          <div>
            <div style="font-size:13px;font-weight:600">${results.length} posts analyzed</div>
            <div style="font-size:11px;color:var(--dim);margin-top:2px">
              Subreddits : ${(data.top_subreddits || []).map(s => 'r/' + s).join(', ') || '—'}
            </div>
          </div>
          <span style="font-size:11px;color:var(--muted)">Click to open Reddit post</span>
        </div>

        <div style="border:1px solid var(--border);border-radius:var(--radius);overflow:hidden">
          <table style="width:100%;border-collapse:collapse;font-size:12px;table-layout:fixed">
            <thead>
              <tr style="background:var(--surface2)">
                <th style="padding:10px 14px;text-align:left;width:38%">Title</th>
                <th style="padding:10px 14px;text-align:left;width:14%">Subreddit</th>
                <th style="padding:10px 14px;text-align:left;width:13%">Sentiment</th>
                <th style="padding:10px 14px;text-align:right;width:10%">Score</th>
                <th style="padding:10px 14px;text-align:right;width:10%">Confidence</th>
                <th style="padding:10px 14px;text-align:center;width:15%">Link</th>
              </tr>
            </thead>
            <tbody>
              ${results.map((r, i) => `
                <tr style="border-top:1px solid var(--border);background:${i % 2 === 0 ? 'var(--surface)' : 'var(--surface2)'}">
                  <td style="padding:10px 14px;overflow:hidden">
                    <div style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${r.title || r.text?.slice(0, 60) || '—'}</div>
                    ${r.text ? `<div style="font-size:11px;color:var(--dim);margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${r.text.slice(0, 80)}…</div>` : ''}
                  </td>
                  <td style="padding:10px 14px;color:var(--muted)">r/${r.subreddit || '—'}</td>
                  <td style="padding:10px 14px">
                    <span style="padding:3px 8px;border-radius:99px;background:${sentBgs[r.sentiment]};color:${sentDarks[r.sentiment]}">
                      ${sentLabels[r.sentiment] || r.sentiment}
                    </span>
                  </td>
                  <td style="padding:10px 14px;text-align:right">${r.score ?? '—'}</td>
                  <td style="padding:10px 14px;text-align:right">${r.confidence ? (r.confidence * 100).toFixed(0) + '%' : '—'}</td>
                  <td style="padding:10px 14px;text-align:center">
                    ${r.url ? `<a href="${r.url}" target="_blank" rel="noreferrer" style="display:inline-flex;align-items:center;gap:4px;font-size:11px;font-weight:600;color:var(--green-dark);background:var(--green-bg);padding:4px 10px;border-radius:99px;text-decoration:none;white-space:nowrap;border:1px solid #9FE1CB">Open ↗</a>` : '<span style="color:var(--dim);font-size:11px">—</span>'}
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } else {
      postsBox.style.display = 'none';
    }

  } catch (e) {
    box.innerHTML = `<div style="padding:12px;color:var(--red-dark);background:var(--red-bg);border-radius:8px">
      Cannot connect to API on port 8000 — start FastAPI server first.
    </div>`;
    document.getElementById('postsBox').style.display = 'none';
  }

  btn.disabled = false;
  btn.textContent = 'Analyze →';
}