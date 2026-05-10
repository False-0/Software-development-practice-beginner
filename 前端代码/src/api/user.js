import request from '../utils/request'

export function loginApi(data) {
  return request({
    url: '/api/user/login',
    method: 'post',
    data,
  })
}

export function registerApi(data) {
  return request({
    url: '/api/user/register',
    method: 'post',
    data,
  })
}

export function fetchUserInfo() {
  return request.get('/api/user/info')
}

export function updateUser(data) {
  return request.put('/api/user/update', data)
}

export function updatePassword(data) {
  return request.put('/api/user/password', data)
}
