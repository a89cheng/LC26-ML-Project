function TimelineBar({ predictions }) {
    const nominalHours = predictions
        .filter(p => p.scenario === "nominal")
        .map(hour => {
            const safeLaunch =  ((10 - hour.predicted_dist_nm) / 10) * 100

            return {
                ...hour,
                p_safe_launch: safeLaunch,
                go_no_go: safeLaunch >= 25
            };
        });
    
    return (
        <div className="flex overflow-x-auto gap-3 p-3">
            {nominalHours.map(hour => {
                const date = new Date(hour.forecast_hour)

                // Ternary: pick styles based on go_no_go being true or false
                const badgeClass = hour.go_no_go
                    ? "bg-[#052e16] text-[#86efac] border-[#166534]"
                    : "bg-[#2d0a0a] text-[#fca5a5] border-[#991b1b]"

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
                                <span className="text-xs text-gray-300">Coords.</span>
                                <span className="text-xs font-medium text-gray-500">
                                    {`${hour.landing_lat.toFixed(4)}, ${hour.landing_lon.toFixed(4)}`}
                                </span>
                            </div>
                            <div className="flex justify-between items-center">
                                <span className="text-xs text-gray-300">Distance</span>
                                {/* Template literal: appends " nm" unit to the number */}
                                <span className="text-xs font-medium text-gray-500">
                                    {`${hour.predicted_dist_nm.toFixed(4)} nm`}
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