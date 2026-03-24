<script setup lang="ts">
import { computed } from 'vue'
import ThemeCard from './ThemeCard.vue'
import { official, community } from '../../themes'
import type { ThemeInfo } from '../../themes'

const props = defineProps<{ collection: 'official' | 'community' }>()

const themes = computed<ThemeInfo[]>(() =>
  props.collection === 'official' ? official : community
)
</script>

<template>
  <div class="theme-gallery">
    <ThemeCard v-for="theme in themes" :key="theme.id" :theme="theme" />
  </div>
</template>

<style scoped>
.theme-gallery {
  display: grid;
  grid-template-columns: repeat(1, 1fr);
  gap: 20px;
  margin: 16px 0;
}

@media (min-width: 640px) {
  .theme-gallery {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 960px) {
  .theme-gallery {
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
