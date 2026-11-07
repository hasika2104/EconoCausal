import React, { useState, useEffect } from 'react';
import {
  Database,
  UploadCloud,
  Download,
  Search,
  Filter,
  CheckCircle,
  AlertTriangle,
  FileText,
  ChevronLeft,
  ChevronRight,
  RefreshCw,
  Table
} from 'lucide-react';
import { fetchDatasetPreview, uploadDataset } from '../services/api';

export default function DatasetExplorerPage() {
  const [datasetType, setDatasetType] = useState('default'); // 'default' or upload_id
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Pagination & filter state
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(20);
  const [search, setSearch] = useState('');
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadFeedback, setUploadFeedback] = useState(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchDatasetPreview({
        dataset_type: datasetType,
        page: page,
        page_size: pageSize,
        search: search
      });
      setData(res);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch dataset preview.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [datasetType, page, pageSize, search]);

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadLoading(true);
    setUploadFeedback(null);
    try {
      const res = await uploadDataset(file);
      setUploadedFiles(prev => [...prev, { id: res.upload_id, name: res.filename, row_count: res.row_count }]);
      setDatasetType(res.upload_id);
      setPage(1);
      setUploadFeedback({
        type: res.validation.valid ? 'success' : 'warning',
        message: `Successfully uploaded ${res.filename} (${res.row_count} rows, ${res.column_count} columns).`,
        warnings: res.validation.warnings
      });
    } catch (err) {
      setUploadFeedback({
        type: 'error',
        message: err.message || 'File upload failed.'
      });
    } finally {
      setUploadLoading(false);
    }
  };

  const handleExport = () => {
    const url = `/api/dataset/export?dataset_type=${datasetType}&search=${encodeURIComponent(search)}`;
    window.open(url, '_blank');
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Page Header */}
      <div>
        <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">Dataset Explorer & Schema Inspector</h2>
        <p className="text-xs text-slate-500 mt-1">
          Inspect, filter, upload, and export raw retail transaction files with automated schema type validation.
        </p>
      </div>

      {/* Upload and Dataset Selector Bar */}
      <div className="bg-white p-6 rounded-xl border border-slate-200/80 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <span className="text-xs font-semibold text-slate-500">Active Dataset:</span>
            <select
              value={datasetType}
              onChange={(e) => {
                setDatasetType(e.target.value);
                setPage(1);
              }}
              className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-3 py-1.5 text-slate-800 font-semibold focus:outline-emerald-500"
            >
              <option value="default">Default Production Retail Cleaned (73,100 records)</option>
              {uploadedFiles.map((f) => (
                <option key={f.id} value={f.id}>
                  {f.name} ({f.row_count} records)
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-center gap-3">
            <label className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-medium cursor-pointer transition-colors">
              <UploadCloud className="w-3.5 h-3.5 text-emerald-600" />
              <span>{uploadLoading ? 'Uploading...' : 'Upload New CSV'}</span>
              <input
                type="file"
                accept=".csv"
                onChange={handleFileUpload}
                disabled={uploadLoading}
                className="hidden"
              />
            </label>

            <button
              onClick={handleExport}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-lg text-xs font-semibold transition-colors"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export CSV</span>
            </button>
          </div>
        </div>

        {/* Upload Feedback Banner */}
        {uploadFeedback && (
          <div className={`p-3.5 rounded-lg text-xs border ${
            uploadFeedback.type === 'error'
              ? 'bg-rose-50 border-rose-200 text-rose-800'
              : 'bg-emerald-50 border-emerald-200 text-emerald-800'
          }`}>
            <div className="font-semibold">{uploadFeedback.message}</div>
            {uploadFeedback.warnings && uploadFeedback.warnings.length > 0 && (
              <ul className="list-disc list-inside mt-1 text-[11px] text-amber-800">
                {uploadFeedback.warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>

      {/* Schema / Column Inspector Strip */}
      {data?.columns && (
        <div className="bg-white p-5 rounded-xl border border-slate-200/80 shadow-xs">
          <div className="text-xs font-bold text-slate-800 mb-3 flex items-center gap-2">
            <Table className="w-4 h-4 text-emerald-600" />
            <span>Dataset Schema & Column Type Audit ({data.columns.length} Fields)</span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-2.5">
            {data.columns.map((col) => (
              <div key={col.name} className="p-2.5 rounded-lg border border-slate-100 bg-slate-50 text-xs">
                <div className="font-bold text-slate-800 font-mono text-[11px] truncate" title={col.name}>
                  {col.name}
                </div>
                <div className="text-[10px] text-slate-400 font-mono mt-0.5">{col.type}</div>
                <div className="text-[10px] text-slate-500 mt-1 flex items-center justify-between">
                  <span>Nulls:</span>
                  <strong className={col.null_count === 0 ? 'text-emerald-700' : 'text-amber-700'}>
                    {col.null_count}
                  </strong>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Data Table with Search and Pagination */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-xs overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex flex-wrap items-center justify-between gap-4">
          <div className="relative min-w-[240px]">
            <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search across all fields..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              className="w-full text-xs bg-slate-50 border border-slate-200 rounded-lg pl-8 pr-3 py-1.5 text-slate-800 focus:outline-emerald-500"
            />
          </div>

          <div className="flex items-center gap-4 text-xs text-slate-500">
            <span>
              Total: <strong>{data?.total_rows?.toLocaleString() || 0}</strong> records
            </span>

            <div className="flex items-center gap-1">
              <span>Show:</span>
              <select
                value={pageSize}
                onChange={(e) => {
                  setPageSize(Number(e.target.value));
                  setPage(1);
                }}
                className="bg-slate-50 border border-slate-200 rounded px-2 py-1 text-slate-700 text-xs"
              >
                <option value={10}>10</option>
                <option value={20}>20</option>
                <option value={50}>50</option>
                <option value={100}>100</option>
              </select>
            </div>
          </div>
        </div>

        {/* Data Rows */}
        <div className="overflow-x-auto">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-500 font-semibold uppercase text-[10px] border-b border-slate-200">
              <tr>
                {data?.columns?.map((col) => (
                  <th key={col.name} className="py-2.5 px-3 whitespace-nowrap">
                    {col.name}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {loading ? (
                <tr>
                  <td colSpan={data?.columns?.length || 5} className="py-12 text-center text-slate-400">
                    <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-emerald-600" />
                    <span>Loading data records...</span>
                  </td>
                </tr>
              ) : data?.rows?.length === 0 ? (
                <tr>
                  <td colSpan={data?.columns?.length || 5} className="py-12 text-center text-slate-400">
                    No matching records found.
                  </td>
                </tr>
              ) : (
                data?.rows?.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/70">
                    {data.columns.map((col) => (
                      <td key={col.name} className="py-2 px-3 whitespace-nowrap font-mono text-[11px]">
                        {row[col.name] !== null ? String(row[col.name]) : '-'}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Controls */}
        <div className="p-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <div>
            Page <strong>{page}</strong> of <strong>{data?.total_pages || 1}</strong>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="px-2.5 py-1 rounded border border-slate-200 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1 font-medium"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
              <span>Previous</span>
            </button>
            <button
              onClick={() => setPage(p => Math.min(data?.total_pages || 1, p + 1))}
              disabled={page >= (data?.total_pages || 1)}
              className="px-2.5 py-1 rounded border border-slate-200 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1 font-medium"
            >
              <span>Next</span>
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
