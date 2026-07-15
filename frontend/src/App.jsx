/* import logo from "./assets/RocketryLogo.png";*/
import Header from "./components/Header"
import SafetyGauge from "./components/SafetyGauge"
import TimelineBar from "./components/TimelineBar"
import MapPanel from "./components/MapPanel"
import WindProfileChart from "./components/WindProfileChart"

// Access them off the object:
import hooks from './hooks/usePredictions'; 
import useWeather from './hooks/useWeather';

import { useState } from "react"

function App() {
    const [selectedHour, setSelectedHour] = useState(null);

    const { data: predictions } = hooks.usePredictions();
    const { data: hourData } = hooks.usePrediction(selectedHour);

    // default export from useWeather; no import needed
    const { data: weatherData, loading: weatherLoading, error: weatherError } = useWeather();

    return (
    <div className="min-h-screen bg-[#0a0e1a]">
        {/*The header*/}
        <Header />

        {/*The top half*/}
        <div className="flex items-stretch">
            <div className="outline outline-2 outline-blue-100 w-2/3 h-[450px]">
                <MapPanel />
            </div>
            <div className="w-1/3 flex">
                <SafetyGauge />
            </div>
        </div>

        {/*The bottom half*/}
        <div>
            <div className=''>
                <TimelineBar predictions={predictions} />
            </div>
            <div>
                <WindProfileChart weather={weatherData}/>
            </div>
        </div>
    </div>
    )
}

export default App;