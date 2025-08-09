import React, { useState, useEffect, useRef } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { ChevronLeft, ChevronRight, ZoomIn, ZoomOut, RotateCw } from 'lucide-react';

// Set up PDF.js worker
pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

const PDFViewer = ({ documentData, currentPage }) => {
  const [numPages, setNumPages] = useState(null);
  const [scale, setScale] = useState(1.0);
  const [rotation, setRotation] = useState(0);
  const [loading, setLoading] = useState(true);
  const containerRef = useRef(null);
  const [containerWidth, setContainerWidth] = useState(0);

  useEffect(() => {
    if (documentData) {
      setNumPages(documentData.total_pages);
      setLoading(false);
    }
  }, [documentData]);

  useEffect(() => {
    const updateWidth = () => {
      if (containerRef.current) {
        const width = containerRef.current.clientWidth;
        setContainerWidth(width);
      }
    };
    updateWidth();
    window.addEventListener('resize', updateWidth);
    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  const handleDocumentLoadSuccess = ({ numPages }) => {
    setNumPages(numPages);
    setLoading(false);
  };

  const handleDocumentLoadError = (error) => {
    console.error('PDF load error:', error);
    setLoading(false);
  };

  const zoomIn = () => {
    setScale(prev => Math.min(prev + 0.2, 3.0));
  };

  const zoomOut = () => {
    setScale(prev => Math.max(prev - 0.2, 0.5));
  };

  const rotate = () => {
    setRotation(prev => (prev + 90) % 360);
  };

  const resetView = () => {
    setScale(1.0);
    setRotation(0);
  };

  if (!documentData) {
    return (
      <div className="flex items-center justify-center h-64 bg-gray-100 rounded-lg">
        <p className="text-gray-500">No document loaded</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex items-center justify-between bg-gray-50 rounded-lg p-3">
        <div className="flex items-center space-x-2">
          <button
            onClick={zoomOut}
            disabled={scale <= 0.5}
            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded transition-colors disabled:opacity-50"
            title="Zoom Out"
          >
            <ZoomOut className="h-4 w-4" />
          </button>
          
          <span className="text-sm font-medium text-gray-700 min-w-[60px] text-center">
            {Math.round(scale * 100)}%
          </span>
          
          <button
            onClick={zoomIn}
            disabled={scale >= 3.0}
            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded transition-colors disabled:opacity-50"
            title="Zoom In"
          >
            <ZoomIn className="h-4 w-4" />
          </button>
          
          <button
            onClick={rotate}
            className="p-2 text-gray-600 hover:text-gray-800 hover:bg-gray-200 rounded transition-colors"
            title="Rotate"
          >
            <RotateCw className="h-4 w-4" />
          </button>
        </div>
        
        <button
          onClick={resetView}
          className="text-sm text-primary-600 hover:text-primary-700 font-medium"
        >
          Reset View
        </button>
      </div>

      {/* PDF Viewer */}
      <div ref={containerRef} className="bg-gray-100 rounded-lg p-4 min-h-[400px] max-h-[70vh] overflow-auto">
        {loading ? (
          <div className="flex items-center space-x-2">
            <div className="loading-spinner"></div>
            <span className="text-gray-600">Loading PDF...</span>
          </div>
        ) : (
          <div className="w-full flex justify-center">
            <Document
              file={`/uploads/${documentData.doc_id}.pdf`}
              onLoadSuccess={handleDocumentLoadSuccess}
              onLoadError={handleDocumentLoadError}
              loading={
                <div className="flex items-center space-x-2">
                  <div className="loading-spinner"></div>
                  <span className="text-gray-600">Loading document...</span>
                </div>
              }
              error={
                <div className="text-center text-red-600">
                  <p>Failed to load PDF document</p>
                  <p className="text-sm">Please try uploading the file again</p>
                </div>
              }
            >
              <Page
                pageNumber={currentPage}
                width={Math.max(200, Math.floor((containerWidth || 800) * scale))}
                rotate={rotation}
                loading={
                  <div className="flex items-center space-x-2">
                    <div className="loading-spinner"></div>
                    <span className="text-gray-600">Loading page...</span>
                  </div>
                }
                error={
                  <div className="text-center text-red-600">
                    <p>Failed to load page {currentPage}</p>
                  </div>
                }
                className="shadow-lg max-w-full h-auto"
                renderTextLayer={false}
                renderAnnotationLayer={false}
              />
            </Document>
          </div>
        )}
      </div>

      {/* Page Info */}
      <div className="text-center text-sm text-gray-500">
        Page {currentPage} of {numPages || documentData.total_pages}
      </div>
    </div>
  );
};

export default PDFViewer;
