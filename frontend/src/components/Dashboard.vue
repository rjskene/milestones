<template>
  <div class="dashboard">
    <h2>Dashboard</h2>
    <div class="dashboard-grid">
      <div class="dashboard-card">
        <h3>Milestone Structures</h3>
        <p class="count">{{ milestoneStructures.length }}</p>
        <router-link to="/milestones" class="card-link">Manage Structures</router-link>
      </div>
      
      <div class="dashboard-card">
        <h3>Equipment Sales</h3>
        <p class="count">{{ equipmentSales.length }}</p>
        <router-link to="/equipment" class="card-link">Manage Sales</router-link>
      </div>
      
      <div class="dashboard-card">
        <h3>View Schedule</h3>
        <p class="description">View payment schedules as gantt charts</p>
        <router-link to="/chart" class="card-link">View Charts</router-link>
      </div>
    </div>
    
    <div class="recent-activity" v-if="equipmentSales.length > 0">
      <h3>Recent Equipment Sales</h3>
      <div class="sales-list">
        <div v-for="sale in recentSales" :key="sale.id" class="sale-item">
          <div class="sale-info">
            <h4>{{ sale.name }}</h4>
            <p>{{ sale.vendor || 'No vendor' }} • ${{ sale.total_amount }}</p>
          </div>
          <div class="sale-actions">
            <button @click="viewSchedule(sale.id)" class="btn-secondary">View Schedule</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMilestoneStore } from '../stores/milestoneStore'
import { useEquipmentStore } from '../stores/equipmentStore'

const router = useRouter()
const milestoneStore = useMilestoneStore()
const equipmentStore = useEquipmentStore()

const milestoneStructures = ref([])
const equipmentSales = ref([])

const recentSales = computed(() => {
  return equipmentSales.value.slice(0, 5)
})

const viewSchedule = (saleId) => {
  router.push(`/chart?sale=${saleId}`)
}

onMounted(async () => {
  try {
    await milestoneStore.fetchMilestoneStructures()
    await equipmentStore.fetchEquipmentSales()
    milestoneStructures.value = milestoneStore.milestoneStructures
    equipmentSales.value = equipmentStore.equipmentSales
  } catch (error) {
    console.error('Error loading dashboard data:', error)
  }
})
</script>

<style scoped>
.dashboard {
  max-width: 1000px;
}

.dashboard h2 {
  margin-bottom: 2rem;
  color: #2c3e50;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.dashboard-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  text-align: center;
}

.dashboard-card h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.count {
  font-size: 2rem;
  font-weight: bold;
  color: #3498db;
  margin-bottom: 1rem;
}

.description {
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.card-link {
  display: inline-block;
  background-color: #3498db;
  color: white;
  padding: 0.75rem 1.5rem;
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.card-link:hover {
  background-color: #2980b9;
}

.recent-activity {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.recent-activity h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.sales-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sale-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border: 1px solid #ecf0f1;
  border-radius: 4px;
}

.sale-info h4 {
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.sale-info p {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}
</style>
