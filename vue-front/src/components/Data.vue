<template>


<!--  <div class="markdown-container">-->
<!--    <div class="markdown-content" v-html="md.render(markdownContent)"></div>-->
<!--  </div>-->
  <div class="markdown-container">
    <div class="markdown-header" @click="toggleMarkdown">
      <h3>Documentation</h3>
      <span class="toggle-icon">{{ showMarkdown ? '−' : '+' }}</span>
    </div>
    <div v-if="showMarkdown" class="markdown-content" v-html="md.render(markdownContent)"></div>
  </div>


  <div class="svg-display-container">
    <div class="svg-display-wrapper">
      <div class="svg-display">
        <img src="../assets/data-map.png" alt="Database structure diagram"
             class="svg-image" :style="{ transform: `scale(${zoomLevel})` }">
      </div>
    </div>
    <div class="svg-controls">
      <button @click="zoomIn" class="zoom-button">+</button>
      <button @click="zoomOut" class="zoom-button">−</button>
      <button @click="resetZoom" class="zoom-button">Reset</button>
    </div>
  </div>


  <div class="db-data-container">
    <div v-for="(tableData, tableName) in ans" :key="tableName" class="table-section">
      <div class="table-header" @click="toggleTable(tableName)">
        <h3>{{ formatTableName(tableName) }}</h3>
        <span class="toggle-icon">{{ expandedTables[tableName] ? '−' : '+' }}</span>
      </div>

      <div v-if="expandedTables[tableName]" class="table-content">
        <table>
          <thead>
          <tr>
            <th v-for="column in tableData.columns" :key="column">{{ formatColumnName(column) }}</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(row, rowIndex) in tableData.data" :key="rowIndex">
            <td v-for="(cell, cellIndex) in row" :key="cellIndex">
              <div class="cell-content">{{ cell }}</div>
            </td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>




</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { requestPack } from "../utils/requests.js";

import MarkdownIt from 'markdown-it';

import docsContent from '../assets/data.md?raw';

// Initialize markdown parser
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
});

const markdownContent = ref(docsContent);
const showMarkdown = ref(true);
const toggleMarkdown = () => {
  showMarkdown.value = !showMarkdown.value;
};



interface TableData {
  columns: string[];
  data: any[][];
}

interface ApiResponse {
  ans: Record<string, TableData>;
  type: string;
  msg: string;
}

const ans = ref<Record<string, TableData>>({});
const expandedTables = ref<Record<string, boolean>>({});

const getDbData = async () => {
  try {
    let response = await requestPack.post<ApiResponse>("/api/db-slice/", {});
    ans.value = response.ans;

    // Initialize all tables as collapsed by default
    Object.keys(response.ans).forEach(tableName => {
      expandedTables.value[tableName] = false;
    });

  } catch (error) {
    console.error("Error fetching chat data:", error);
  }
};

const toggleTable = (tableName: string) => {
  expandedTables.value[tableName] = !expandedTables.value[tableName];
};

