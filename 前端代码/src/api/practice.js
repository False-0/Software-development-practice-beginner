import request from '../utils/request'

/** 分页拉取章节下全部题目（多次请求直到无更多） */
export async function fetchChapterQuestionsAll(chapterId) {
  const all = []
  let page = 1
  let hasMore = true
  while (hasMore) {
    const data = await request.get('/api/question/list', {
      params: {
        chapterId,
        page,
        pageSize: 100,
      },
    })
    const list = data?.list || []
    all.push(...list)
    hasMore = Boolean(data?.hasMore) && list.length > 0
    page += 1
    if (page > 50) break
  }
  return all
}

export function fetchQuestionDetail(id) {
  return request.get('/api/question/detail', {
    params: { id },
  })
}

export function submitAnswer(questionId, answer) {
  return request.post('/api/question/submit', null, {
    params: {
      question_id: questionId,
      answer,
    },
  })
}
