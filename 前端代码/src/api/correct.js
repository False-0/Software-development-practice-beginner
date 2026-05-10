import request from '../utils/request'

export function fetchCorrectList(params) {
  return request.get('/api/correct/list', { params })
}

export async function fetchAllCorrectRecords(maxPages = 50) {
  const all = []
  let page = 1
  let hasMore = true
  while (hasMore && page <= maxPages) {
    const data = await fetchCorrectList({ page, pageSize: 100 })
    const list = data?.list || []
    all.push(...list)
    hasMore = Boolean(data?.hasMore) && list.length > 0
    page += 1
    if (!list.length) hasMore = false
  }
  return all
}

export function deleteCorrectRecord(questionId) {
  return request.delete(`/api/correct/delete/${questionId}`)
}

export function clearAllCorrectRecords() {
  return request.delete('/api/correct/clear')
}
