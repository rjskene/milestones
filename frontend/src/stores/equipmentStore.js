import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export const useEquipmentStore = defineStore('equipment', {
  state: () => ({
    equipmentSales: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchEquipmentSales() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/equipment/sales/`)
        this.equipmentSales = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch equipment sales'
        console.error('Error fetching equipment sales:', error)
      } finally {
        this.loading = false
      }
    },

    async createEquipmentSale(saleData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_BASE}/equipment/sales/`, saleData)
        this.equipmentSales.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create equipment sale'
        console.error('Error creating equipment sale:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateEquipmentSale(id, saleData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.put(`${API_BASE}/equipment/sales/${id}/`, saleData)
        const index = this.equipmentSales.findIndex(s => s.id === id)
        if (index !== -1) {
          this.equipmentSales[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update equipment sale'
        console.error('Error updating equipment sale:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteEquipmentSale(id) {
      this.loading = true
      this.error = null
      try {
        await axios.delete(`${API_BASE}/equipment/sales/${id}/`)
        this.equipmentSales = this.equipmentSales.filter(s => s.id !== id)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete equipment sale'
        console.error('Error deleting equipment sale:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async getEquipmentSaleSchedule(id) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/equipment/sales/${id}/schedule/`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch equipment sale schedule'
        console.error('Error fetching equipment sale schedule:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async getAllEquipmentSaleSchedules() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/equipment/sales/schedules/`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch equipment sale schedules'
        console.error('Error fetching equipment sale schedules:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async assignMilestoneStructure(saleId, milestoneStructureId) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(
          `${API_BASE}/equipment/sales/${saleId}/assign_milestone/`,
          { milestone_structure_id: milestoneStructureId }
        )
        
        // Update the sale in the local state
        const index = this.equipmentSales.findIndex(s => s.id === saleId)
        if (index !== -1) {
          this.equipmentSales[index] = response.data
        }
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to assign milestone structure'
        console.error('Error assigning milestone structure:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
