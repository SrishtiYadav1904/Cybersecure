const API_BASE = '/api';

export function getAuthToken() {
  return localStorage.getItem('cyberguard_token');
}

export function setAuthToken(token) {
  if (token) {
    localStorage.setItem('cyberguard_token', token);
  } else {
    localStorage.removeItem('cyberguard_token');
  }
}

export function getStoredUser() {
  if (!getAuthToken()) {
    return null;
  }
  const u = localStorage.getItem('cyberguard_user');
  return u ? JSON.parse(u) : null;
}

export function setStoredUser(user) {
  if (user) {
    localStorage.setItem('cyberguard_user', JSON.stringify(user));
  } else {
    localStorage.removeItem('cyberguard_user');
  }
}

async function request(endpoint, options = {}) {
  const token = getAuthToken();
  const headers = {
    ...(options.headers || {})
  };

  if (token && !headers['Authorization']) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Handle JSON vs FormData
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers
  });

  if (response.status === 401) {
    // Expired or unauthorized
    setAuthToken(null);
    setStoredUser(null);
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Request failed with status ${response.status}`);
  }

  // Handle binary/blob (e.g. PDF download)
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/pdf')) {
    return response.blob();
  }

  return response.json();
}

export const api = {
  // Auth
  register: (data) => request('/auth/register', { method: 'POST', body: JSON.stringify(data) }),
  login: (data) => request('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  getMe: () => request('/auth/me'),

  // Analysis
  analyzeText: (data) => request('/analyze/text', { method: 'POST', body: JSON.stringify(data) }),
  uploadImageOCR: (formData) => request('/analyze/image', { method: 'POST', body: formData }),
  confirmImageAnalysis: (formData) => request('/analyze/confirm-image', { method: 'POST', body: formData }),
  analyzeChat: (data) => request('/analyze/chat', { method: 'POST', body: JSON.stringify(data) }),

  // Incidents
  listIncidents: () => request('/incidents'),
  createIncident: (data) => request('/incidents', { method: 'POST', body: JSON.stringify(data) }),
  getIncident: (id) => request(`/incidents/${id}`),
  closeIncident: (id) => request(`/incidents/${id}/close`, { method: 'POST' }),

  // Reports
  listReports: () => request('/reports'),
  generateReport: (incidentId) => request(`/reports/generate/${incidentId}`, { method: 'POST' }),
  downloadReport: (reportId) => request(`/reports/${reportId}/download`),

  // Support
  startSupportSession: (incidentId) => request('/support/start', { method: 'POST', body: JSON.stringify({ incident_id: incidentId }) }),
  sendSupportMessage: (data) => request('/support/message', { method: 'POST', body: JSON.stringify(data) }),
  getSupportHistory: () => request('/support/history'),
  getEmergencyResources: () => request('/support/resources'),

  // Help Requests
  submitHelpRequest: (data) => request('/help-request', { method: 'POST', body: JSON.stringify(data) }),
  getEscalatedCases: () => request('/help-request/cases'),

  // Admin
  getAdminDashboard: () => request('/admin/dashboard'),
  getAdminModels: () => request('/admin/models'),
  promoteModel: (versionTag) => request(`/admin/models/${versionTag}/promote`, { method: 'POST' }),
  getAdminDrift: () => request('/admin/drift'),
  getAdminSlang: () => request('/admin/slang'),
  approveSlang: (id, meaning) => request(`/admin/slang/${id}/approve?meaning=${encodeURIComponent(meaning || '')}`, { method: 'POST' })
};
