<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <h1>🍽️ Google Menu Translator</h1>
      <p>Upload a menu image and get instant translations with detailed descriptions</p>
    </header>

    <!-- Input Section -->
    <section class="input-section">
      <div class="input-group">
        <input
          v-model="filename"
          type="text"
          placeholder="Enter image filename (e.g., Snipaste_14.png)"
          class="input-field"
          @keyup.enter="translateMenu"
        />
        <input
          v-model="language"
          type="text"
          placeholder="Enter target language (e.g., 英文)"
          class="input-field"
          @keyup.enter="translateMenu"
        />
        <button
          @click="translateMenu"
          :disabled="!filename || isLoading"
          class="translate-btn"
        >
          <span v-if="isLoading" class="loading"></span>
          {{ isLoading ? 'Translating...' : 'Translate Menu' }}
        </button>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </section>

    <!-- Image Display Section -->
    <section v-if="imageUrl" class="image-section">
      <h2>📸 Menu Image</h2>
      <img :src="imageUrl" :alt="filename" class="menu-image" />
    </section>

    <!-- Menu Items Section -->
    <section v-if="menuItems && Object.keys(menuItems).length > 0" class="menu-section">
      <h2 class="menu-title">🍴 Translated Menu Items</h2>
      
      <div v-for="(item, originalName) in menuItems" :key="originalName" class="menu-item">
        <div 
          class="menu-item-header"
          @click="toggleItem(originalName)"
        >
          <div>
            <div class="menu-item-name">{{ originalName }}</div>
            <div class="menu-item-translation">{{ item.translated_name }}</div>
          </div>
          <span class="expand-icon" :class="{ expanded: expandedItems[originalName] }">
            ▼
          </span>
        </div>
        
        <div v-if="expandedItems[originalName]" class="menu-item-details">
          <div class="ingredients-section">
            <div class="section-title">🥘 Ingredients & Seasonings:</div>
            <div class="ingredients-list">
              <span 
                v-for="ingredient in item.ingredients_and_seasonings" 
                :key="ingredient"
                class="ingredient-tag"
              >
                {{ ingredient }}
              </span>
            </div>
          </div>
          
          <div class="flavor-section">
            <div class="section-title">👨‍🍳 Flavor & Preparation:</div>
            <div class="flavor-text">{{ item.flavor_and_preparation }}</div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { menuService } from './services/api.js'

export default {
  name: 'App',
  setup() {
    const filename = ref('')
    const language = ref('英文')
    const imageUrl = ref('')
    const menuItems = ref({})
    const isLoading = ref(false)
    const error = ref('')
    const expandedItems = reactive({})

    const toggleItem = (itemName) => {
      expandedItems[itemName] = !expandedItems[itemName]
    }

    const translateMenu = async () => {
      if (!filename.value.trim()) {
        error.value = 'Please enter a filename'
        return
      }

      isLoading.value = true
      error.value = ''
      menuItems.value = {}
      expandedItems.value = {}

      try {
        // Get image URL
        imageUrl.value = await menuService.getImageUrl(filename.value.trim())
        
        // Extract menu items
        const result = await menuService.extractMenuItems(filename.value.trim(), language.value.trim())
        
        // Parse the result (it comes as a JSON string)
        let parsedResult
        if (typeof result === 'string') {
          parsedResult = JSON.parse(result)
        } else {
          parsedResult = result
        }
        
        menuItems.value = parsedResult
        
        // Auto-expand first item
        const firstItem = Object.keys(parsedResult)[0]
        if (firstItem) {
          expandedItems[firstItem] = true
        }
        
      } catch (err) {
        error.value = err.message || 'An error occurred while processing the menu'
        console.error('Translation error:', err)
      } finally {
        isLoading.value = false
      }
    }

    return {
      filename,
      language,
      imageUrl,
      menuItems,
      isLoading,
      error,
      expandedItems,
      translateMenu,
      toggleItem
    }
  }
}
</script>
