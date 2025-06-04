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



</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { requestPack } from "../utils/requests.js";

import MarkdownIt from 'markdown-it';

import docsContent from '../assets/functions.md?raw';

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




</script>

<style scoped>

.table-header h3 {
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.toggle-icon {
  font-weight: bold;
  font-size: 1.2rem;
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