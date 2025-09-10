<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <div class="modal-header">
        <h3>Assign Milestone Structure</h3>
        <button @click="closeModal" class="close-button">&times;</button>
      </div>
      
      <div class="modal-body">
        <div class="sale-info">
          <h4>{{ sale.name }}</h4>
          <p>Total Amount: ${{ sale.total_amount }}</p>
        </div>
        
        <div class="form-group">
          <label for="milestone-structure">Select Milestone Structure *</label>
          <select 
            id="milestone-structure" 
            v-model="selectedMilestoneStructureId"
            required
          >
            <option value="">Choose a milestone structure</option>
            <option 
              v-for="structure in milestoneStructures" 
              :key="structure.id" 
              :value="structure.id"
            >
              {{ structure.name }}
            </option>
          </select>
        </div>
        
        <!-- Milestone Structure Preview -->
        <div v-if="selectedMilestoneStructure" class="milestone-preview">
          <h4>Milestone Structure Preview: {{ selectedMilestoneStructure.name }}</h4>
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
            <strong>Total: ${{ sale.total_amount }}</strong>
          </div>
        </div>
      </div>
      
      <div class="modal-footer">
        <button @click="closeModal" class="btn-secondary">Cancel</button>
        <button 
          @click="assignMilestone" 
          class="btn-primary" 
          :disabled="!selectedMilestoneStructureId || loading"
        >
          {{ loading ? 'Assigning...' : 'Assign Milestone Structure' }}
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useMilestoneStore } from '../stores/milestoneStore'
import { useEquipmentStore } from '../stores/equipmentStore'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  sale: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'assigned'])

const milestoneStore = useMilestoneStore()
const equipmentStore = useEquipmentStore()

const selectedMilestoneStructureId = ref('')
const loading = ref(false)
const error = ref(null)

const milestoneStructures = computed(() => milestoneStore.milestoneStructures)

const selectedMilestoneStructure = computed(() => {
  return milestoneStructures.value.find(s => s.id === selectedMilestoneStructureId.value)
})

const calculateMilestoneAmount = (percentage) => {
  return (props.sale.total_amount * percentage) / 100
}

const closeModal = () => {
  selectedMilestoneStructureId.value = ''
  error.value = null
  emit('close')
}

const assignMilestone = async () => {
  if (!selectedMilestoneStructureId.value) return
  
  loading.value = true
  error.value = null
  
  try {
    await equipmentStore.assignMilestoneStructure(
      props.sale.id, 
      selectedMilestoneStructureId.value
    )
    
    emit('assigned')
    closeModal()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to assign milestone structure'
  } finally {
    loading.value = false
  }
}

// Load milestone structures when modal opens
watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    milestoneStore.fetchMilestoneStructures()
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.modal-header h3 {
  margin: 0;
  color: #2c3e50;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #7f8c8d;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  color: #2c3e50;
}

.modal-body {
  padding: 1.5rem;
}

.sale-info {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.sale-info h4 {
  margin: 0 0 0.5rem 0;
  color: #2c3e50;
}

.sale-info p {
  margin: 0;
  color: #7f8c8d;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.milestone-preview {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 4px;
  margin-top: 1rem;
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

.modal-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
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
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 1rem;
  margin: 1rem 1.5rem;
  border-radius: 4px;
}
</style>
