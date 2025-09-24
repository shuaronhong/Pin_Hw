import axios from 'axios'

const API_BASE_URL = 'https://flask.9top.org'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 30 seconds timeout for image processing
  headers: {
    'Content-Type': 'application/json',
  }
})

export const menuService = {
  async extractMenuItems(filename, language = '英文') {
    try {
      const response = await api.post('/extract-menu', {
        filename: filename,
        language: language
      })
      return response.data
    } catch (error) {
      console.error('Error extracting menu items:', error)
      throw new Error(error.response?.data?.error || 'Failed to extract menu items')
    }
  },

  async getImageUrl(filename) {
    return `${API_BASE_URL}/images/${filename}`
  }
}

export default api
