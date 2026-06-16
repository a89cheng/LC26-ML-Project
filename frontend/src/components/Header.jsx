function Header() {
    const now = new Date().toLocaleString();

    return (
        <header className="h-24 px-8 flex items-center justify-between bg-gradient-to-b from-[#0a0e1a] to-[#111827] border-b border-slate-700">
            <div>
                <h1 className="text-2xl font-bold tracking-wide text-yellow-500">
                    UWATERLOO POLARIS
                </h1>
                <p className="text-sm uppercase tracking-[0.25em] text-blue-300">
                    Launch Canada 2026 Dashboard
                </p>
            </div>

            <div className="text-right">
                <p className="text-xs uppercase tracking-wider text-slate-400">
                    Countdown until launch window
                </p>
                <p className="font-mono text-lg text-cyan-300">
                    {now}
                </p>
            </div>
        </header>
    );
}

export default Header