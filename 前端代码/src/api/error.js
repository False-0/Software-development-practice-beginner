import request from '../utils/request'

export function fetchErrorStatistics() {
  return request.get('/api/error/statistics')
}

export function fetchErrorList(params) {
  return request.get('/api/error/list', { params })
}

/** 拉取全部错题（分页循环） */
export async function fetchAllErrors(maxPages = 50) {
  const all = []
  let page = 1
  let hasMore = true
  while (hasMore && page <= maxPages) {
    const data = await fetchErrorList({ page, pageSize: 100 })
    const list = data?.list || []
    all.push(...list)
    hasMore = Boolean(data?.hasMore) && list.length > 0
    page += 1
    if (!list.length) hasMore = false
  }
  return all
}

export function deleteErrorByQuestionId(questionId) {
  return request.delete(`/api/error/delete/${questionId}`)
}

export function clearAllErrors() {
  return request.delete('/api/error/clear')
}

export function fetchChapterDistribution() {
  return request.get('/api/error/chapter-distribution')
}
