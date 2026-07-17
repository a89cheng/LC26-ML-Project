const SCENARIOS = [
    { value: "main", label: "Main" },
    { value: "drogue_only", label: "Drogue Only" },
    { value: "ballistic", label: "Ballistic" },
    { value: "nominal", label: "Nominal" },
]

function MapControls({
    predictions, // All the prediction data
    selectedScenarios, 
    onScenarioToggle, // The useState funtion to update scenarios
    startHour, // The actual start hour change value
    endHour, // The actual end hour change value
    onStartHourChange, // The actual start hour change function
    onEndHourChange, // The actual end hour change function
}) {
    // Build a de-duplicated, sorted list of available hours from the predictions data
    // (predictions has 4 rows per hour, so we dedupe by forecast_hour string)
    const availableHours = [...new Set(predictions.map(p => p.forecast_hour))].sort()

    const handleScenarioChange = (scenarioValue) => {
        if (selectedScenarios.includes(scenarioValue)) {
            onScenarioToggle(selectedScenarios.filter(s => s !== scenarioValue))
        } else {
            onScenarioToggle([...selectedScenarios, scenarioValue]) // Deconstruct + add the current
        }
    }

    const scenarioColours = {
        main: "#2563eb",         // blue
        nominal: "#16a34a",      // green
        ballistic: "#dc2626",    // red
        drogue_only: "#f59e0b"   // orange
    }

    return (
        <div className="bg-[#111827] border border-[#1e293b] rounded-xl p-4">
            <p className="text-sm text-gray-300 font-mono mb-2">Scenarios</p>
            <div className="space-y-1.5 mb-4">
                {SCENARIOS.map(scenario => (
                    <label
                        key={scenario.value}
                        className="flex items-center gap-2 text-xs text-gray-300 cursor-pointer"
                    >
                        <input
                            type="checkbox"
                            checked={selectedScenarios.includes(scenario.value)}
                            onChange={() => handleScenarioChange(scenario.value)}
                        />
                        <span
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: scenarioColours[scenario.value] }}
                        ></span>
                        <span>{scenario.label}</span>
                    </label>
                ))}
            </div>

            <p className="text-sm text-gray-300 font-mono mb-2">Hour Range</p>
            <div className="space-y-2">
                <div>
                    <label className="text-xs text-gray-500 block mb-1">Start</label>
                    <select
                        className="w-full bg-[#0a0e1a] border border-[#1e293b] rounded-md text-xs text-gray-300 p-1.5"
                        value={startHour ?? ""}
                        onChange={e => onStartHourChange(e.target.value)}
                    >
                        {availableHours.map(hour => (
                            <option key={hour} value={hour}>
                                {new Date(hour).toLocaleString("en-US", {
                                    month: "short",
                                    day: "numeric",
                                    weekday: "short",
                                    hour: "numeric",
                                    minute: "2-digit",
                                    hour12: true,
                                })}
                            </option>
                        ))}
                    </select>
                </div>
                <div>
                    <label className="text-xs text-gray-500 block mb-1">End</label>
                    <select
                        className="w-full bg-[#0a0e1a] border border-[#1e293b] rounded-md text-xs text-gray-300 p-1.5"
                        value={endHour ?? ""}
                        onChange={e => onEndHourChange(e.target.value)}
                    >
                        {availableHours.map(hour => (
                            <option key={hour} value={hour}>
                                {new Date(hour).toLocaleString("en-US", {
                                    month: "short",
                                    day: "numeric",
                                    weekday: "short",
                                    hour: "numeric",
                                    minute: "2-digit",
                                    hour12: true,
                                })}
                            </option>
                        ))}
                    </select>
                </div>
            </div>
        </div>
    )
}

export default MapControls