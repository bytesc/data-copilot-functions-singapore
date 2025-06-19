<template>


  <div class="settings-container">
    <h2>OpenAI API Settings</h2>
    <form @submit.prevent="saveSettings" class="settings-form">
      <div class="form-group">
        <label for="apiUrl">API URL:</label>
        <input
            id="apiUrl"
            v-model="apiSettings.url"
            type="text"
            placeholder="https://api.openai.com/v1"
            class="form-input"
        />
      </div>

      <div class="form-group">
        <label for="modelName">Model Name:</label>
        <input
            id="modelName"
            v-model="apiSettings.model"
            type="text"
            placeholder="gpt-3.5-turbo"
            class="form-input"
        />
      </div>

      <div class="form-group">
        <label for="apiKey">API Key:</label>
        <input
            id="apiKey"
            v-model="apiSettings.key"
            type="password"
            placeholder="sk-...your-api-key..."
            class="form-input"
        />
      </div>

      <div class="form-actions">
        <button type="submit" class="save-button">Save Settings</button>
        <button type="button" @click="resetToDefaults" class="default-button">Reset to Defaults</button>
      </div>
    </form>

    <div v-if="message" class="message" :class="{ 'success': isSuccess, 'error': !isSuccess }">
      {{ message }}
    </div>
  </div>


</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { requestPack } from "../utils/requests.js";

import MarkdownIt from 'markdown-it';

interface ApiSettings {
  url: string;
  model: string;
  key: string;
}

const defaultSettings: ApiSettings = {
  url: 'https://api.openai.com/v1',
  model: 'gpt-4o',
  key: ''
};

const apiSettings = ref<ApiSettings>({
  ...defaultSettings
});

const message = ref<string>('');
const isSuccess = ref<boolean>(false);

// Load saved settings from localStorage if available
const loadSettings = () => {
  const savedSettings = localStorage.getItem('openai-settings');
  if (savedSettings) {
    try {
      apiSettings.value = JSON.parse(savedSettings);
    } catch (e) {
      console.error('Failed to parse saved settings', e);
    }
  }
};

// Save settings to localStorage
const saveSettings = () => {
  try {
    localStorage.setItem('openai-settings', JSON.stringify(apiSettings.value));
    showMessage('Settings saved successfully!', true);
  } catch (e) {
    console.error('Failed to save settings', e);
    showMessage('Failed to save settings', false);
  }
};

// Reset to default settings
const resetToDefaults = () => {
  apiSettings.value = { ...defaultSettings };
  showMessage('Reset to default settings', true);
};

// Show status message
const showMessage = (msg: string, success: boolean) => {
  message.value = msg;
  isSuccess.value = success;
  setTimeout(() => {
    message.value = '';
  }, 3000);
};

// Load settings when component mounts
loadSettings();

</script>

<style scoped>
.settings-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.save-button, .default-button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.save-button {
  background-color: #4CAF50;
  color: white;
}

.save-button:hover {
  background-color: #45a049;
}

.default-button {
  background-color: #f1f1f1;
  border: 1px solid #ddd;
}

.default-button:hover {
  background-color: #e1e1e1;
}

.message {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.success {
  background-color: #dff0d8;
  color: #3c763d;
}

.error {
  background-color: #f2dede;
  color: #a94442;
}

h2 {
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

</style>