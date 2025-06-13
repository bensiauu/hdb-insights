import HistoricalPrice from "./HistoricalPrice";
import PredictPrice from "./PredictPrice";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-tr from-blue-50 via-white to-green-100 text-gray-900 w-full px-4 sm:px-6 lg:px-12 py-6">
      <h1 className="text-4xl font-bold text-center text-blue-800">
        HDB Resale Insights
      </h1>
      <hr className="my-8 border-t border-gray-300" />
      <HistoricalPrice />
      <hr className="my-8 border-t border-gray-300" />
      <PredictPrice />
    </div>
  );
}
