<template>
  <div class="projects-page">
    <div class="page-header">
      <h1>Projects</h1>
      <button @click="showCreateForm = true" class="btn-primary">Create New Project</button>
    </div>

    <!-- Create/Edit Form -->
    <div v-if="showCreateForm" class="form-container">
      <ProjectForm 
        :project="editingProject"
        :is-editing="!!editingProject"
        @close="closeForm"
        @saved="onFormSaved"
      />
    </div>

    <!-- Projects List -->
    <div v-else class="projects-list">
      <div v-if="loading" class="loading">
        Loading projects...
      </div>

      <div v-else-if="projects.length === 0" class="empty-state">
        <h3>No Projects Yet</h3>
        <p>Create your first project to get started with organizing your equipment sales.</p>
        <button @click="showCreateForm = true" class="btn-primary">Create Project</button>
      </div>

      <div v-else class="projects-grid">
        <div 
          v-for="project in projects" 
          :key="project.id" 
          class="project-card"
        >
          <div class="project-header">
            <h3>{{ project.name }}</h3>
            <div class="project-actions">
              <button @click="viewProject(project)" class="btn-secondary">View Timeline</button>
              <button @click="editProject(project)" class="btn-edit">Edit</button>
              <button @click="deleteProject(project)" class="btn-delete">Delete</button>
            </div>
          </div>

          <div class="project-details">
            <div class="detail-item">
              <label>Start Date:</label>
              <span>{{ formatDate(project.start_date) }}</span>
            </div>
            <div class="detail-item">
              <label>Equipment Sales:</label>
              <span>{{ project.equipment_sales_count }}</span>
            </div>
            <div class="detail-item">
              <label>Total Value:</label>
              <span class="total-value">{{ formatCurrency(project.total_value) }}</span>
            </div>
            <div v-if="project.description" class="detail-item description">
              <label>Description:</label>
              <span>{{ project.description }}</span>
            </div>
          </div>

          <div v-if="project.equipment_sales && project.equipment_sales.length > 0" class="equipment-sales">
            <h4>Equipment Sales</h4>
            <div class="sales-list">
              <div 
                v-for="sale in project.equipment_sales" 
                :key="sale.id" 
                class="sale-item"
              >
                <span class="sale-name">{{ sale.name }}</span>
                <span class="sale-type">{{ sale.sale_type }}</span>
                <span class="sale-amount">{{ formatCurrency(sale.total_amount) }}</span>
              </div>
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
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProjectStore } from '../stores/projectStore'
import { formatCurrency, formatDate } from '../utils/formatters'
import ProjectForm from './ProjectForm.vue'

const router = useRouter()
const projectStore = useProjectStore()

const projects = ref([])
const loading = ref(false)
const error = ref(null)
const showCreateForm = ref(false)
const editingProject = ref(null)

const loadProjects = async () => {
  loading.value = true
  error.value = null
  try {
    await projectStore.fetchProjects()
    projects.value = projectStore.projects
  } catch (err) {
    error.value = 'Failed to load projects'
    console.error('Error loading projects:', err)
  } finally {
    loading.value = false
  }
}

const closeForm = () => {
  showCreateForm.value = false
  editingProject.value = null
}

const onFormSaved = async () => {
  await loadProjects()
  closeForm()
}

const editProject = (project) => {
  editingProject.value = project
  showCreateForm.value = true
}

const deleteProject = async (project) => {
  if (!confirm(`Are you sure you want to delete "${project.name}"? This will also delete all associated equipment sales.`)) {
    return
  }

  try {
    await projectStore.deleteProject(project.id)
    await loadProjects()
  } catch (err) {
    error.value = 'Failed to delete project'
    console.error('Error deleting project:', err)
  }
}

const viewProject = (project) => {
  router.push(`/chart?project=${project.id}`)
}

onMounted(() => {
  loadProjects()
})
</script>

<style scoped>
.projects-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.page-header h1 {
  color: #2c3e50;
  margin: 0;
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

.btn-primary:hover {
  background-color: #2980b9;
}

.form-container {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 2rem;
}

.loading {
  padding: 3rem;
  text-align: center;
  color: #7f8c8d;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.empty-state {
  padding: 3rem;
  text-align: center;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.empty-state h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #7f8c8d;
  margin-bottom: 2rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.15);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.project-header h3 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.25rem;
}

.project-actions {
  display: flex;
  gap: 0.5rem;
}

.btn-secondary {
  background-color: #95a5a6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-secondary:hover {
  background-color: #7f8c8d;
}

.btn-edit {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-edit:hover {
  background-color: #2980b9;
}

.btn-delete {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-delete:hover {
  background-color: #c0392b;
}

.project-details {
  padding: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item label {
  font-weight: 500;
  color: #2c3e50;
}

.detail-item span {
  color: #7f8c8d;
}

.total-value {
  font-weight: 600;
  color: #27ae60 !important;
}

.description {
  flex-direction: column;
  align-items: flex-start;
}

.description span {
  margin-top: 0.5rem;
  line-height: 1.5;
}

.equipment-sales {
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
  background: #f8f9fa;
}

.equipment-sales h4 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
  font-size: 1rem;
}

.sales-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.sale-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem;
  background: white;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.sale-name {
  font-weight: 500;
  color: #2c3e50;
}

.sale-type {
  font-size: 0.8rem;
  color: #7f8c8d;
  text-transform: capitalize;
}

.sale-amount {
  font-weight: 500;
  color: #27ae60;
}

.error-message {
  background-color: #e74c3c;
  color: white;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .project-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .project-actions {
    justify-content: center;
  }
  
  .sale-item {
    flex-direction: column;
    gap: 0.25rem;
    align-items: flex-start;
  }
}
</style>
