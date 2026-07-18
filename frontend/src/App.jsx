import Header from "./components/Header"
import SafetyGauge from "./components/SafetyGauge"
import TimelineBar from "./components/TimelineBar"
import MapPanel from "./components/MapPanel"
import WindProfileChart from "./components/WindProfileChart"
import MapControls from "./components/MapControls"

import hooks from './hooks/usePredictions';
import useWeather from './hooks/useWeather';

import { useState, useEffect } from "react"

function App() {
    const [selectedHour, setSelectedHour] = useState(null);

    // Specifically between MapControls and the Map | Which cases, and start + end
    const [selectedScenarios, setSelectedScenarios] = useState(["nominal"]);
    const [startHour, setStartHour] = useState(null);
    const [endHour, setEndHour] = useState(null);

    const { data: predictionData } = hooks.usePredictions();
    const { data: hourData } = hooks.usePrediction(selectedHour);
    const { data: weatherData, loading: weatherLoading, error: weatherError } = useWeather();

    useEffect(() => {
        if (!selectedHour && predictionData.length > 0) {
            setSelectedHour(predictionData[0].forecast_hour);
        }
    }, [predictionData]);

    // Filter predictions for the map: matching scenario AND within the selected hour range
    // If startHour/endHour haven't been picked yet (still null), show everything
    const mapPredictions = predictionData.filter(p => {
        const matchesScenario = selectedScenarios.includes(p.scenario);
        const afterStart = !startHour || new Date(p.forecast_hour) >= new Date(startHour);
        const beforeEnd = !endHour || new Date(p.forecast_hour) <= new Date(endHour);
        return matchesScenario && afterStart && beforeEnd;
    });

    const hourWeather = weatherData.find(w => w.forecast_hour === selectedHour);

    return (
    <div className="min-h-screen bg-[#0a0e1a]">
        {/*The header*/}
        <Header />

        {/*The top half*/}
        <div className="flex items-stretch">
            <div className="outline outline-2 outline-blue-100 w-4/5 h-[730px]">
                <MapPanel predictions={mapPredictions} />
            </div>
            <div className="w-1/5 flex flex-col gap-3 p-3">
                <SafetyGauge 
                    predData={hourData} 
                    weatherData={hourWeather} 
                />
                <MapControls
                    predictions={predictionData}
                    selectedScenarios={selectedScenarios}
                    onScenarioToggle={setSelectedScenarios}
                    startHour={startHour}
                    endHour={endHour}
                    onStartHourChange={setStartHour}
                    onEndHourChange={setEndHour}
                />
            </div>
        </div>

        {/*The bottom half*/}
        <div>
            <div className=''>
                <TimelineBar predictions={predictionData} />
            </div>
            <div className="p-4">
                <WindProfileChart weather={weatherData} />
            </div>
        </div>
    </div>
    )
}

export default App;