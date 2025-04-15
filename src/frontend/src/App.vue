<script setup>
import NotificationComponent from '@/components/NotificationComponent.vue';

import { auth } from '@/api/auth';
import { BackButton } from 'vue-tg'

import { onMounted, onUnmounted, ref, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';

import Layout from '@/Layout.vue';

auth();

import { useBackButton } from 'vue-tg';

const router = useRouter();
const route = useRoute();

const visitHistory = ref([]);
const isNavigatingBack = ref(false);

const showBackButton = computed(() => {
  return visitHistory.value.length > 1;
});

const getVisitHistory = () => {
  const historyStr = sessionStorage.getItem('visitHistory');
  return historyStr ? JSON.parse(historyStr) : [];
};

const saveVisitHistory = (history) => {
  sessionStorage.setItem('visitHistory', JSON.stringify(history));
};

const cleanUrl = (url) => {
  try {
    const urlObj = new URL(url, window.location.origin);
    urlObj.searchParams.delete('ref');
    
    if (urlObj.search === '?') {
      return urlObj.pathname;
    }
    
    return urlObj.pathname + urlObj.search;
  } catch (e) {
    return url;
  }
};

onMounted(() => {
  visitHistory.value = getVisitHistory();
  
  const currentPath = cleanUrl(route.fullPath);
  if (visitHistory.value.length === 0 || visitHistory.value[visitHistory.value.length - 1] !== currentPath) {
    visitHistory.value.push(currentPath);
    saveVisitHistory(visitHistory.value);
  }
  
  router.afterEach((to, from) => {
    if (isNavigatingBack.value) {
      isNavigatingBack.value = false;
      return;
    }
    
    const cleanedPath = cleanUrl(to.fullPath);
    
    const existingIndex = visitHistory.value.indexOf(cleanedPath);
    if (existingIndex !== -1 && existingIndex < visitHistory.value.length - 1) {
      visitHistory.value = visitHistory.value.slice(0, existingIndex + 1);
      saveVisitHistory(visitHistory.value);
    } else if (visitHistory.value.length === 0 || visitHistory.value[visitHistory.value.length - 1] !== cleanedPath) {
      visitHistory.value.push(cleanedPath);
      saveVisitHistory(visitHistory.value);
    }
  });
});

const handleBackClick = () => {
  const history = getVisitHistory();
  
  if (history.length > 1) {
    history.pop();
    const previousPage = history[history.length - 1];
    
    visitHistory.value = history;
    saveVisitHistory(history);
    
    isNavigatingBack.value = true;
    
    router.replace(previousPage);
  } else {
    router.push('/');
  }
};
</script>

<template>
  <Layout>
    <RouterView />
    <BackButton v-if="showBackButton" @click="handleBackClick"></BackButton>
  </Layout>
  <NotificationComponent />
</template>
