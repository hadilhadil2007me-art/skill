// Simple API client for SkillUp frontend.
// GitHub Pages can only serve static files, so API calls must go to the
// deployed FastAPI service when the frontend is opened from github.io.
const DEFAULT_REMOTE_API_BASE = 'https://skillup-web.onrender.com/api/v1';
const API_BASE = (
  window.SKILLUP_API_BASE ||
  (window.location.hostname.endsWith('github.io')
    ? DEFAULT_REMOTE_API_BASE
    : `${window.location.origin}/api/v1`)
).replace(/\/$/, '');

// Use cookie-based auth by default (server sets HttpOnly cookie on login).
async function apiFetch(path, options = {}) {
  const headers = options.headers || {};
  headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  const token = getToken();
  if (token && !headers.Authorization) {
    headers.Authorization = `Bearer ${token}`;
  }
  // Send credentials to include cookies for same-origin requests
  let res;
  try {
    res = await fetch(API_BASE + path, { ...options, headers, credentials: 'include' });
  } catch (error) {
    throw { detail: 'تعذر الاتصال بخادم المنصة. تأكد أن رابط API صحيح وأن الخادم يعمل.' };
  }
  if (!res.ok) {
    const text = await res.text();
    let json;
    try { json = JSON.parse(text); } catch(e) { json = { detail: text }; }
    throw json;
  }
  // Some endpoints return no content
  if (res.status === 204) return null;
  return res.json();
}

async function registerUser(user) {
  return apiFetch('/auth/register', { method: 'POST', body: JSON.stringify(user) });
}

async function loginUser(email, password) {
  // OAuth2 password form
  const form = new URLSearchParams();
  form.append('username', email);
  form.append('password', password);
  const res = await fetch(API_BASE + '/auth/login', {
    method: 'POST',
    body: form,
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    credentials: 'include',
  });
  if (!res.ok) {
    const j = await res.json().catch(() => ({ detail: 'Login failed' }));
    throw j;
  }
  const data = await res.json();
  if (data.access_token) {
    setToken(data.access_token);
  }
  // server sets HttpOnly cookie; return response body for compatibility
  return data;
}

async function getCurrentUser() {
  return apiFetch('/users/me');
}

function getToken() {
  // Check if HttpOnly cookie is set by checking if we can access user
  // Since we're using HttpOnly cookies, we can't directly access the token
  // Instead, check if user is authenticated by making a request
  return localStorage.getItem('auth_token') || null;
}

function setToken(token) {
  if (token) {
    localStorage.setItem('auth_token', token);
  } else {
    localStorage.removeItem('auth_token');
  }
}

function logout() {
  setToken(null);
  // Clear any other auth-related data
  localStorage.removeItem('user_data');
}

export { 
  apiFetch, 
  registerUser, 
  loginUser, 
  getCurrentUser,
  getToken,
  setToken,
  logout
};
