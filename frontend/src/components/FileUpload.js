import React, { useState, useRef } from 'react';
import axios from 'axios';
import { Upload, FileText, X, AlertCircle } from 'lucide-react';

const FileUpload = ({ onProcessingStart, onDocumentProcessed, onError, isProcessing }) => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      if (file.type === 'application/pdf') {
        setSelectedFile(file);
      } else {
        onError('Please select a PDF file');
      }
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setSelectedFile(file);
    } else if (file) {
      onError('Please select a PDF file');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedFile) {
      onError('Please select a PDF file');
      return;
    }

    onProcessingStart();

    try {
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await axios.post('/upload-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 300000, // 5 minutes timeout
      });

      onDocumentProcessed(response.data);
    } catch (error) {
      console.error('Upload error:', error);
      if (error.response) {
        onError(error.response.data.detail || 'Upload failed');
      } else if (error.request) {
        onError('Network error. Please check your connection.');
      } else {
        onError('An unexpected error occurred');
      }
    }
  };

  const removeFile = () => {
    setSelectedFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* File Upload Area */}
      <div className="card">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Upload PDF Document</h3>
        
        <div
          className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
            dragActive 
              ? 'border-primary-400 bg-primary-50' 
              : 'border-gray-300 hover:border-gray-400'
          }`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          {selectedFile ? (
            <div className="space-y-4">
              <div className="flex items-center justify-center space-x-2">
                <FileText className="h-8 w-8 text-primary-600" />
                <span className="text-lg font-medium text-gray-900">{selectedFile.name}</span>
              </div>
              <p className="text-sm text-gray-500">
                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
              </p>
              <button
                onClick={removeFile}
                className="btn-secondary text-sm"
              >
                <X className="h-4 w-4 mr-1" />
                Remove File
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <Upload className="h-12 w-12 text-gray-400 mx-auto" />
              <div>
                <p className="text-lg font-medium text-gray-900">
                  Drop your PDF file here
                </p>
                <p className="text-gray-500">or</p>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="btn-primary mt-2"
                >
                  Browse Files
                </button>
              </div>
              <p className="text-sm text-gray-500">
                Supports scanned and digital PDF documents
              </p>
            </div>
          )}
          
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>
      </div>

      {/* Submit Button */}
      <div className="text-center">
        <button
          type="button"
          onClick={handleSubmit}
          disabled={!selectedFile || isProcessing}
          className={`btn-primary text-lg px-8 py-3 ${
            (!selectedFile || isProcessing)
              ? 'opacity-50 cursor-not-allowed'
              : ''
          }`}
        >
          {isProcessing ? (
            <div className="flex items-center space-x-2">
              <div className="loading-spinner"></div>
              <span>Processing...</span>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <Upload className="h-5 w-5" />
              <span>Process Document</span>
            </div>
          )}
        </button>
      </div>

      {/* Info Box */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <AlertCircle className="h-5 w-5 text-blue-500 mt-0.5" />
          <div className="text-sm text-blue-800">
            <p className="font-medium mb-1">Supported Languages</p>
            <p>Our AI-powered OCR system can extract fields from documents in multiple languages including:</p>
            <ul className="list-disc list-inside mt-1 space-y-1">
              <li>English, Thai, Mandarin Chinese</li>
              <li>Bahasa Indonesia, Vietnamese</li>
              <li>Japanese, Korean, Spanish, French</li>
              <li>German, Italian, Portuguese, Russian, Arabic</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FileUpload;
