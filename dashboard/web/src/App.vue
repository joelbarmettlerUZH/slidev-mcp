<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from "vue";
import DailyChart from "./components/DailyChart.vue";
import ThemeChart from "./components/ThemeChart.vue";
import type { Overview } from "./types";

const RANGES = [7, 30, 90] as const;
const days = ref<(typeof RANGES)[number]>(30);
const data = ref<Overview | null>(null);
const error = ref<string | null>(null);
const loading = ref(false);
let timer: number | undefined;

async function load() {
  loading.value = true;
  try {
    const res = await fetch(`/api/overview?days=${days.value}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    data.value = (await res.json()) as Overview;
    error.value = null;
  } catch (e) {
    error.value = e instanceof Error ? e.message : String(e);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  load();
  timer = window.setInterval(load, 60_000);
});
onBeforeUnmount(() => window.clearInterval(timer));
watch(days, load);

const nf = new Intl.NumberFormat("en-US");
const fmt = (n: number | null) => (n === null ? "-" : nf.format(n));
const pct = (r: number) => `${(r * 100).toFixed(1)}%`;

const maxTool = computed(() => Math.max(1, ...(data.value?.tools.map((t) => t.count) ?? [1])));
const maxClient = computed(() => Math.max(1, ...(data.value?.clients.map((c) => c.count) ?? [1])));
const avgPerDay = computed(() =>
  data.value ? Math.round(data.value.totals.events / data.value.days) : 0,
);
</script>

<template>
  <header class="head">
    <div>
      <h1>Slidev MCP usage</h1>
      <p class="sub" v-if="data?.totals.lastEvent">
        Last event {{ new Date(data.totals.lastEvent).toLocaleString() }}
      </p>
    </div>
    <div class="range" role="group" aria-label="Time range">
      <button v-for="r in RANGES" :key="r" :class="{ on: r === days }" @click="days = r">
        {{ r }} days
      </button>
    </div>
  </header>

  <p v-if="error" class="banner">Could not load data: {{ error }}</p>
  <p v-else-if="!data" class="muted">Loading...</p>

  <template v-else>
    <section class="tiles">
      <div class="tile">
        <span class="label">Requests</span>
        <strong>{{ fmt(data.totals.events) }}</strong>
        <span class="muted">{{ fmt(avgPerDay) }} per day</span>
      </div>
      <div class="tile">
        <span class="label">Tool calls</span>
        <strong>{{ fmt(data.totals.toolCalls) }}</strong>
        <span class="muted">{{ fmt(data.totals.resourceReads) }} resource reads</span>
      </div>
      <div class="tile">
        <span class="label">Render latency p50 / p95</span>
        <strong>{{ fmt(data.totals.p50Ms) }} / {{ fmt(data.totals.p95Ms) }} ms</strong>
        <span class="muted">render_slides, measured calls only</span>
      </div>
      <div class="tile">
        <span class="label">Errors</span>
        <strong :class="{ bad: data.totals.errors > 0 }">{{ fmt(data.totals.errors) }}</strong>
        <span class="muted">{{ pct(data.totals.errorRate) }} of requests</span>
      </div>
    </section>

    <section class="card">
      <h2>Requests per day</h2>
      <DailyChart :daily="data.daily" />
    </section>

    <div class="cols">
      <section class="card">
        <h2>Tools</h2>
        <table>
          <thead>
            <tr><th>Tool</th><th class="r">Calls</th><th class="r">p50</th><th class="r">p95</th><th class="r">Err</th></tr>
          </thead>
          <tbody>
            <tr v-for="t in data.tools" :key="t.name">
              <td>
                <div class="name">{{ t.name }}</div>
                <div class="track"><div class="fill" :style="{ width: (t.count / maxTool) * 100 + '%' }"></div></div>
              </td>
              <td class="r">{{ fmt(t.count) }}</td>
              <td class="r">{{ fmt(t.p50Ms) }}</td>
              <td class="r">{{ fmt(t.p95Ms) }}</td>
              <td class="r" :class="{ bad: t.errors > 0 }">{{ t.errors }}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section class="card">
        <h2>Themes rendered</h2>
        <p v-if="!data.themes.length" class="muted">No theme usage recorded.</p>
        <ThemeChart v-else :themes="data.themes" />
      </section>
    </div>

    <div class="cols">
      <section class="card">
        <h2>Clients</h2>
        <ul class="bars">
          <li v-for="c in data.clients" :key="c.client">
            <span class="name">{{ c.client }}</span>
            <span class="track"><span class="fill" :style="{ width: (c.count / maxClient) * 100 + '%' }"></span></span>
            <span class="n">{{ fmt(c.count) }}</span>
          </li>
        </ul>
      </section>

      <section class="card">
        <h2>Most read resources</h2>
        <p v-if="!data.resources.length" class="muted">No resource reads recorded.</p>
        <ol class="queries">
          <li v-for="r in data.resources" :key="r.name">
            <span class="q">{{ r.name }}</span><span class="n">{{ fmt(r.count) }}</span>
          </li>
        </ol>
      </section>
    </div>

    <div class="cols">
      <section class="card">
        <h2>Error codes</h2>
        <p v-if="!data.errorCodes.length" class="muted">No errors in this range.</p>
        <ol class="queries">
          <li v-for="e in data.errorCodes" :key="e.error">
            <span class="q bad">{{ e.error }}</span><span class="n">{{ fmt(e.count) }}</span>
          </li>
        </ol>
      </section>

      <section class="card">
        <h2>Recent errors</h2>
        <p v-if="!data.recentErrors.length" class="muted">No errors in this range.</p>
        <ul class="errors">
          <li v-for="(e, i) in data.recentErrors" :key="i">
            <span class="muted">{{ new Date(e.timestamp).toLocaleString() }}</span>
            <strong>{{ e.name }}</strong><span v-if="e.theme"> ({{ e.theme }})</span>
            <div class="bad">{{ e.error }}</div>
          </li>
        </ul>
      </section>
    </div>
  </template>
</template>

<style scoped>
.head { display: flex; justify-content: space-between; align-items: flex-end; gap: 12px; flex-wrap: wrap; margin-bottom: 16px; }
h1 { margin: 0; font-size: 22px; }
h2 { margin: 0 0 12px; font-size: 14px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
.sub, .muted { color: var(--muted); font-size: 13px; margin: 2px 0 0; }
.range button { background: var(--card); color: var(--text); border: 1px solid var(--line); padding: 6px 12px; cursor: pointer; font: inherit; }
.range button:first-child { border-radius: 8px 0 0 8px; }
.range button:last-child { border-radius: 0 8px 8px 0; }
.range button + button { border-left: 0; }
.range button.on { background: var(--tool); border-color: var(--tool); color: #fff; }
.banner { background: color-mix(in srgb, var(--err) 12%, var(--card)); border: 1px solid var(--err); padding: 10px 14px; border-radius: 8px; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 12px; margin-bottom: 12px; }
.tile, .card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 16px; }
.tile { display: flex; flex-direction: column; gap: 2px; }
.tile strong { font-size: 26px; font-variant-numeric: tabular-nums; }
.label { color: var(--muted); font-size: 13px; }
.card { margin-bottom: 12px; }
.cols { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 12px; }
table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
th { text-align: left; color: var(--muted); font-weight: 500; font-size: 12px; padding-bottom: 6px; }
td { padding: 6px 0; border-top: 1px solid var(--line); }
.r { text-align: right; padding-left: 10px; }
.track { background: var(--line); border-radius: 4px; height: 6px; overflow: hidden; }
td .track { margin-top: 4px; }
.fill { display: block; height: 100%; background: var(--bar); border-radius: 4px; }
.bars, .queries, .errors { list-style: none; margin: 0; padding: 0; }
.bars li { display: grid; grid-template-columns: 110px 1fr 56px; gap: 10px; align-items: center; padding: 4px 0; }
.n { text-align: right; font-variant-numeric: tabular-nums; color: var(--muted); }
.queries li { display: flex; justify-content: space-between; gap: 12px; padding: 6px 0; border-top: 1px solid var(--line); }
.queries li:first-child { border-top: 0; }
.q { overflow-wrap: anywhere; }
.errors li { padding: 8px 0; border-top: 1px solid var(--line); font-size: 13px; }
.errors li:first-child { border-top: 0; }
.errors strong { margin-left: 8px; }
.bad { color: var(--err); }
</style>
