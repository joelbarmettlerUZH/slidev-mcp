<script setup>
import DefaultTheme from 'vitepress/theme'
import { useData } from 'vitepress'

const { Layout } = DefaultTheme
const { frontmatter } = useData()
</script>

<template>
  <Layout>
    <template #home-hero-before>
      <slot name="home-hero-before" />
    </template>
  </Layout>
</template>

<style>
/* Hide default VitePress home hero and features when we use our custom page */
.VPHome .VPHero,
.VPHome .VPFeatures {
  display: none !important;
}
</style>
