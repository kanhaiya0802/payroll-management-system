const API_BASE = "https://payroll-management-system-production-7089.up.railway.app";

function getToken() {
  return localStorage.getItem("token");
}

function getRole() {
  return localStorage.getItem("role");
}

function requireAuth(requiredRole = null) {
  const token = getToken();
  const role = getRole();

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  if (requiredRole && role !== requiredRole) {
    alert("Access denied ❌");
    window.location.href = "login.html";
  }
}

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  localStorage.removeItem("email");
  window.location.href = "login.html";
}

async function apiFetch(path, options = {}) {
  const token = getToken();

  const headers = options.headers || {};
  headers["Authorization"] = "Bearer " + token;

  // if body is JSON
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }

  const res = await fetch(API_BASE + path, {
    ...options,
    headers,
  });

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.detail || "Request failed");
  }

  return data;
}
