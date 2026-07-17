import L from 'leaflet' // This should be useful to make custom icons
import { MapContainer, TileLayer, Marker, Circle, CircleMarker, Tooltip} from 'react-leaflet'
// MapContainer is the wrapper, 
// TileLayer draws the actual map tiles (from OpenStreetMap, free), 
// Marker drops a pin, 
// Circle draws  10 NM safe zone + confidence circles

// predictions is an array of JSONs with the keys:
// ["forecast_hour", "scenario", "landing_lat", "landing_lon", "predicted_dist_nm", "p_safe_launch" , "go_no_go"]
// The scenarios are: "main", "ballistic", "nominal", "drogue_only"

function MapPanel({predictions}) {
    // The launch coordinates of the launchpad
    const launchSite = [47.965378, -81.873536]
    const lodgeSite = [47.8708, -81.6875]
    const radiusInMetres = 18520 // 10 nm

    const bounds = [
        [launchSite[0] - 0.2, launchSite[1] - 0.2],
        [launchSite[0] + 0.2, launchSite[1] + 0.2]
    ]

    const scenarioColours = {
        main: "#2563eb",         // blue
        nominal: "#16a34a",      // green
        ballistic: "#dc2626",    // red
        drogue_only: "#f59e0b"   // orange
    }

    const launchIcon = L.divIcon({
        className: "",
        html: `
            <div style="
                background-color: #000000ff;
                width: 16px;
                height: 16px;
                border-radius: 50%;
                border: 3px solid white;
            "></div>
        `,
        iconSize: [16, 16],
        iconAnchor: [8, 8],
    })

    const lodgeIcon = L.divIcon({
        className: "",
        html: `
            <div style="
                font-size: 28px;
                transform: translate(-50%, -50%);
            ">
                🛖
            </div>
        `,
        iconSize: [45, 45],
        iconAnchor: [15, 15],
    })

    return (
        <MapContainer center={launchSite} zoom={10.7} zoomSnap={0.25} zoomDelta={0.25} minZoom={10.5} maxBounds={bounds} maxBoundsViscosity={1.0} style={{ height: '100%', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            
            <Marker position={launchSite} icon={launchIcon}>
                <Tooltip>Launch Site: 47.965378, -81.873536</Tooltip>
            </Marker>
            <Marker position={lodgeSite} icon={lodgeIcon}>
                <Tooltip>Tata Chika Pika Lake Lodge: 47.8708, -81.6875</Tooltip>
            </Marker>

            <Circle center={launchSite} radius={radiusInMetres} pathOptions={{ color: 'red', dashArray: '8' }} />

            {predictions.map((prediction, index) => (
                <CircleMarker
                    key={index}
                    center={[prediction.landing_lat, prediction.landing_lon]}
                    radius={6}
                    pathOptions={{
                        color: scenarioColours[prediction.scenario],
                        fillColor: scenarioColours[prediction.scenario],
                        fillOpacity: 1
                    }}
                >
                    <Tooltip>
                        {new Date(prediction.forecast_hour).toLocaleString([], {
                            weekday: "short",
                            hour: "numeric",
                            minute: "2-digit",
                        })} {": "}
                        {prediction.landing_lat} {","}{prediction.landing_lon}
                    </Tooltip>
                </CircleMarker>
            ))}
        </MapContainer>
    )
}

export default MapPanel