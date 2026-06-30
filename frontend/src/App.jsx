/* import logo from "./assets/RocketryLogo.png";*/
import Header from "./components/Header"
import SafetyGauge from "./components/SafetyGauge"
import TimelineBar from "./components/TimelineBar"

function App() {
    return (
    <div className="min-h-screen bg-[#0a0e1a]">
        <Header />
        <div className="flex items-stretch">
            <div className="outline outline-2 outline-blue-100 w-2/3">
                {/* Map placeholder */}
            </div>
            <div className="w-1/3 flex">
                <SafetyGauge />
            </div>
        </div>
        <div>
            <div className=''>
                <TimelineBar />
            </div>
        </div>
    </div>
    )
}

export default App;