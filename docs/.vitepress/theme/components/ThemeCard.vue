<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { ThemeInfo } from '../../themes'

const props = defineProps<{ theme: ThemeInfo }>()

const current = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  // Random initial delay so cards don't all rotate in sync
  const delay = Math.random() * 3000
  setTimeout(() => {
    timer = setInterval(() => {
      current.value = (current.value + 1) % props.theme.previews.length
    }, 3000)
  }, delay)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<template>
  <div class="theme-card">
    <div class="preview-container">
      <img
        v-for="(src, i) in theme.previews"
        :key="i"
        :src="src"
        :alt="`${theme.name} preview ${i + 1}`"
        :class="{ active: i === current }"
        loading="lazy"
      />
    </div>
    <div class="info">
      <div class="name-row">
        <strong>{{ theme.name }}</strong>
        <code class="theme-id">{{ theme.id }}</code>
      </div>
      <p class="description">{{ theme.description }}</p>
      <div class="tags" v-if="theme.tags?.length">
        <span v-for="tag in theme.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.theme-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  overflow: hidden;
  transition: box-shadow 0.2s;
}

.theme-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.preview-container {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 */
  background: var(--vp-c-bg-soft);
  overflow: hidden;
}

.preview-container img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transform: translateX(20%);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.preview-container img.active {
  opacity: 1;
  transform: translateX(0);
}

.info {
  padding: 12px 16px;
}

.name-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.theme-id {
  font-size: 0.75em;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--vp-c-bg-soft);
}

.description {
  font-size: 0.85em;
  color: var(--vp-c-text-2);
  margin: 0 0 8px;
  line-height: 1.4;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag {
  font-size: 0.7em;
  padding: 1px 6px;
  border-radius: 10px;
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}
</style>
