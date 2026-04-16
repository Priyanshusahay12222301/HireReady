const API_BASE_URL =
  window.location.hostname === "127.0.0.1" || window.location.hostname === "localhost"
    ? "http://127.0.0.1:5000/api"
    : "/api";

async function apiRequest(path, options = {}) {
  const isFormData = options.body instanceof FormData;
  const defaultHeaders = isFormData ? {} : { "Content-Type": "application/json" };

  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      ...defaultHeaders,
      ...(options.headers || {}),
    },
    ...options,
  });

  const payload = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(payload.error || "Request failed");
  }

  return payload;
}

window.HireReadyAPI = {
  register(body) {
    const isFormData = body instanceof FormData;
    return apiRequest("/auth/register", {
      method: "POST",
      body: isFormData ? body : JSON.stringify(body),
    });
  },

  login(body) {
    return apiRequest("/auth/login", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  health() {
    return apiRequest("/health");
  },

  listMockTests() {
    return apiRequest("/mock-tests");
  },

  getMockTest(testId) {
    return apiRequest(`/mock-tests/${testId}`);
  },

  submitMockTest(testId, body) {
    return apiRequest(`/mock-tests/${testId}/submit`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  listJobs() {
    return apiRequest("/jobs");
  },

  listApplications(userId) {
    const query = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
    return apiRequest(`/applications${query}`);
  },

  applyToJob(body) {
    return apiRequest("/applications", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  listInterviews(userId) {
    const query = userId ? `?user_id=${encodeURIComponent(userId)}` : "";
    return apiRequest(`/interviews${query}`);
  },

  createInterview(body) {
    return apiRequest("/interviews", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  updateInterview(interviewId, body) {
    return apiRequest(`/interviews/${interviewId}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
  },

  deleteInterview(interviewId) {
    return apiRequest(`/interviews/${interviewId}`, {
      method: "DELETE",
    });
  },

  getDashboard(userId) {
    return apiRequest(`/dashboard/${encodeURIComponent(userId)}`);
  },

  uploadResume(userId, formData) {
    return apiRequest(`/auth/users/${encodeURIComponent(userId)}/resume`, {
      method: "POST",
      body: formData,
    });
  },

  updateUserProfile(userId, body) {
    return apiRequest(`/auth/users/${encodeURIComponent(userId)}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
  },
};