const formatTableName = (name: string) => {
  return name.split('_').map(word =>
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ');
};

const formatColumnName = (name: string) => {
  return name.split('_').map(word =>
      word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ');
};

getDbData();


const zoomLevel = ref(1);

const zoomIn = () => {
  zoomLevel.value = Math.min(zoomLevel.value + 0.1, 2);
};

const zoomOut = () => {
  zoomLevel.value = Math.max(zoomLevel.value - 0.1, 0.5);
};

const resetZoom = () => {
  zoomLevel.value = 1;
};

</script>

<style scoped>
.db-data-container {
  font-family: Arial, sans-serif;
  max-width: 100%;
  overflow-x: auto;
  margin: 0 16px; /* Added left and right margins */
}

.table-section {
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: #f5f5f5;
  cursor: pointer;
  transition: background-color 0.2s;
}

.table-header:hover {
  background-color: #e9e9e9;
}

.table-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.toggle-icon {
  font-weight: bold;
  font-size: 1.2rem;
}

.table-content {
  overflow-x: auto;
  margin: 0 8px; /* Added left and right margins for table content */
}

table {
  width: calc(100% - 16px); /* Adjusted width to account for margins */
  border-collapse: collapse;
  margin: 0 8px; /* Added left and right margins */
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
  max-width: 200px; /* Limit cell width */
}

.cell-content {
  display: -webkit-box;
  -webkit-line-clamp: 3; /* Limit to 3 lines */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4; /* Adjust line height for better readability */
  max-height: calc(1.4em * 3); /* Approximate height for 3 lines */
}

th {
  background-color: #f9f9f9;
  font-weight: 600;
}

tr:hover {
  background-color: #f5f5f5;
}

@media (max-width: 768px) {
  th, td {
    padding: 0.5rem;
    font-size: 0.9rem;
  }

  .db-data-container {
    margin: 0 8px; /* Smaller margins on mobile */
  }

  table {
    width: calc(100% - 8px); /* Adjusted width for mobile */
    margin: 0 4px;
  }
}

.svg-display-container {
  margin: 20px 16px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: relative;  /* 为控制按钮创建定位上下文 */
}

.svg-display-wrapper {
  overflow: auto;
  max-height: 80vh;
}

.svg-display {
  display: inline-block;
  min-width: 100%;
  text-align: center;
}

.svg-image {
  max-width: 100%;
  height: auto;
  transition: transform 0.2s ease;
  transform-origin: top left;
  border: 1px solid #e0e0e0;
  background-color: white;
  padding: 10px;
}

.svg-controls {
  position: absolute;  /* 使用绝对定位 */
  bottom: 20px;       /* 距离容器底部的距离 */
  right: 20px;        /* 距离容器右侧的距离 */
  display: flex;
  gap: 5px;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 5px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.zoom-button {
  background-color: #ffffff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 5px 10px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.zoom-button:hover {
  background-color: #f0f0f0;
}

@media (max-width: 768px) {
  .svg-display-container {
    margin: 10px 8px;
    padding: 10px;
  }

  .svg-controls {
    bottom: 5px;
    right: 5px;
  }
}


.info-image-container {
  margin: 20px 16px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.info-image {
  max-width: 100%;
  height: auto;
  border: 1px solid #e0e0e0;
  background-color: white;
  padding: 10px;
}

@media (max-width: 768px) {
  .info-image-container {
    margin: 10px 8px;
    padding: 10px;
  }
}

/* styles for the markdown section */
.markdown-container {
  margin: 20px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.markdown-content {
  padding: 20px;
  background-color: #f9f9f9;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  line-height: 1.6;
  color: #333;
}

.markdown-content >>> h1,
.markdown-content >>> h2,
.markdown-content >>> h3 {
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-content >>> p {
  margin-bottom: 1em;
}

.markdown-content >>> a {
  color: #0366d6;
  text-decoration: none;
}

.markdown-content >>> a:hover {
  text-decoration: underline;
}

.markdown-content >>> code {
  font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
  background-color: rgba(27, 31, 35, 0.05);
  border-radius: 3px;
  padding: 0.2em 0.4em;
  font-size: 85%;
}

.markdown-content >>> pre {
  background-color: #f6f8fa;
  border-radius: 3px;
  padding: 16px;
  overflow: auto;
  line-height: 1.45;
}

.markdown-content >>> blockquote {
  border-left: 4px solid #dfe2e5;
  color: #6a737d;
  padding: 0 1em;
  margin: 0 0 16px 0;
}

@media (max-width: 768px) {
  .markdown-container {
    margin: 10px 8px;
    padding: 10px;
  }
}

.markdown-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: #f5f5f5;
  cursor: pointer;
  transition: background-color 0.2s;
}

.markdown-header:hover {
  background-color: #e9e9e9;
}

.markdown-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

</style>