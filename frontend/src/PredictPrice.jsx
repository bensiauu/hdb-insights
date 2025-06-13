import { useEffect, useState } from "react";
import { MdAttachMoney, MdExpandMore, MdExpandLess } from "react-icons/md";

export default function PricePrediction() {
  /* ───────────── state ───────────── */
  const [town, setTown] = useState("");
  const [flatType, setFlatType] = useState("");
  const [storeyRange, setStoreyRange] = useState("");
  const [leaseYear, setLeaseYear] = useState("");

  // optional fields
  const [month, setMonth] = useState("");
  const [floorArea, setFloorArea] = useState("");
  const [flatModel, setFlatModel] = useState("");
  const [block, setBlock] = useState("");
  const [streetName, setStreetName] = useState("");

  // ui helpers
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [townOptions, setTownOptions] = useState([]);
  const [flatTypeOptions, setFlatTypeOptions] = useState([]);
  const [storeyOptions, setStoreyOptions] = useState([]);
  const [predicted, setPredicted] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:8001/api/options/town").then((r) => r.json()),
      fetch("http://localhost:8001/api/options/flat_type").then((r) =>
        r.json(),
      ),
      fetch("http://localhost:8001/api/options/storey_range").then((r) =>
        r.json(),
      ),
    ])
      .then(([towns, types, storey]) => {
        setTownOptions(towns);
        setFlatTypeOptions(types);
        setStoreyOptions(storey);
      })
      .catch(() => console.error("Failed to fetch select options"));
  }, []);

  const handlePredict = async (e) => {
    e.preventDefault();
    setError("");
    setPredicted(null);
    setLoading(true);

    const body = {
      town: town.toUpperCase(),
      flat_type: flatType.toUpperCase(),
      storey_range: storeyRange,
      lease_commence_date: Number(leaseYear),
    };
    if (month) body.month = month;
    if (floorArea) body.floor_area_sqm = Number(floorArea);
    if (flatModel) body.flat_model = flatModel;
    if (block) body.block = block;
    if (streetName) body.street_name = streetName;

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error(await res.text());
      const { prediction } = await res.json();
      setPredicted(prediction);
    } catch (err) {
      setError(err.message || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-2xl font-semibold mb-4 flex items-center gap-2">
        <MdAttachMoney /> Predict Resale Price
      </h2>

      <form onSubmit={handlePredict} className="flex flex-col gap-4">
        {/* required fields */}
        <div className="flex flex-col md:flex-row gap-4">
          <select
            value={town}
            onChange={(e) => setTown(e.target.value)}
            required
            className="flex-1 bg-white border border-gray-300 rounded px-3 py-2"
          >
            <option value="">Select Town</option>
            {townOptions.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>

          <select
            value={flatType}
            onChange={(e) => setFlatType(e.target.value)}
            required
            className="flex-1 bg-white border border-gray-300 rounded px-3 py-2"
          >
            <option value="">Flat Type</option>
            {flatTypeOptions.map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>

          <select
            value={storeyRange}
            onChange={(e) => setStoreyRange(e.target.value)}
            required
            className="flex-1 bg-white border border-gray-300 rounded px-3 py-2"
          >
            <option value="">Storey Range</option>
            {storeyOptions.map((f) => (
              <option key={f} value={f}>
                {f}
              </option>
            ))}
          </select>

          <input
            type="number"
            min={1966}
            max={new Date().getFullYear()}
            placeholder="Lease Yr"
            value={leaseYear}
            onChange={(e) => setLeaseYear(e.target.value)}
            required
            className="flex-1 bg-white border border-gray-300 rounded px-3 py-2"
          />
        </div>

        {/* advanced toggle */}
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center gap-1 text-green-700 hover:underline self-start"
        >
          {showAdvanced ? <MdExpandLess /> : <MdExpandMore />}
          {showAdvanced ? "Hide" : "Show"} advanced options
        </button>

        {showAdvanced && (
          <div className="grid md:grid-cols-2 gap-4">
            <input
              type="text"
              placeholder="YYYY-MM"
              value={month}
              onChange={(e) => setMonth(e.target.value)}
              className="bg-white border border-gray-300 rounded px-3 py-2"
            />
            <input
              type="number"
              placeholder="Floor Area (sqm)"
              value={floorArea}
              onChange={(e) => setFloorArea(e.target.value)}
              className="bg-white border border-gray-300 rounded px-3 py-2"
            />
            <input
              type="text"
              placeholder="Flat Model"
              value={flatModel}
              onChange={(e) => setFlatModel(e.target.value)}
              className="bg-white border border-gray-300 rounded px-3 py-2"
            />
            <input
              type="text"
              placeholder="Block"
              value={block}
              onChange={(e) => setBlock(e.target.value)}
              className="bg-white border border-gray-300 rounded px-3 py-2"
            />
            <input
              type="text"
              placeholder="Street Name"
              value={streetName}
              onChange={(e) => setStreetName(e.target.value)}
              className="bg-white border border-gray-300 rounded px-3 py-2 md:col-span-2"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="mt-2 bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? "Predicting…" : "Predict"}
        </button>
      </form>

      {error && <p className="mt-4 text-red-600 font-medium">Error: {error}</p>}

      {predicted !== null && !error && (
        <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded text-center">
          <p className="text-xl font-semibold text-green-700">
            {predicted.toLocaleString("en-SG", {
              style: "currency",
              currency: "SGD",
              maximumFractionDigits: 0,
            })}
          </p>
          <p className="text-sm text-gray-600">Estimated resale price</p>
        </div>
      )}
    </section>
  );
}
