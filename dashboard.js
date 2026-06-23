import { apiFetch, getCurrentUser, getToken, setToken } from './api.js';

async function init() {
  // auth check
  const navActions = document.getElementById('nav-actions');
  if (!getToken()) {
    navActions.innerHTML = `<a href="login.html" class="btn btn-ghost">تسجيل الدخول</a> <a href="register.html" class="btn btn-primary">انضم الآن</a>`;
  } else {
    navActions.innerHTML = `<button id="btn-logout" class="btn btn-ghost">تسجيل الخروج</button>`;
    document.getElementById('btn-logout').addEventListener('click', () => { setToken(null); window.location.href = 'index.html'; });
  }

  let user;
  try {
    user = await getCurrentUser();
  } catch (err) {
    // Not authenticated
    document.getElementById('user-info').innerHTML = `<p>لم يتم تسجيل الدخول. <a href="login.html">تسجيل الدخول</a></p>`;
    return;
  }

  document.getElementById('user-info').innerHTML = `
    <strong>${user.full_name}</strong> — <small>${user.email}</small>
    <div>الدور: ${user.role}</div>
  `;

  // role-specific UI
  if (user.role === 'trainer') {
    document.getElementById('trainer-section').style.display = 'block';
    await loadSkills();
    await loadTrainerProfile(user.id);
    await loadRequests(user.id);
  } else {
    document.getElementById('trainee-section').style.display = 'block';
    await loadTrainers();
    await loadMyRequests(user.id);
    document.getElementById('btn-search-trainers').addEventListener('click', () => loadTrainers(document.getElementById('search-trainer').value));
  }
}

async function loadSkills() {
  const skills = await apiFetch('/skills');
  const sel = document.getElementById('skill-select');
  sel.innerHTML = skills.map(s => `<option value="${s.id}">${s.name}</option>`).join('');
  document.getElementById('trainer-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
      skill_id: parseInt(sel.value),
      city: document.getElementById('trainer-city').value || 'غير محدد',
      experience_years: parseInt(document.getElementById('trainer-exp').value) || 0,
      bio: document.getElementById('trainer-bio').value || ''
    };
    try {
      const res = await apiFetch('/trainers/me', { method: 'POST', body: JSON.stringify(payload) });
      alert('تم حفظ ملف المدرب');
      loadTrainerProfile(res.user_id || res.id);
    } catch (err) { alert(err.detail || 'خطأ'); }
  });
}

async function loadTrainerProfile(userId) {
  try {
    const profile = await apiFetch('/trainers/me');
    const container = document.getElementById('trainer-profile');
    if (!profile) { container.innerHTML = '<p>لم تقم بإنشاء ملف بعد.</p>'; return; }
    container.innerHTML = `
      <div><strong>المدينة:</strong> ${profile.city}</div>
      <div><strong>المهارة:</strong> ${profile.skill?.name || '—'}</div>
      <div><strong>سنوات الخبرة:</strong> ${profile.experience_years}</div>
      <div><strong>نبذة:</strong> ${profile.bio || '—'}</div>
    `;
  } catch (err) { console.error(err); }
}

async function loadRequests(trainerId) {
  // trainer sees received requests via /requests
  const list = await apiFetch('/requests');
  const el = document.getElementById('requests-list');
  if (!list.length) { el.innerHTML = '<p>لا توجد طلبات واردة.</p>'; return; }
  el.innerHTML = list.map(r => `
    <div class="request-item card">
      <div><strong>${r.trainee.full_name}</strong> — ${r.message || ''}</div>
      <div>الحالة: ${r.status}</div>
      <div style="margin-top:8px;"><button class="btn" data-id="${r.id}" data-action="accept">قبول</button> <button class="btn btn-ghost" data-id="${r.id}" data-action="reject">رفض</button></div>
    </div>
  `).join('');
  el.querySelectorAll('button').forEach(b => {
    b.addEventListener('click', async (e) => {
      const id = e.target.dataset.id;
      const action = e.target.dataset.action;
      try {
        const status = action === 'accept' ? 'accepted' : 'rejected';
        await apiFetch(`/requests/${id}`, { method: 'PATCH', body: JSON.stringify({ status }) });
        alert('تم تحديث الحالة');
        loadRequests();
      } catch (err) { alert(err.detail || 'خطأ'); }
    });
  });
}

async function loadTrainers(query = '') {
  const trainers = await apiFetch('/trainers');
  const filtered = trainers.filter(t => !query || (t.user.full_name + ' ' + (t.city||'')).toLowerCase().includes(query.toLowerCase()));
  const el = document.getElementById('trainers-list');
  if (!filtered.length) { el.innerHTML = '<p>لا يوجد مدربون.</p>'; return; }
  el.innerHTML = filtered.map(t => `
    <div class="trainer-card card">
      <div><strong>${t.user.full_name}</strong></div>
      <div>${t.skill?.name || ''} — ${t.city}</div>
      <div style="margin-top:8px;"><button class="btn" data-id="${t.user.id}">أرسل طلب تدريب</button></div>
    </div>
  `).join('');
  el.querySelectorAll('button').forEach(b => b.addEventListener('click', async (e) => {
    const trainerId = e.target.dataset.id;
    const message = prompt('اكتب رسالة قصيرة لتعريف نفسك');
    if (!message) return;
    try {
      const res = await apiFetch('/requests', { method: 'POST', body: JSON.stringify({ trainer_id: trainerId, message }) });
      alert('تم إرسال الطلب');
      loadMyRequests();
    } catch (err) { alert(err.detail || 'خطأ'); }
  }));
}

async function loadMyRequests() {
  const list = await apiFetch('/requests');
  const el = document.getElementById('my-requests');
  if (!list.length) { el.innerHTML = '<p>لا توجد طلبات لديك.</p>'; return; }
  el.innerHTML = list.map(r => `<div class="card"><div><strong>${r.trainer.full_name}</strong> — الحالة: ${r.status}</div></div>`).join('');
}

init();
