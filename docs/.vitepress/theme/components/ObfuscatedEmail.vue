<script setup>
import { ref, onMounted } from 'vue'

// The address is stored reversed-then-base64-encoded so it never appears
// in the server-rendered HTML. It is decoded in the browser on mount, which
// defeats the regex-based scrapers that only read static markup.
// Encoding: reverse(base64(email)). Decoding: base64(reverse(blob)).
const blob = '=UWbu0GcAV2YhB3c05WZ0FGb'

const address = ref('')

onMounted(() => {
  try {
    address.value = atob(blob.split('').reverse().join(''))
  } catch {
    address.value = ''
  }
})
</script>

<template>
  <a v-if="address" :href="`mailto:${address}`">{{ address }}</a>
  <span v-else aria-hidden="true">[please enable JavaScript to view the email address]</span>
</template>
