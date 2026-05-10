import { defineStore } from 'pinia'
import { fetchChapterQuestionsAll } from '../api/practice'
import { normalizeQuestion } from '../utils/question'

export const usePracticeStore = defineStore('practice', {
  state: () => ({
    chapterId: null,
    questions: [],
    loading: false,
    error: null,
  }),
  getters: {
    total: (s) => s.questions.length,
  },
  actions: {
    async ensureChapter(chapterId) {
      const id = Number(chapterId)
      if (!id) return
      if (this.chapterId === id && this.questions.length) return

      this.loading = true
      this.error = null
      try {
        const rawList = await fetchChapterQuestionsAll(id)
        this.chapterId = id
        this.questions = rawList.map(normalizeQuestion).filter(Boolean)
      } catch (e) {
        this.error = e?.message || '加载失败'
        this.chapterId = id
        this.questions = []
      } finally {
        this.loading = false
      }
    },
    clear() {
      this.chapterId = null
      this.questions = []
      this.error = null
    },
  },
})
