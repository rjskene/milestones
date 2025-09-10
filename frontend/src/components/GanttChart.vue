<template>
  <div class="gantt-chart">
    <div class="chart-header">
      <h2>Payment Milestone Schedule</h2>
      <div class="chart-controls">
        <select v-model="selectedSaleId" @change="loadSchedule" class="sale-selector">
          <option value="">Select an equipment sale</option>
          <option 
            v-for="sale in equipmentSales" 
            :key="sale.id" 
            :value="sale.id"
          >
            {{ sale.name }} - ${{ sale.total_amount }}
          </option>
        </select>
        <button @click="refreshChart" class="btn-secondary" :disabled="!selectedSaleId">
          Refresh
        </button>
      </div>
    </div>

    <div v-if="loading" class="loading">
      Loading schedule data...
    </div>

    <div v-else-if="!selectedSaleId" class="empty-state">
      <p>Please select an equipment sale to view its payment milestone schedule.</p>
    </div>

    <div v-else-if="!scheduleData" class="empty-state">
      <p>No schedule data available for the selected sale.</p>
    </div>

    <div v-else class="chart-container">
      <!-- Sale Information -->
      <div class="sale-info">
        <h3>{{ selectedSale.name }}</h3>
        <div class="sale-details">
          <span><strong>Vendor:</strong> {{ selectedSale.vendor || 'N/A' }}</span>
          <span><strong>Quantity:</strong> {{ selectedSale.quantity }}</span>
          <span><strong>Total Amount:</strong> ${{ selectedSale.total_amount }}</span>
          <span><strong>Unit Price:</strong> ${{ selectedSale.unit_price.toFixed(2) }}</span>
          <span><strong>Project Start:</strong> {{ formatDate(selectedSale.project_start_date) }}</span>
        </div>
      </div>

      <!-- Gantt Chart -->
      <highcharts :constructorType="'ganttChart'" class="chart" :options="ganttOptions" ref="chartContainer"></highcharts>
      
      <!-- Schedule Summary -->
      <div class="schedule-summary">
        <h4>Payment Schedule Summary</h4>
        <div class="summary-table">
          <div class="summary-header">
            <span>Milestone</span>
            <span>Due Date</span>
            <span>Payment Due</span>
            <span>Amount</span>
            <span>Percentage</span>
          </div>
          <div 
            v-for="milestone in scheduleData.milestone_schedule" 
            :key="milestone.id" 
            class="summary-row"
          >
            <span class="milestone-name">{{ milestone.name }}</span>
            <span>{{ formatDate(milestone.due_date) }}</span>
            <span>{{ formatDate(milestone.payment_due_date) }}</span>
            <span class="amount">${{ milestone.payment_amount.toFixed(2) }}</span>
            <span>{{ milestone.payment_percentage }}%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { useEquipmentStore } from '../stores/equipmentStore'

const route = useRoute()
const equipmentStore = useEquipmentStore()

const chartContainer = ref(null)
const ganttOptions = ref(null)

const selectedSaleId = ref('')
const loading = ref(false)
const error = ref(null)
const scheduleData = ref(null)
const equipmentSales = ref([])

const selectedSale = computed(() => {
  return equipmentSales.value.find(sale => sale.id === parseInt(selectedSaleId.value))
})

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const loadEquipmentSales = async () => {
  try {
    await equipmentStore.fetchEquipmentSales()
    equipmentSales.value = equipmentStore.equipmentSales
  } catch (err) {
    error.value = 'Failed to load equipment sales'
    console.error('Error loading equipment sales:', err)
  }
}

const loadSchedule = async () => {
  if (!selectedSaleId.value) {
    scheduleData.value = null
    return
  }

  loading.value = true
  error.value = null

  try {
    const data = await equipmentStore.getEquipmentSaleSchedule(selectedSaleId.value)
    scheduleData.value = data
    await nextTick()
    createGanttChart()
  } catch (err) {
    error.value = 'Failed to load schedule data'
    console.error('Error loading schedule:', err)
  } finally {
    loading.value = false
  }
}

const refreshChart = () => {
  if (selectedSaleId.value) {
    loadSchedule()
  }
}

