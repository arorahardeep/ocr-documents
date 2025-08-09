import React from 'react';
import { CheckCircle, XCircle, AlertCircle, Copy, Check } from 'lucide-react';

const ExtractedFieldsTable = ({ fields, keyFields }) => {
  const [copiedField, setCopiedField] = React.useState(null);

  const copyToClipboard = async (text, fieldName) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedField(fieldName);
      setTimeout(() => setCopiedField(null), 2000);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getConfidenceIcon = (confidence) => {
    if (confidence >= 0.8) return <CheckCircle className="h-4 w-4 text-green-500" />;
    if (confidence >= 0.6) return <AlertCircle className="h-4 w-4 text-yellow-500" />;
    return <XCircle className="h-4 w-4 text-red-500" />;
  };

  const getConfidenceText = (confidence) => {
    if (confidence >= 0.8) return 'High';
    if (confidence >= 0.6) return 'Medium';
    return 'Low';
  };

  if (!fields || fields.length === 0) {
    return (
      <div className="text-center py-8">
        <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-500">No fields extracted from this page</p>
        <p className="text-sm text-gray-400 mt-1">
          The AI couldn't find the specified fields on this page
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Summary */}
      <div className="bg-gray-50 rounded-lg p-3">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Fields found:</span>
          <span className="font-medium text-gray-900">{fields.length} of {keyFields.length}</span>
        </div>
        <div className="flex items-center space-x-4 mt-2 text-xs">
          <div className="flex items-center space-x-1">
            <CheckCircle className="h-3 w-3 text-green-500" />
            <span className="text-gray-600">
              {fields.filter(f => f.confidence >= 0.8).length} High confidence
            </span>
          </div>
          <div className="flex items-center space-x-1">
            <AlertCircle className="h-3 w-3 text-yellow-500" />
            <span className="text-gray-600">
              {fields.filter(f => f.confidence >= 0.6 && f.confidence < 0.8).length} Medium confidence
            </span>
          </div>
          <div className="flex items-center space-x-1">
            <XCircle className="h-3 w-3 text-red-500" />
            <span className="text-gray-600">
              {fields.filter(f => f.confidence < 0.6).length} Low confidence
            </span>
          </div>
        </div>
      </div>

      {/* Fields Table */}
      <div className="overflow-hidden border border-gray-200 rounded-lg">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Field Name
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Extracted Value
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Confidence
              </th>
              <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {fields.map((field, index) => (
              <tr key={index} className="hover:bg-gray-50">
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900 capitalize">
                    {field.field_name.replace(/_/g, ' ')}
                  </div>
                </td>
                <td className="px-4 py-3">
                  <div className="text-sm text-gray-900 max-w-xs truncate">
                    {field.value || (
                      <span className="text-gray-400 italic">Not found</span>
                    )}
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  <div className="flex items-center space-x-2">
                    {getConfidenceIcon(field.confidence)}
                    <div>
                      <div className={`text-sm font-medium ${getConfidenceColor(field.confidence)}`}>
                        {getConfidenceText(field.confidence)}
                      </div>
                      <div className="text-xs text-gray-500">
                        {Math.round(field.confidence * 100)}%
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-4 py-3 whitespace-nowrap">
                  {field.value && (
                    <button
                      onClick={() => copyToClipboard(field.value, field.field_name)}
                      className="p-1 text-gray-400 hover:text-gray-600 transition-colors"
                      title="Copy to clipboard"
                    >
                      {copiedField === field.field_name ? (
                        <Check className="h-4 w-4 text-green-500" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Missing Fields */}
      {fields.length < keyFields.length && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-5 w-5 text-yellow-500 mt-0.5" />
            <div className="text-sm text-yellow-800">
              <p className="font-medium mb-1">Missing Fields</p>
              <p>The following fields were not found on this page:</p>
              <div className="mt-2 flex flex-wrap gap-2">
                {keyFields
                  .filter(keyField => !fields.some(field => field.field_name === keyField))
                  .map(field => (
                    <span
                      key={field}
                      className="px-2 py-1 bg-yellow-100 text-yellow-800 text-xs rounded-full"
                    >
                      {field.replace(/_/g, ' ')}
                    </span>
                  ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Export JSON */}
      <div className="flex justify-end">
        <button
          onClick={() => copyToClipboard(JSON.stringify(fields, null, 2), 'json')}
          className="btn-secondary text-sm"
        >
          {copiedField === 'json' ? (
            <div className="flex items-center space-x-1">
              <Check className="h-4 w-4" />
              <span>Copied!</span>
            </div>
          ) : (
            <div className="flex items-center space-x-1">
              <Copy className="h-4 w-4" />
              <span>Copy JSON</span>
            </div>
          )}
        </button>
      </div>
    </div>
  );
};

export default ExtractedFieldsTable;
