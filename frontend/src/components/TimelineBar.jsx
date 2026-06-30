import { mockHours } from "../mock_data.jsx"

function TimelineBar() {
    const launchHours = mockHours.filter(hour => {
        const h = new Date(hour.forecast_hour).getHours()
        return h >= 11 && h < 19
    })

    return (
        <div className="flex overflow-x-auto gap-3 p-3">
            {launchHours.map(hour => {
                const date = new Date(hour.forecast_hour)

                // Ternary: pick styles based on go_no_go being true or false

                const badgeClass = hour.go_no_go
                    ? "bg-[#052e16] text-[#86efac] border-[#166534]"
                    : "bg-[#2d0a0a] text-[#fca5a5] border-[#991b1b]"

                const statClass = hour.go_no_go
                    ? "text-green-700"
                    : "text-red-700"

                const textValue = hour.go_no_go
                    ? "✓" 
                    : "✗"

                return (
                    <div
                        key={hour.forecast_hour}
                        className={`rounded-xl w-48 flex-shrink-0 p-4 bg-[#111827] border border-[#1e293b]`}
                    >
                        <div className="flex items-center gap-3 mb-3">
                            <span className={`inline-block text-xl font-semibold px-3 py-1.5 rounded-md mb-3 ${badgeClass}`}>
                                {textValue}
                            </span>

                            <div>
                                <div className="font-mono text-2xl font-medium text-[#f1f5f9] leading-none">
                                    {date.toLocaleTimeString("en-US", {
                                        hour: "numeric",
                                        timeZone: "America/Toronto",
                                        hour12: true,
                                    })}
                                </div>
                                <div className="text-xs text-gray-500 mt-0.5">
                                    {date.toLocaleDateString("en-US", {
                                        weekday: "short",
                                        month: "short",
                                        day: "numeric",
                                    })}
                                </div>
                            </div>
                        </div>
                        
                        <div className="w-full h-1.5 bg-[#1e293b] rounded-full overflow-hidden">
                            <div
                                className={`h-full ${hour.go_no_go ? "bg-[#22c55e]" : "bg-[#ef4444]"} rounded-full`}
                                style={{ width: `${hour.p_safe_launch}%` }}
                            />
                        </div>

                        {/* Stat rows */}
                        <div className="border-t pt-2 space-y-1.5">
                            <div className="flex justify-between items-center">
                                <span className="text-xs text-gray-300">Predicted Coords.</span>
                                {/* toFixed(1) rounds to 1 decimal place */}
                                <span className={`text-xs font-medium ${statClass}`}>
                                    {hour.p_safe_launch.toFixed(1)}%
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-xs text-gray-300">Distance</span>
                                {/* Template literal: appends " nm" unit to the number */}
                                <span className="text-xs font-medium text-gray-500">
                                    {`${hour.predicted_dist_nm} nm`}
                                </span>
                            </div>
                        </div>
                    </div>
                )
            })}
        </div>
    )
}

export default TimelineBar