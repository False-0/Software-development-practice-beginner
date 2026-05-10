<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { showConfirmDialog, showFailToast, showSuccessToast } from 'vant'
import {
  deleteForumComment,
  deleteForumPost,
  fetchForumDetail,
  postForumComment,
} from '../api/forum'
import { useUserStore } from '../store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const loading = ref(true)
const detail = ref(null)
const commentText = ref('')
const submitting = ref(false)

const showPostSheet = ref(false)
const showCommentSheet = ref(false)
const pendingComment = ref(null)

const postId = computed(() => Number(route.params.postId))

const currentUsername = computed(() => userStore.userInfo?.username || '')

/** 详情接口若返回作者字段 / userId 则用于判断是否本人帖子 */
const canDeletePost = computed(() => {
  const u = currentUsername.value
  const d = detail.value
  const meId = userStore.userInfo?.id
  if (!d) return false
  if (meId != null && d.authorUserId != null && d.authorUserId === meId) return true
  if (meId != null && d.userId != null && d.userId === meId) return true
  if (!u) return false
  const author =
    d.authorUsername ??
    d.username ??
    d.authorName ??
    d.ownerUsername ??
    ''
  return Boolean(author && author === u)
})

function canDeleteComment(c) {
  const u = currentUsername.value
  return u && c?.username === u
}

const sortedComments = computed(() => {
  const arr = detail.value?.comments || []
  return [...arr].sort(
    (a, b) =>
      new Date(b.createdAt || 0).getTime() -
      new Date(a.createdAt || 0).getTime(),
  )
})

async function loadDetail() {
  loading.value = true
  try {
    const data = await fetchForumDetail(postId.value)
    detail.value = data
  } catch {
    showFailToast('帖子加载失败')
    detail.value = null
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.back()
}

async function submitComment() {
  const text = commentText.value.trim()
  if (!text) {
    showFailToast('请输入评论')
    return
  }
  submitting.value = true
  try {
    await postForumComment({
      postId: postId.value,
      content: text,
    })
    commentText.value = ''
    showSuccessToast('评论成功')
    await loadDetail()
  } catch {
    /* */
  } finally {
    submitting.value = false
  }
}

async function confirmDeletePost() {
  if (!canDeletePost.value) return
  try {
    await showConfirmDialog({
      title: '删除帖子',
      message: '确定删除该帖子吗？',
    })
  } catch {
    return
  }
  try {
    await deleteForumPost(postId.value)
    showSuccessToast('已删除')
    router.replace('/comment')
  } catch {
    /* */
  }
}

async function confirmDeleteComment(commentId) {
  try {
    await showConfirmDialog({
      title: '删除评论',
      message: '确定删除该评论吗？',
    })
  } catch {
    return
  }
  try {
    await deleteForumComment(commentId)
    showSuccessToast('已删除')
    await loadDetail()
  } catch {
    await loadDetail()
  }
}

function openPostMenu(e) {
  if (!canDeletePost.value) return
  e?.preventDefault?.()
  showPostSheet.value = true
}

function onPostSheetSelect(action) {
  if (action.name === '删除') confirmDeletePost()
}

function openCommentMenu(c, e) {
  if (!canDeleteComment(c)) return
  e?.preventDefault?.()
  pendingComment.value = c
  showCommentSheet.value = true
}

function onCommentSheetSelect(action) {
  const c = pendingComment.value
  pendingComment.value = null
  if (action.name === '删除' && c) {
    confirmDeleteComment(c.commentId)
  }
}

/** 长按弹出删除选项（移动端） */
let pressTimer = null
function onPostPressStart() {
  clearTimeout(pressTimer)
  if (!canDeletePost.value) return
  pressTimer = window.setTimeout(() => {
    showPostSheet.value = true
  }, 650)
}

function onCommentPressStart(c) {
  clearTimeout(pressTimer)
  if (!canDeleteComment(c)) return
  pressTimer = window.setTimeout(() => {
    pendingComment.value = c
    showCommentSheet.value = true
  }, 650)
}

function onPressEnd() {
  clearTimeout(pressTimer)
}

onMounted(() => {
  loadDetail()
})
</script>

<template>
  <div class="detail-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <span class="title">帖子详情</span>
        <span class="spacer" />
      </header>

      <div v-if="loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" size="28px" />
      </div>

      <template v-else-if="detail">
        <section
          class="main-card"
          @contextmenu.prevent="openPostMenu"
          @touchstart.passive="onPostPressStart"
          @touchend="onPressEnd"
          @touchcancel="onPressEnd"
        >
          <div class="main-head">
            <h1 class="post-h1">{{ detail.title }}</h1>
            <button
              v-if="canDeletePost"
              type="button"
              class="icon-more"
              aria-label="更多"
              @click.stop="openPostMenu"
            >
              ⋯
            </button>
          </div>
          <div class="meta">
            <span>浏览 {{ detail.viewCount ?? 0 }}</span>
            <span v-if="detail.createdAt" class="dot">{{ detail.createdAt }}</span>
          </div>
          <div class="main-body">{{ detail.content }}</div>
        </section>

        <section class="cmt-head">评论</section>

        <div v-if="!sortedComments.length" class="empty-cmt">暂无评论</div>

        <div
          v-for="c in sortedComments"
          :key="c.commentId"
          class="cmt-card"
          @contextmenu.prevent="openCommentMenu(c, $event)"
          @touchstart.passive="() => onCommentPressStart(c)"
          @touchend="onPressEnd"
          @touchcancel="onPressEnd"
        >
          <div class="cmt-top">
            <span class="cmt-user">{{ c.username || '用户' }}</span>
            <button
              v-if="canDeleteComment(c)"
              type="button"
              class="icon-more sm"
              aria-label="更多"
              @click.stop="openCommentMenu(c, $event)"
            >
              ⋯
            </button>
          </div>
          <div class="cmt-body">{{ c.content }}</div>
          <div v-if="c.createdAt" class="cmt-time">{{ c.createdAt }}</div>
        </div>

        <section class="composer">
          <van-field
            v-model="commentText"
            type="textarea"
            rows="2"
            autosize
            maxlength="500"
            show-word-limit
            placeholder="发表你的看法"
            class="composer-field"
          />
          <van-button
            type="primary"
            block
            round
            class="send-btn"
            :loading="submitting"
            @click="submitComment"
          >
            发表评论
          </van-button>
        </section>
      </template>

      <div v-else class="empty-tip">帖子不存在</div>
    </div>

    <van-action-sheet
      v-model:show="showPostSheet"
      :actions="[{ name: '删除', color: '#ee0a24' }]"
      cancel-text="取消"
      @select="onPostSheetSelect"
    />

    <van-action-sheet
      v-model:show="showCommentSheet"
      :actions="[{ name: '删除', color: '#ee0a24' }]"
      cancel-text="取消"
      @select="onCommentSheetSelect"
      @closed="pendingComment = null"
    />
  </div>
</template>

<style scoped>
.detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  padding-bottom: 24px;
  box-sizing: border-box;
}

