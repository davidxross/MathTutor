import { useStock } from '../context/StockContext';
import StockCard from './StockCard';

function LoadingSkeleton() {
  return (
    <div className="p-4 bg-white dark:bg-slate-800 rounded-lg shadow border border-slate-200 dark:border-slate-700 animate-pulse">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-slate-200 dark:bg-slate-700 rounded-lg" />
          <div>
            <div className="h-5 w-16 bg-slate-200 dark:bg-slate-700 rounded" />
            <div className="h-4 w-24 bg-slate-200 dark:bg-slate-700 rounded mt-1" />
          </div>
        </div>
        <div className="w-4 h-4 bg-slate-200 dark:bg-slate-700 rounded" />
      </div>
      <div className="mt-4">
        <div className="h-8 w-32 bg-slate-200 dark:bg-slate-700 rounded" />
        <div className="mt-3 grid grid-cols-2 gap-2">
          <div className="h-4 w-20 bg-slate-200 dark:bg-slate-700 rounded" />
          <div className="h-4 w-20 bg-slate-200 dark:bg-slate-700 rounded" />
          <div className="h-4 w-20 bg-slate-200 dark:bg-slate-700 rounded" />
          <div className="h-4 w-20 bg-slate-200 dark:bg-slate-700 rounded" />
        </div>
      </div>
    </div>
  );
}

export default function StockList() {
  const { watchlist, stockData, loading } = useStock();

  if (watchlist.length === 0) {
    return (
      <div className="text-center py-12">
        <svg
          className="mx-auto h-12 w-12 text-slate-400 dark:text-slate-500"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
          />
        </svg>
        <h3 className="mt-2 text-sm font-medium text-slate-900 dark:text-white">
          No stocks in watchlist
        </h3>
        <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
          Search for stocks to add them to your watchlist
        </p>
      </div>
    );
  }

  if (loading && Object.keys(stockData).length === 0) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {watchlist.map((symbol) => (
          <LoadingSkeleton key={symbol} />
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      {watchlist.map((symbol) => (
        <StockCard
          key={symbol}
          symbol={symbol}
          data={stockData[symbol]}
        />
      ))}
    </div>
  );
}
