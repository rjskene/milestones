import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export const useMilestoneStore = defineStore('milestone', {
  state: () => ({
    milestoneStructures: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchMilestoneStructures() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/milestones/structures/`)
        this.milestoneStructures = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch milestone structures'
        console.error('Error fetching milestone structures:', error)
      } finally {
        this.loading = false
      }
    },

    async createMilestoneStructure(structureData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_BASE}/milestones/structures/`, structureData)
        this.milestoneStructures.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create milestone structure'
        console.error('Error creating milestone structure:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateMilestoneStructure(id, structureData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.put(`${API_BASE}/milestones/structures/${id}/`, structureData)
        const index = this.milestoneStructures.findIndex(s => s.id === id)
        if (index !== -1) {
          this.milestoneStructures[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update milestone structure'
        console.error('Error updating milestone structure:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteMilestoneStructure(id) {
      this.loading = true
      this.error = null
      try {
        await axios.delete(`${API_BASE}/milestones/structures/${id}/`)
        this.milestoneStructures = this.milestoneStructures.filter(s => s.id !== id)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete milestone structure'
        console.error('Error deleting milestone structure:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
