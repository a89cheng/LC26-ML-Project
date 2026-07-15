import { useState, useEffect } from "react";

function useWeather () {
    const [state, setState] = useState({ data: [], loading: true, error: null });

    useEffect ( () => {
        // Use protection kids!
        let isMounted = true; 

        const fetchWeather = () => {
            fetch('http://127.0.0.1:8000/forecasts')
            .then( response => {
                if (!response.ok) {
                    throw new Error(`Server responded with status ${response.status}`);
                } 
                return response.json();
            })
            .then( data => {
                if (isMounted) {
                    setState({ data, loading: false, error: null });
                }
            })
            .catch ( error => {
                if (isMounted) {
                    setState({ data: [], loading: false, error: error.message });
                }
            })
        }
        
        fetchWeather();

        const intervalId = setInterval(fetchWeather, 60000);

        return () => {
            isMounted = false;
            clearInterval(intervalId);
        };
    }, [])
    
    return state;
}

export default useWeather;