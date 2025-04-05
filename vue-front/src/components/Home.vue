<script lang="ts" setup>
import { ref,reactive,computed } from 'vue'

defineProps({
  msg: String,
})

const activeIndex = ref('1')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

const Question = reactive({
  content: '',
})

// 表格数据
const tableData = ref([
  // { name: 'Alice', age: 30, country: 'USA' ,gen:"xx"},
  // { name: 'Bob', age: 25, country: 'Canada' },
  // { name: 'Bob', age: 25, country: 'Canada' ,gen:"xx"},
]);
// 从 JSON 数据中提取列
const columns = ref([]);

const SubmitData = ref({
})

const CurDatabaseName = ref("")
const CurTableName = ref("")


const onClear = () => {
  Question.content=""
  tableData.value=[]
  columns.value=[]
  SubmitData.value={}
  CurTableName.value=""
  CurDatabaseName.value=""
}

const onSubmit = () => {
  // console.log('submit!')
  // console.log(SqlStatement.content)
  CurTableName.value=""
  CurDatabaseName.value=""
  getTableData()
}

const onHelp = () => {

}




import {requestPack} from "../utils/requests.js";
import {Box, ChatDotRound, CloseBold, Coin, Files, House, Plus, Refrigerator, Tickets} from "@element-plus/icons-vue";
const getTableData = async ()=>{
  // let res= await request.get(`user/list/?pageSize=${pageSize.value}&pageNum=${cur}`)
  let res= await requestPack.post(`/mydbms/index?statement=${Question.content}`)
  console.log(res)
  tableData.value = res.msg
  console.log(res.msg)
  if (tableData.value.length > 0) {
    columns.value = Object.keys(tableData.value[0]);
  }
}
// getTableData()

</script>

<template>

  <el-container >
    <el-header  style="padding: 0">
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
        <div class="flex-grow" />
      </el-menu>
    </el-header>

    <el-container>
      <el-main style="padding: 20px; margin-left: 20px;margin-right: 20px" >
        <el-row :gutter="20">
          <el-col :xs="24" :sm="24" :md="14" :lg="16" :xl="16"
          >


          </el-col>

          <el-col :xs="24" :sm="24" :md="10" :lg="8" :xl="8"
          >

            <el-form :model="Question" label-width="120px" label-position="top">
              <el-form-item label="Question">
                <el-input v-model="Question.content" type="textarea" :rows="6"/>
              </el-form-item>
              <el-form-item>
                <el-button type="success" @click="onHelp"><el-icon><ChatDotRound /></el-icon>Help</el-button>
                <div style="flex-grow: 1;"/>
                <el-button type="primary" @click="onSubmit"><el-icon><Select /> </el-icon> Submit</el-button>
                <el-button @click="onClear"><el-icon><CloseBold /></el-icon> Clear</el-button>
              </el-form-item>
            </el-form>

          </el-col>
        </el-row>




      </el-main>
      <el-footer style="padding: 0">
        <el-row :gutter="20" >
          <el-col :span="4" class="foot-bottom"><div class="grid-content ep-bg-purple" ></div></el-col>
          <el-col :span="16" class="foot-bottom"><div class="grid-content ep-bg-purple" >
            <a href="http://www.bytesc.top" >
              <!--              style="text-decoration: none;-->
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

</style>
