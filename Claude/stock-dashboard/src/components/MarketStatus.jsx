import { useState, useEffect } from 'react';

function isMarketOpen() {
  const now = new Date();
  const etOffset = -5; // EST offset from UTC (simplified, doesn't account for DST)
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  const etTime = new Date(utc + 3600000 * etOffset);

  const day = etTime.getDay();
  const hours = etTime.getHours();
  const minutes = etTime.getMinutes();
  const timeInMinutes = hours * 60 + minutes;

  // Market hours: 9:30 AM - 4:00 PM ET, Monday - Friday
  const marketOpen = 9 * 60 + 30; // 9:30 AM
  const marketClose = 16 * 60; // 4:00 PM

  const isWeekday = day >= 1 && day <= 5;
  const isDuringHours = timeInMinutes >= marketOpen && timeInMinutes < marketClose;

  return isWeekday && isDuringHours;
}

export default function MarketStatus() {
  const [open, setOpen] = useState(isMarketOpen());

  useEffect(() => {
    const interval = setInterval(() => {
      setOpen(isMarketOpen());
    }, 60000); // Check every minute

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex items-center gap-2">
      <span
        className={`w-2.5 h-2.5 rounded-full ${
          open ? 'bg-green-500 animate-pulse' : 'bg-red-500'
        }`}
      />
      <span className="text-sm text-slate-600 dark:text-slate-400">
        Market {open ? 'Open' : 'Closed'}
      </span>
    </div>
  );
}
