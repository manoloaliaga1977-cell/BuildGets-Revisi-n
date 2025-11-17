import React, { useState } from 'react'
import axios from 'axios'

const API_BASE_URL = '/api'

function FileConverter() {
  const [file, setFile] = useState(null)
  const [conversionType, setConversionType] = useState('bc3-to-pdf')
  const [enhanceWithAI, setEnhanceWithAI] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [success, setSuccess] = useState(null)

  const conversionOptions = [
    { value: 'bc3-to-pdf', label: 'BC3 → PDF', accept: '.bc3' },
    { value: 'pdf-to-bc3', label: 'PDF → BC3', accept: '.pdf' },
    { value: 'bc3-to-json', label: 'BC3 → JSON', accept: '.bc3' },
    { value: 'pdf-to-json', label: 'PDF → JSON', accept: '.pdf' },
  ]

  const currentOption = conversionOptions.find(opt => opt.value === conversionType)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
    setError(null)
    setSuccess(null)
  }

  const handleConvert = async () => {
    if (!file) {
      setError('Por favor selecciona un archivo')
      return
    }

    setLoading(true)
    setError(null)
    setSuccess(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      let endpoint = ''
      let responseType = 'blob'

      switch (conversionType) {
        case 'bc3-to-pdf':
          endpoint = `${API_BASE_URL}/convert/bc3-to-pdf${enhanceWithAI ? '?enhance=true' : ''}`
          break
        case 'pdf-to-bc3':
          endpoint = `${API_BASE_URL}/convert/pdf-to-bc3`
          break
        case 'bc3-to-json':
          endpoint = `${API_BASE_URL}/convert/bc3-to-json`
          responseType = 'json'
          break
        case 'pdf-to-json':
          endpoint = `${API_BASE_URL}/convert/pdf-to-json`
          responseType = 'json'
          break
        default:
          throw new Error('Tipo de conversión no válido')
      }

      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        responseType: responseType,
      })

      if (responseType === 'json') {
        // Show JSON in a new window or download it
        const jsonStr = JSON.stringify(response.data, null, 2)
        const blob = new Blob([jsonStr], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `presupuesto.json`
        a.click()
        window.URL.revokeObjectURL(url)
      } else {
        // Download the file
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const a = document.createElement('a')
        a.href = url

        const extension = conversionType.includes('pdf') ? 'pdf' : 'bc3'
        a.download = `presupuesto_convertido.${extension}`
        a.click()
        window.URL.revokeObjectURL(url)
      }

      setSuccess('Conversión completada con éxito')
      setFile(null)
    } catch (err) {
      console.error('Conversion error:', err)
      setError(err.response?.data?.detail || 'Error al convertir el archivo')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">
          Convertir Archivos
        </h2>

        {/* Conversion Type Selector */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Tipo de conversión
          </label>
          <div className="grid grid-cols-2 gap-4">
            {conversionOptions.map(option => (
              <button
                key={option.value}
                onClick={() => {
                  setConversionType(option.value)
                  setFile(null)
                  setError(null)
                  setSuccess(null)
                }}
                className={`p-4 border-2 rounded-lg text-center font-medium transition-all ${
                  conversionType === option.value
                    ? 'border-primary-500 bg-primary-50 text-primary-700'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                {option.label}
              </button>
            ))}
          </div>
        </div>

        {/* AI Enhancement Option (only for specific conversions) */}
        {(conversionType === 'bc3-to-pdf' || conversionType === 'pdf-to-bc3') && (
          <div className="mb-6">
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={enhanceWithAI}
                onChange={(e) => setEnhanceWithAI(e.target.checked)}
                className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              />
              <span className="text-sm font-medium text-gray-700">
                Mejorar con IA (descripciones más claras y profesionales)
              </span>
            </label>
          </div>
        )}

        {/* File Upload */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Selecciona el archivo
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
                  <span>Subir archivo</span>
                  <input
                    type="file"
                    accept={currentOption.accept}
                    onChange={handleFileChange}
                    className="sr-only"
                  />
                </label>
                <p className="pl-1">o arrastra y suelta</p>
              </div>
              <p className="text-xs text-gray-500">
                {currentOption.accept.toUpperCase()} hasta 10MB
              </p>
            </div>
          </div>
          {file && (
            <div className="mt-3 flex items-center space-x-2 text-sm text-gray-700">
              <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <span className="font-medium">{file.name}</span>
              <span className="text-gray-500">({(file.size / 1024).toFixed(2)} KB)</span>
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

        {/* Success Message */}
        {success && (
          <div className="mb-6 bg-green-50 border border-green-200 rounded-lg p-4">
            <div className="flex">
              <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <p className="ml-3 text-sm text-green-800">{success}</p>
            </div>
          </div>
        )}

        {/* Convert Button */}
        <button
          onClick={handleConvert}
          disabled={!file || loading}
          className={`w-full py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white transition-colors ${
            !file || loading
              ? 'bg-gray-300 cursor-not-allowed'
              : 'bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
          }`}
        >
          {loading ? (
            <span className="flex items-center justify-center">
              <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Convirtiendo...
            </span>
          ) : (
            'Convertir'
          )}
        </button>
      </div>

      {/* Information Card */}
      <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">
          ℹ️ Información
        </h3>
        <ul className="space-y-2 text-sm text-blue-800">
          <li>• <strong>BC3</strong>: Formato estándar español FIEBDC-3 para presupuestos de construcción</li>
          <li>• <strong>PDF</strong>: Genera documentos profesionales con formato y estructura clara</li>
          <li>• <strong>JSON</strong>: Formato para integración con otras aplicaciones</li>
          <li>• <strong>IA</strong>: Mejora automática de descripciones y extracción inteligente de datos</li>
        </ul>
      </div>
    </div>
  )
}

export default FileConverter
