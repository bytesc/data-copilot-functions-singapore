



<script lang="ts" setup>
import {Box, ChatDotRound, CloseBold, Coin, Files, House, Plus, Refrigerator, Tickets, Select} from "@element-plus/icons-vue";
import {ref} from "vue";
import {useRouter} from 'vue-router';

const router = useRouter();
const activeIndex = ref('1')

const handleSelect = (key: string) => {
  if (key === '1') {
    router.push('/');
  } else if (key === '2') {
    router.push('/data');
  } else if (key === '3') {
    router.push('/api');
  } else if (key === '4') {
    router.push('/functions');
  }
  else if (key === '5') {
    router.push('/system');
  }
  else if (key === '6') {
    router.push('/setting');
  }
}

// Set active index based on current route
import {onMounted} from 'vue';
import {useRoute} from 'vue-router';

const route = useRoute();

onMounted(() => {
  const pathToIndexMap: Record<string, string> = {
    '/': '1',
    '/data': '2',
    '/api': '3',
    '/functions': '4',
    '/system': '5',
    '/setting': '6'
  };

  activeIndex.value = pathToIndexMap[route.path] || '1';
});
</script>

<template>
  <el-header style="padding: 0">
    <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        :ellipsis="false"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
    >
      <el-menu-item index="1"><h1><strong>Data Copilot</strong></h1></el-menu-item>
      <el-menu-item index="2">Data</el-menu-item>
      <el-menu-item index="3">API</el-menu-item>
      <el-menu-item index="4">Functions</el-menu-item>
      <el-menu-item index="5">System</el-menu-item>
      <el-menu-item index="6">Setting</el-menu-item>
      <div class="flex-grow" />
    </el-menu>
  </el-header>

  <!--  <div>-->
  <!--    <a href="https://vitejs.dev" target="_blank">-->
  <!--      <img src="/vite.svg" class="logo" alt="Vite logo" />-->
  <!--    </a>-->
  <!--    <a href="https://vuejs.org/" target="_blank">-->
  <!--      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />-->
  <!--    </a>-->
  <!--  </div>-->
  <!--  <Home msg="Vite + Vue" />-->
  <!--  <router-link to="/">Home</router-link> |-->
  <!--  <router-link to="/setting">About</router-link>-->
  <router-view></router-view>
</template>

<style scoped>

/*.logo {*/
/*  height: 6em;*/
/*  padding: 1.5em;*/
/*  will-change: filter;*/
/*  transition: filter 300ms;*/
/*}*/
/*.logo:hover {*/
/*  filter: drop-shadow(0 0 2em #646cffaa);*/
/*}*/
/*.logo.vue:hover {*/
/*  filter: drop-shadow(0 0 2em #42b883aa);*/
/*}*/
</style>