const createGanttChart = () => {

  const milestones = scheduleData.value.milestone_schedule
  const projectStartDate = new Date(scheduleData.value.project_start_date)

  // Prepare data for Highcharts Gantt
  const seriesData = milestones.map((milestone, index) => {
    const startDate = new Date(projectStartDate.getTime() + milestone.start_days * 24 * 60 * 60 * 1000)
    const endDate = new Date(projectStartDate.getTime() + milestone.end_days * 24 * 60 * 60 * 1000)

    return {
      id: `milestone-${milestone.id}`,
      name: milestone.name,
      start: startDate.getTime(),
      end: endDate.getTime(),
      completed: {
        amount: 0 // No completion tracking for now
      },
      color: getMilestoneColor(index)
    }
  })
  // Create the chart
  ganttOptions.value = {
    title: {
      text: 'Payment Milestone Timeline'
    },
    subtitle: {
      text: `${selectedSale.value.name} - Payment Schedule`
    },
    accessibility: {
      enabled: false
    },
    xAxis: {
      type: 'datetime',
      title: {
        text: 'Timeline'
      }
    },
    yAxis: {
      title: {
        text: 'Milestones'
      }
    },
    tooltip: {
      formatter: function() {
        const milestone = milestones.find(m => m.name === this.point.name)
        if (!milestone) return ''

        const startDate = new Date(this.point.start)
        const endDate = new Date(this.point.end)
        
        return `
          <b>${this.point.name}</b><br/>
          Start: ${startDate.toLocaleDateString()}<br/>
          End: ${endDate.toLocaleDateString()}<br/>
          Payment: $${milestone.payment_amount.toFixed(2)} (${milestone.payment_percentage}%)<br/>
          Due: ${formatDate(milestone.payment_due_date)}
        `
      }
    },
    series: [{
      name: 'Payment Milestones',
      data: seriesData
    }],
    plotOptions: {
      gantt: {
        dataLabels: {
          enabled: true,
          formatter: function() {
            const milestone = milestones.find(m => m.name === this.point.name)
            return milestone ? `$${milestone.payment_amount.toFixed(0)}` : ''
          }
        }
      }
    },
    credits: {
      enabled: false
    },
    legend: {
      enabled: false
    }
  }
}

const getMilestoneColor = (index) => {
  const colors = [
    '#3498db', // Blue
    '#e74c3c', // Red
    '#2ecc71', // Green
    '#f39c12', // Orange
    '#9b59b6', // Purple
    '#1abc9c', // Turquoise
    '#e67e22', // Carrot
    '#34495e'  // Dark blue-gray
  ]
  return colors[index % colors.length]
}

onMounted(async () => {
  await loadEquipmentSales()
  
  // Check if a sale ID was passed in the URL
  const saleId = route.query.sale
  if (saleId) {
    selectedSaleId.value = saleId
    await loadSchedule()
  }
})
</script>

<style scoped>
.gantt-chart {
  max-width: 1200px;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.chart-header h2 {
  color: #2c3e50;
  margin: 0;
}

.chart-controls {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.sale-selector {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  min-width: 250px;
}

.sale-selector:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.loading, .empty-state {
  padding: 3rem;
  text-align: center;
  color: #7f8c8d;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.chart-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.sale-info {
  padding: 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.sale-info h3 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.sale-details {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.sale-details span {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.chart {
  height: 400px;
  padding: 1rem;
}

.schedule-summary {
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.schedule-summary h4 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.summary-table {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 0.5rem;
}

.summary-header {
  display: contents;
}

.summary-header span {
  font-weight: 600;
  color: #2c3e50;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
  text-align: center;
}

.summary-row {
  display: contents;
}

.summary-row span {
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e9ecef;
  text-align: center;
}

.milestone-name {
  text-align: left !important;
  font-weight: 500;
  color: #2c3e50;
}

.amount {
  font-weight: 500;
  color: #27ae60;
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

.btn-secondary:hover:not(:disabled) {
  background-color: #7f8c8d;
}

.btn-secondary:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chart-controls {
    justify-content: center;
  }
  
  .sale-details {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .summary-table {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .summary-header,
  .summary-row {
    display: block;
  }
  
  .summary-header span,
  .summary-row span {
    display: block;
    text-align: left;
    border-bottom: none;
    border-right: none;
  }
  
  .summary-header span {
    background: #f8f9fa;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }
}
</style>
