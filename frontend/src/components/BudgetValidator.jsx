import React, { useState } from 'react'
import axios from 'axios'

// Detectar URL del backend automáticamente
const getApiBaseUrl = () => {
  // Si estamos en desarrollo local, usar proxy
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return '/api'
  }
  // En producción (Replit, Railway, etc.), el backend está en el mismo host
  return window.location.origin
}

const API_BASE_URL = getApiBaseUrl()

console.log('API URL configurada:', API_BASE_URL)

function BudgetValidator() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [validationResult, setValidationResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
    setError(null)
    setValidationResult(null)
  }

  const handleValidate = async () => {
    if (!file) {
      setError('Por favor selecciona un archivo BC3')
      return
    }

    setLoading(true)
    setError(null)
    setValidationResult(null)

    try {
      // First, convert BC3 to JSON
      const formData = new FormData()
      formData.append('file', file)

      const convertResponse = await axios.post(
        `${API_BASE_URL}/convert/bc3-to-json`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )

      const budgetData = convertResponse.data

      // Then, validate the budget
      const validateResponse = await axios.post(
        `${API_BASE_URL}/ai/validate-budget`,
        budgetData
      )

      setValidationResult(validateResponse.data)
    } catch (err) {
      console.error('Validation error:', err)
      setError(err.response?.data?.detail || 'Error al validar el presupuesto')
    } finally {
      setLoading(false)
    }
  }

  const handleEnhance = async () => {
    if (!file) {
      setError('Por favor selecciona un archivo BC3')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post(
        `${API_BASE_URL}/ai/enhance-bc3`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      )

      // Download enhanced budget as JSON
      const jsonStr = JSON.stringify(response.data, null, 2)
      const blob = new Blob([jsonStr], { type: 'application/json' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `presupuesto_mejorado.json`
      a.click()
      window.URL.revokeObjectURL(url)

      alert('Presupuesto mejorado descargado como JSON')
    } catch (err) {
      console.error('Enhancement error:', err)
      setError(err.response?.data?.detail || 'Error al mejorar el presupuesto')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Validador con IA
        </h2>

        {/* File Upload */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Selecciona un archivo BC3
          </label>
          <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-lg hover:border-primary-400 transition-colors">
            <div className="space-y-1 text-center">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                stroke="currentColor"
                fill="none"
                viewBox="0 0 48 48"
              >
                <path
                  d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                  strokeWidth={2}
                  strokeLinecap="round"
                  strokeLinejoin="round"
                />
              </svg>
              <div className="flex text-sm text-gray-600">
                <label className="relative cursor-pointer bg-white rounded-md font-medium text-primary-600 hover:text-primary-500">
                  <span>Subir archivo BC3</span>
                  <input
                    type="file"
                    accept=".bc3"
                    onChange={handleFileChange}
                    className="sr-only"
                  />
                </label>
              </div>
            </div>
          </div>
          {file && (
            <div className="mt-3 flex items-center space-x-2 text-sm text-gray-700">
              <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="font-medium">{file.name}</span>
            </div>
          )}
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
            <div className="flex">
              <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
              <p className="ml-3 text-sm text-red-800">{error}</p>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-4 mb-6">
          <button
            onClick={handleValidate}
            disabled={!file || loading}
            className={`py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white transition-colors ${
              !file || loading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-primary-600 hover:bg-primary-700'
            }`}
          >
            {loading ? 'Validando...' : 'Validar Presupuesto'}
          </button>

          <button
            onClick={handleEnhance}
            disabled={!file || loading}
            className={`py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white transition-colors ${
              !file || loading
                ? 'bg-gray-300 cursor-not-allowed'
                : 'bg-green-600 hover:bg-green-700'
            }`}
          >
            {loading ? 'Mejorando...' : 'Mejorar con IA'}
          </button>
        </div>

        {/* Validation Results */}
        {validationResult && (
          <div className="space-y-4">
            {/* Status */}
            <div className={`rounded-lg p-4 ${
              validationResult.is_valid
                ? 'bg-green-50 border border-green-200'
                : 'bg-yellow-50 border border-yellow-200'
            }`}>
              <div className="flex items-center">
                {validationResult.is_valid ? (
                  <>
                    <svg className="h-6 w-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                    <span className="ml-3 text-green-800 font-medium">
                      Presupuesto válido
                    </span>
                  </>
                ) : (
                  <>
                    <svg className="h-6 w-6 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    <span className="ml-3 text-yellow-800 font-medium">
                      Presupuesto con advertencias
                    </span>
                  </>
                )}
              </div>
            </div>

            {/* Errors */}
            {validationResult.errors && validationResult.errors.length > 0 && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <h4 className="text-sm font-medium text-red-900 mb-2">
                  ❌ Errores encontrados:
                </h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-red-800">
                  {validationResult.errors.map((error, index) => (
                    <li key={index}>{error}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Warnings */}
            {validationResult.warnings && validationResult.warnings.length > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                <h4 className="text-sm font-medium text-yellow-900 mb-2">
                  ⚠️ Advertencias:
                </h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-yellow-800">
                  {validationResult.warnings.map((warning, index) => (
                    <li key={index}>{warning}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Suggestions */}
            {validationResult.suggestions && validationResult.suggestions.length > 0 && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <h4 className="text-sm font-medium text-blue-900 mb-2">
                  💡 Sugerencias de mejora:
                </h4>
                <ul className="list-disc list-inside space-y-1 text-sm text-blue-800">
                  {validationResult.suggestions.map((suggestion, index) => (
                    <li key={index}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Information Card */}
      <div className="mt-8 bg-purple-50 border border-purple-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-purple-900 mb-3">
          🤖 Funciones de IA
        </h3>
        <ul className="space-y-2 text-sm text-purple-800">
          <li>• <strong>Validar</strong>: Analiza el presupuesto para detectar errores, inconsistencias y precios sospechosos</li>
          <li>• <strong>Mejorar</strong>: Mejora automáticamente las descripciones haciéndolas más claras y profesionales</li>
          <li>• <strong>IA powered by Claude</strong>: Utiliza inteligencia artificial avanzada para análisis detallado</li>
        </ul>
      </div>
    </div>
  )
}

export default BudgetValidator
