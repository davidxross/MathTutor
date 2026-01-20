import { StockProvider } from './context/StockContext';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import StockList from './components/StockList';
import StockChart from './components/StockChart';

export default function App() {
  return (
    <StockProvider>
      <div className="min-h-screen bg-slate-100 dark:bg-slate-900 transition-colors">
        <Header />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <SearchBar />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2">
              <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                Your Watchlist
              </h2>
              <StockList />
            </div>

            <div className="lg:col-span-1">
              <h2 className="text-lg font-semibold text-slate-900 dark:text-white mb-4">
                Price History
              </h2>
              <StockChart />
            </div>
          </div>
        </main>

        <footer className="mt-auto py-4 text-center text-sm text-slate-500 dark:text-slate-400">
          Data provided by{' '}
          <a
            href="https://finnhub.io"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:text-blue-600 dark:hover:text-blue-400"
          >
            Finnhub
          </a>
          . Prices update every 30 seconds.
        </footer>
      </div>
    </StockProvider>
  );
}
