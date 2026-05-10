<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { fetchRankInfo, fetchRankList } from '../api/rank'

const router = useRouter()

const loading = ref(true)
const myRank = ref(0)
const correctRate = ref(0)
const top3 = ref([])

const rankList = ref([])

const CHART_PLOT_PX = 140

/** 将数值向上取为「整档」坐标上限，避免 Y 轴写死 */
function niceCeil(n) {
  if (n <= 0) return 10
  const exp = Math.floor(Math.log10(n))
  const base = 10 ** exp
  const m = n / base
  let f
  if (m <= 1) f = 1
  else if (m <= 2) f = 2
  else if (m <= 5) f = 5
  else f = 10
  return f * base
}

/** 根据真实刷题量生成 Y 轴刻度与上限 */
const chartScale = computed(() => {
  const list = top3.value || []
  const nums = list.map((u) => Number(u?.totalDone) || 0)
  const maxData = nums.length ? Math.max(...nums) : 0
  const yMax = maxData > 0 ? niceCeil(maxData) : 10
  const divisions = 5
  const ticks = []
  for (let i = 0; i <= divisions; i += 1) {
    ticks.push(Math.round((yMax * i) / divisions))
  }
  const uniq = [...new Set(ticks)].sort((a, b) => a - b)
  return { yMax, ticks: uniq, ticksDesc: [...uniq].reverse() }
})

/** 左 2 名、中 1 名、右 3 名，与 API 下标对应 */
const podiumSlots = computed(() => {
  const t = top3.value || []
  return [
    { place: '第二名', user: t[1] || null },
    { place: '第一名', user: t[0] || null },
    { place: '第三名', user: t[2] || null },
  ]
})

function barHeightPct(totalDone) {
  const yMax = chartScale.value.yMax
  if (!yMax) return 0
  const v = Number(totalDone) || 0
  return Math.min(100, Math.max(0, (v / yMax) * 100))
}

const rankText = computed(() => {
  const r = myRank.value
  if (r == null || r === 0) return '—'
  if (r >= 9999) return '未上榜'
  return `第 ${r} 名`
})

const correctRateText = computed(() => {
  const c = correctRate.value
  if (c == null || Number.isNaN(Number(c))) return '—'
  return `${Number(c).toFixed(2)}%`
})

function normalizeListPayload(data) {
  if (Array.isArray(data)) return data
  if (data && Array.isArray(data.list)) return data.list
  if (data && Array.isArray(data.records)) return data.records
  if (data && Array.isArray(data.items)) return data.items
  return []
}

function listItemRank(item, index) {
  if (item?.rank != null) return item.rank
  if (item?.order != null) return item.order
  return index + 1
}

function goBack() {
  router.replace('/home')
}

function gridLineTopPct(index) {
  const n = chartScale.value.ticksDesc.length
  if (n <= 1) return '0%'
  return `${(index / (n - 1)) * 100}%`
}

async function load() {
  loading.value = true
  try {
    const [info, listRaw] = await Promise.all([
      fetchRankInfo(),
      fetchRankList(),
    ])
    myRank.value = info?.myRank ?? 0
    correctRate.value = info?.correctRate ?? 0
    top3.value = Array.isArray(info?.top3) ? info.top3 : []
    rankList.value = normalizeListPayload(listRaw)
  } catch (e) {
    showFailToast('排行榜加载失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  load()
})
</script>

<template>
  <div class="rank-page">
    <div class="phone-shell">
      <header class="top-bar">
        <button type="button" class="back-btn" @click="goBack">返回</button>
        <span class="page-title">刷题排行榜</span>
        <span class="top-spacer" />
      </header>

      <div v-if="loading" class="loading-box">
        <van-loading type="spinner" color="#1989fa" size="28px" />
        <div class="loading-text">加载中...</div>
      </div>

      <template v-else>
        <section class="info-card">
          <div class="info-line">今日排行：{{ rankText }}</div>
          <div class="info-line">正确率：{{ correctRateText }}</div>
        </section>

        <section class="chart-card">
          <div class="chart-title">前三名刷题量</div>
          <div class="chart-body">
            <div
              class="y-axis"
              :style="{ height: CHART_PLOT_PX + 'px' }"
            >
              <span
                v-for="(t, i) in chartScale.ticksDesc"
                :key="`y-${i}-${t}`"
                class="y-num"
              >{{ t }}</span>
            </div>
            <div class="chart-plot">
              <div
                class="plot-stack"
                :style="{ height: CHART_PLOT_PX + 'px' }"
              >
                <div
                  v-for="(_, gi) in chartScale.ticksDesc"
                  :key="`grid-${gi}`"
                  class="h-grid"
                  :style="{ top: gridLineTopPct(gi) }"
                />
                <div class="bar-row">
                  <div
                    v-for="(slot, idx) in podiumSlots"
                    :key="`bar-${idx}`"
                    class="bar-col"
                  >
                    <div
                      class="bar-track"
                      :style="{ height: CHART_PLOT_PX + 'px' }"
                    >
                      <div
                        class="bar-fill"
                        :style="{ height: barHeightPct(slot.user?.totalDone) + '%' }"
                      />
                    </div>
                  </div>
                </div>
              </div>
              <div class="podium-labels">
                <div
                  v-for="(slot, idx) in podiumSlots"
                  :key="`pod-${idx}`"
                  class="bar-col bar-col--footer"
                >
                  <div class="place-label">{{ slot.place }}</div>
                  <div class="name-clip" :title="slot.user?.username || '—'">
                    {{ slot.user?.username || '—' }}
                  </div>
                  <div class="count-text">
                    {{ slot.user != null ? slot.user.totalDone : 0 }} 题
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="list-section">
          <div class="list-header">完整排名</div>
          <div v-if="!rankList.length" class="list-empty">暂无排名数据</div>
          <div v-else class="list-card">
            <div
              v-for="(item, index) in rankList"
              :key="item.id || item.username + index"
              class="list-item"
            >
              <div class="rank-no">{{ listItemRank(item, index) }}</div>
              <div class="list-mid">
                <div class="username">{{ item.username || '—' }}</div>
                <div class="sub">刷题量</div>
              </div>
              <div class="total">{{ item.totalDone ?? 0 }}</div>
            </div>
          </div>
        </section>
      </template>
    </div>
  </div>
</template>

<style scoped>
.rank-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
  padding-bottom: 24px;
  box-sizing: border-box;
}

