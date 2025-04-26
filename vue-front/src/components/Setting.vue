<template>
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
              {{ cell }}
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
</script>

<style scoped>
.db-data-container {
  font-family: Arial, sans-serif;
  max-width: 100%;
  overflow-x: auto;
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
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid #e0e0e0;
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
}
</style>