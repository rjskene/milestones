<template>
  <div class="project-form">
    <div class="form-header">
      <h2>{{ isEditing ? 'Edit Project' : 'Create New Project' }}</h2>
      <button @click="$emit('close')" class="btn-close">×</button>
    </div>

    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-group">
        <label for="name">Project Name *</label>
        <input
          type="text"
          id="name"
          v-model="formData.name"
          required
          class="form-input"
          placeholder="Enter project name"
        >
      </div>

      <div class="form-group">
        <label for="start_date">Start Date *</label>
        <input
          type="date"
          id="start_date"
          v-model="formData.start_date"
          required
          class="form-input"
        >
      </div>

      <div class="form-group">
        <label for="description">Description</label>
        <textarea
          id="description"
          v-model="formData.description"
          class="form-textarea"
          placeholder="Enter project description (optional)"
          rows="3"
        ></textarea>
      </div>

      <div class="form-actions">
        <button type="button" @click="$emit('close')" class="btn-secondary">
          Cancel
        </button>
        <button type="submit" :disabled="loading" class="btn-primary">
          {{ loading ? 'Saving...' : (isEditing ? 'Update' : 'Create') }}
        </button>
      </div>
    </form>

    <div v-if="error" class="error-message">
      {{ error }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useProjectStore } from '../stores/projectStore'

const props = defineProps({
  project: {
    type: Object,
    default: null
  },
  isEditing: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'saved'])

const projectStore = useProjectStore()

const formData = ref({
  name: '',
  start_date: '',
  description: ''
})

const loading = ref(false)
const error = ref(null)

// Watch for changes in the project prop
watch(() => props.project, (newProject) => {
  if (newProject) {
    formData.value = {
      name: newProject.name || '',
      start_date: newProject.start_date || '',
      description: newProject.description || ''
    }
  }
}, { immediate: true })

const handleSubmit = async () => {
  loading.value = true
  error.value = null

  try {
    if (props.isEditing && props.project) {
      await projectStore.updateProject(props.project.id, formData.value)
    } else {
      await projectStore.createProject(formData.value)
    }
    
    emit('saved')
    emit('close')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to save project'
    console.error('Error saving project:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.project-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.form-header h2 {
  margin: 0;
  color: #2c3e50;
}

.btn-close {
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
  border-radius: 50%;
  transition: background-color 0.2s;
}

.btn-close:hover {
  background-color: #f8f9fa;
}

.form {
  padding: 1.5rem;
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

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
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
  font-size: 1rem;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 1rem;
  margin: 1rem;
  border-radius: 4px;
}
</style>
