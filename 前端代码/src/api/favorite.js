import request from '../utils/request'

export function checkFavorite(questionId) {
  return request.get('/api/favorite/check', {
    params: { question_id: questionId },
  })
}

export function addFavorite(questionId) {
  return request.post('/api/favorite/add', {
    questionId,
  })
}

export function cancelFavorite(questionId) {
  return request.delete(`/api/favorite/cancel/${questionId}`)
}

export function fetchFavoriteList(params) {
  return request.get('/api/favorite/list', { params })
}

export async function fetchAllFavorites(maxPages = 50) {
  const all = []
  let page = 1
  let hasMore = true
  while (hasMore && page <= maxPages) {
    const data = await fetchFavoriteList({ page, pageSize: 100 })
    const list = data?.list || []
    all.push(...list)
    hasMore = Boolean(data?.hasMore) && list.length > 0
    page += 1
    if (!list.length) hasMore = false
  }
  return all
}

export function clearAllFavorites() {
  return request.delete('/api/favorite/clear')
}
