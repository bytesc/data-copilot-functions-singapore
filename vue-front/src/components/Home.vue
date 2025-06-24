<script lang="ts" setup>
import { ref,reactive,computed, nextTick} from 'vue'
import {Box, ChatDotRound, CloseBold, Coin, Files, House, Plus, Refrigerator, Tickets, Select} from "@element-plus/icons-vue";
import MarkdownIt from 'markdown-it';

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true
});

import {requestPack} from "../utils/requests.js";

defineProps({
  msg: String,
})



const Question = reactive({
  content: '',
})

const Cot = reactive({
  content: '',
})

const LastAns = reactive({
  content: '',
})

// 聊天记录细节
const chatLogs = ref([]);

// 聊天记录
const chat= ref([]);

const scrollToBottom = () => {
  nextTick(() => {
    const container = document.querySelector('.chat-container')
    if (container) {
      container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth'
      })
    }

    const logContainer = document.querySelector('.chat-log-container')
    if (logContainer) {
      logContainer.scrollTo({
        top: logContainer.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}

// 获取聊天数据的方法
// const getChatDataFromAgent = async () => {
//   try {
//     const response = await requestPack.post("/api/ask-agent/", {
//       question: Question.content
//     });
//     if (response.type === "success") {
//       chatLogs.value.push({
//         role: 'user',
//         content: Question.content
//       });
//       chatLogs.value.push({
//         role: 'agent',
//         content: response.ans,
//         isMarkdown: true
//       });
//
//     } else {
//       chatLogs.value.push({
//         role: 'user',
//         content: Question.content
//       });
//       chatLogs.value.push({
//         role: 'agent',
//         content: response.ans,
//         isMarkdown: true
//       });
//
//       console.error(response.msg);
//     }
//   } catch (error) {
//     console.error("Error fetching chat data:", error);
//   }
// };


const getChatDataFromAgent = async () => {
  try {
    let code = ""
    let ans = ""
    let response = await requestPack.post("/api/get-code/", {
      question: Question.content+"\n"+Cot.content+"\n"+LastAns.content+"\n"
    });
    console.log(response)

    if (response.type === "success") {
      // chatLogs.value.push({
      //   role: 'user',
      //   content: Question.content
      // });
      // chat.value.push({
      //   role: 'user',
      //   content: Question.content
      // });

      chatLogs.value.push({
        role: 'agent',
        content: response.code,
        isMarkdown: true
      });
      code = response.code
    } else {

    }

    response = await requestPack.post("/api/exe-code/", {
      question: code
    });
    console.log(response)
    if (response.type === "success") {
      // chatLogs.value.push({
      //   role: 'agent',
      //   content: response.ans,
      //   isMarkdown: true
      // });
      ans = response.ans

      chat.value.push({
        role: 'agent',
        content: response.ans,
        isMarkdown: true
      });

      LastAns.content = response.ans

    } else {

    }

    response = await requestPack.post("/api/review/", {
      question: Question.content,
      ans: ans,
      code: code
    });
    console.log(response)
    if (response.type === "success") {
      // chatLogs.value.push({
      //   role: 'agent',
      //   content: response.ans,
      //   isMarkdown: true
      // });

      chat.value.push({
        role: 'agent',
        content: response.ans,
        isMarkdown: true
      });

    } else {

    }

  } catch (error) {
    console.error("Error fetching chat data:", error);
  }
};


const getCotChatFromAgent = async () => {
  try {
    const chatHistory = chat.value.map(log =>
        `${log.role === 'user' ? 'User' : 'Agent'}: ${log.content}`
    ).join('\n');
    let response = await requestPack.post("/api/cot-chat/", {
      question: chatHistory+"\n"+Question.content
    });
    console.log(response)

    if (response.type === "success") {

      chat.value.push({
        role: 'user',
        content: Question.content
      });

      let cleanedAns = response.ans.toLowerCase().replace(/\s+/g, '');
      if (cleanedAns=="one"){
        await getChatDataFromAgent()
        return
      }

      chat.value.push({
        role: 'agent',
        content: response.ans,
        isMarkdown: true
      });

      Cot.content = response.ans

    } else {

    }

  } catch (error) {
    console.error("Error fetching chat data:", error);
  }
};



const onClear = () => {
  Question.content = '';
  chatLogs.value = [];
  chat.value = [];
  Cot.content = ""
}

const onSubmit = async () => {
  if (Question.content.trim()) {
    await getCotChatFromAgent();
    Question.content = '';
    scrollToBottom();
  }
}

const onExe = async () => {
  if (Question.content.trim() || Cot.content.trim()) {
    await getChatDataFromAgent();
    Question.content = '';
    scrollToBottom();
  }
};
</script>

<template>
  <el-container>

    <el-container>
      <el-main style="padding: 20px; margin-left: 20px;margin-right: 20px">
        <el-row :gutter="20">

          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">

            <el-card class="box-card" style="margin-bottom: 20px;">
              <template #header>
                <div class="card-header">
                  <span>Chat</span>
                </div>
              </template>
              <div class="chat-container">
                <div class="chat-log" v-for="(log, index) in chat" :key="index">
                  <div :class="log.role === 'user' ? 'user-log' : 'agent-log'">
                    <div v-if="log.role === 'user'">{{ log.content }}</div>
                    <div v-else v-html="md.render(log.content)" class="markdown-content"></div>
                  </div>
                </div>
              </div>
            </el-card>

          </el-col>

          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">

            <el-row :gutter="20">
              <el-col :span="24">
                <el-card class="box-card" style="margin-bottom: 20px;">
                  <template #header>
                    <div class="card-header">
                      <span>Chat Logs</span>
                    </div>
                  </template>
                  <div class="chat-container chat-log-container">
                    <div class="chat-log" v-for="(log, index) in chatLogs" :key="index">
                      <div :class="log.role === 'user' ? 'user-log' : 'agent-log'">
                        <div v-if="log.role === 'user'">{{ log.content }}</div>
                        <div v-else v-html="md.render(log.content)" class="markdown-content"></div>
                      </div>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>

            <el-form :model="Question" label-width="120px" label-position="top">
              <el-form-item label="Question">
                <el-input v-model="Question.content" type="textarea" :rows="6"/>
              </el-form-item>
              <el-form-item>
                <el-button type="success" @click="onExe">Execute</el-button>
                <div style="flex-grow: 1;"/>
                <el-button type="primary" @click="onSubmit"><el-icon><Select /> </el-icon> Submit</el-button>
                <el-button @click="onClear"><el-icon><CloseBold /></el-icon> Clear</el-button>
              </el-form-item>
            </el-form>

          </el-col>

        </el-row>
      </el-main>


      <el-footer style="padding: 0">
        <el-row :gutter="20">
          <el-col :span="4" class="foot-bottom"><div class="grid-content ep-bg-purple" ></div></el-col>
          <el-col :span="16" class="foot-bottom"><div class="grid-content ep-bg-purple" >
            <a href="http://www.bytesc.top">
              <p style="text-align: center; color: #888888"><strong>© 2024 Copyright: bytesc</strong></p>
            </a>
          </div></el-col>
          <el-col :span="4" class="foot-bottom"><div class="grid-content ep-bg-purple" ></div></el-col>
        </el-row>
      </el-footer>
    </el-container>
  </el-container>
</template>

<style scoped>
.flex-grow {
  flex-grow: 1;
}
.foot-item{
  padding: 0 !important;
  background: #dadada;
}
.foot-bottom{
  padding: 0 !important;
  background: #ebebeb;
}
.grid-content {
  min-height: 36px;
}
.chat-log {
  margin: 10px;
  padding: 5px;
  border-radius: 5px;
}

.user-log {
  text-align: right;
  background-color: #e6f7ff;
  border-left: 3px solid #409eff;
  padding: 8px 12px;
  margin: 5px 0;
  border-radius: 4px;
}

.agent-log {
  text-align: left;
  background-color: #f4f4f5;
  border-right: 3px solid #909399;
  padding: 8px 12px;
  margin: 5px 0;
  border-radius: 4px;
}

.markdown-content {
  text-align: left;
  overflow-wrap: break-word;
}

.markdown-content >>> img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 10px 0;
}

.markdown-content >>> table {
  border-collapse: collapse;
  width: 100%;
  margin: 10px 0;
  display: block;
  overflow-x: auto;
  white-space: nowrap;
}

.markdown-content >>> th, .markdown-content >>> td {
  border: 1px solid #ddd;
  padding: 8px;
  white-space: normal;
}

.markdown-content >>> th {
  background-color: #f2f2f2;
  text-align: left;
}

.markdown-content >>> pre {
  background-color: #f5f5f5;
  padding: 10px;
  border-radius: 4px;
  overflow-x: auto;
  max-width: 100%;
}

.markdown-content >>> code {
  font-family: monospace;
  background-color: #f5f5f5;
  padding: 2px 4px;
  border-radius: 2px;
}

.markdown-content >>> blockquote {
  border-left: 4px solid #ddd;
  padding-left: 10px;
  color: #666;
  margin: 10px 0;
}

/* Style for the iframe container */
.box-card {
  height: 100%;
}

/* Ensure iframe fills its container */
iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.chat-container {
  height: 600px;
  overflow-y: auto;
  padding-right: 8px; /* Prevents content from touching scrollbar */
}

.chat-log-container{
  height: 400px;
}

/* Custom scrollbar styling (optional) */
.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

</style>