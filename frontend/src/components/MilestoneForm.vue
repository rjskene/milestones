<template>
  <div class="milestone-form">
    <div class="form-header">
      <h2>Payment Milestone Structures</h2>
      <button @click="showCreateForm = true" class="btn-primary">Create New Structure</button>
    </div>

    <!-- Create/Edit Form -->
    <div v-if="showCreateForm" class="form-container">
      <h3>{{ editingStructure ? 'Edit' : 'Create' }} Milestone Structure</h3>
      
      <form @submit.prevent="saveStructure" class="milestone-form-content">
        <div class="form-group">
          <label for="name">Structure Name *</label>
          <input 
            type="text" 
            id="name" 
            v-model="formData.name" 
            required 
            placeholder="e.g., Standard 30-60-90"
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea 
            id="description" 
            v-model="formData.description" 
            placeholder="Optional description of this milestone structure"
            rows="3"
          ></textarea>
        </div>

        <div class="milestones-section">
          <h4>Milestones</h4>
          <div v-for="(milestone, index) in formData.milestones" :key="index" class="milestone-item">
            <div class="milestone-header">
              <h5>Milestone {{ index + 1 }}</h5>
              <button type="button" @click="removeMilestone(index)" class="btn-danger" v-if="formData.milestones.length > 1">
                Remove
              </button>
            </div>
            
            <div class="milestone-fields">
              <div class="form-group">
                <label>Name *</label>
                <input 
                  type="text" 
                  v-model="milestone.name" 
                  required 
                  placeholder="e.g., Down Payment, Final Payment"
                />
              </div>

              <div class="form-group">
                <label>Payment Percentage *</label>
                <input 
                  type="number" 
                  v-model.number="milestone.payment_percentage" 
                  required 
                  min="0" 
                  max="100" 
                  step="0.01"
                  placeholder="0.00"
                />
                <span class="input-suffix">%</span>
              </div>

              <div class="form-group">
                <label>Days After Previous *</label>
                <input 
                  type="number" 
                  v-model.number="milestone.days_after_previous" 
                  required 
                  min="0"
                  placeholder="0"
                />
                <span class="input-suffix">days</span>
              </div>

              <div class="form-group">
                <label>Net Terms Days</label>
                <input 
                  type="number" 
                  v-model.number="milestone.net_terms_days" 
                  min="0"
                  placeholder="0"
                />
                <span class="input-suffix">days</span>
              </div>
            </div>
          </div>

          <button type="button" @click="addMilestone" class="btn-secondary">
            Add Milestone
          </button>
        </div>

        <div class="form-actions">
          <button type="button" @click="cancelForm" class="btn-secondary">Cancel</button>
          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? 'Saving...' : (editingStructure ? 'Update' : 'Create') }}
          </button>
        </div>
      </form>
    </div>

    <!-- Structures List -->
    <div class="structures-list">
      <div v-if="loading" class="loading">Loading milestone structures...</div>
      <div v-else-if="milestoneStructures.length === 0" class="empty-state">
        <p>No milestone structures created yet.</p>
        <button @click="showCreateForm = true" class="btn-primary">Create Your First Structure</button>
      </div>
      <div v-else>
        <div v-for="structure in milestoneStructures" :key="structure.id" class="structure-card">
          <div class="structure-header">
            <h3>{{ structure.name }}</h3>
            <div class="structure-actions">
              <button @click="editStructure(structure)" class="btn-secondary">Edit</button>
              <button @click="deleteStructure(structure.id)" class="btn-danger">Delete</button>
            </div>
          </div>
          
          <p v-if="structure.description" class="structure-description">{{ structure.description }}</p>
          
          <div class="milestones-preview">
            <h4>Milestones:</h4>
            <div v-for="milestone in structure.milestones" :key="milestone.id" class="milestone-preview">
              <span class="milestone-name">{{ milestone.name }}</span>
              <span class="milestone-details">
                {{ milestone.payment_percentage }}% • {{ milestone.days_after_previous }} days
                <span v-if="milestone.net_terms_days > 0">• {{ milestone.net_terms_days }} net terms</span>
              </span>
            </div>
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
import { ref, reactive, onMounted } from 'vue'
import { useMilestoneStore } from '../stores/milestoneStore'

const milestoneStore = useMilestoneStore()

const showCreateForm = ref(false)
const editingStructure = ref(null)
const loading = ref(false)
const error = ref(null)

const milestoneStructures = ref([])

const formData = reactive({
  name: '',
  description: '',
  milestones: [
    {
      name: '',
      payment_percentage: 0,
      days_after_previous: 0,
      net_terms_days: 0,
      order: 0
    }
  ]
})

const addMilestone = () => {
  formData.milestones.push({
    name: '',
    payment_percentage: 0,
    days_after_previous: 0,
    net_terms_days: 0,
    order: formData.milestones.length
  })
}

const removeMilestone = (index) => {
  if (formData.milestones.length > 1) {
    formData.milestones.splice(index, 1)
  }
}

const resetForm = () => {
  formData.name = ''
  formData.description = ''
  formData.milestones = [
    {
      name: '',
      payment_percentage: 0,
      days_after_previous: 0,
      net_terms_days: 0,
      order: 0
    }
  ]
  editingStructure.value = null
  error.value = null
}

const cancelForm = () => {
  showCreateForm.value = false
  resetForm()
}

const editStructure = (structure) => {
  editingStructure.value = structure
  formData.name = structure.name
  formData.description = structure.description || ''
  formData.milestones = structure.milestones.map((milestone, index) => ({
    ...milestone,
    order: index
  }))
  showCreateForm.value = true
}

const saveStructure = async () => {
  loading.value = true
  error.value = null

  try {
    // Set order for milestones
    const milestonesWithOrder = formData.milestones.map((milestone, index) => ({
      ...milestone,
      order: index
    }))

    const structureData = {
      name: formData.name,
      description: formData.description,
      milestones: milestonesWithOrder
    }

    if (editingStructure.value) {
      await milestoneStore.updateMilestoneStructure(editingStructure.value.id, structureData)
    } else {
      await milestoneStore.createMilestoneStructure(structureData)
    }

    await loadStructures()
    cancelForm()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save milestone structure'
  } finally {
    loading.value = false
  }
}

const deleteStructure = async (id) => {
  if (confirm('Are you sure you want to delete this milestone structure?')) {
    try {
      await milestoneStore.deleteMilestoneStructure(id)
      await loadStructures()
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to delete milestone structure'
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

onMounted(() => {
  loadStructures()
})
</script>

<style scoped>
.milestone-form {
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
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.input-suffix {
  margin-left: 0.5rem;
  color: #7f8c8d;
}

.milestones-section {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #ecf0f1;
}

.milestones-section h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.milestone-item {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.milestone-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.milestone-header h5 {
  color: #2c3e50;
  margin: 0;
}

.milestone-fields {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #ecf0f1;
}

.structures-list {
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

.structure-card {
  padding: 1.5rem;
  border-bottom: 1px solid #ecf0f1;
}

.structure-card:last-child {
  border-bottom: none;
}

.structure-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.structure-header h3 {
  color: #2c3e50;
  margin: 0;
}

.structure-actions {
  display: flex;
  gap: 0.5rem;
}

.structure-description {
  color: #7f8c8d;
  margin-bottom: 1rem;
}

.milestones-preview h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.milestone-preview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f2f6;
}

.milestone-preview:last-child {
  border-bottom: none;
}

.milestone-name {
  font-weight: 500;
  color: #2c3e50;
}

.milestone-details {
  color: #7f8c8d;
  font-size: 0.9rem;
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
