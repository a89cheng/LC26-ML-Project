/* import logo from "./assets/RocketryLogo.png";*/
import Header from "./components/Header"
import SafetyGauge from "./components/SafetyGauge"
import TimelineBar from "./components/TimelineBar"
import MapPanel from "./components/MapPanel"
import WindProfileChart from "./components/WindProfileChart"

function App() {
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
                <TimelineBar />
            </div>
            <div>
                <WindProfileChart />
            </div>
        </div>
    </div>
    )
}

export default App;