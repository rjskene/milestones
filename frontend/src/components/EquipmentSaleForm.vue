<template>
  <div class="equipment-form">
    <div class="form-header">
      <h2>Equipment Sales</h2>
      <button @click="showCreateForm = true" class="btn-primary">Create New Sale</button>
    </div>

    <!-- Create/Edit Form -->
    <div v-if="showCreateForm" class="form-container">
      <h3>{{ editingSale ? 'Edit' : 'Create' }} Equipment Sale</h3>
      
      <form @submit.prevent="saveSale" class="equipment-form-content">
        <div class="form-row">
          <div class="form-group">
            <label for="name">Sale Name *</label>
            <input 
              type="text" 
              id="name" 
              v-model="formData.name" 
              required 
              placeholder="e.g., Industrial Equipment Sale"
            />
          </div>

          <div class="form-group">
            <label for="vendor">Vendor</label>
            <input 
              type="text" 
              id="vendor" 
              v-model="formData.vendor" 
              placeholder="Vendor name (optional)"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="quantity">Quantity *</label>
            <input 
              type="number" 
              id="quantity" 
              v-model.number="formData.quantity" 
              required 
              min="1"
              placeholder="1"
            />
          </div>

          <div class="form-group">
            <label for="total_amount">Total Amount *</label>
            <div class="input-with-prefix">
              <span class="input-prefix">$</span>
              <input 
                type="number" 
                id="total_amount" 
                v-model.number="formData.total_amount" 
                required 
                min="0"
                step="0.01"
                placeholder="0.00"
              />
            </div>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="milestone_structure">Payment Milestone Structure *</label>
            <select 
              id="milestone_structure" 
              v-model="formData.milestone_structure_id" 
              required
            >
              <option value="">Select a milestone structure</option>
              <option 
                v-for="structure in milestoneStructures" 
                :key="structure.id" 
                :value="structure.id"
              >
                {{ structure.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="project_start_date">Project Start Date *</label>
            <input 
              type="date" 
              id="project_start_date" 
              v-model="formData.project_start_date" 
              required
            />
          </div>
        </div>

        <!-- Milestone Structure Preview -->
        <div v-if="selectedMilestoneStructure" class="milestone-preview">
          <h4>Selected Milestone Structure: {{ selectedMilestoneStructure.name }}</h4>
          <div class="milestones-list">
            <div v-for="milestone in selectedMilestoneStructure.milestones" :key="milestone.id" class="milestone-item">
              <div class="milestone-info">
                <span class="milestone-name">{{ milestone.name }}</span>
                <span class="milestone-details">
                  {{ milestone.payment_percentage }}% • {{ milestone.days_after_previous }} days
                  <span v-if="milestone.net_terms_days > 0">• {{ milestone.net_terms_days }} net terms</span>
                </span>
              </div>
              <div class="milestone-amount">
                ${{ calculateMilestoneAmount(milestone.payment_percentage).toFixed(2) }}
              </div>
            </div>
          </div>
          <div class="total-summary">
            <strong>Total: ${{ formData.total_amount || 0 }}</strong>
          </div>
        </div>

        <div class="form-actions">
          <button type="button" @click="cancelForm" class="btn-secondary">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Saving...' : (editingSale ? 'Update' : 'Create') }}
          </button>
        </div>
      </form>
    </div>

    <!-- Sales List -->
    <div class="sales-list">
      <div v-if="loading" class="loading">Loading equipment sales...</div>
      <div v-else-if="equipmentSales.length === 0" class="empty-state">
        <p>No equipment sales created yet.</p>
        <button @click="showCreateForm = true" class="btn-primary">Create Your First Sale</button>
      </div>
      <div v-else>
        <div v-for="sale in equipmentSales" :key="sale.id" class="sale-card">
          <div class="sale-header">
            <div class="sale-info">
              <h3>{{ sale.name }}</h3>
              <p class="sale-details">
                {{ sale.vendor || 'No vendor' }} • Qty: {{ sale.quantity }} • 
                Unit Price: ${{ sale.unit_price.toFixed(2) }}
              </p>
            </div>
            <div class="sale-amount">
              <span class="amount">${{ sale.total_amount }}</span>
            </div>
          </div>
          
          <div class="sale-details-row">
            <div class="detail-item">
              <label>Milestone Structure:</label>
              <span>{{ sale.milestone_structure.name }}</span>
            </div>
            <div class="detail-item">
              <label>Project Start:</label>
              <span>{{ formatDate(sale.project_start_date) }}</span>
            </div>
          </div>

          <div class="sale-actions">
            <button @click="viewSchedule(sale.id)" class="btn-secondary">View Schedule</button>
            <button @click="editSale(sale)" class="btn-secondary">Edit</button>
            <button @click="deleteSale(sale.id)" class="btn-danger">Delete</button>
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
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMilestoneStore } from '../stores/milestoneStore'
import { useEquipmentStore } from '../stores/equipmentStore'

const router = useRouter()
const milestoneStore = useMilestoneStore()
const equipmentStore = useEquipmentStore()

const showCreateForm = ref(false)
const editingSale = ref(null)
const loading = ref(false)
const error = ref(null)

const milestoneStructures = ref([])
const equipmentSales = ref([])

const formData = reactive({
  name: '',
  vendor: '',
  quantity: 1,
  total_amount: 0,
  milestone_structure_id: '',
  project_start_date: new Date().toISOString().split('T')[0]
})

const selectedMilestoneStructure = computed(() => {
  return milestoneStructures.value.find(s => s.id === formData.milestone_structure_id)
})

const calculateMilestoneAmount = (percentage) => {
  return (formData.total_amount * percentage) / 100
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString()
}

const resetForm = () => {
  formData.name = ''
  formData.vendor = ''
  formData.quantity = 1
  formData.total_amount = 0
  formData.milestone_structure_id = ''
  formData.project_start_date = new Date().toISOString().split('T')[0]
  editingSale.value = null
  error.value = null
}

const cancelForm = () => {
  showCreateForm.value = false
  resetForm()
}

const editSale = (sale) => {
  editingSale.value = sale
  formData.name = sale.name
  formData.vendor = sale.vendor || ''
  formData.quantity = sale.quantity
  formData.total_amount = parseFloat(sale.total_amount)
  formData.milestone_structure_id = sale.milestone_structure.id
  formData.project_start_date = sale.project_start_date
  showCreateForm.value = true
}

const viewSchedule = (saleId) => {
  router.push(`/chart?sale=${saleId}`)
}

const saveSale = async () => {
  loading.value = true
  error.value = null

  try {
    const saleData = {
      name: formData.name,
      vendor: formData.vendor,
      quantity: formData.quantity,
      total_amount: formData.total_amount,
      milestone_structure_id: formData.milestone_structure_id,
      project_start_date: formData.project_start_date
    }

    if (editingSale.value) {
      await equipmentStore.updateEquipmentSale(editingSale.value.id, saleData)
    } else {
      await equipmentStore.createEquipmentSale(saleData)
    }

    await loadSales()
    cancelForm()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save equipment sale'
  } finally {
    loading.value = false
  }
}

const deleteSale = async (id) => {
  if (confirm('Are you sure you want to delete this equipment sale?')) {
    try {
      await equipmentStore.deleteEquipmentSale(id)
      await loadSales()
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete equipment sale'
    }
  }
}

const loadStructures = async () => {
  try {
    await milestoneStore.fetchMilestoneStructures()
    milestoneStructures.value = milestoneStore.milestoneStructures
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load milestone structures'
  }
}

const loadSales = async () => {
  try {
    await equipmentStore.fetchEquipmentSales()
    equipmentSales.value = equipmentStore.equipmentSales
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load equipment sales'
  }
}

onMounted(() => {
  loadStructures()
  loadSales()
})
</script>

<style scoped>
.equipment-form {
  max-width: 1000px;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.form-header h2 {
  color: #2c3e50;
}

.form-container {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.form-container h3 {
  color: #2c3e50;
  margin-bottom: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.input-with-prefix {
  position: relative;
  display: flex;
  align-items: center;
}

.input-prefix {
  position: absolute;
  left: 0.75rem;
  color: #7f8c8d;
  z-index: 1;
}

.input-with-prefix input {
  padding-left: 2rem;
}

.milestone-preview {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 4px;
  margin: 1.5rem 0;
}

.milestone-preview h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.milestones-list {
  margin-bottom: 1rem;
}

.milestone-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid #e9ecef;
}

.milestone-item:last-child {
  border-bottom: none;
}

.milestone-info {
  display: flex;
  flex-direction: column;
}

.milestone-name {
  font-weight: 500;
  color: #2c3e50;
}

.milestone-details {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.milestone-amount {
  font-weight: 500;
  color: #27ae60;
}

.total-summary {
  text-align: right;
  padding-top: 1rem;
  border-top: 2px solid #e9ecef;
  color: #2c3e50;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #ecf0f1;
}

.sales-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
}

.loading, .empty-state {
  padding: 3rem;
  text-align: center;
  color: #7f8c8d;
}

.sale-card {
  padding: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.sale-card:last-child {
  border-bottom: none;
}

.sale-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.sale-info h3 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
}

.sale-details {
  color: #7f8c8d;
  margin: 0;
}

.sale-amount {
  text-align: right;
}

.amount {
  font-size: 1.5rem;
  font-weight: bold;
  color: #27ae60;
}

.sale-details-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item label {
  font-weight: 500;
  color: #2c3e50;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.detail-item span {
  color: #7f8c8d;
}

.sale-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.btn-primary {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
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

.btn-danger {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-danger:hover {
  background-color: #c0392b;
}

.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}
</style>
