<template>
  <div class="flex items-center gap-2">
    <div class="w-4 h-4 border-2 border-current border-t-transparent rounded-full animate-spin"></div>
    <span v-if="text">{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  text?: string;
}>();
</script> 