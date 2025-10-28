const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:3001'

export function apiClient(token) {
  const headers = {
    'Content-Type': 'application/json',
  }
  if (token) headers['Authorization'] = `Bearer ${token}`

  async function request(path, options = {}) {
    const res = await fetch(`${BASE_URL}${path}`, {
      ...options,
      headers: { ...headers, ...(options.headers || {}) },
    })
    if (!res.ok) {
      const msg = await res.text()
      throw new Error(msg || `HTTP ${res.status}`)
    }
    const contentType = res.headers.get('content-type') || ''
    if (contentType.includes('application/json')) {
      return res.json()
    }
    return res.text()
  }

  return {
    get: (path) => request(path),
    post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
    postForm: (path, formData) => fetch(`${BASE_URL}${path}`, { method: 'POST', body: formData }),
  }
}
