// Simple API client for SkillUp frontend
const API_BASE = (window.location.origin) + '/api/v1';

// Use cookie-based auth by default (server sets HttpOnly cookie on login).
async function apiFetch(path, options = {}) {
  const headers = options.headers || {};
  headers['Content-Type'] = headers['Content-Type'] || 'application/json';
  // Send credentials to include cookies for same-origin requests
  const res = await fetch(API_BASE + path, { ...options, headers, credentials: 'include' });
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
  // server sets HttpOnly cookie; return response body for compatibility
  return data;
}

async function getCurrentUser() {
  return apiFetch('/users/me');
}

export { apiFetch, registerUser, loginUser, getCurrentUser };
