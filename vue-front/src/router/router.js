import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'
import Setting from '../components/Setting.vue'

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
    }
]

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes
})

export default router