import React from 'react';
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-react';

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  const getVisiblePages = () => {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];

    for (
      let i = Math.max(2, currentPage - delta);
      i <= Math.min(totalPages - 1, currentPage + delta);
      i++
    ) {
      range.push(i);
    }

    if (currentPage - delta > 2) {
      rangeWithDots.push(1, '...');
    } else {
      rangeWithDots.push(1);
    }

    rangeWithDots.push(...range);

    if (currentPage + delta < totalPages - 1) {
      rangeWithDots.push('...', totalPages);
    } else {
      rangeWithDots.push(totalPages);
    }

    return rangeWithDots;
  };

  const handlePageChange = (page) => {
    if (page >= 1 && page <= totalPages && page !== currentPage) {
      onPageChange(page);
    }
  };

  if (totalPages <= 1) {
    return null;
  }

  return (
    <div className="flex items-center justify-center space-x-2">
      {/* First Page */}
      <button
        onClick={() => handlePageChange(1)}
        disabled={currentPage === 1}
        className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        title="First page"
      >
        <ChevronsLeft className="h-4 w-4" />
      </button>

      {/* Previous Page */}
      <button
        onClick={() => handlePageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        title="Previous page"
      >
        <ChevronLeft className="h-4 w-4" />
      </button>

      {/* Page Numbers */}
      <div className="flex items-center space-x-1">
        {getVisiblePages().map((page, index) => (
          <React.Fragment key={index}>
            {page === '...' ? (
              <span className="px-3 py-2 text-gray-400">...</span>
            ) : (
              <button
                onClick={() => handlePageChange(page)}
                className={`px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                  page === currentPage
                    ? 'bg-primary-600 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                {page}
              </button>
            )}
          </React.Fragment>
        ))}
      </div>

      {/* Next Page */}
      <button
        onClick={() => handlePageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        title="Next page"
      >
        <ChevronRight className="h-4 w-4" />
      </button>

      {/* Last Page */}
      <button
        onClick={() => handlePageChange(totalPages)}
        disabled={currentPage === totalPages}
        className="p-2 text-gray-400 hover:text-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        title="Last page"
      >
        <ChevronsRight className="h-4 w-4" />
      </button>
    </div>
  );
};

export default Pagination;
