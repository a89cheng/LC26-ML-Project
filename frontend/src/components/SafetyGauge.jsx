function SafetyGauge() {
    return (
        <div className="w-full border border-slate-500 p-6 font-mono text-slate-200">
            <h2 className="text-xl mb-6">
                Safety Predictions
            </h2>

            <div className="text-center text-3xl mb-3">
                87%
            </div>

            <div className="h-5 border border-slate-400 mb-6">
                <div className="h-full w-[87%] bg-slate-200" />
            </div>

            <div className="grid grid-cols-2 gap-y-3">
                <span>Decision</span>
                <span>GO</span>

                <span>Landing Dist.</span>
                <span>4.2 NM</span>

                <span>Max Wind</span>
                <span>11.4 mph</span>

                <span>Confidence</span>
                <span>92%</span>
            </div>
        </div>
    );
}

export default SafetyGauge