import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import './assets/styles.css'
import MilestoneForm from './components/MilestoneForm.vue'
import EquipmentSaleForm from './components/EquipmentSaleForm.vue'
import GanttChart from './components/GanttChart.vue'
import Dashboard from './components/Dashboard.vue'

// Create router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Dashboard },
    { path: '/milestones', component: MilestoneForm },
    { path: '/equipment', component: EquipmentSaleForm },
    { path: '/chart', component: GanttChart },
  ]
})

// Create Pinia store
const pinia = createPinia()

// Create and mount app
const app = createApp(App)
app.use(pinia)
app.use(router)
app.mount('#app')