.shell {
  max-width: 420px;
  margin: 0 auto;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.ghost-btn {
  border: none;
  border-radius: 8px;
  background: #fff;
  color: #323233;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.title {
  font-size: 17px;
  font-weight: 700;
  color: #323233;
}

.spacer {
  width: 64px;
}

.state-card {
  display: flex;
  justify-content: center;
  padding: 48px;
  background: #fff;
  border-radius: 12px;
}

.main-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 14px 12px 16px;
}

.main-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.post-h1 {
  margin: 0;
  font-size: 17px;
  font-weight: 700;
  color: #323233;
  line-height: 1.45;
  flex: 1;
}

.icon-more {
  flex-shrink: 0;
  width: 36px;
  height: 32px;
  border: none;
  background: #f7f8fa;
  border-radius: 8px;
  font-size: 18px;
  line-height: 1;
  color: #646566;
}

.icon-more.sm {
  width: 30px;
  height: 26px;
  font-size: 16px;
}

.meta {
  margin-top: 8px;
  font-size: 12px;
  color: #969799;
}

.dot {
  margin-left: 10px;
}

.main-body {
  margin-top: 14px;
  font-size: 15px;
  color: #323233;
  line-height: 1.65;
  white-space: pre-wrap;
}

.cmt-head {
  margin: 16px 0 10px 4px;
  font-size: 15px;
  font-weight: 700;
  color: #646566;
}

.empty-cmt {
  padding: 20px;
  text-align: center;
  color: #969799;
  font-size: 14px;
}

.cmt-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  padding: 12px;
  margin-bottom: 10px;
}

.cmt-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.cmt-user {
  font-size: 14px;
  font-weight: 700;
  color: #1989fa;
}

.cmt-body {
  font-size: 14px;
  color: #323233;
  line-height: 1.5;
}

.cmt-time {
  margin-top: 8px;
  font-size: 11px;
  color: #c8c9cc;
}

.composer {
  margin-top: 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  padding: 12px;
}

.composer-field {
  padding: 8px 0;
  background: transparent;
}

.send-btn {
  margin-top: 10px;
}

.empty-tip {
  text-align: center;
  padding: 40px 16px;
  color: #969799;
}
</style>
