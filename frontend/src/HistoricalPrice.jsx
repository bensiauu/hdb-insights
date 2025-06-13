import { useEffect, useState } from "react";
import {
    MdApartment,
    MdLocationCity,
    MdEvent,
    MdSquareFoot,
    MdAttachMoney,
    MdArrowBack,
    MdArrowForward,
    MdLayers,
    MdStreetview,
} from "react-icons/md";

export default function HistoricalPrice() {
    // ── History State ──
    const [historyTown, setHistoryTown] = useState("");
    const [historyFlatType, setHistoryFlatType] = useState("");
    const [historyData, setHistoryData] = useState([]);
    const [loadingHistory, setLoadingHistory] = useState(false);
    const [historyError, setHistoryError] = useState("");
    const [flatTypeOptions, setFlatTypeOptions] = useState([]);
    const [townOptions, setTownOptions] = useState([]);

    // -- History Pagination --
    const [currentPage, setCurrentPage] = useState(1);
    const limit = 10;

    useEffect(() => {
        fetch("http://localhost:8001/api/options/town")
            .then((res) => res.json())
            .then(setTownOptions)
            .catch((err) => console.error("Failed to fetch town options", err));

        fetch("http://localhost:8001/api/options/flat_type")
            .then((res) => res.json())
            .then(setFlatTypeOptions)
            .catch((err) =>
                console.error("Failed to fetch flat_type options", err),
            );
    }, []);

    // ── Handlers for History Form ──
    const fetchHistory = async (page = 1) => {
        setHistoryError("");
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
        <section className="bg-white shadow-md rounded-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">
                View Historical Prices
            </h2>
            <form
                onSubmit={submitHistory}
                className="flex flex-col md:flex-row items-center gap-4"
            >
                <select
                    value={historyTown}
                    onChange={(e) => setHistoryTown(e.target.value)}
                    required
                    className="flex-grow bg-white border border-gray-300 rounded px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                    <option value="">Select Town</option>
                    {townOptions.map((town) => (
                        <option key={town} value={town}>
                            {town}
                        </option>
                    ))}
                </select>
                <select
                    value={historyFlatType}
                    onChange={(e) => setHistoryFlatType(e.target.value)}
                    required
                    className="flex-grow bg-white border border-gray-300 rounded px-3 py-2 text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                    <option value="">Select Flat Type</option>
                    {flatTypeOptions.map((type) => (
                        <option key={type} value={type}>
                            {type}
                        </option>
                    ))}
                </select>
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
               disabled:cursor-not-allowed transition-colors duration-200
             "
                >
                    {loadingHistory ? "Loading…" : "Fetch History"}
                </button>
            </form>

            {historyError && (
                <p className="mt-4 text-red-600 font-medium">
                    Error: {historyError}
                </p>
            )}
            {historyData && historyData.length > 0 && (
                <div className="mt-6 overflow-x-auto">
                    <div className="mt-6 overflow-x-auto rounded-lg border border-gray-300 shadow-sm">
                        <table className="min-w-full table-auto border-collapse">
                            <thead>
                                <tr className="bg-gray-200">
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        #
                                    </th>
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        <div className="flex items-center gap-1">
                                            <MdApartment /> Flat Type
                                        </div>
                                    </th>
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        <div className="flex items-center gap-1">
                                            <MdLocationCity /> Town
                                        </div>
                                    </th>
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        <div className="flex items-center gap-1">
                                            <MdStreetview /> Street
                                        </div>
                                    </th>
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        <div className="flex items-center gap-1">
                                            <MdLayers /> Storey Range
                                        </div>
                                    </th>
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        <div className="flex items-center gap-1">
                                            <MdEvent /> Lease Start
                                        </div>
                                    </th>
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        <div className="flex items-center gap-1">
                                            <MdSquareFoot /> Area (sqm)
                                        </div>
                                    </th>
                                    <th className="px-4 py-2 text-left text-gray-900">
                                        <div className="flex items-center gap-1">
                                            <MdAttachMoney /> Price
                                        </div>
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                {historyData.map((row, idx) => (
                                    <tr
                                        key={offset + idx}
                                        className={`${
                                            idx % 2 === 0
                                                ? "bg-white"
                                                : "bg-gray-50"
                                        } hover:bg-gray-100`}
                                    >
                                        <td className="border px-2 py-1 font-medium">
                                            {(currentPage - 1) * limit +
                                                idx +
                                                1}
                                        </td>
                                        <td className="border px-2 py-1">
                                            {row.flat_type}
                                        </td>
                                        <td className="border px-2 py-1">
                                            {row.town}
                                        </td>
                                        <td className="border px-2 py-1">
                                            {row.street_name}
                                        </td>

                                        <td className="border px-2 py-1">
                                            {row.storey_range}
                                        </td>
                                        <td className="border px-2 py-1">
                                            {row.lease_commence_date}
                                        </td>
                                        <td className="border px-2 py-1">
                                            {row.floor_area_sqm}
                                        </td>
                                        <td className="border px-2 py-1 font-semibold text-green-700">
                                            ${row.resale_price.toLocaleString()}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                    <div className="mt-4 flex justify-center items-center gap-2">
                        <button
                            disabled={currentPage === 1}
                            onClick={() => fetchHistory(currentPage - 1)}
                            className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                        >
                            <MdArrowBack />
                            Prev
                        </button>

                        <span className="px-4 py-2 text-sm font-medium text-gray-700">
                            Page {currentPage}
                        </span>

                        <button
                            disabled={historyData.length < limit}
                            onClick={() => fetchHistory(currentPage + 1)}
                            className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            Next
                            <MdArrowForward />
                        </button>
                    </div>
                </div>
            )}
        </section>
    );
}
