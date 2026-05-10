import axios from 'axios'
import { showFailToast } from 'vant'

function getPersistedToken() {
  try {
    const raw = localStorage.getItem('user')
    if (!raw) return ''
    const parsed = JSON.parse(raw)
    return parsed?.token || ''
  } catch (error) {
    return ''
  }
}

const request = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
})

request.interceptors.request.use(
  (config) => {
    const token = getPersistedToken()
    const hasAuthorization = Boolean(config?.headers?.Authorization)
    if (token && !hasAuthorization) {
      config.headers.Authorization = token.startsWith('Bearer ') ? token : `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

request.interceptors.response.use(
  (response) => {
    const res = response.data
    if (res?.code === 200) {
      return res.data
    }
    showFailToast(res?.message || '请求失败')
    return Promise.reject(new Error(res?.message || 'Request Error'))
  },
  (error) => {
    const message = error?.response?.data?.message || error.message || '网络异常'
    showFailToast(message)
    return Promise.reject(error)
  },
)

export default request
