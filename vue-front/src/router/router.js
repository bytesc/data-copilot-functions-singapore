import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Setting from '../components/Setting.vue'
import Data from '../components/Data.vue'
import Api from '../components/Api.vue'
import System from '../components/System.vue'
import Functions from '../components/Functions.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/setting',
        name: 'Setting',
        component: Setting
    },
    {
        path: '/data',
        name: 'Data',
        component: Data
    },
    {
        path: '/api',
        name: 'Api',
        component: Api
    },
    {
        path: '/system',
        name: 'System',
        component: System
    },
    {
        path: '/functions',
        name: 'Functions',
        component: Functions
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router