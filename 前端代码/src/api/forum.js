import request from '../utils/request'

export function fetchForumList(params) {
  return request.get('/api/forum/list', { params })
}

export function fetchForumHot() {
  return request.get('/api/forum/hot')
}

export function createForumPost(data) {
  return request.post('/api/forum/create', data)
}

export function fetchForumDetail(postId) {
  return request.get(`/api/forum/detail/${postId}`)
}

export function deleteForumPost(postId) {
  return request.delete(`/api/forum/post/${postId}`)
}

export function postForumComment(data) {
  return request.post('/api/forum/comment', data)
}

export function deleteForumComment(commentId) {
  return request.delete(`/api/forum/comment/${commentId}`)
}
