import { apiFetch, getCurrentUser, getToken, setToken } from './api.js';

const roleLabels = {
  admin: 'مدير',
  trainer: 'حرفي',
  trainee: 'متدرب',
};

const statusLabels = {
  approved: 'مقبول',
  pending: 'في الانتظار',
  rejected: 'مرفوض',
};

function byId(id) {
  return document.getElementById(id);
}

function escapeHtml(value = '') {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function setNav() {
  const navActions = byId('nav-actions');
  if (!getToken()) {
    navActions.innerHTML = `
      <a href="login.html" class="btn btn-ghost">تسجيل الدخول</a>
      <a href="register.html" class="btn btn-primary">إنشاء حساب</a>
    `;
    return;
  }
  navActions.innerHTML = '<button id="btn-logout" class="btn btn-ghost">تسجيل الخروج</button>';
  byId('btn-logout').addEventListener('click', () => {
    setToken(null);
    window.location.href = 'index.html';
  });
}

function showAuthMessage(message) {
  byId('auth-message').style.display = 'block';
  byId('auth-message').innerHTML = message;
  byId('dashboard-content').style.display = 'none';
}

function renderUser(user) {
  byId('page-title').textContent = `مرحبًا ${user.full_name}`;
  byId('page-subtitle').textContent = `حساب ${roleLabels[user.role] || user.role} على منصة مهنتي.`;
  byId('user-info').innerHTML = `
    <div class="profile-line"><span>الاسم</span><span>${escapeHtml(user.full_name)}</span></div>
    <div class="profile-line"><span>البريد</span><span>${escapeHtml(user.email)}</span></div>
    <div class="profile-line"><span>الهاتف</span><span>${escapeHtml(user.phone || '-')}</span></div>
    <div class="profile-line"><span>الولاية</span><span>${escapeHtml(user.wilaya || '-')}</span></div>
    <div class="profile-line"><span>المهنة</span><span>${escapeHtml(user.profession || '-')}</span></div>
    <div class="profile-line"><span>الدور</span><span>${roleLabels[user.role] || user.role}</span></div>
    <div class="profile-line">
      <span>الحالة</span>
      <span><span class="badge ${user.account_status}">${statusLabels[user.account_status] || user.account_status}</span></span>
    </div>
    <div class="profile-line">
      <span>التحقق</span>
      <span>${user.is_verified ? 'مؤكد' : 'غير مؤكد'}</span>
    </div>
  `;
}

function addTab(id, label, active = false) {
  const tabs = byId('tabs');
  const button = document.createElement('button');
  button.className = `tab-btn${active ? ' active' : ''}`;
  button.dataset.panel = id;
  button.textContent = label;
  tabs.appendChild(button);
  byId(id).classList.toggle('active', active);
  button.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach((tab) => tab.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach((panel) => panel.classList.remove('active'));
    button.classList.add('active');
    byId(id).classList.add('active');
  });
}

async function loadAdminPanel() {
  const el = byId('pending-users');
  el.innerHTML = '<p class="empty">جاري تحميل الحسابات...</p>';
  const users = await apiFetch('/users?account_status=pending');
  if (!users.length) {
    el.innerHTML = '<p class="empty">لا توجد حسابات في انتظار الموافقة.</p>';
    return;
  }
  el.innerHTML = users.map((user) => `
    <div class="item">
      <div class="item-head">
        <div>
          <div class="item-title">${escapeHtml(user.full_name)}</div>
          <div class="item-meta">
            ${escapeHtml(user.email)}<br />
            ${roleLabels[user.role] || user.role} - ${escapeHtml(user.wilaya || '-')} - ${escapeHtml(user.profession || '-')}
          </div>
        </div>
        <span class="badge pending">في الانتظار</span>
      </div>
      <div class="item-actions">
        <button class="btn btn-primary" data-user-id="${user.id}" data-status="approved">قبول</button>
        <button class="btn btn-ghost" data-user-id="${user.id}" data-status="rejected">رفض</button>
      </div>
    </div>
  `).join('');
  el.querySelectorAll('button[data-user-id]').forEach((button) => {
    button.addEventListener('click', async () => {
      button.disabled = true;
      await apiFetch(`/users/${button.dataset.userId}/approval`, {
        method: 'PATCH',
        body: JSON.stringify({ account_status: button.dataset.status }),
      });
      await loadAdminPanel();
    });
  });
}

async function loadSkills() {
  const skills = await apiFetch('/skills');
  const sel = byId('skill-select');
  sel.innerHTML = skills.map((skill) => `<option value="${skill.id}">${escapeHtml(skill.name)}</option>`).join('');
}

async function loadTrainerProfile() {
  const el = byId('trainer-profile');
  try {
    const profile = await apiFetch('/trainers/me');
    el.innerHTML = `
      <div class="notice" style="border-color:rgba(34,197,94,0.3);background:rgba(34,197,94,0.1);color:#166534;">
        ملفك ظاهر للمتدربين بعد اعتماد الحساب.
      </div>
      <div class="profile-line"><span>الولاية / المدينة</span><span>${escapeHtml(profile.city)}</span></div>
      <div class="profile-line"><span>المهارة</span><span>${escapeHtml(profile.skill?.name || '-')}</span></div>
      <div class="profile-line"><span>سنوات الخبرة</span><span>${profile.experience_years}</span></div>
      <div class="profile-line"><span>نبذة</span><span>${escapeHtml(profile.bio || '-')}</span></div>
    `;
    byId('trainer-city').value = profile.city || '';
    byId('trainer-exp').value = profile.experience_years || 0;
    byId('trainer-bio').value = profile.bio || '';
    if (profile.skill?.id) byId('skill-select').value = profile.skill.id;
  } catch (err) {
    el.innerHTML = '<div class="notice">لم تنشئ ملف الحرفي بعد. أكمل البيانات بالأسفل ليظهر ملفك بعد اعتماد الحساب.</div>';
  }
}

