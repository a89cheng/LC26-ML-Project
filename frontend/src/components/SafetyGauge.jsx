function SafetyGauge({ predData, weatherData}) {
    console.log(weatherData)

    if (!weatherData || !predData || predData.length === 0) {
        return (
            <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 shadow-lg">
                <p className="text-slate-400 text-sm">Loading...</p>
            </div>
        );
    }
    
    let maxWind = 0;
    let maxHeight = 0;
    
    for (const [key, value] of Object.entries(weatherData)) {
        if (key.slice(0,11) === "wind_speed_") {
            console.log(key, value)
        }
        if (value > maxWind && key.slice(0,11) === "wind_speed_") {
            maxHeight = key.slice(11)
            maxWind = value
            console.log("this is the highest")
        }
    }


    
    return (
        <div className="bg-slate-900 border border-slate-700 rounded-2xl p-6 shadow-lg">

            <h2 className="text-xl font-semibold text-white mb-5">
                Hourly Prediction
            </h2>

            <div className="grid grid-cols-2 gap-y-2 text-sm mb-5">
                <span className="text-slate-400">Max Wind</span>
                <span className="text-slate-100">{maxWind.toFixed(4)}{" kph -> "}{(maxWind*0.539957).toFixed(4)}{" knots"}</span>

                <span className="text-slate-400">Height</span>
                <span className="text-slate-100">{maxHeight}{"m"}</span>
            </div>

            <hr className="border-slate-700 mb-4" />

            {/* Scenarios */}

            
            <div className="space-y-2 text-xs">
                <div className="mb-3">
                    {predData.map(row => {
                        const percentage = 100 * (row.predicted_dist_nm / 10);

                        let bgColor = "bg-red-400";
                        let textColor = "text-red-400";

                        if (percentage <= 60) {
                            bgColor = "bg-green-400";
                            textColor = "text-green-400";
                        } else if (percentage <= 80) {
                            bgColor = "bg-yellow-400";
                            textColor = "text-yellow-400";
                        } else if (percentage > 100) {
                            bgColor = "bg-red-600";
                            textColor = "text-red-600";
                        }

                        let scenarioName = "Nom"

                        if (row.scenario === "drogue_only") {
                            scenarioName = "Dro";
                        } else if (row.scenario === "main"){
                            scenarioName = "Main";
                        } else if (row.scenario === "ballistic"){
                            scenarioName = "Bal";
                        }

                        return(
                            <div key={row.scenario}>
                                <div className="flex justify-between text-sm mb-1">
                                    <span className="text-slate-300"> 

                                        {scenarioName}{": "}
                                        {(row.predicted_dist_nm).toFixed(2)}{" nm  "}
                                        ({(row.landing_lat).toFixed(3)},{(row.landing_lon).toFixed(3)}) 
                                    </span>
                                    <span className={`${textColor}`}>{(percentage).toFixed(2)}{"%"}</span>
                                </div>
                                <div className="pb-4">
                                    <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
                                        <div
                                            className={`h-full rounded-full ${bgColor}`}
                                            style={{width: `${percentage}%` }}
                                        />
                                    </div>
                                </div>
                            </div>
                        )
                    })}
                </div>
            </div>

        </div>
    )
}

export default SafetyGauge