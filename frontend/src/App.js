import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import PDFViewer from './components/PDFViewer';
import ExtractedFieldsTable from './components/ExtractedFieldsTable';
import axios from 'axios';
import Pagination from './components/Pagination';
import LoadingSpinner from './components/LoadingSpinner';
import { FileText, Upload, CheckCircle, AlertCircle } from 'lucide-react';

function App() {
  const [documentData, setDocumentData] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState(null);

  const handleDocumentProcessed = (data) => {
    setDocumentData(data);
    setCurrentPage(1);
    setIsProcessing(false);
    setError(null);
  };

  const handleProcessingStart = () => {
    setIsProcessing(true);
    setError(null);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setIsProcessing(false);
  };

  const handlePageChange = (pageNumber) => {
    setCurrentPage(pageNumber);
  };

  const getCurrentPageData = () => {
    if (!documentData || !documentData.pages) return null;
    return documentData.pages.find(page => page.page_number === currentPage);
  };

  const [pageFieldsInput, setPageFieldsInput] = useState('');
  const [pageExtracting, setPageExtracting] = useState(false);

  const extractFieldsForCurrentPage = async () => {
    const page = getCurrentPageData();
    if (!documentData || !page) return;
    const fields = pageFieldsInput
      .split(',')
      .map(f => f.trim())
      .filter(Boolean);
    if (fields.length === 0) return;

    setPageExtracting(true);
    try {
      const res = await axios.post(`/document/${documentData.doc_id}/page/${page.page_number}/extract`, {
        key_fields: fields,
      });
      const updatedPage = res.data;
      setDocumentData(prev => {
        const copy = { ...prev };
        copy.pages = prev.pages.map(p => p.page_number === updatedPage.page_number ? updatedPage : p);
        return copy;
      });
    } catch (e) {
      setError('Failed to extract fields for this page');
    } finally {
      setPageExtracting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <FileText className="h-8 w-8 text-primary-600" />
              <h1 className="text-xl font-semibold text-gray-900">
                OCR Document Processor
              </h1>
            </div>
            <div className="text-sm text-gray-500">
              Powered by OpenAI GPT-5
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!documentData ? (
          /* Upload Section */
          <div className="space-y-8">
            <div className="text-center">
              <h2 className="text-3xl font-bold text-gray-900 mb-4">
                Extract Key Fields from PDF Documents
              </h2>
              <p className="text-lg text-gray-600 max-w-2xl mx-auto">
                Upload a PDF document (scanned or digital) and specify the fields you want to extract. 
                Our AI-powered OCR system supports multiple languages including Thai, Mandarin, Bahasa, Vietnamese, and English.
              </p>
            </div>

            <FileUpload
              onProcessingStart={handleProcessingStart}
              onDocumentProcessed={handleDocumentProcessed}
              onError={handleError}
              isProcessing={isProcessing}
            />
          </div>
        ) : (
          /* Document Viewer Section */
          <div className="space-y-6">
            {/* Document Info */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">
                      {documentData.filename}
                    </h3>
                    <p className="text-sm text-gray-500">
                      {documentData.total_pages} pages • {documentData.key_fields.length} fields to extract
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    setDocumentData(null);
                    setCurrentPage(1);
                    setError(null);
                  }}
                  className="btn-secondary"
                >
                  Upload New Document
                </button>
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="h-5 w-5 text-red-500" />
                  <p className="text-red-800">{error}</p>
                </div>
              </div>
            )}

            {/* Processing Indicator */}
            {isProcessing && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex items-center space-x-3">
                  <LoadingSpinner />
                  <div>
                    <p className="text-blue-800 font-medium">Processing document...</p>
                    <p className="text-blue-600 text-sm">This may take a few moments depending on the document size.</p>
                  </div>
                </div>
              </div>
            )}

            {/* Document Content */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* PDF Viewer */}
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-medium text-gray-900">Document Preview</h3>
                  <span className="text-sm text-gray-500">
                    Page {currentPage} of {documentData.total_pages}
                  </span>
                </div>
                <PDFViewer
                  documentData={documentData}
                  currentPage={currentPage}
                />
                {/* Per-page field input */}
                <div className="mt-4 border-t pt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Fields to extract on this page (comma-separated)
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={pageFieldsInput}
                      onChange={(e) => setPageFieldsInput(e.target.value)}
                      placeholder="e.g., invoice_number, date, amount"
                      className="input-field flex-1"
                      disabled={pageExtracting}
                    />
                    <button
                      onClick={extractFieldsForCurrentPage}
                      className="btn-primary"
                      disabled={pageExtracting || !pageFieldsInput.trim()}
                    >
                      {pageExtracting ? 'Extracting...' : 'Extract'}
                    </button>
                  </div>
                  <p className="text-xs text-gray-500 mt-1">Extraction runs only for the current page.</p>
                </div>
              </div>

              {/* Extracted Fields */}
              <div className="card">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-medium text-gray-900">Extracted Fields</h3>
                  <span className="text-sm text-gray-500">
                    Page {currentPage}
                  </span>
                </div>
                <ExtractedFieldsTable
                  fields={getCurrentPageData()?.extracted_fields || []}
                  keyFields={documentData.key_fields}
                />
              </div>
            </div>

            {/* Pagination */}
            {documentData.total_pages > 1 && (
              <div className="flex justify-center">
                <Pagination
                  currentPage={currentPage}
                  totalPages={documentData.total_pages}
                  onPageChange={handlePageChange}
                />
              </div>
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500 text-sm">
            <p>OCR Document Processor • Built with React, FastAPI, and OpenAI</p>
            <p className="mt-2">Supports multiple languages: English, Thai, Mandarin, Bahasa, Vietnamese, and more</p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
