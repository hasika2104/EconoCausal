import React, { useState, useEffect, useRef } from 'react';
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
  Table,
  ShieldCheck,
  FileSpreadsheet,
  Layers,
  Settings2,
  Sliders,
  CheckCircle2,
  XCircle
} from 'lucide-react';
import {
  fetchDatasetPreview,
  uploadDataset,
  mapDatasetColumns,
  getExportCleanedUrl,
  getExportDatasetUrl
} from '../services/api';

const STANDARD_FIELDS = [
  { key: "product_id", label: "Product ID / SKU", required: true },
  { key: "price", label: "Price ($)", required: true },
  { key: "units_sold", label: "Units Sold / Demand", required: true },
  { key: "date", label: "Transaction Date", required: false },
  { key: "cost", label: "Unit Cost / COGS", required: false },
  { key: "inventory", label: "Inventory Level", required: false },
  { key: "category", label: "Category", required: false },
  { key: "region", label: "Region / Store", required: false },
  { key: "promotion", label: "Promotion / Discount", required: false },
  { key: "competitor_price", label: "Competitor Price", required: false }
];

export default function DatasetExplorerPage({ lang = 'en' }) {
  const [datasetType, setDatasetType] = useState('default');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Pagination & filter state
  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(25);
  const [search, setSearch] = useState('');
  const [sortBy, setSortBy] = useState(null);
  const [sortDir, setSortDir] = useState('asc');

  // Upload state
  const [isDragging, setIsDragging] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [uploadFeedback, setUploadFeedback] = useState(null);

  // Column Mapping modal / panel state
  const [showMappingPanel, setShowMappingPanel] = useState(false);
  const [mappings, setMappings] = useState({});
  const [mappingLoading, setMappingLoading] = useState(false);

  const fileInputRef = useRef(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchDatasetPreview({
        dataset_type: datasetType,
        page: page,
        page_size: pageSize,
        sort_by: sortBy,
        sort_dir: sortDir,
        search: search
      });
      setData(res);
    } catch (err) {
      console.error(err);
      setError('Failed to fetch dataset preview. Please check backend server.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [datasetType, page, pageSize, sortBy, sortDir, search]);

  const handleFile = async (file) => {
    if (!file) return;
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['csv', 'xlsx', 'xls'].includes(ext)) {
      setUploadFeedback({
        type: 'error',
        message: 'Unsupported format. Please upload a .csv, .xlsx, or .xls file.'
      });
      return;
    }

    setUploadLoading(true);
    setUploadFeedback(null);
    try {
      const res = await uploadDataset(file);
      const newFileObj = { id: res.upload_id, name: res.filename, row_count: res.row_count, audit: res.audit };
      setUploadedFiles((prev) => [newFileObj, ...prev]);
      setDatasetType(res.upload_id);
      setPage(1);

      // Pre-fill auto-detected mappings
      if (res.audit?.detected_mappings) {
        setMappings(res.audit.detected_mappings);
      }

      setUploadFeedback({
        type: res.audit?.issues?.length === 0 ? 'success' : 'warning',
        message: `Successfully uploaded ${res.filename} (${res.row_count.toLocaleString()} rows, ${res.column_count} columns). Health score: ${res.audit?.quality_score}%`,
        audit: res.audit
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

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const applyColumnMappings = async () => {
    if (datasetType === 'default') return;
    setMappingLoading(true);
    try {
      const res = await mapDatasetColumns(datasetType, mappings);
      setShowMappingPanel(false);
      loadData();
      setUploadFeedback({
        type: 'success',
        message: `Column mappings successfully applied! New quality score: ${res.audit.quality_score}%`
      });
    } catch (err) {
      setUploadFeedback({
        type: 'error',
        message: err.message || 'Failed to apply column mappings.'
      });
    } finally {
      setMappingLoading(false);
    }
  };

  const audit = data?.audit;

  return (
    <div className="space-y-8 pb-12 max-w-7xl mx-auto">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-slate-900 tracking-tight">
            {lang === 'te' ? 'డేటా అప్‌లోడ్ & వ్యాలిడేషన్ మాడ్యూల్' : 'Data Upload & Quality Validator'}
          </h1>
          <p className="text-xs text-slate-500 mt-1 font-medium">
            Upload CSV or Excel files, map non-standard retail columns, audit missing data, and download cleaned datasets.
          </p>
        </div>

        {/* Dataset Switcher */}
        <div className="flex items-center gap-2">
          <span className="text-xs font-semibold text-slate-500">Active Dataset:</span>
          <select
            value={datasetType}
            onChange={(e) => {
              setDatasetType(e.target.value);
              setPage(1);
            }}
            className="px-3 py-1.5 bg-white border border-slate-300 rounded-xl text-xs font-semibold text-slate-800 shadow-2xs focus:ring-2 focus:ring-emerald-500/20"
          >
            <option value="default">Demo Benchmark (73,100 Rows)</option>
            {uploadedFiles.map((f) => (
              <option key={f.id} value={f.id}>
                {f.name} ({f.row_count?.toLocaleString()} rows)
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Drag & Drop Upload Zone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`border-2 border-dashed rounded-3xl p-8 md:p-10 text-center cursor-pointer transition-all ${
          isDragging
            ? 'border-emerald-600 bg-emerald-50/70 scale-[1.01]'
            : 'border-slate-300 bg-white hover:border-emerald-500 hover:bg-slate-50/60'
        } shadow-xs relative`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          className="hidden"
          onChange={(e) => {
            if (e.target.files && e.target.files.length > 0) {
              handleFile(e.target.files[0]);
            }
          }}
        />

        <div className="max-w-md mx-auto space-y-3">
          <div className="w-14 h-14 rounded-2xl bg-emerald-100 text-emerald-800 flex items-center justify-center mx-auto shadow-xs">
            {uploadLoading ? (
              <RefreshCw className="w-7 h-7 animate-spin text-emerald-700" />
            ) : (
              <UploadCloud className="w-7 h-7 text-emerald-700" />
            )}
          </div>

          <div>
            <h3 className="text-base font-bold text-slate-900">
              {uploadLoading ? 'Parsing and Auditing Dataset...' : 'Drag and drop your sales dataset here'}
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Supports <strong>.CSV</strong> and <strong>Excel (.XLSX, .XLS)</strong> up to 25MB
            </p>
          </div>

          <div className="pt-2">
            <span className="inline-flex items-center gap-1.5 px-4 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-semibold shadow-xs">
              Browse Local Files
            </span>
          </div>
        </div>
      </div>

      {/* Upload Feedback Banner */}
      {uploadFeedback && (
        <div
          className={`p-4 rounded-2xl border text-xs md:text-sm flex items-start gap-3 ${
            uploadFeedback.type === 'error'
              ? 'bg-red-50 border-red-200 text-red-800'
              : uploadFeedback.type === 'warning'
              ? 'bg-amber-50 border-amber-200 text-amber-900'
              : 'bg-emerald-50 border-emerald-200 text-emerald-900'
          }`}
        >
          {uploadFeedback.type === 'error' ? (
            <XCircle className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
          ) : uploadFeedback.type === 'warning' ? (
            <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
          ) : (
            <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
          )}
          <div className="flex-1">
            <div className="font-bold">{uploadFeedback.message}</div>
            {uploadFeedback.warnings && (
              <ul className="mt-1 space-y-0.5 list-disc list-inside text-xs">
                {uploadFeedback.warnings.map((w, idx) => (
                  <li key={idx}>{w}</li>
                ))}
              </ul>
            )}
          </div>
        </div>
      )}

      {/* Data Health & Quality Audit Card */}
      {audit && (
        <div className="bg-white rounded-3xl border border-slate-200/90 p-6 md:p-8 shadow-xs space-y-6">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-slate-100 pb-4">
            <div>
              <div className="text-xs font-bold uppercase tracking-wider text-emerald-700 mb-1">
                Data Quality Audit
              </div>
              <h2 className="text-xl font-bold text-slate-900">
                Dataset Health & Schema Diagnosis
              </h2>
            </div>

            <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-xs text-slate-400 font-medium">Health Score</div>
                <div className={`text-2xl font-black ${
                  audit.quality_score >= 80 ? 'text-emerald-700' : audit.quality_score >= 60 ? 'text-amber-600' : 'text-red-600'
                }`}>
                  {audit.quality_score}%
                </div>
              </div>

              {datasetType !== 'default' && (
                <button
                  onClick={() => setShowMappingPanel(!showMappingPanel)}
                  className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition-all"
                >
                  <Settings2 className="w-4 h-4 text-emerald-700" />
                  <span>Map Columns</span>
                </button>
              )}
            </div>
          </div>

          {/* Audit Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Total Rows</div>
              <div className="text-lg font-bold text-slate-900 mt-1">
                {audit.total_rows?.toLocaleString()}
              </div>
            </div>

            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Duplicate Records</div>
              <div className="text-lg font-bold text-slate-900 mt-1">
                {audit.duplicate_rows?.toLocaleString()}{' '}
                <span className="text-xs text-slate-400 font-normal">({audit.duplicate_pct}%)</span>
              </div>
            </div>

            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Missing Data Cells</div>
              <div className="text-lg font-bold text-slate-900 mt-1">
                {audit.missing_cells?.toLocaleString()}{' '}
                <span className="text-xs text-slate-400 font-normal">({audit.missing_pct}%)</span>
              </div>
            </div>

            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200/80">
              <div className="text-xs text-slate-500 font-medium">Core Pricing Columns</div>
              <div className="text-xs font-semibold mt-2 flex items-center gap-2">
                <span className={`px-2 py-0.5 rounded-full ${audit.has_price ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
                  Price: {audit.has_price ? '✓' : '✕'}
                </span>
                <span className={`px-2 py-0.5 rounded-full ${audit.has_units ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'}`}>
                  Demand: {audit.has_units ? '✓' : '✕'}
                </span>
              </div>
            </div>
          </div>

          {/* Cleaned Dataset Export Actions */}
          <div className="pt-2 flex flex-wrap items-center justify-between gap-4 border-t border-slate-100">
            <div className="text-xs text-slate-500">
              Never silently modifies your uploaded file. You can download an auto-cleaned copy below.
            </div>

            <div className="flex items-center gap-2">
              <a
                href={getExportCleanedUrl(datasetType, true, true, 'csv')}
                download
                className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 rounded-xl text-xs font-semibold transition-all"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Cleaned CSV</span>
              </a>

              <a
                href={getExportCleanedUrl(datasetType, true, true, 'xlsx')}
                download
                className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-xs font-semibold transition-all"
              >
                <FileSpreadsheet className="w-3.5 h-3.5 text-emerald-700" />
                <span>Cleaned Excel (.xlsx)</span>
              </a>
            </div>
          </div>
        </div>
      )}

      {/* Column Mapping Interface (Drawer / Accordion) */}
      {showMappingPanel && (
        <div className="bg-white rounded-3xl border border-emerald-300 p-6 md:p-8 shadow-sm space-y-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Settings2 className="w-5 h-5 text-emerald-700" />
                <span>Retail Column Mapping Wizard</span>
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Map custom column names in your uploaded file to EconoCausal's standard schema.
              </p>
            </div>
            <button
              onClick={() => setShowMappingPanel(false)}
              className="text-xs text-slate-400 hover:text-slate-600 font-semibold"
            >
              Close
            </button>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data?.columns?.map((col) => (
              <div key={col.name} className="p-3 bg-slate-50 rounded-xl border border-slate-200 flex items-center justify-between gap-3 text-xs">
                <div className="font-mono font-bold text-slate-800 truncate max-w-[180px]">
                  {col.name} <span className="text-[10px] text-slate-400 font-normal">({col.type})</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-slate-400">maps to:</span>
                  <select
                    value={mappings[col.name] || ""}
                    onChange={(e) => {
                      const val = e.target.value;
                      setMappings((prev) => ({ ...prev, [col.name]: val }));
                    }}
                    className="px-2.5 py-1 bg-white border border-slate-300 rounded-lg text-xs text-slate-800"
                  >
                    <option value="">-- Ignore / Unmapped --</option>
                    {STANDARD_FIELDS.map((f) => (
                      <option key={f.key} value={f.key}>
                        {f.label} {f.required ? '*' : ''}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            ))}
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <button
              onClick={() => setShowMappingPanel(false)}
              className="px-4 py-2 border border-slate-300 rounded-xl text-xs font-semibold text-slate-700 hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              onClick={applyColumnMappings}
              disabled={mappingLoading}
              className="px-5 py-2 bg-emerald-700 hover:bg-emerald-800 text-white rounded-xl text-xs font-semibold shadow-xs"
            >
              {mappingLoading ? 'Applying Schema...' : 'Save & Re-Audit'}
            </button>
          </div>
        </div>
      )}

      {/* Dataset Table & Search Bar */}
      <div className="bg-white rounded-3xl border border-slate-200/90 p-6 md:p-8 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="relative flex-1 max-w-md">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search across any row or product ID..."
              className="w-full pl-10 pr-4 py-2 bg-slate-50 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-emerald-500/20"
            />
          </div>

          <div className="flex items-center gap-3 text-xs text-slate-500">
            <span>Rows per page:</span>
            <select
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value));
                setPage(1);
              }}
              className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-lg text-xs"
            >
              <option value={10}>10</option>
              <option value={25}>25</option>
              <option value={50}>50</option>
            </select>
          </div>
        </div>

        {/* Data Table */}
        <div className="overflow-x-auto rounded-2xl border border-slate-200/80">
          <table className="w-full text-xs text-left">
            <thead className="bg-slate-50 text-slate-600 font-semibold border-b border-slate-200">
              <tr>
                {data?.columns?.map((col) => (
                  <th
                    key={col.name}
                    onClick={() => {
                      if (sortBy === col.name) {
                        setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
                      } else {
                        setSortBy(col.name);
                        setSortDir('asc');
                      }
                    }}
                    className="py-3 px-4 cursor-pointer hover:bg-slate-100/80 select-none"
                  >
                    <div className="flex items-center gap-1.5">
                      <span>{col.name}</span>
                      {sortBy === col.name && (
                        <span className="text-[10px] text-emerald-700 font-bold">
                          {sortDir === 'asc' ? '▲' : '▼'}
                        </span>
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {loading ? (
                <tr>
                  <td colSpan={data?.columns?.length || 5} className="py-12 text-center text-slate-400">
                    <RefreshCw className="w-5 h-5 animate-spin mx-auto text-emerald-600 mb-2" />
                    <span>Loading rows...</span>
                  </td>
                </tr>
              ) : data?.rows?.length === 0 ? (
                <tr>
                  <td colSpan={data?.columns?.length || 5} className="py-8 text-center text-slate-400">
                    No matching rows found.
                  </td>
                </tr>
              ) : (
                data?.rows?.map((row, idx) => (
                  <tr key={idx} className="hover:bg-slate-50/60">
                    {data?.columns?.map((col) => (
                      <td key={col.name} className="py-2.5 px-4 font-mono text-slate-800">
                        {row[col.name] !== null ? String(row[col.name]) : <span className="text-slate-300 italic">null</span>}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2 text-xs text-slate-500">
          <div>
            Showing row {((page - 1) * pageSize) + 1} to {Math.min(page * pageSize, data?.total_rows || 0)} of {data?.total_rows?.toLocaleString()} rows
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
              className="p-1.5 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-40"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="px-2 font-semibold text-slate-700">
              Page {page} of {data?.total_pages || 1}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(data?.total_pages || 1, p + 1))}
              disabled={page >= (data?.total_pages || 1)}
              className="p-1.5 border border-slate-200 rounded-lg hover:bg-slate-50 disabled:opacity-40"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
