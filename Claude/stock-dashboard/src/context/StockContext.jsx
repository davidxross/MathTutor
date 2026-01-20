import { createContext, useContext, useReducer, useEffect } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';
import { useStockData } from '../hooks/useStockData';

const StockContext = createContext(null);

const initialState = {
  watchlist: ['AAPL', 'GOOGL', 'MSFT'],
  selectedStock: null,
  darkMode: false,
};

function stockReducer(state, action) {
  switch (action.type) {
    case 'ADD_STOCK':
      if (state.watchlist.includes(action.payload.toUpperCase())) {
        return state;
      }
      return {
        ...state,
        watchlist: [...state.watchlist, action.payload.toUpperCase()],
      };
    case 'REMOVE_STOCK':
      return {
        ...state,
        watchlist: state.watchlist.filter(
          symbol => symbol !== action.payload
        ),
        selectedStock:
          state.selectedStock === action.payload ? null : state.selectedStock,
      };
    case 'SELECT_STOCK':
      return {
        ...state,
        selectedStock: action.payload,
      };
    case 'TOGGLE_DARK_MODE':
      return {
        ...state,
        darkMode: !state.darkMode,
      };
    case 'SET_DARK_MODE':
      return {
        ...state,
        darkMode: action.payload,
      };
    case 'SET_WATCHLIST':
      return {
        ...state,
        watchlist: action.payload,
      };
    default:
      return state;
  }
}

export function StockProvider({ children }) {
  const [savedWatchlist, setSavedWatchlist] = useLocalStorage(
    'stock-watchlist',
    initialState.watchlist
  );
  const [savedDarkMode, setSavedDarkMode] = useLocalStorage(
    'stock-dark-mode',
    initialState.darkMode
  );

  const [state, dispatch] = useReducer(stockReducer, {
    ...initialState,
    watchlist: savedWatchlist,
    darkMode: savedDarkMode,
  });

  const { stockData, loading, error, refetch } = useStockData(state.watchlist);

  // Persist watchlist changes
  useEffect(() => {
    setSavedWatchlist(state.watchlist);
  }, [state.watchlist, setSavedWatchlist]);

  // Persist dark mode changes
  useEffect(() => {
    setSavedDarkMode(state.darkMode);
  }, [state.darkMode, setSavedDarkMode]);

  // Apply dark mode class to document
  useEffect(() => {
    if (state.darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [state.darkMode]);

  const addStock = symbol => dispatch({ type: 'ADD_STOCK', payload: symbol });
  const removeStock = symbol => dispatch({ type: 'REMOVE_STOCK', payload: symbol });
  const selectStock = symbol => dispatch({ type: 'SELECT_STOCK', payload: symbol });
  const toggleDarkMode = () => dispatch({ type: 'TOGGLE_DARK_MODE' });

  const value = {
    watchlist: state.watchlist,
    selectedStock: state.selectedStock,
    darkMode: state.darkMode,
    stockData,
    loading,
    error,
    addStock,
    removeStock,
    selectStock,
    toggleDarkMode,
    refetch,
  };

  return (
    <StockContext.Provider value={value}>{children}</StockContext.Provider>
  );
}

export function useStock() {
  const context = useContext(StockContext);
  if (!context) {
    throw new Error('useStock must be used within a StockProvider');
  }
  return context;
}
