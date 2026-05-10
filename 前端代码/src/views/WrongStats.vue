<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { showFailToast } from 'vant'
import { fetchChapterDistribution } from '../api/error'

const router = useRouter()

const loading = ref(true)
const rows = ref([])

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

const chart = computed(() => {
  const list = rows.value || []
  const counts = list.map((r) => Number(r.count) || 0)
  const maxRaw = counts.length ? Math.max(...counts) : 0
  const yMax = maxRaw > 0 ? niceCeil(maxRaw) : 10
  const n = list.length || 1
  const w = 320
  const h = 220
  const pad = { t: 16, r: 12, b: 52, l: 36 }
  const innerW = w - pad.l - pad.r
  const innerH = h - pad.t - pad.b

  const ticks = 5
  const yTicks = []
  for (let i = 0; i <= ticks; i += 1) {
    yTicks.push(Math.round((yMax * i) / ticks))
  }

  const points = list.map((row, i) => {
    const x = n <= 1 ? pad.l + innerW / 2 : pad.l + (innerW * i) / (n - 1)
    const v = Number(row.count) || 0
    const y = pad.t + innerH - (v / yMax) * innerH
    return { x, y, label: row.chapterName || `章节${i + 1}`, count: v }
  })

  const pointsStr = points.map((p) => `${p.x.toFixed(1)},${p.y.toFixed(1)}`).join(' ')

  return {
    w,
    h,
    pad,
    innerW,
    innerH,
    yMax,
    yTicks,
    yTicksDesc: [...yTicks].reverse(),
    points,
    pointsStr,
  }
})

async function load() {
  loading.value = true
  try {
    const data = await fetchChapterDistribution()
    const list = data?.list || []
    rows.value = Array.isArray(list) ? list : []
  } catch {
    showFailToast('统计数据加载失败')
    rows.value = []
  } finally {
    loading.value = false
  }
}

function goBack() {
  router.replace('/wrong')
}

onMounted(() => {
  load()
})
</script>

<template>
  <div class="stats-page">
    <div class="shell">
      <header class="top-bar">
        <button type="button" class="ghost-btn" @click="goBack">返回</button>
        <span class="page-title">错题统计</span>
        <span class="spacer" />
      </header>

      <div v-if="loading" class="state-card">
        <van-loading type="spinner" color="#1989fa" size="28px" />
        <span class="state-text">加载中...</span>
      </div>

      <section v-else class="chart-card">
        <div class="chart-head">章节错题分布</div>
        <div v-if="!rows.length" class="empty-tip">暂无分布数据</div>
        <div v-else class="chart-wrap">
          <svg
            class="chart-svg"
            :viewBox="`0 0 ${chart.w} ${chart.h}`"
            preserveAspectRatio="xMidYMid meet"
          >
            <!-- 横向网格 -->
            <line
              v-for="(tick, i) in chart.yTicks"
              :key="'h-' + i"
              :x1="chart.pad.l"
              :y1="chart.pad.t + chart.innerH - (tick / chart.yMax) * chart.innerH"
              :x2="chart.w - chart.pad.r"
              :y2="chart.pad.t + chart.innerH - (tick / chart.yMax) * chart.innerH"
              stroke="#ebedf0"
              stroke-width="1"
            />

            <!-- 折线（至少两点才绘制线段） -->
            <polyline
              v-if="chart.points.length >= 2"
              :points="chart.pointsStr"
              fill="none"
              stroke="#1989fa"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />

            <!-- 数据点 -->
            <circle
              v-for="(p, i) in chart.points"
              :key="'c-' + i"
              :cx="p.x"
              :cy="p.y"
              r="4"
              fill="#fff"
              stroke="#1989fa"
              stroke-width="2"
            />

            <!-- Y 轴刻度文字 -->
            <text
              v-for="(tick, i) in chart.yTicksDesc"
              :key="'yt-' + i"
              :x="chart.pad.l - 6"
              :y="chart.pad.t + chart.innerH - (tick / chart.yMax) * chart.innerH + 4"
              text-anchor="end"
              class="axis-text"
            >{{ tick }}</text>

            <!-- X 轴章节名 -->
            <text
              v-for="(p, i) in chart.points"
              :key="'xt-' + i"
              :x="p.x"
              :y="chart.h - 10"
              text-anchor="middle"
              class="axis-text axis-x"
            >{{ p.label }}</text>
          </svg>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.stats-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 16px;
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
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.ghost-btn:active {
  background: #f2f3f5;
}

.page-title {
  font-size: 17px;
  font-weight: 700;
  color: #323233;
}

.spacer {
  width: 64px;
}

.state-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 16px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.state-text {
  font-size: 14px;
  color: #969799;
}

.chart-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 14px 12px 16px;
}

.chart-head {
  font-size: 15px;
  font-weight: 600;
  color: #323233;
  margin-bottom: 12px;
}

.empty-tip {
  text-align: center;
  padding: 32px 12px;
  color: #969799;
  font-size: 14px;
}

.chart-wrap {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.chart-svg {
  display: block;
  width: 100%;
  min-height: 240px;
}

.axis-text {
  font-size: 9px;
  fill: #969799;
}

.axis-x {
  font-size: 8px;
}
</style>
