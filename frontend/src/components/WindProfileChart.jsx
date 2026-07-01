import { useState } from "react"
import { useEffect, useRef } from "react"
import { mockAltitudes } from "../mock_data.jsx"
import {
    Chart, LineController,
    LineElement, PointElement,
    LinearScale, CategoryScale,
    Tooltip, Title
} from "chart.js"

Chart.register(
    LineController,
    LineElement, PointElement,
    LinearScale, CategoryScale,
    Tooltip, Title
)


function WindProfileChart () {
    // Initially set to null since canvas not made yet
    const canvasRef = useRef(null)
    const [times, updateTimes] = useState(1)

    // Need a state of usage; should be an enum (Next Hour, 4 hours, 8 hours, 16 hours, 24 hours, 56 hours)
    const ranges = [
        { h: 1,  color: "#efc851ff" },
        { h: 4,  color: "#60a5fa" },
        { h: 8,  color: "#34d399" },
        { h: 16, color: "#f472b6" },
        { h: 24, color: "#fb923c" },
        { h: 56, color: "#a78bfa" },
    ]

    useEffect(() => {
        const chart = new Chart(canvasRef.current, {
            type: "line",
            data: {
                datasets: Array.from({ length: times }, (_, i) => {
                    const hour = i + 1
                    const color = `hsl(${(hour / times) * 240}, 70%, 60%)`
                    return {
                        data: mockAltitudes[hour].map(d => ({ x: d.windSpeed, y: d.altitude })),
                        borderColor: color,
                        backgroundColor: color,
                        pointRadius: 2,
                        tension: 0,
                    }
                })
            },
            options: {
                plugins: {
                    legend: { display: false },
                },
                scales: {
                    x: {
                        type: "linear",
                        title: { display: true, text: "Wind speed [m/s]", color: "#94a3b8" },
                        min: 0,
                        ticks: { color: "#94a3b8" },
                        grid: { color: "#1e293b" }
                    },
                    y: {
                        type: "linear",
                        title: { display: true, text: "Altitude [m]", color: "#94a3b8" },
                        min: 0,
                        ticks: { color: "#94a3b8" },
                        grid: { color: "#1e293b" }
                    }
                }
            }
        })

        return () => chart.destroy()
    }, [times])

    return (
        <div className="bg-[#111827] border border-[#1e293b] rounded-xl p-4">
            <div className="flex items-center justify-between mb-3">
                <p className="text-xl text-[#374151] font-mono">Wind profile</p>
                <div className="flex gap-2 pr-3">
                    {ranges.map(setting => (
                        <button
                            key={setting.h}
                            className="w-16 font-mono px-2 py-1 rounded-md border text-[#374151] border-[#1e293b]"
                            style={times === setting.h ? { borderColor: setting.color, color: setting.color } : {}}
                            onClick={() => updateTimes(setting.h)}
                        >
                            {setting.h}hrs
                        </button>
                    ))}
                </div>
            </div>
            <canvas ref={canvasRef} />
        </div>
    )
}

export default WindProfileChart 