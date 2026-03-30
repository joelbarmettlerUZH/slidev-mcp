<script setup>
</script>

<template>
  <div class="demo-section">
    <div class="demo-container">
      <video
        autoplay
        loop
        muted
        playsinline
        class="demo-video"
      >
        <source src="/demo-fast.mp4" type="video/mp4" />
      </video>
    </div>
  </div>
</template>

<style scoped>
.demo-section {
  max-width: 960px;
  margin: 0 auto;
  padding: 0 24px 48px;
}

.demo-container {
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

:root.dark .demo-container {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.demo-video {
  width: 100%;
  display: block;
}
</style>