async function saveTrainerProfile(event) {
  event.preventDefault();
  const payload = {
    skill_id: Number(byId('skill-select').value),
    city: byId('trainer-city').value.trim() || 'غير محدد',
    experience_years: Number(byId('trainer-exp').value) || 0,
    bio: byId('trainer-bio').value.trim(),
  };
  try {
    await apiFetch('/trainers/me', { method: 'POST', body: JSON.stringify(payload) });
  } catch (err) {
    if (String(err.detail || '').includes('already exists')) {
      await apiFetch('/trainers/me', { method: 'PUT', body: JSON.stringify(payload) });
    } else {
      alert(err.detail || 'تعذر حفظ ملف الحرفي');
      return;
    }
  }
  await loadTrainerProfile();
}

async function loadRequests() {
  const list = await apiFetch('/requests');
  const el = byId('requests-list');
  if (!list.length) {
    el.innerHTML = '<p class="empty">لا توجد طلبات واردة.</p>';
    return;
  }
  el.innerHTML = list.map((request) => `
    <div class="item">
      <div class="item-head">
        <div>
          <div class="item-title">${escapeHtml(request.trainee.full_name)}</div>
          <div class="item-meta">${escapeHtml(request.message || '')}</div>
        </div>
        <span class="badge ${request.status === 'pending' ? 'pending' : 'approved'}">${escapeHtml(request.status)}</span>
      </div>
      ${request.status === 'pending' ? `
        <div class="item-actions">
          <button class="btn btn-primary" data-id="${request.id}" data-status="accepted">قبول</button>
          <button class="btn btn-ghost" data-id="${request.id}" data-status="rejected">رفض</button>
        </div>` : ''}
    </div>
  `).join('');
  el.querySelectorAll('button[data-id]').forEach((button) => {
    button.addEventListener('click', async () => {
      await apiFetch(`/requests/${button.dataset.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ status: button.dataset.status }),
      });
      await loadRequests();
    });
  });
}

async function loadTrainers(query = '') {
  const trainers = await apiFetch('/trainers');
  const text = query.trim().toLowerCase();
  const filtered = trainers.filter((trainer) => {
    const haystack = `${trainer.user.full_name} ${trainer.city || ''} ${trainer.skill?.name || ''}`.toLowerCase();
    return !text || haystack.includes(text);
  });
  const el = byId('trainers-list');
  if (!filtered.length) {
    el.innerHTML = '<p class="empty">لا توجد نتائج مطابقة.</p>';
    return;
  }
  el.innerHTML = filtered.map((trainer) => `
    <div class="item">
      <div class="item-head">
        <div>
          <div class="item-title">${escapeHtml(trainer.user.full_name)}</div>
          <div class="item-meta">${escapeHtml(trainer.skill?.name || '-')} - ${escapeHtml(trainer.city || '-')}</div>
        </div>
      </div>
      <div class="item-actions">
        <button class="btn btn-primary" data-id="${trainer.user.id}">إرسال طلب تدريب</button>
      </div>
    </div>
  `).join('');
  el.querySelectorAll('button[data-id]').forEach((button) => {
    button.addEventListener('click', async () => {
      const message = prompt('اكتب رسالة قصيرة للحرفي');
      if (!message) return;
      await apiFetch('/requests', {
        method: 'POST',
        body: JSON.stringify({ trainer_id: button.dataset.id, message }),
      });
      await loadMyRequests();
    });
  });
}

async function loadMyRequests() {
  const list = await apiFetch('/requests');
  const el = byId('my-requests');
  if (!list.length) {
    el.innerHTML = '<p class="empty">لا توجد طلبات لديك.</p>';
    return;
  }
  el.innerHTML = list.map((request) => `
    <div class="item">
      <div class="item-title">${escapeHtml(request.trainer.full_name)}</div>
      <div class="item-meta">الحالة: ${escapeHtml(request.status)}</div>
    </div>
  `).join('');
}

async function init() {
  setNav();
  if (!getToken()) {
    showAuthMessage('<p>لم يتم تسجيل الدخول. <a href="login.html">سجل الدخول</a> للوصول إلى لوحة التحكم.</p>');
    return;
  }

  let user;
  try {
    user = await getCurrentUser();
  } catch (err) {
    setToken(null);
    showAuthMessage(`<p>${escapeHtml(err.detail || 'انتهت الجلسة أو الحساب غير مفعل بعد.')} <a href="login.html">تسجيل الدخول</a></p>`);
    return;
  }

  byId('dashboard-content').style.display = 'grid';
  renderUser(user);

  let firstTab = true;
  if (user.role === 'admin') {
    addTab('admin-panel', 'موافقة الحسابات', firstTab);
    firstTab = false;
    await loadAdminPanel();
  }
  if (user.role === 'trainer') {
    addTab('trainer-panel', 'ملف الحرفي', firstTab);
    firstTab = false;
    await loadSkills();
    await loadTrainerProfile();
    await loadRequests();
    byId('trainer-form').addEventListener('submit', saveTrainerProfile);
  }
  if (user.role === 'trainee') {
    addTab('trainee-panel', 'فرص التدريب', firstTab);
    await loadTrainers();
    await loadMyRequests();
    byId('btn-search-trainers').addEventListener('click', () => loadTrainers(byId('search-trainer').value));
  }
}

init();
