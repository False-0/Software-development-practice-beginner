/** 统一列表 / 详情接口返回的题目字段 */
export function normalizeQuestion(raw) {
  if (!raw) return null
  const ans = raw.answer != null ? String(raw.answer).trim().toUpperCase() : ''
  return {
    id: raw.id,
    chapterId: raw.chapter_id ?? raw.chapterId ?? null,
    title: raw.title ?? '',
    optionA: raw.option_a ?? raw.optionA ?? '',
    optionB: raw.option_b ?? raw.optionB ?? '',
    optionC: raw.option_c ?? raw.optionC ?? '',
    optionD: raw.option_d ?? raw.optionD ?? '',
    answer: ans,
  }
}

export function optionLetter(index) {
  return ['A', 'B', 'C', 'D'][index] ?? ''
}
