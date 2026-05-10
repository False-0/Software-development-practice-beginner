import request from '../utils/request'

export function fetchRankInfo() {
  return request.get('/api/rank/info')
}

export function fetchRankList() {
  return request.get('/api/rank/list')
}
