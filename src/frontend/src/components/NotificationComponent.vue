<template>
  <Transition name="fade">
    <div 
      v-if="viewStore.notification.show" 
      class="fixed top-4 left-1/2 transform -translate-x-1/2 z-50 w-full max-w-md p-4 rounded-lg shadow-lg mx-auto"
      :class="{
        'bg-green-600': viewStore.notification.type === 'success',
        'bg-red-600': viewStore.notification.type === 'error',
        'bg-blue-600': viewStore.notification.type === 'info'
      }"
    >
      <div class="flex items-center">
        <div class="flex-shrink-0">
          <svg v-if="viewStore.notification.type === 'success'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          
          <svg v-if="viewStore.notification.type === 'error'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          
          <svg v-if="viewStore.notification.type === 'info'" class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        
        <div class="ml-3 flex-grow">
          <p class="text-sm font-medium text-white">
            {{ viewStore.notification.message }}
          </p>
        </div>
        
        <div class="ml-auto pl-3 flex items-center">
          <button
            class="inline-flex text-white focus:outline-none"
            @click="viewStore.hideNotification()"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { useViewStore } from '@/services/stores.js';

const viewStore = useViewStore();
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s, transform 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style> 