import { MapContainer, TileLayer, Marker, Circle } from 'react-leaflet'
// MapContainer is the wrapper, 
// TileLayer draws the actual map tiles (from OpenStreetMap, free), 
// Marker drops a pin, 
// Circle draws  10 NM safe zone + confidence circles


function MapPanel() {
    // The launch coordinates of the launchpad
    const launchSite = [47.965378, -81.873536]
    const radiusInMetres = 18520 // 10 nm
    const bounds = [
        [launchSite[0] - 0.2, launchSite[1] - 0.2],
        [launchSite[0] + 0.2, launchSite[1] + 0.2]
    ]

    return (
        <MapContainer center={launchSite} zoom={10} zoomSnap={0.25} zoomDelta={0.25} minZoom={9.5} maxBounds={bounds} maxBoundsViscosity={1.0} style={{ height: '100%', width: '100%' }}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
            <Marker position={launchSite} />
            <Circle center={launchSite} radius={radiusInMetres} pathOptions={{ color: 'red', dashArray: '8' }} />
        </MapContainer>
    )
}

export default MapPanel