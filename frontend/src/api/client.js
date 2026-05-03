import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL ?? '/' })

export async function uploadFile(file, onProgress) {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: (e) => onProgress && onProgress(e),
  })
  return data // { job_id, step, message }
}

export async function pollStatus(jobId) {
  const { data } = await api.get(`/status/${jobId}`)
  return data // { job_id, step, message }
}

export function downloadUrl(jobId) {
  return `${import.meta.env.VITE_API_URL ?? ''}/download/${jobId}`
}
