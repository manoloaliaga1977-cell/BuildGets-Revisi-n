import React, { useState } from 'react'
import FileConverter from './components/FileConverter'
import BudgetValidator from './components/BudgetValidator'
import Header from './components/Header'
import Footer from './components/Footer'

function App() {
  const [activeTab, setActiveTab] = useState('converter')

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <Header />

      <main className="flex-grow container mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="mb-8">
          <div className="border-b border-gray-200">
            <nav className="-mb-px flex space-x-8" aria-label="Tabs">
              <button
                onClick={() => setActiveTab('converter')}
                className={`${
                  activeTab === 'converter'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
              >
                Convertidor de Archivos
              </button>
              <button
                onClick={() => setActiveTab('validator')}
                className={`${
                  activeTab === 'validator'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors`}
              >
                Validador con IA
              </button>
            </nav>
          </div>
        </div>

        {/* Content */}
        {activeTab === 'converter' && <FileConverter />}
        {activeTab === 'validator' && <BudgetValidator />}
      </main>

      <Footer />
    </div>
  )
}

export default App
