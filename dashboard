import React, { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { ArrowUpDown, TrendingUp, DollarSign, Clock, Percent } from 'lucide-react';

const CryptoArbitrageDashboard = () => {
  // Initial parameters
  const [initialCapital, setInitialCapital] = useState(4000);
  const [months, setMonths] = useState(12);
  const [spreadPercentage, setSpreadPercentage] = useState(5.5);
  const [reinvestmentRate, setReinvestmentRate] = useState(100);
  const [cyclesPerMonth, setCyclesPerMonth] = useState(15);
  
  // Capital distribution
  const [robinhoodCapital, setRobinhoodCapital] = useState(1000);
  const [coinbaseCapital, setCoinbaseCapital] = useState(1500);
  const [krakenCapital, setKrakenCapital] = useState(1000);
  const [cashappCapital, setCashappCapital] = useState(500);
  
  // Platform fees and constraints
  const platformData = {
    robinhood: { fee: 0.1, transferTime: 24, dailyLimit: 1000 },
    coinbase: { fee: 0.4, transferTime: 144, dailyLimit: 10000 },
    kraken: { fee: 0.26, transferTime: 24, dailyLimit: 5000 },
    cashappFast: { fee: 1.7, transferTime: 1, dailyLimit: 7500 },
    cashappStandard: { fee: 0, transferTime: 48, dailyLimit: 7500 }
  };
  
  // Simulation data
  const [simulationData, setSimulationData] = useState([]);
  const [comparisonData, setComparisonData] = useState([]);
  
  // Get total allocated capital
  const getTotalAllocatedCapital = () => {
    return robinhoodCapital + coinbaseCapital + krakenCapital + cashappCapital;
  };
  
  // Run simulation when parameters change
  useEffect(() => {
    runSimulation();
  }, [initialCapital, months, spreadPercentage, reinvestmentRate, cyclesPerMonth,
      robinhoodCapital, coinbaseCapital, krakenCapital, cashappCapital]);
  
  // Format platform name for display
  const formatPlatformName = (name) => {
    if (!name) return '';
    return name.replace(/([A-Z])/g, ' $1')
      .split(' ')
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ');
  };
  
  // Calculate profit for a specific platform
  const calculatePlatformProfit = (platformKey, capital) => {
    const platform = platformData[platformKey];
    if (!platform) return 0;
    
    const fee = platform.fee;
    const transferTime = platform.transferTime;
    const dailyLimit = platform.dailyLimit;
    
    // Effective capital is limited by daily limit
    const effectiveCapital = Math.min(capital, dailyLimit * 30);
    
    // Calculate cycles based on time and capital constraints
    const timeBasedCycles = cyclesPerMonth * (720 / (720 + transferTime));
    const capitalBasedCycles = Math.floor(30 * effectiveCapital / dailyLimit);
    const adjustedCycles = Math.min(timeBasedCycles, capitalBasedCycles);
    
    // Calculate profit
    const cycleProfit = (spreadPercentage - fee) / 100;
    const monthlyReturn = Math.pow(1 + cycleProfit, adjustedCycles) - 1;
    
    return capital * monthlyReturn;
  };
  
  // Run the simulation
  const runSimulation = () => {
    const simData = [];
    const compData = [];
    
    // Initial state
    let currentCapital = initialCapital;
    let previousCapital = initialCapital;
    let rCapital = robinhoodCapital;
    let cCapital = coinbaseCapital;
    let kCapital = krakenCapital;
    let caCapital = cashappCapital;
    
    // Calculate total profit from all platforms
    const calculateMultiPlatformReturn = () => {
      const robinhoodProfit = calculatePlatformProfit('robinhood', rCapital);
      const coinbaseProfit = calculatePlatformProfit('coinbase', cCapital);
      const krakenProfit = calculatePlatformProfit('kraken', kCapital);
      const cashappProfit = calculatePlatformProfit('cashappStandard', caCapital);
      
      return robinhoodProfit + coinbaseProfit + krakenProfit + cashappProfit;
    };
    
    // Simulate month by month
    for (let month = 0; month <= months; month++) {
      if (month === 0) {
        // Initial month
        simData.push({
          month,
          capital: initialCapital,
          profit: 0,
          robinhoodCapital: robinhoodCapital,
          coinbaseCapital: coinbaseCapital,
          krakenCapital: krakenCapital,
          cashappCapital: cashappCapital,
          returnRate: 0,
          accumulatedReturn: 0
        });
      } else {
        // Calculate profit for this month
        const monthlyProfit = calculateMultiPlatformReturn();
        const monthlyReturn = monthlyProfit / currentCapital;
        
        // Apply reinvestment
        const reinvestedProfit = monthlyProfit * reinvestmentRate / 100;
        currentCapital = previousCapital + reinvestedProfit;
        
        // Distribute reinvested profits proportionally
        const totalPrevious = previousCapital;
        const rPercent = rCapital / totalPrevious;
        const cPercent = cCapital / totalPrevious;
        const kPercent = kCapital / totalPrevious;
        const caPercent = caCapital / totalPrevious;
        
        rCapital += reinvestedProfit * rPercent;
        cCapital += reinvestedProfit * cPercent;
        kCapital += reinvestedProfit * kPercent;
        caCapital += reinvestedProfit * caPercent;
        
        // Record data
        simData.push({
          month,
          capital: parseFloat(currentCapital.toFixed(2)),
          profit: parseFloat(monthlyProfit.toFixed(2)),
          robinhoodCapital: parseFloat(rCapital.toFixed(2)),
          coinbaseCapital: parseFloat(cCapital.toFixed(2)),
          krakenCapital: parseFloat(kCapital.toFixed(2)),
          cashappCapital: parseFloat(caCapital.toFixed(2)),
          returnRate: parseFloat((monthlyReturn * 100).toFixed(2)),
          accumulatedReturn: parseFloat(((currentCapital / initialCapital - 1) * 100).toFixed(2))
        });
        
        previousCapital = currentCapital;
      }
    }
    
    // Generate comparison data for each platform
    const platformKeys = ['robinhood', 'coinbase', 'kraken', 'cashappFast', 'cashappStandard'];
    
    platformKeys.forEach(key => {
      const platform = platformData[key];
      
      const adjustedCycles = Math.min(
        cyclesPerMonth * (720 / (720 + platform.transferTime)),
        Math.floor(30 * initialCapital / platform.dailyLimit)
      );
      
      const cycleProfit = (spreadPercentage - platform.fee) / 100;
      const monthlyReturn = Math.pow(1 + cycleProfit, adjustedCycles) - 1;
      const yearlyReturn = Math.pow(1 + monthlyReturn, 12) - 1;
      
      compData.push({
        platform: key,
        fee: platform.fee,
        transferTime: platform.transferTime,
        dailyLimit: platform.dailyLimit,
        monthlyVolume: platform.dailyLimit * 30,
        cyclesPerMonth: parseFloat(adjustedCycles.toFixed(1)),
        monthlyReturn: parseFloat((monthlyReturn * 100).toFixed(2)),
        yearlyReturn: parseFloat((yearlyReturn * 100).toFixed(2))
      });
    });
    
    setSimulationData(simData);
    setComparisonData(compData);
  };
  
  return (
    <div className="flex flex-col gap-4">
      <div className="p-6 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-4">Crypto Arbitrage System Optimization</h1>
        <p className="text-gray-600 mb-6">
          Optimize your cryptocurrency arbitrage between Robinhood, Coinbase, Kraken, and Binance
        </p>
        
        {/* Main parameters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="p-4 bg-gray-50 rounded-lg">
            <h2 className="text-sm font-medium mb-2">Initial Capital</h2>
            <div className="flex items-center">
              <DollarSign className="mr-2 h-4 w-4 text-gray-500" />
              <input
                type="number"
                value={initialCapital}
                onChange={(e) => setInitialCapital(parseFloat(e.target.value))}
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-lg">
            <h2 className="text-sm font-medium mb-2">Spread Percentage</h2>
            <div className="flex items-center">
              <Percent className="mr-2 h-4 w-4 text-gray-500" />
              <input
                type="number"
                value={spreadPercentage}
                onChange={(e) => setSpreadPercentage(parseFloat(e.target.value))}
                step="0.1"
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-lg">
            <h2 className="text-sm font-medium mb-2">Cycles Per Month</h2>
            <div className="flex items-center">
              <ArrowUpDown className="mr-2 h-4 w-4 text-gray-500" />
              <input
                type="number"
                value={cyclesPerMonth}
                onChange={(e) => setCyclesPerMonth(parseFloat(e.target.value))}
                step="1"
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-lg">
            <h2 className="text-sm font-medium mb-2">Time Horizon (Months)</h2>
            <div className="flex items-center">
              <Clock className="mr-2 h-4 w-4 text-gray-500" />
              <input
                type="number"
                value={months}
                onChange={(e) => setMonths(parseInt(e.target.value))}
                min="1"
                max="36"
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
          
          <div className="p-4 bg-gray-50 rounded-lg">
            <h2 className="text-sm font-medium mb-2">Reinvestment Rate (%)</h2>
            <div className="flex items-center">
              <TrendingUp className="mr-2 h-4 w-4 text-gray-500" />
              <input
                type="number"
                value={reinvestmentRate}
                onChange={(e) => setReinvestmentRate(parseFloat(e.target.value))}
                min="0"
                max="100"
                className="w-full p-2 border rounded"
              />
            </div>
          </div>
        </div>
        
        {/* Capital distribution */}
        <div className="p-4 bg-white rounded-lg border mb-6">
          <h2 className="text-xl font-bold mb-4">Capital Distribution</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="text-sm font-medium mb-2">Robinhood Capital</h3>
              <div className="flex items-center">
                <input
                  type="number"
                  value={robinhoodCapital}
                  onChange={(e) => setRobinhoodCapital(parseFloat(e.target.value))}
                  className="w-full p-2 border rounded"
                />
              </div>
              <div className="mt-2 text-xs text-gray-500">
                Daily limit: $1,000
              </div>
            </div>
            
            <div className="p-4 bg-purple-50 rounded-lg">
              <h3 className="text-sm font-medium mb-2">Coinbase Capital</h3>
              <div className="flex items-center">
                <input
                  type="number"
                  value={coinbaseCapital}
                  onChange={(e) => setCoinbaseCapital(parseFloat(e.target.value))}
                  className="w-full p-2 border rounded"
                />
              </div>
              <div className="mt-2 text-xs text-gray-500">
                6-day holding period
              </div>
            </div>
            
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="text-sm font-medium mb-2">Kraken Capital</h3>
              <div className="flex items-center">
                <input
                  type="number"
                  value={krakenCapital}
                  onChange={(e) => setKrakenCapital(parseFloat(e.target.value))}
                  className="w-full p-2 border rounded"
                />
              </div>
              <div className="mt-2 text-xs text-gray-500">
                Daily limit: $5,000
              </div>
            </div>
            
            <div className="p-4 bg-yellow-50 rounded-lg">
              <h3 className="text-sm font-medium mb-2">CashApp Capital</h3>
              <div className="flex items-center">
                <input
                  type="number"
                  value={cashappCapital}
                  onChange={(e) => setCashappCapital(parseFloat(e.target.value))}
                  className="w-full p-2 border rounded"
                />
              </div>
              <div className="mt-2 text-xs text-gray-500">
                Instant (1.7% fee) or Standard (0% fee, 48h)
              </div>
            </div>
          </div>
          
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="flex justify-between items-center">
              <h3 className="font-medium">Total Allocated Capital:</h3>
              <p className={getTotalAllocatedCapital() !== initialCapital ? "font-bold text-red-500" : "font-bold text-green-600"}>
                ${getTotalAllocatedCapital().toLocaleString()} 
                {getTotalAllocatedCapital() !== initialCapital ? 
                  ` (Mismatch: $${(getTotalAllocatedCapital() - initialCapital).toLocaleString()})` : 
                  " (Matches initial capital)"}
              </p>
            </div>
          </div>
        </div>
        
        {/* Summary statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="p-4 bg-blue-50 rounded-lg">
            <h2 className="text-lg font-medium mb-1">Ending Capital</h2>
            <p className="text-2xl font-bold">
              ${simulationData.length > 0 ? 
                simulationData[simulationData.length - 1].capital.toLocaleString('en-US', {maximumFractionDigits: 2}) : 
                initialCapital.toLocaleString('en-US', {maximumFractionDigits: 2})}
            </p>
          </div>
          
          <div className="p-4 bg-green-50 rounded-lg">
            <h2 className="text-lg font-medium mb-1">Total Profit</h2>
            <p className="text-2xl font-bold text-green-600">
              ${simulationData.length > 0 ? 
                (simulationData[simulationData.length - 1].capital - initialCapital).toLocaleString('en-US', {maximumFractionDigits: 2}) : 
                0}
            </p>
          </div>
          
          <div className="p-4 bg-purple-50 rounded-lg">
            <h2 className="text-lg font-medium mb-1">Return Rate</h2>
            <p className="text-2xl font-bold text-blue-600">
              {simulationData.length > 0 ? 
                simulationData[simulationData.length - 1].accumulatedReturn.toLocaleString('en-US', {maximumFractionDigits: 2}) : 
                0}%
            </p>
          </div>
        </div>
        
        {/* Capital growth chart */}
        <div className="p-4 bg-white rounded-lg border mb-6">
          <h2 className="text-xl font-bold mb-4">Capital Growth Over Time</h2>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={simulationData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" label={{ value: 'Month', position: 'insideBottom', offset: -5 }} />
                <YAxis label={{ value: 'Capital ($)', angle: -90, position: 'insideLeft' }} />
                <Tooltip formatter={(value) => ['$' + value.toLocaleString('en-US', {maximumFractionDigits: 2}), 'Capital']} />
                <Legend />
                <Line type="monotone" dataKey="capital" stroke="#8884d8" activeDot={{ r: 8 }} name="Total Capital ($)" />
                <Line type="monotone" dataKey="robinhoodCapital" stroke="#2196F3" name="Robinhood Capital" />
                <Line type="monotone" dataKey="coinbaseCapital" stroke="#9C27B0" name="Coinbase Capital" />
                <Line type="monotone" dataKey="krakenCapital" stroke="#4CAF50" name="Kraken Capital" />
                <Line type="monotone" dataKey="cashappCapital" stroke="#FFC107" name="CashApp Capital" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Monthly profit chart */}
        <div className="p-4 bg-white rounded-lg border mb-6">
          <h2 className="text-xl font-bold mb-4">Monthly Profit</h2>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={simulationData.filter(item => item.month > 0)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip formatter={(value) => ['$' + value.toLocaleString('en-US', {maximumFractionDigits: 2}), 'Profit']} />
                <Legend />
                <Bar dataKey="profit" fill="#82ca9d" name="Monthly Profit ($)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        
        {/* Platform comparison */}
        <div className="p-4 bg-white rounded-lg border mb-6">
          <h2 className="text-xl font-bold mb-4">Platform Comparison</h2>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Platform</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fee (%)</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Transfer Time (hrs)</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Daily Limit ($)</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monthly Volume ($)</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cycles/Month</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monthly Return</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Yearly Return</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {comparisonData.map((platform, index) => (
                  <tr key={index}>
                    <td className="px-6 py-4 whitespace-nowrap font-medium">{formatPlatformName(platform.platform)}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{platform.fee}%</td>
                    <td className="px-6 py-4 whitespace-nowrap">{platform.transferTime}</td>
                    <td className="px-6 py-4 whitespace-nowrap">${platform.dailyLimit.toLocaleString()}</td>
                    <td className="px-6 py-4 whitespace-nowrap">${platform.monthlyVolume.toLocaleString()}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{platform.cyclesPerMonth}</td>
                    <td className="px-6 py-4 whitespace-nowrap">{platform.monthlyReturn}%</td>
                    <td className="px-6 py-4 whitespace-nowrap">{platform.yearlyReturn}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        
        {/* Optimized strategy */}
        <div className="p-4 bg-white rounded-lg border">
          <h2 className="text-xl font-bold mb-4">Optimized Multi-Platform Strategy</h2>
          
          <div className="mt-6 p-4 bg-yellow-50 rounded-lg">
            <h3 className="font-medium text-lg mb-3">Current Capital Distribution</h3>
            <p className="mb-4">Optimized allocation of your ${initialCapital.toLocaleString()} starting capital:</p>
            <ul className="list-disc pl-6 space-y-2 mb-4">
              <li><strong>Robinhood:</strong> ${robinhoodCapital.toLocaleString()} (${Math.min(platformData.robinhood.dailyLimit, robinhoodCapital).toLocaleString()}/day effective throughput)</li>
              <li><strong>Coinbase:</strong> ${coinbaseCapital.toLocaleString()} (6-day cycle, rolling deposits)</li>
              <li><strong>Kraken:</strong> ${krakenCapital.toLocaleString()} (${Math.min(platformData.kraken.dailyLimit, krakenCapital).toLocaleString()}/day effective throughput)</li>
              <li><strong>CashApp:</strong> ${cashappCapital.toLocaleString()} (reserve for opportunistic trades)</li>
            </ul>
            
            <p className="font-medium mb-2">Daily Operational Schedule:</p>
            <div className="bg-white p-3 rounded mb-4">
              <p className="mb-1"><strong>Monday-Friday:</strong></p>
              <ul className="list-disc pl-6 space-y-1">
                <li>Deploy Robinhood capital ($1,000/day)</li>
                <li>Deploy Kraken capital (up to $5,000/day)</li>
                <li>Monitor Coinbase capital releases (after 6-day hold)</li>
              </ul>
              <p className="mt-3 mb-1"><strong>Timing Strategy:</strong></p>
              <ul className="list-disc pl-6 space-y-1">
                <li>Morning: Initiate transfers from purchasing platforms</li>
                <li>Afternoon: Execute P2P trades on Binance</li>
                <li>Evening: Prepare next day's transactions</li>
              </ul>
            </div>
            
            <p className="font-medium mb-2">Maximum Monthly Throughput:</p>
            <p className="text-lg font-bold text-green-600 mb-2">
              ${(platformData.robinhood.dailyLimit * 30 + platformData.kraken.dailyLimit * 30 + coinbaseCapital / 2).toLocaleString()}
            </p>
            <p className="text-sm text-gray-600 mb-3">
              (Based on Robinhood: ${(platformData.robinhood.dailyLimit * 30).toLocaleString()}, Kraken: ${(platformData.kraken.dailyLimit * 30).toLocaleString()}, 
              Coinbase: ~${(coinbaseCapital / 2).toLocaleString()} with 6-day cycle)
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CryptoArbitrageDashboard;