.phone-shell {
  max-width: 420px;
  margin: 0 auto;
}

.top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.back-btn {
  border: none;
  border-radius: 8px;
  background: #fff;
  color: #323233;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: background-color 0.2s, transform 0.1s;
}

.back-btn:active {
  background: #f2f3f5;
  transform: scale(0.98);
}

.page-title {
  font-size: 17px;
  font-weight: 700;
  color: #323233;
}

.top-spacer {
  width: 64px;
}

.loading-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 0;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.loading-text {
  margin-top: 10px;
  font-size: 14px;
  color: #969799;
}

.info-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 18px 16px;
  text-align: center;
  margin-bottom: 12px;
}

.info-line {
  font-size: 15px;
  color: #333;
  line-height: 1.6;
  font-weight: 600;
}

.info-line + .info-line {
  margin-top: 6px;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 14px 12px 16px;
  margin-bottom: 12px;
}

.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: #323233;
  margin-bottom: 10px;
  padding-left: 2px;
}

.chart-body {
  display: flex;
  gap: 8px;
  align-items: flex-start;
}

.y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-shrink: 0;
  width: 32px;
}

.y-num {
  font-size: 11px;
  color: #969799;
  line-height: 1;
  text-align: right;
  width: 100%;
}

.chart-plot {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.plot-stack {
  position: relative;
  width: 100%;
}

.h-grid {
  position: absolute;
  left: 0;
  right: 0;
  height: 1px;
  background: #ebedf0;
  pointer-events: none;
  z-index: 0;
}

.bar-row {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 0;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 8px;
  z-index: 1;
}

.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 0;
}

.podium-labels {
  display: flex;
  justify-content: space-between;
  gap: 8px;
  padding-top: 2px;
}

.bar-col--footer {
  flex: 1;
  min-width: 0;
  align-items: center;
}

.bar-track {
  width: 100%;
  max-width: 56px;
  margin: 0 auto;
  background: #f7f8fa;
  border-radius: 8px 8px 4px 4px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  overflow: hidden;
}

.bar-fill {
  width: 100%;
  background: linear-gradient(180deg, #5cadff 0%, #1989fa 100%);
  border-radius: 6px 6px 2px 2px;
  min-height: 0;
  transition: height 0.35s ease;
}

.place-label {
  margin-top: 8px;
  font-size: 12px;
  color: #646566;
  font-weight: 600;
}

.name-clip {
  margin-top: 4px;
  font-size: 12px;
  color: #323233;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  text-align: center;
}

.count-text {
  margin-top: 2px;
  font-size: 11px;
  color: #969799;
}

.list-section {
  margin-top: 4px;
}

.list-header {
  font-size: 14px;
  font-weight: 600;
  color: #646566;
  margin: 0 0 8px 4px;
}

.list-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.list-item {
  display: flex;
  align-items: center;
  padding: 14px 14px;
  border-bottom: 1px solid #f0f1f3;
  transition: background-color 0.2s;
}

.list-item:last-child {
  border-bottom: none;
}

.list-item:active {
  background: #f7f8fa;
}

.rank-no {
  width: 36px;
  font-size: 16px;
  font-weight: 700;
  color: #1989fa;
  flex-shrink: 0;
}

.list-mid {
  flex: 1;
  min-width: 0;
  padding: 0 8px;
}

.username {
  font-size: 15px;
  font-weight: 600;
  color: #323233;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.sub {
  font-size: 12px;
  color: #969799;
  margin-top: 2px;
}

.total {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  flex-shrink: 0;
}

.list-empty {
  text-align: center;
  padding: 24px;
  color: #969799;
  font-size: 14px;
  background: #fff;
  border-radius: 12px;
  border: 1px solid #f0f1f3;
}
</style>
