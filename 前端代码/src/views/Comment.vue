<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast, showSuccessToast } from 'vant'
import { createForumPost, fetchForumHot } from '../api/forum'

const router = useRouter()

const loading = ref(true)
const hotList = ref([])

const showPost = ref(false)
const postTitle = ref('')
const postContent = ref('')
const submitting = ref(false)

async function loadHot() {
  loading.value = true
  try {
    const data = await fetchForumHot()
    const list = data?.list || []
    hotList.value = Array.isArray(list) ? list.slice(0, 10) : []
  } catch {
    showFailToast('热搜加载失败')
    hotList.value = []
  } finally {
    loading.value = false
  }
}

function goAll() {
  router.push('/comment/all')
}

function openPost() {
  postTitle.value = ''
  postContent.value = ''
  showPost.value = true
}

function closePost() {
  showPost.value = false
}

async function submitPost() {
  const title = postTitle.value.trim()
  const content = postContent.value.trim()
  if (!title) {
    showFailToast('请输入标题')
    return
  }
  if (!content) {
    showFailToast('请输入正文')
    return
  }
  submitting.value = true
  try {
    await createForumPost({ title, content })
    showSuccessToast('发表成功')
    showPost.value = false
    await loadHot()
  } catch {
    /* 拦截器 */
  } finally {
    submitting.value = false
  }
}

function goDetail(postId) {
  router.push(`/comment/post/${postId}`)
}

onMounted(() => {
  loadHot()
})
</script>

<template>
  <div class="forum-home">
    <div class="shell">
      <header class="top-row">
        <button type="button" class="btn-outline" @click="goAll">
          查看所有帖子
        </button>
        <button type="button" class="btn-primary" @click="openPost">
          发表
        </button>
      </header>

      <section class="hot-card">
        <div class="hot-title">热搜话题</div>

        <div v-if="loading" class="state-inline">
          <van-loading type="spinner" color="#1989fa" size="24px" />
        </div>

        <div v-else-if="!hotList.length" class="empty-tip">暂无热搜</div>

        <button
          v-for="(item, index) in hotList"
          :key="item.postId"
          type="button"
          class="hot-item"
          @click="goDetail(item.postId)"
        >
          <span class="hot-rank">{{ index + 1 }}</span>
          <span class="hot-text">{{ item.title }}</span>
        </button>
      </section>
    </div>

    <van-popup
      v-model:show="showPost"
      position="bottom"
      round
      :style="{ maxHeight: '85%' }"
      closeable
      close-icon-position="top-right"
    >
      <div class="post-dialog">
        <div class="dlg-title">发表帖子</div>
        <van-field v-model="postTitle" label="标题" placeholder="请输入标题" />
        <van-field
          v-model="postContent"
          type="textarea"
          rows="6"
          autosize
          label="正文"
          placeholder="写点什么..."
          class="dlg-area"
        />
        <div class="dlg-actions">
          <van-button round block plain hairline @click="closePost">取消</van-button>
          <van-button round block type="primary" :loading="submitting" @click="submitPost">
            发表
          </van-button>
        </div>
      </div>
    </van-popup>

    <van-tabbar route fixed active-color="#1989fa" inactive-color="#7d7e80">
      <van-tabbar-item replace to="/home">主页</van-tabbar-item>
      <van-tabbar-item replace to="/wrong">错题</van-tabbar-item>
      <van-tabbar-item replace to="/comment">评论</van-tabbar-item>
      <van-tabbar-item replace to="/mine">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<style scoped>
.forum-home {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  padding-bottom: 66px;
  box-sizing: border-box;
}

.shell {
  max-width: 420px;
  margin: 0 auto;
}

.top-row {
  display: flex;
  gap: 12px;
  margin-bottom: 14px;
}

.btn-outline {
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 12px 10px;
  font-size: 14px;
  font-weight: 600;
  color: #323233;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
}

.btn-outline:active {
  background: #f7f8fa;
}

.btn-primary {
  flex: 1;
  border: none;
  border-radius: 10px;
  padding: 12px 10px;
  font-size: 14px;
  font-weight: 600;
  color: #fff;
  background: #1989fa;
  box-shadow: 0 2px 10px rgba(25, 137, 250, 0.35);
}

.btn-primary:active {
  opacity: 0.92;
}

.hot-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 14px 12px 10px;
}

.hot-title {
  font-size: 16px;
  font-weight: 700;
  color: #323233;
  margin-bottom: 12px;
}

.state-inline {
  display: flex;
  justify-content: center;
  padding: 28px 0;
}

.empty-tip {
  text-align: center;
  padding: 28px 12px;
  color: #969799;
  font-size: 14px;
}

.hot-item {
  width: 100%;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 10px;
  margin-bottom: 8px;
  border: none;
  border-radius: 10px;
  background: #f7f8fa;
  text-align: left;
  transition: background 0.15s;
}

.hot-item:last-child {
  margin-bottom: 0;
}

.hot-item:active {
  background: #eef1f4;
}

.hot-rank {
  flex-shrink: 0;
  width: 22px;
  font-size: 14px;
  font-weight: 700;
  color: #1989fa;
}

.hot-text {
  flex: 1;
  font-size: 14px;
  color: #323233;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-dialog {
  padding: 16px 14px 20px;
  padding-top: 36px;
}

.dlg-title {
  font-size: 17px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 12px;
  color: #323233;
}

.dlg-area {
  margin-top: 8px;
}

.dlg-actions {
  display: flex;
  gap: 12px;
  margin-top: 18px;
}

.dlg-actions .van-button {
  flex: 1;
}
</style>
