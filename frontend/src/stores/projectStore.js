import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [],
    loading: false,
    error: null
  }),

  actions: {
    async fetchProjects() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/projects/`)
        this.projects = response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch projects'
        console.error('Error fetching projects:', error)
      } finally {
        this.loading = false
      }
    },

    async createProject(projectData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.post(`${API_BASE}/projects/`, projectData)
        this.projects.push(response.data)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to create project'
        console.error('Error creating project:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async updateProject(id, projectData) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.put(`${API_BASE}/projects/${id}/`, projectData)
        const index = this.projects.findIndex(p => p.id === id)
        if (index !== -1) {
          this.projects[index] = response.data
        }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to update project'
        console.error('Error updating project:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async deleteProject(id) {
      this.loading = true
      this.error = null
      try {
        await axios.delete(`${API_BASE}/projects/${id}/`)
        this.projects = this.projects.filter(p => p.id !== id)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to delete project'
        console.error('Error deleting project:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async getProjectTimeline(id) {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/projects/${id}/timeline/`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch project timeline'
        console.error('Error fetching project timeline:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async getAllProjectTimelines() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/projects/timelines/`)
        return response.data
      } catch (error) {
        this.error = error.response?.data?.detail || 'Failed to fetch project timelines'
        console.error('Error fetching project timelines:', error)
        throw error
      } finally {
        this.loading = false
      }
    }
  }
})
