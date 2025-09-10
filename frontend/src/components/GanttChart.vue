<template>
  <div class="gantt-chart">
    <div class="chart-header">
      <h2>Payment Milestone Schedule</h2>
      <div class="chart-controls">
        <div class="view-toggle">
          <label>
            <input 
              type="radio" 
              v-model="viewMode" 
              value="projects" 
              @change="onViewModeChange"
            >
            Projects
          </label>
          <label>
            <input 
              type="radio"
              v-model="viewMode" 
              value="single" 
              @change="onViewModeChange"
            >
            Single Sales
          </label>
        </div>
        
        <select v-model="selectedId" @change="loadData" class="selector">
          <option value="">{{ viewMode === 'projects' ? 'Select a project' : 'Select an equipment sale' }}</option>
          <option 
            v-for="item in viewMode === 'projects' ? projects : equipmentSales" 
            :key="item.id" 
            :value="item.id"
          >
            {{ item.name }} - {{ formatCurrency(item.total_value || item.total_amount) }}
          </option>
        </select>
        
        <button @click="refreshChart" class="btn-secondary" :disabled="!selectedId">
          Refresh
        </button>
        
        <div class="action-buttons">
          <button @click="showCreateForm = true" class="btn-primary">
            {{ viewMode === 'projects' ? 'Create Project' : 'Create Sale' }}
          </button>
          <button v-if="viewMode === 'projects'" @click="createEquipmentSale" class="btn-primary">
            Create Sale
          </button>
          <button @click="showMilestoneForm = true" class="btn-primary">
            Create Milestones
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">
      Loading schedule data...
    </div>

    <div v-else-if="!selectedId" class="empty-state">
      <p>Please select a {{ viewMode === 'projects' ? 'project' : 'equipment sale' }} to view its payment milestone schedule.</p>
    </div>

    <div v-else-if="!chartData" class="empty-state">
      <p>No schedule data available for the selected {{ viewMode === 'projects' ? 'project' : 'sale' }}.</p>
    </div>

    <div v-else class="chart-container">
      <!-- Project/Sale Information -->
      <div class="info-section">
        <div class="info-header">
          <h3>{{ selectedItem.name }}</h3>
          <div class="info-actions">
            <button @click="editItem(selectedItem)" class="btn-edit">Edit</button>
            <button @click="deleteItem(selectedItem)" class="btn-delete">Delete</button>
          </div>
        </div>
        <div class="details">
          <span v-if="viewMode === 'projects'">
            <strong>Start Date:</strong> {{ formatDate(selectedItem.start_date) }}
          </span>
          <span v-if="viewMode === 'projects'">
            <strong>Equipment Sales:</strong> {{ selectedItem.equipment_sales_count }}
          </span>
          <span v-if="viewMode === 'single'">
            <strong>Vendor:</strong> {{ selectedItem.vendor || 'N/A' }}
          </span>
          <span v-if="viewMode === 'single'">
            <strong>Sale Type:</strong> {{ selectedItem.sale_type }}
          </span>
          <span>
            <strong>Quantity:</strong> {{ viewMode === 'projects' ? 'N/A' : selectedItem.quantity }}
          </span>
          <span>
            <strong>Total Amount:</strong> {{ formatCurrency(viewMode === 'projects' ? selectedItem.total_value : selectedItem.total_amount) }}
          </span>
          <span v-if="viewMode === 'single'">
            <strong>Unit Price:</strong> {{ formatCurrency(selectedItem.unit_price) }}
          </span>
          <span>
            <strong>Start Date:</strong> {{ formatDate(viewMode === 'projects' ? selectedItem.start_date : selectedItem.project_start_date) }}
          </span>
        </div>
      </div>

      <!-- Gantt Chart -->
      <div class="chart-wrapper">
        <highcharts 
          :constructorType="'ganttChart'" 
          class="chart" 
          :options="ganttOptions" 
          ref="chartContainer"
        ></highcharts>
      </div>
      
      <!-- Equipment Sale Details Table -->
      <div v-if="selectedItem && (viewMode === 'single' || (viewMode === 'projects' && selectedItem.equipment_sales?.length > 0))" class="equipment-sale-details">
        <h4>Equipment Sale Details</h4>
        
        <!-- Single Sale View - Vertical Table -->
        <div v-if="viewMode === 'single'" class="details-table">
          <div class="details-header">
            <span>Property</span>
            <span>Value</span>
          </div>
          <div class="details-row">
            <span class="property-name">Sale Name</span>
            <span>{{ selectedItem.name }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Vendor</span>
            <span>{{ selectedItem.vendor || 'N/A' }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Sale Type</span>
            <span>{{ selectedItem.sale_type }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Quantity</span>
            <span>{{ selectedItem.quantity }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Unit Price</span>
            <span class="amount">{{ formatCurrency(selectedItem.unit_price) }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Total Amount</span>
            <span class="amount">{{ formatCurrency(selectedItem.total_amount) }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Project Start Date</span>
            <span>{{ formatDate(selectedItem.project_start_date) }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Milestone Structure</span>
            <span>{{ selectedItem.milestone_structure?.name || 'None Assigned' }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Project</span>
            <span>{{ selectedItem.project?.name || 'Standalone Sale' }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Created</span>
            <span>{{ formatDate(selectedItem.created_at) }}</span>
          </div>
          <div class="details-row">
            <span class="property-name">Last Updated</span>
            <span>{{ formatDate(selectedItem.updated_at) }}</span>
          </div>
        </div>

        <!-- Projects View - Horizontal Table -->
        <div v-else-if="viewMode === 'projects'" class="equipment-sales-table">
          <div class="sales-header">
            <span>Sale Name</span>
            <span>Vendor</span>
            <span>Type</span>
            <span>Quantity</span>
            <span>Unit Price</span>
            <span>Total Amount</span>
            <span>Milestone Structure</span>
            <span>Actions</span>
          </div>
          <div 
            v-for="sale in equipmentSalesForProject" 
            :key="sale.id" 
            class="sales-row"
          >
            <span class="sale-name">{{ sale.name }}</span>
            <span>{{ sale.vendor || 'N/A' }}</span>
            <span>{{ sale.sale_type }}</span>
            <span>{{ sale.quantity }}</span>
            <span class="amount">{{ formatCurrency(sale.unit_price) }}</span>
            <span class="amount">{{ formatCurrency(sale.total_amount) }}</span>
            <span 
              v-if="sale.milestone_structure" 
              @click="viewMilestoneStructureDetails(sale.milestone_structure)" 
              class="milestone-structure-clickable"
              title="Click to view milestone details"
            >
              {{ sale.milestone_structure.name }}
            </span>
            <span v-else class="no-milestone">None</span>
            <span class="sale-actions">
              <button @click="editEquipmentSaleFromProjects(sale)" class="btn-edit-small" title="Edit sale">
                ✏️
              </button>
              <button @click="selectEquipmentSale(sale)" class="btn-info-small" title="View schedule">
                📊
              </button>
              <button v-if="!sale.milestone_structure" @click="assignMilestoneToSale(sale)" class="btn-secondary-small" title="Assign milestone">
                ⚙️
              </button>
            </span>
          </div>
          <!-- Add New Sale Row -->
          <div class="add-sale-row">
            <span class="add-sale-cell">
              <button @click="createEquipmentSaleFromProjects" class="btn-add-sale" title="Add new equipment sale">
                <span class="plus-icon">+</span>
                <span class="add-text">Add New Sale</span>
              </button>
            </span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>

    </div>

    <!-- Error Message -->
    <div v-if="error" class="error-message">
      {{ error }}
    </div>

    <!-- Create/Edit Forms -->
    <div v-if="showCreateForm" class="modal-overlay" @click="closeForm">
      <div class="modal-content" @click.stop>
        <ProjectForm 
          v-if="viewMode === 'projects'"
          :project="editingItem"
          :is-editing="!!editingItem"
          @close="closeForm"
          @saved="onFormSaved"
        />
        <EquipmentSaleForm 
          v-else
          :sale="editingItem"
          :is-editing="!!editingItem"
          @close="closeForm"
          @saved="onFormSaved"
        />
      </div>
    </div>

    <!-- Milestone Structure Form -->
    <div v-if="showMilestoneForm" class="modal-overlay" @click="closeMilestoneForm">
      <div class="modal-content" @click.stop>
        <MilestoneForm 
          :structure="editingMilestoneStructure"
          :is-editing="!!editingMilestoneStructure"
          @close="closeMilestoneForm"
          @saved="onMilestoneFormSaved"
        />
      </div>
    </div>

    <!-- Milestone Assignment Modal -->
    <div v-if="showMilestoneAssignment" class="modal-overlay" @click="closeMilestoneAssignment">
      <div class="modal-content" @click.stop>
        <div class="milestone-assignment-form">
          <div class="form-header">
            <h3>Assign Milestone Structure to {{ selectedSaleForMilestone?.name }}</h3>
            <button @click="closeMilestoneAssignment" class="btn-close">×</button>
          </div>
          <div class="form-content">
            <div class="form-group">
              <label for="milestone-structure">Select Milestone Structure</label>
              <select id="milestone-structure" v-model="selectedMilestoneStructureId">
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
            <div class="form-actions">
              <button @click="closeMilestoneAssignment" class="btn-secondary">Cancel</button>
              <button @click="assignMilestone" class="btn-primary" :disabled="!selectedMilestoneStructureId">
                Assign
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Milestone Details Modal -->
    <div v-if="showMilestoneDetails" class="modal-overlay" @click="closeMilestoneDetails">
      <div class="modal-content" @click.stop>
        <div class="milestone-details-form">
          <div class="form-header">
            <h3>{{ isEditingMilestone ? 'Edit' : 'View' }} Milestone Details</h3>
            <button @click="closeMilestoneDetails" class="btn-close">×</button>
          </div>
          <div class="form-content">
            <div v-if="!isEditingMilestone" class="milestone-info">
              <div class="info-row">
                <label>Milestone Name:</label>
                <span>{{ selectedMilestoneDetails?.milestone_name || selectedMilestoneDetails?.name }}</span>
              </div>
              <div class="info-row">
                <label>Payment Amount:</label>
                <span>{{ formatCurrency(selectedMilestoneDetails?.payment_amount) }}</span>
              </div>
              <div class="info-row">
                <label>Payment Percentage:</label>
                <span>{{ selectedMilestoneDetails?.payment_percentage }}%</span>
              </div>
              <div class="info-row">
                <label>Due Date:</label>
                <span>{{ formatDate(selectedMilestoneDetails?.due_date) }}</span>
              </div>
              <div class="info-row">
                <label>Payment Due Date:</label>
                <span>{{ formatDate(selectedMilestoneDetails?.payment_due_date) }}</span>
              </div>
              <div v-if="viewMode === 'projects'" class="info-row">
                <label>Equipment Sale:</label>
                <span>{{ selectedMilestoneDetails?.sale_name }}</span>
              </div>
            </div>
            
            <div v-else class="milestone-edit-form">
              <div class="form-group">
                <label for="milestone-name">Milestone Name</label>
                <input 
                  type="text" 
                  id="milestone-name" 
                  v-model="milestoneEditData.name"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="payment-amount">Payment Amount</label>
                <input 
                  type="number" 
                  id="payment-amount" 
                  v-model.number="milestoneEditData.payment_amount"
                  step="0.01"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="payment-percentage">Payment Percentage</label>
                <input 
                  type="number" 
                  id="payment-percentage" 
                  v-model.number="milestoneEditData.payment_percentage"
                  step="0.01"
                  min="0"
                  max="100"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="due-date">Due Date</label>
                <input 
                  type="date" 
                  id="due-date" 
                  v-model="milestoneEditData.due_date"
                  class="form-input"
                />
              </div>
              <div class="form-group">
                <label for="payment-due-date">Payment Due Date</label>
                <input 
                  type="date" 
                  id="payment-due-date" 
                  v-model="milestoneEditData.payment_due_date"
                  class="form-input"
                />
              </div>
            </div>
            
            <div class="form-actions">
              <button @click="closeMilestoneDetails" class="btn-secondary">
                {{ isEditingMilestone ? 'Cancel' : 'Close' }}
              </button>
              <button v-if="!isEditingMilestone" @click="startEditingMilestone" class="btn-primary">
                Edit
              </button>
              <button v-if="isEditingMilestone" @click="saveMilestoneChanges" class="btn-primary">
                Save Changes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Equipment Sale Modal -->
    <div v-if="showEditSaleModal" class="modal-overlay" @click="closeEditSaleModal">
      <div class="modal-content" @click.stop>
        <EquipmentSaleForm 
          :sale="editingItem"
          :is-editing="true"
          @close="closeEditSaleModal"
          @saved="onEditSaleSaved"
        />
      </div>
    </div>

    <!-- Create Equipment Sale Modal -->
    <div v-if="showCreateSaleModal" class="modal-overlay" @click="closeCreateSaleModal">
      <div class="modal-content" @click.stop>
        <EquipmentSaleForm 
          :sale="null"
          :is-editing="false"
          :project="creatingFromProjects ? selectedItem : null"
          @close="closeCreateSaleModal"
          @saved="onCreateSaleSaved"
        />
      </div>
    </div>

    <!-- Milestone Structure Details Modal -->
    <div v-if="showMilestoneStructureDetails" class="modal-overlay" @click="closeMilestoneStructureDetails">
      <div class="modal-content" @click.stop>
        <div class="milestone-structure-details-form">
          <div class="form-header">
            <h3>{{ selectedMilestoneStructure?.name }} - Milestone Details</h3>
            <button @click="closeMilestoneStructureDetails" class="btn-close">×</button>
          </div>
          <div class="form-content">
            <div v-if="selectedMilestoneStructure" class="milestone-structure-info">
              <div class="structure-summary">
                <div class="info-row">
                  <label>Structure Name:</label>
                  <span>{{ selectedMilestoneStructure.name }}</span>
                </div>
                <div class="info-row">
                  <label>Total Milestones:</label>
                  <span>{{ selectedMilestoneStructure.milestones?.length || 0 }}</span>
                </div>
                <div class="info-row">
                  <label>Total Percentage:</label>
                  <span>{{ selectedMilestoneStructure.milestones?.reduce((sum, m) => sum + (m.payment_percentage || 0), 0) || 0 }}%</span>
                </div>
              </div>
              
              <div class="milestones-list">
                <h4>Milestone Breakdown</h4>
                <div v-if="selectedMilestoneStructure.milestones?.length > 0" class="milestones-table">
                  <div class="milestones-header">
                    <span>Milestone Name</span>
                    <span>Payment %</span>
                    <span>Days After Previous</span>
                    <span>Net Terms</span>
                  </div>
                  <div 
                    v-for="milestone in selectedMilestoneStructure.milestones" 
                    :key="milestone.id" 
                    class="milestones-row"
                  >
                    <span class="milestone-name">{{ milestone.name }}</span>
                    <span class="milestone-percentage">{{ milestone.payment_percentage }}%</span>
                    <span class="milestone-days">{{ milestone.days_after_previous }} days</span>
                    <span class="milestone-terms">{{ milestone.net_terms_days || 0 }} days</span>
                  </div>
                </div>
                <div v-else class="no-milestones">
                  <p>No milestones defined for this structure.</p>
                </div>
              </div>
            </div>
            
            <div class="form-actions">
              <button @click="closeMilestoneStructureDetails" class="btn-secondary">Close</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEquipmentStore } from '../stores/equipmentStore'
import { useProjectStore } from '../stores/projectStore'
import { useMilestoneStore } from '../stores/milestoneStore'
import { formatCurrency, formatDate } from '../utils/formatters'
import ProjectForm from './ProjectForm.vue'
import EquipmentSaleForm from './EquipmentSaleForm.vue'
import MilestoneForm from './MilestoneForm.vue'

const route = useRoute()
const router = useRouter()
const equipmentStore = useEquipmentStore()
const projectStore = useProjectStore()
const milestoneStore = useMilestoneStore()

const chartContainer = ref(null)
const ganttOptions = ref(null)

const viewMode = ref('projects') // 'single' or 'projects'
const selectedId = ref('')

// LocalStorage keys
const STORAGE_KEYS = {
  VIEW_MODE: 'gantt-chart-view-mode',
  SELECTED_ID: 'gantt-chart-selected-id'
}

// Persistence functions
const saveToLocalStorage = (key, value) => {
  try {
    localStorage.setItem(key, value)
  } catch (error) {
    console.warn('Failed to save to localStorage:', error)
  }
}

const loadFromLocalStorage = (key, defaultValue = '') => {
  try {
    return localStorage.getItem(key) || defaultValue
  } catch (error) {
    console.warn('Failed to load from localStorage:', error)
    return defaultValue
  }
}


const updateUrlParams = () => {
  const query = {}
  if (selectedId.value) {
    if (viewMode.value === 'projects') {
      query.project = selectedId.value
    } else {
      query.sale = selectedId.value
    }
  }
  
  // Update URL without triggering navigation
  router.replace({ query })
}

// Watchers for persistence
watch(viewMode, (newValue) => {
  saveToLocalStorage(STORAGE_KEYS.VIEW_MODE, newValue)
  updateUrlParams()
})

watch(selectedId, (newValue) => {
  saveToLocalStorage(STORAGE_KEYS.SELECTED_ID, newValue)
  updateUrlParams()
})


// Watch for route changes to handle navigation
watch(() => route.query, async (newQuery) => {
  const saleId = newQuery.sale
  const projectId = newQuery.project
  
  if (projectId && projectId !== selectedId.value) {
    viewMode.value = 'projects'
    selectedId.value = projectId
    await loadData()
  } else if (saleId && saleId !== selectedId.value) {
    viewMode.value = 'single'
    selectedId.value = saleId
    await loadData()
  }
}, { immediate: false })
const loading = ref(false)
const error = ref(null)
const chartData = ref(null)
const equipmentSales = ref([])
const projects = ref([])
const milestoneStructures = ref([])

// Form states
const showCreateForm = ref(false)
const showMilestoneForm = ref(false)
const showMilestoneAssignment = ref(false)
const showEditSaleModal = ref(false)
const showCreateSaleModal = ref(false)
const editingItem = ref(null)
const editingMilestoneStructure = ref(null)
const selectedSaleForMilestone = ref(null)
const selectedMilestoneStructureId = ref('')
const editingFromProjects = ref(false)
const creatingFromProjects = ref(false)

// List visibility states
const showQuickActions = ref(false)
const showProjectList = ref(false)
const showEquipmentList = ref(false)
const showMilestoneList = ref(false)

// Milestone details modal states
const showMilestoneDetails = ref(false)
const selectedMilestoneDetails = ref(null)
const isEditingMilestone = ref(false)
const milestoneEditData = ref({
  name: '',
  payment_amount: 0,
  payment_percentage: 0,
  due_date: '',
  payment_due_date: ''
})

// Milestone structure details modal states
const showMilestoneStructureDetails = ref(false)
const selectedMilestoneStructure = ref(null)




const selectedItem = computed(() => {
  if (viewMode.value === 'projects') {
    return projects.value.find(project => project.id === parseInt(selectedId.value))
  } else {
    return equipmentSales.value.find(sale => sale.id === parseInt(selectedId.value))
  }
})
const equipmentSalesForProject = computed(() => {
  const project = projects.value.find(project => project.id === parseInt(selectedId.value))
  return project?.equipment_sales || []
})




const loadEquipmentSales = async () => {
  try {
    await equipmentStore.fetchEquipmentSales()
    equipmentSales.value = equipmentStore.equipmentSales
  } catch (err) {
    error.value = 'Failed to load equipment sales'
    console.error('Error loading equipment sales:', err)
  }
}

const loadProjects = async () => {
  try {
    await projectStore.fetchProjects()
    projects.value = projectStore.projects
  } catch (err) {
    error.value = 'Failed to load projects'
    console.error('Error loading projects:', err)
  }
}

const loadMilestoneStructures = async () => {
  try {
    await milestoneStore.fetchMilestoneStructures()
    milestoneStructures.value = milestoneStore.milestoneStructures
  } catch (err) {
    error.value = 'Failed to load milestone structures'
    console.error('Error loading milestone structures:', err)
  }
}

const loadData = async () => {
  if (!selectedId.value) {
    chartData.value = null
    return
  }

  loading.value = true
  error.value = null

  try {
    if (viewMode.value === 'projects') {
      const data = await projectStore.getProjectTimeline(selectedId.value)
      console.log('Project timeline data:', data)
      chartData.value = data
    } else {
      const data = await equipmentStore.getEquipmentSaleSchedule(selectedId.value)
      chartData.value = data
    }
    await nextTick()
    createGanttChart()
  } catch (err) {
    error.value = `Failed to load ${viewMode.value === 'projects' ? 'project' : 'sale'} data`
    console.error('Error loading data:', err)
  } finally {
    loading.value = false
  }
}

const onViewModeChange = () => {
  // Don't clear selectedId when changing view modes - let user keep their selection
  chartData.value = null
  ganttOptions.value = null
}

const refreshChart = () => {
  if (selectedId.value) {
    loadData()
  }
}

const closeForm = () => {
  showCreateForm.value = false
  editingItem.value = null
}

const onFormSaved = async () => {
  // Reload data after form is saved
  if (viewMode.value === 'projects') {
    await loadProjects()
  } else {
    await loadEquipmentSales()
  }
  
  // Refresh chart if we have a selected item
  if (selectedId.value) {
    await loadData()
  }
  
  // Close any open lists to show the updated chart
  showProjectList.value = false
  showEquipmentList.value = false
}

const editItem = (item) => {
  editingItem.value = item
  showCreateForm.value = true
}

const deleteItem = async (item) => {
  if (!confirm(`Are you sure you want to delete "${item.name}"?`)) {
    return
  }

  try {
    if (viewMode.value === 'projects') {
      await projectStore.deleteProject(item.id)
      await loadProjects()
    } else {
      await equipmentStore.deleteEquipmentSale(item.id)
      await loadEquipmentSales()
    }
    
    // Clear selection if we deleted the currently selected item
    if (selectedId.value == item.id) {
      selectedId.value = ''
      chartData.value = null
    }
  } catch (err) {
    error.value = `Failed to delete ${viewMode.value === 'projects' ? 'project' : 'sale'}`
    console.error('Error deleting item:', err)
  }
}

// Project CRUD methods
const createProject = () => {
  editingItem.value = null
  showCreateForm.value = true
}

const editProject = (project) => {
  editingItem.value = project
  viewMode.value = 'projects'
  showCreateForm.value = true
}

const deleteProject = async (project) => {
  if (!confirm(`Are you sure you want to delete project "${project.name}"?`)) {
    return
  }

  try {
    await projectStore.deleteProject(project.id)
    await loadProjects()
    
    // Clear selection if we deleted the currently selected item
    if (selectedId.value == project.id) {
      selectedId.value = ''
      chartData.value = null
    }
  } catch (err) {
    error.value = 'Failed to delete project'
    console.error('Error deleting project:', err)
  }
}

const selectProject = (project) => {
  viewMode.value = 'projects'
  selectedId.value = project.id
  showProjectList.value = false
  loadData()
}

// Equipment Sale CRUD methods
const createEquipmentSale = () => {
  editingItem.value = null
  viewMode.value = 'single'
  showCreateForm.value = true
}

const editEquipmentSale = (sale) => {
  editingItem.value = sale
  viewMode.value = 'single'
  showCreateForm.value = true
}

const editEquipmentSaleFromProjects = (sale) => {
  editingItem.value = sale
  editingFromProjects.value = true
  showEditSaleModal.value = true
}

const createEquipmentSaleFromProjects = () => {
  editingItem.value = null
  creatingFromProjects.value = true
  showCreateSaleModal.value = true
}

const deleteEquipmentSale = async (sale) => {
  if (!confirm(`Are you sure you want to delete equipment sale "${sale.name}"?`)) {
    return
  }

  try {
    await equipmentStore.deleteEquipmentSale(sale.id)
    await loadEquipmentSales()
    
    // Clear selection if we deleted the currently selected item
    if (selectedId.value == sale.id) {
      selectedId.value = ''
      chartData.value = null
    }
  } catch (err) {
    error.value = 'Failed to delete equipment sale'
    console.error('Error deleting equipment sale:', err)
  }
}

const selectEquipmentSale = (sale) => {
  viewMode.value = 'single'
  selectedId.value = sale.id
  showEquipmentList.value = false
  loadData()
}

// Milestone Structure CRUD methods
const createMilestoneStructure = () => {
  editingMilestoneStructure.value = null
  showMilestoneForm.value = true
}

const editMilestoneStructure = (structure) => {
  editingMilestoneStructure.value = structure
  showMilestoneForm.value = true
}

const deleteMilestoneStructure = async (structure) => {
  if (!confirm(`Are you sure you want to delete milestone structure "${structure.name}"?`)) {
    return
  }

  try {
    await milestoneStore.deleteMilestoneStructure(structure.id)
    await loadMilestoneStructures()
  } catch (err) {
    error.value = 'Failed to delete milestone structure'
    console.error('Error deleting milestone structure:', err)
  }
}

// Milestone Assignment methods
const assignMilestoneToSale = (sale) => {
  selectedSaleForMilestone.value = sale
  selectedMilestoneStructureId.value = ''
  showMilestoneAssignment.value = true
}

const assignMilestone = async () => {
  if (!selectedMilestoneStructureId.value || !selectedSaleForMilestone.value) {
    return
  }

  try {
    await equipmentStore.assignMilestoneStructure(
      selectedSaleForMilestone.value.id,
      selectedMilestoneStructureId.value
    )
    await loadEquipmentSales()
    closeMilestoneAssignment()
    
    // If this was the currently selected sale, refresh the chart
    if (selectedId.value == selectedSaleForMilestone.value.id) {
      await loadData()
    }
  } catch (err) {
    error.value = 'Failed to assign milestone structure'
    console.error('Error assigning milestone structure:', err)
  }
}

// Form close methods
const closeMilestoneForm = () => {
  showMilestoneForm.value = false
  editingMilestoneStructure.value = null
}

const closeMilestoneAssignment = () => {
  showMilestoneAssignment.value = false
  selectedSaleForMilestone.value = null
  selectedMilestoneStructureId.value = ''
}

const onMilestoneFormSaved = async () => {
  await loadMilestoneStructures()
  closeMilestoneForm()
}

// Milestone details methods
const editMilestoneDetails = (milestone) => {
  selectedMilestoneDetails.value = milestone
  isEditingMilestone.value = true
  milestoneEditData.value = {
    name: milestone.milestone_name || milestone.name,
    payment_amount: milestone.payment_amount,
    payment_percentage: milestone.payment_percentage,
    due_date: milestone.due_date,
    payment_due_date: milestone.payment_due_date
  }
  showMilestoneDetails.value = true
}

const viewMilestoneDetails = (milestone) => {
  selectedMilestoneDetails.value = milestone
  isEditingMilestone.value = false
  showMilestoneDetails.value = true
}

const startEditingMilestone = () => {
  isEditingMilestone.value = true
  milestoneEditData.value = {
    name: selectedMilestoneDetails.value.milestone_name || selectedMilestoneDetails.value.name,
    payment_amount: selectedMilestoneDetails.value.payment_amount,
    payment_percentage: selectedMilestoneDetails.value.payment_percentage,
    due_date: selectedMilestoneDetails.value.due_date,
    payment_due_date: selectedMilestoneDetails.value.payment_due_date
  }
}

const saveMilestoneChanges = async () => {
  try {
    // Note: This would require backend API support for updating individual milestones
    // For now, we'll just show a message that this feature requires backend support
    alert('Milestone editing requires backend API support. This feature is ready for implementation.')
    
    // Close the modal
    closeMilestoneDetails()
    
    // Refresh the chart data
    if (selectedId.value) {
      await loadData()
    }
  } catch (err) {
    error.value = 'Failed to update milestone'
    console.error('Error updating milestone:', err)
  }
}

const closeMilestoneDetails = () => {
  showMilestoneDetails.value = false
  selectedMilestoneDetails.value = null
  isEditingMilestone.value = false
  milestoneEditData.value = {
    name: '',
    payment_amount: 0,
    payment_percentage: 0,
    due_date: '',
    payment_due_date: ''
  }
}

// Milestone structure details methods
const viewMilestoneStructureDetails = (milestoneStructure) => {
  selectedMilestoneStructure.value = milestoneStructure
  showMilestoneStructureDetails.value = true
}

const closeMilestoneStructureDetails = () => {
  showMilestoneStructureDetails.value = false
  selectedMilestoneStructure.value = null
}

const closeEditSaleModal = () => {
  showEditSaleModal.value = false
  editingItem.value = null
  editingFromProjects.value = false
}

const closeCreateSaleModal = () => {
  showCreateSaleModal.value = false
  editingItem.value = null
  creatingFromProjects.value = false
}

const onEditSaleSaved = async () => {
  // Reload data after sale is saved
  if (editingFromProjects.value) {
    // If editing from projects, reload both projects and equipment sales data
    await Promise.all([
      loadProjects(),
      loadEquipmentSales()
    ])
    // Force Vue to re-evaluate computed properties
    await nextTick()
    // Refresh chart if we have a selected project
    if (selectedId.value) {
      await loadData()
    }
  } else {
    // If editing from equipment sales list, reload equipment sales
    await loadEquipmentSales()
    // Force Vue to re-evaluate computed properties
    await nextTick()
    // Refresh chart if we have a selected sale
    if (selectedId.value) {
      await loadData()
    }
  }
  
  closeEditSaleModal()
}

const onCreateSaleSaved = async () => {
  // Reload data after sale is created
  if (creatingFromProjects.value) {
    // If creating from projects, reload both projects and equipment sales data
    await Promise.all([
      loadProjects(),
      loadEquipmentSales()
    ])
    // Force Vue to re-evaluate computed properties
    await nextTick()
    // Refresh chart if we have a selected project
    if (selectedId.value) {
      await loadData()
    }
  } else {
    // If creating from equipment sales list, reload equipment sales
    await loadEquipmentSales()
    // Force Vue to re-evaluate computed properties
    await nextTick()
    // Refresh chart if we have a selected sale
    if (selectedId.value) {
      await loadData()
    }
  }
  
  closeCreateSaleModal()
}

const createGanttChart = () => {
  if (!chartData.value) return
  
  const milestones = chartData.value.milestone_schedule || chartData.value.project_timeline
  if (!milestones || !Array.isArray(milestones)) return
  
  const startDate = new Date(chartData.value.start_date || chartData.value.project_start_date)

  // Group milestones by equipment sale
  const groupedBySale = {}
  milestones.forEach((milestone, index) => {
    const saleId = milestone.sale_id || 'standalone'
    const saleName = milestone.sale_name || 'Standalone Sale'
    
    if (!groupedBySale[saleId]) {
      groupedBySale[saleId] = {
        saleId: saleId,
        saleName: saleName,
        milestones: []
      }
    }
    groupedBySale[saleId].milestones.push({ ...milestone, originalIndex: index })
  })

  // Create series data in the correct Highcharts Gantt format
  const series = Object.values(groupedBySale).map((saleGroup) => {
    const saleParentId = `sale-${saleGroup.saleId}`
    
    // Create the series data array starting with the parent equipment sale
    const seriesData = [
      {
        name: saleGroup.saleName,
        id: saleParentId,
        pointWidth: 3, // Smaller width for parent task
        color: '#95a5a6' // Gray color for parent rows
      }
    ]
    
    // Add milestones as children with parent references
    saleGroup.milestones.forEach((milestone) => {
      const startDateMs = new Date(startDate.getTime() + (milestone.start_days || 0) * 24 * 60 * 60 * 1000)
      const endDateMs = new Date(startDate.getTime() + (milestone.end_days || 0) * 24 * 60 * 60 * 1000)
      
      // Validate dates
      if (isNaN(startDateMs.getTime()) || isNaN(endDateMs.getTime())) {
        console.warn('Invalid milestone dates:', milestone)
        return
      }

      seriesData.push({
        parent: saleParentId,
        id: `milestone-${milestone.milestone_id || milestone.id}`,
        name: milestone.milestone_name || milestone.name,
        start: startDateMs.getTime(),
        end: endDateMs.getTime(),
        completed: {
          amount: 0 // No completion tracking for now
        },
        color: getMilestoneColor(milestone.originalIndex),
        saleName: milestone.sale_name || null,
        milestoneData: milestone
      })
    })
    
    return {
      name: saleGroup.saleName,
      data: seriesData
    }
  })

  // Calculate dynamic height based on number of rows (sales + milestones)
  const baseHeight = 200
  const heightPerRow = 50
  const totalRows = Object.keys(groupedBySale).length + milestones.length
  const chartHeight = Math.max(baseHeight, totalRows * heightPerRow)

  // Create the chart
  ganttOptions.value = {
    title: {
      text: viewMode.value === 'projects' ? 'Project Timeline - Grouped by Equipment Sales' : 'Equipment Sale Timeline - Grouped by Milestones'
    },
    subtitle: {
      text: `${selectedItem.value.name} - Payment Schedule`
    },
    accessibility: {
      enabled: false
    },
    chart: {
      height: chartHeight,
      scrollablePlotArea: {
        minWidth: 800,
        scrollPositionX: 1
      }
    },
    xAxis: {
      type: 'datetime',
      title: {
        text: 'Timeline'
      }
    },
    yAxis: {
      title: {
        text: viewMode.value === 'projects' ? 'Equipment Sales & Milestones' : 'Milestones'
      }
    },
    tooltip: {
      formatter: function() {
        // Handle parent rows (equipment sales)
        if (!this.point.start && !this.point.end) {
          return `<b>${this.point.name}</b><br/>Equipment Sale`
        }
        
        // Handle child rows (milestones)
        const milestone = this.point.milestoneData
        if (!milestone) return ''

        const startDate = new Date(this.point.start)
        const endDate = new Date(this.point.end)
        
        return `
          <b>${milestone.sale_name}</b><br/>
          <b>${this.point.name}</b><br/>
          Start: ${startDate.toLocaleDateString()}<br/>
          End: ${endDate.toLocaleDateString()}<br/>
          Payment: ${formatCurrency(milestone.payment_amount)} (${milestone.payment_percentage}%)<br/>
          Due: ${formatDate(milestone.payment_due_date)}
        `
      }
    },
    series: series,
    plotOptions: {
      gantt: {
        dataLabels: {
          enabled: true,
          formatter: function() {
            // Don't show labels on parent rows
            if (!this.point.start && !this.point.end) {
              return ''
            }
            
            const milestone = this.point.milestoneData
            return milestone ? formatCurrency(milestone.payment_amount, '$', 0) : ''
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
  await Promise.all([
    loadEquipmentSales(),
    loadProjects(),
    loadMilestoneStructures()
  ])
  
  // Check URL parameters first (highest priority)
  const saleId = route.query.sale
  const projectId = route.query.project
  
  if (projectId) {
    viewMode.value = 'projects'
    selectedId.value = projectId
    await loadData()
  } else if (saleId) {
    viewMode.value = 'single'
    selectedId.value = saleId
    await loadData()
  } else {
    // If no URL params, restore from localStorage
    const savedViewMode = loadFromLocalStorage(STORAGE_KEYS.VIEW_MODE, 'projects')
    const savedSelectedId = loadFromLocalStorage(STORAGE_KEYS.SELECTED_ID, '')
    
    viewMode.value = savedViewMode
    selectedId.value = savedSelectedId
    
    // Load data if we have a saved selection
    if (savedSelectedId) {
      await loadData()
    }
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
  flex-wrap: wrap;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.view-toggle {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.view-toggle label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  font-size: 0.9rem;
}

.view-toggle input[type="radio"] {
  margin: 0;
}

.selector {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  min-width: 250px;
}

.selector:focus {
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

.info-section {
  padding: 1.5rem;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.info-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.info-header h3 {
  color: #2c3e50;
  margin: 0;
}

.info-actions {
  display: flex;
  gap: 0.5rem;
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

.btn-primary {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.details {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.details span {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.chart-wrapper {
  padding: 1rem;
  overflow: auto;
  max-height: 80vh;
}

.chart {
  min-height: 300px;
  width: 100%;
}

.equipment-sale-details {
  padding: 1.5rem;
  border-top: 1px solid #e9ecef;
}

.equipment-sale-details h4 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.details-table {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 0.5rem;
  overflow-x: auto;
}

.details-header {
  display: contents;
}

.details-header span {
  font-weight: 600;
  color: #2c3e50;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
  text-align: left;
}

.details-row {
  display: contents;
}

.details-row span {
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e9ecef;
  text-align: left;
}

.property-name {
  font-weight: 500;
  color: #2c3e50;
  background: #f8f9fa;
}

.equipment-sales-table {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr 1.5fr 1fr;
  gap: 0.5rem;
  overflow-x: auto;
}

.sales-header {
  display: contents;
}

.sales-header span {
  font-weight: 600;
  color: #2c3e50;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
  text-align: center;
}

.sales-row {
  display: contents;
}

.sales-row span {
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e9ecef;
  text-align: center;
}


.sale-name {
  text-align: left !important;
  font-weight: 500;
  color: #2c3e50;
}

.sale-actions {
  display: flex;
  gap: 0.25rem;
  justify-content: center;
}

.btn-secondary-small {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  border-radius: 3px;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-secondary-small:hover {
  background-color: #95a5a6;
}

.add-sale-row {
  display: contents;
}

.add-sale-cell {
  grid-column: 1 / -1;
  padding: 1rem 0.5rem;
  text-align: center;
  border-bottom: 1px solid #e9ecef;
}

.btn-add-sale {
  background: linear-gradient(135deg, #3498db, #2980b9);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
}

.btn-add-sale:hover {
  background: linear-gradient(135deg, #2980b9, #1f5f8b);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
}

.plus-icon {
  font-size: 1.2rem;
  font-weight: bold;
  line-height: 1;
}

.add-text {
  font-size: 0.9rem;
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
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .chart-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .chart-controls {
    justify-content: center;
    flex-direction: column;
  }
  
  .view-toggle {
    justify-content: center;
  }
  
  .details {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .details-table {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .details-header,
  .details-row {
    display: block;
  }
  
  .details-header span,
  .details-row span {
    display: block;
    text-align: left;
    border-bottom: none;
    border-right: none;
  }
  
  .details-header span {
    background: #f8f9fa;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .equipment-sales-table {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .sales-header,
  .sales-row {
    display: block;
  }
  
  .sales-header span,
  .sales-row span {
    display: block;
    text-align: left;
    border-bottom: none;
    border-right: none;
  }
  
  .sales-header span {
    background: #f8f9fa;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }

  .sale-actions {
    justify-content: flex-start;
  }

  .add-sale-cell {
    grid-column: 1;
    padding: 0.75rem 0.5rem;
  }

  .btn-add-sale {
    width: 100%;
    justify-content: center;
    padding: 0.75rem 1rem;
  }

}

/* Quick Actions Panel */
.quick-actions-panel {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.quick-actions-panel h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.quick-action-card {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.quick-action-card h4 {
  color: #2c3e50;
  margin: 0 0 0.5rem 0;
  font-size: 1rem;
}

.quick-actions {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

/* Entity Lists */
.entity-list {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.entity-list h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.entity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
}

.entity-card {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 4px;
  padding: 1rem;
  transition: box-shadow 0.2s;
}

.entity-card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.entity-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.75rem;
}

.entity-header h4 {
  color: #2c3e50;
  margin: 0;
  font-size: 1.1rem;
}

.entity-actions {
  display: flex;
  gap: 0.25rem;
  flex-wrap: wrap;
}

.entity-details {
  color: #7f8c8d;
  font-size: 0.9rem;
}

.entity-details p {
  margin: 0.25rem 0;
}

.entity-details strong {
  color: #2c3e50;
}

.milestones-preview {
  margin-top: 0.5rem;
}

.milestone-item {
  padding: 0.25rem 0;
  font-size: 0.85rem;
  color: #7f8c8d;
}

/* Milestone Assignment Form */
.milestone-assignment-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 500px;
  margin: 0 auto;
}

.milestone-assignment-form .form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.milestone-assignment-form .form-header h3 {
  margin: 0;
  color: #2c3e50;
}

.milestone-assignment-form .form-content {
  padding: 1.5rem;
}

.milestone-assignment-form .form-group {
  margin-bottom: 1.5rem;
}

.milestone-assignment-form .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.milestone-assignment-form .form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.milestone-assignment-form .form-group select:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.milestone-assignment-form .form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

/* Milestone Details Modal */
.milestone-details-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.milestone-details-form .form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.milestone-details-form .form-header h3 {
  margin: 0;
  color: #2c3e50;
}

.milestone-details-form .form-content {
  padding: 1.5rem;
}

.milestone-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #f1f2f6;
}

.info-row:last-child {
  border-bottom: none;
}

.info-row label {
  font-weight: 500;
  color: #2c3e50;
  min-width: 150px;
}

.info-row span {
  color: #7f8c8d;
  text-align: right;
}

.milestone-edit-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.milestone-edit-form .form-group {
  margin-bottom: 1rem;
}

.milestone-edit-form .form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: #2c3e50;
}

.milestone-edit-form .form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.milestone-edit-form .form-input:focus {
  outline: none;
  border-color: #3498db;
  box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
}

.milestone-details-form .form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

/* Milestone Actions in Summary Table */
.milestone-actions {
  display: flex;
  gap: 0.25rem;
  justify-content: center;
}

.btn-edit-small,
.btn-info-small {
  background: none;
  border: none;
  padding: 0.25rem;
  cursor: pointer;
  border-radius: 3px;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.btn-edit-small:hover {
  background-color: #3498db;
}

.btn-info-small:hover {
  background-color: #95a5a6;
}

/* Milestone Structure Clickable */
.milestone-structure-clickable {
  color: #3498db;
  cursor: pointer;
  text-decoration: underline;
  transition: color 0.2s;
}

.milestone-structure-clickable:hover {
  color: #2980b9;
}

.no-milestone {
  color: #e74c3c;
  font-style: italic;
}

/* Milestone Structure Details Modal */
.milestone-structure-details-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 0 auto;
}

.milestone-structure-details-form .form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e9ecef;
}

.milestone-structure-details-form .form-header h3 {
  margin: 0;
  color: #2c3e50;
}

.milestone-structure-details-form .form-content {
  padding: 1.5rem;
}

.milestone-structure-info {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.structure-summary {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 4px;
  border: 1px solid #e9ecef;
}

.structure-summary .info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
  border-bottom: 1px solid #e9ecef;
}

.structure-summary .info-row:last-child {
  border-bottom: none;
}

.structure-summary .info-row label {
  font-weight: 500;
  color: #2c3e50;
  min-width: 150px;
}

.structure-summary .info-row span {
  color: #7f8c8d;
  text-align: right;
}

.milestones-list h4 {
  color: #2c3e50;
  margin: 0 0 1rem 0;
}

.milestones-table {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 0.5rem;
  overflow-x: auto;
}

.milestones-header {
  display: contents;
}

.milestones-header span {
  font-weight: 600;
  color: #2c3e50;
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 4px;
  text-align: center;
}

.milestones-row {
  display: contents;
}

.milestones-row span {
  padding: 0.75rem 0.5rem;
  border-bottom: 1px solid #e9ecef;
  text-align: center;
}

.milestones-row .milestone-name {
  text-align: left !important;
  font-weight: 500;
  color: #2c3e50;
}

.milestones-row .milestone-percentage {
  color: #27ae60;
  font-weight: 500;
}

.milestones-row .milestone-days {
  color: #7f8c8d;
}

.milestones-row .milestone-terms {
  color: #7f8c8d;
}

.no-milestones {
  text-align: center;
  padding: 2rem;
  color: #7f8c8d;
  font-style: italic;
}

.milestone-structure-details-form .form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .quick-actions-grid {
    grid-template-columns: 1fr;
  }
  
  .entity-grid {
    grid-template-columns: 1fr;
  }
  
  .entity-header {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }
  
  .entity-actions {
    justify-content: flex-start;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: stretch;
  }

  .milestones-table {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .milestones-header,
  .milestones-row {
    display: block;
  }
  
  .milestones-header span,
  .milestones-row span {
    display: block;
    text-align: left;
    border-bottom: none;
    border-right: none;
  }
  
  .milestones-header span {
    background: #f8f9fa;
    font-weight: 600;
    margin-bottom: 0.25rem;
  }
}
</style>