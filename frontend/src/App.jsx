import { useState } from "react";

export default function App() {
  // ── Predict Price State ──
  const [predictInput, setPredictInput] = useState({
    town: "",
    flat_model: "",
    floor_area_sqm: "",
    storey_range: "",
    remaining_lease: "",
    flat_type: "",
  });
  const [predictedPrice, setPredictedPrice] = useState(null);
  const [loadingPredict, setLoadingPredict] = useState(false);
  const [predictError, setPredictError] = useState("");

  // ── History State ──
  const [historyTown, setHistoryTown] = useState("");
  const [historyFlatType, setHistoryFlatType] = useState("");
  const [historyData, setHistoryData] = useState([]);
  const [loadingHistory, setLoadingHistory] = useState(false);
  const [historyError, setHistoryError] = useState("");

  // -- History Pagination --
  const [currentPage, setCurrentPage] = useState(1);
  const limit = 10;

  // ── Handlers for Predict Form ──
  const handlePredictChange = (e) => {
    const { name, value } = e.target;
    setPredictInput((prev) => ({ ...prev, [name]: value }));
  };

  const submitPredict = async (e) => {
    e.preventDefault();
    setPredictError("");
    setPredictedPrice(null);
    setLoadingPredict(true);

    try {
      const response = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          town: predictInput.town,
          flat_model: predictInput.flat_model,
          floor_area_sqm: predictInput.floor_area_sqm,
          storey_range: predictInput.storey_range,
          remaining_lease: predictInput.remaining_lease,
          flat_type: predictInput.flat_type,
        }),
      });
      if (!response.ok) {
        const err = await response.text();
        throw new Error(err || "Prediction Failed");
      }
      const data = await response.json();
      setPredictedPrice(data.predicted_price);
    } catch (err) {
      setPredictError(err.message);
    } finally {
      setLoadingPredict(false);
    }
  };

  // ── Handlers for History Form ──
  const handleHistoryChange = (e) => {
    setHistoryTown(e.target.value);
  };

  const handleHistoryFlatTypeChange = (e) => {
    setHistoryFlatType(e.target.value);
  };

  const fetchHistory = async (page = 1) => {
    setHistoryError("");
    setHistoryData([]);
    setLoadingHistory(true);

    try {
      const offset = (page - 1) * limit;
      const params = new URLSearchParams({
        town: historyTown.toUpperCase(),
        flat_type: historyFlatType.toUpperCase(),
        limit: String(limit),
        offset: String(offset),
      });

      const res = await fetch(
        `http://localhost:8001/api/history?${params.toString()}`,
      );
      if (!res.ok) {
        throw new Error((await res.text()) || "Fetch History Failed");
      }

      const data = await res.json();
      setHistoryData(data);
      setCurrentPage(page);
    } catch (err) {
      setHistoryError(err.message);
    } finally {
      setLoadingHistory(false);
    }
  };

  const submitHistory = async (e) => {
    e.preventDefault();
    fetchHistory(1);
  };

  const offset = (currentPage - 1) * limit;
  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 max-w-3xl mx-auto p-6 space-y-12">
      <h1 className="text-4xl font-bold text-center">HDB Resale Insights</h1>

      {/* ── Predict Resale Price Section ── */}
      <section className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-2xl font-semibold mb-4">Predict Resale Price</h2>
        <form
          onSubmit={submitPredict}
          className="grid grid-cols-1 md:grid-cols-3 gap-4"
        >
          {[
            {
              label: "Town",
              name: "town",
              type: "text",
              placeholder: "ANG MO KIO",
            },
            {
              label: "Flat Model",
              name: "flat_model",
              type: "text",
              placeholder: "Improved",
            },
            {
              label: "Floor Area (sqm)",
              name: "floor_area_sqm",
              type: "number",
              placeholder: "75",
            },
            {
              label: "Storey Range",
              name: "storey_range",
              type: "text",
              placeholder: "01 TO 03",
            },
            {
              label: "Remaining Lease (yrs)",
              name: "remaining_lease",
              type: "number",
              placeholder: "75",
            },
            {
              label: "Flat Type",
              name: "flat_type",
              type: "text",
              placeholder: "3 ROOM",
            },
          ].map(({ label, name, type, placeholder }) => (
            <div key={name} className="flex flex-col">
              <label className="font-medium mb-1">{label}</label>
              <input
                className="
                   bg-white
                   border border-gray-300
                   rounded
                   px-3 py-2
                   text-gray-900
                   placeholder-gray-500
                   focus:outline-none focus:ring-2 focus:ring-blue-400
                 "
                type={type}
                name={name}
                value={predictInput[name]}
                onChange={handlePredictChange}
                required
                placeholder={placeholder}
                step={type === "number" ? "0.1" : undefined}
              />
            </div>
          ))}

          <div className="col-span-1 md:col-span-3 flex justify-end">
            <button
              type="submit"
              disabled={loadingPredict}
              className="
                 mt-2
                 bg-blue-600
                 text-white
                 px-6 py-2
                 rounded
                 hover:bg-blue-700
                 disabled:opacity-50
                 disabled:cursor-not-allowed
               "
            >
              {loadingPredict ? "Predicting…" : "Predict Price"}
            </button>
          </div>
        </form>

        {predictError && (
          <p className="mt-4 text-red-600 font-medium">Error: {predictError}</p>
        )}
        {predictedPrice !== null && (
          <p className="mt-4 text-lg">
            Estimated Price:{" "}
            <span className="font-bold text-blue-700">
              ${predictedPrice.toLocaleString()}
            </span>
          </p>
        )}
      </section>

      {/* ── View Historical Prices Section ── */}
      <section className="bg-white shadow-md rounded-lg p-6">
        <h2 className="text-2xl font-semibold mb-4">View Historical Prices</h2>
        <form
          onSubmit={submitHistory}
          className="flex flex-col md:flex-row items-center gap-4"
        >
          <input
            className="
               flex-grow
               bg-white
               border border-gray-300
               rounded
               px-3 py-2
               text-gray-900
               placeholder-gray-500
               focus:outline-none focus:ring-2 focus:ring-green-500
             "
            type="text"
            value={historyTown}
            onChange={handleHistoryChange}
            required
            placeholder="Enter Town (e.g. ANG MO KIO)"
          />
          <input
            className="flex-grow bg-white border border-gray-300 rounded px-3 py-2 text-gray-900 placeholder-gray-500
               focus:outline-none focus:ring-2 focus:ring-green-500"
            type="text"
            value={historyFlatType}
            onChange={handleHistoryFlatTypeChange}
            required
            placeholder="Enter Flat Type (e.g. 3 ROOM)"
          />
          <button
            type="submit"
            disabled={loadingHistory}
            className="
               bg-green-600
               text-white
               px-6 py-2
               rounded
               hover:bg-green-700
               disabled:opacity-50
               disabled:cursor-not-allowed
             "
          >
            {loadingHistory ? "Loading…" : "Fetch History"}
          </button>
        </form>

        {historyError && (
          <p className="mt-4 text-red-600 font-medium">Error: {historyError}</p>
        )}
        {historyData && historyData.length > 0 && (
          <div className="mt-6 overflow-x-auto">
            <table className="min-w-full table-auto border-collapse">
              <thead>
                <tr className="bg-gray-200">
                  <th className="px-4 py-2 text-left text-gray-900"></th>
                  <th className="px-4 py-2 text-left text-gray-900">
                    Flat Type
                  </th>
                  <th className="px-4 py-2 text-left text-gray-900">Town</th>
                  <th className="px-4 py-2 text-left text-gray-900">
                    Lease Commencement
                  </th>
                  <th className="px-4 py-2 text-left text-gray-900">
                    Floor Area (sqm)
                  </th>
                  <th className="px-4 py-2 text-left text-gray-900">
                    Resale Price
                  </th>
                </tr>
              </thead>
              <tbody>
                {historyData.map((row, idx) => (
                  <tr key={offset + idx} className="hover:bg-gray-100">
                    <td className="border px-2 py-1">
                      {(currentPage - 1) * limit + idx + 1}
                    </td>
                    <td className="border px-2 py-1">{row.flat_type}</td>
                    <td className="border px-2 py-1">{row.town}</td>
                    <td className="border px-2 py-1">
                      {row.lease_commence_date}
                    </td>
                    <td className="border px-2 py-1">{row.floor_area_sqm}</td>
                    <td className="border px-2 py-1">
                      ${row.resale_price.toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div className="flex justify-center space-x-2">
              <button
                disabled={currentPage === 1}
                onClick={() => fetchHistory(currentPage - 1)}
                className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50"
              >
                Prev
              </button>
              <span className="px-3 py-1">Page {currentPage}</span>
              <button
                disabled={historyData.length < limit}
                onClick={() => fetchHistory(currentPage + 1)}
                className="px-3 py-1 bg-gray-300 rounded disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}
