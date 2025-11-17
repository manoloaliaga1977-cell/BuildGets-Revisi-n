import React from 'react'

function Footer() {
  return (
    <footer className="bg-white border-t border-gray-200 mt-12">
      <div className="container mx-auto px-4 py-6">
        <div className="text-center text-gray-600 text-sm">
          <p>Budget Converter - Convierte presupuestos BC3 y PDF con inteligencia artificial</p>
          <p className="mt-2">
            Formatos soportados: BC3 (FIEBDC-3) • PDF • JSON
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
