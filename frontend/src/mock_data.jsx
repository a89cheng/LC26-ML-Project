export const mockHours = Array.from({ length: 168 }, (_, i) => {
    const date = new Date("2026-06-17T06:00:00")
    date.setHours(date.getHours() + i)
    return {
        forecast_hour: date.toISOString(),
        go_no_go: Math.random() > 0.4,
        p_safe_launch: Math.random() * 100,
        predicted_dist_nm: (Math.random() * 12).toFixed(1),
    }
})

const altitudes = [110, 320, 500, 800, 1000, 1500, 1900, 3200, 4200, 5600, 7200, 9200, 10400, 11800, 13500, 15800, 17700, 19300, 22000]

export const mockAltitudes = altitudes.map(altitude => ({
    altitude: altitude,
    windSpeed: altitude < 1000 ? Math.random() * 30 :
           altitude < 5000 ? Math.random() * 60 :
           Math.random() * 150,
    windDirection: Math.floor(Math.random() * 360),
}))