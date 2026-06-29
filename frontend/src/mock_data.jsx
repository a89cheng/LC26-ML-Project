export const mockHours = Array.from({ length: 168 }, (_, i) => {
    const date = new Date("2026-06-17T06:00:00")
    date.setHours(date.getHours() + i)
    return {
        forecast_hour: date.toISOString(),
        go_no_go: Math.random() > 0.4,
        p_safe_launch: Math.random(),
        predicted_dist_nm: (Math.random() * 12).toFixed(1),
    }
})