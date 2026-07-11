import { useState, useEffect } from 'react';
// the actually have to be imported fromr React...

function usePredictions() {
  // state is the variable, and the default values are set below
  const [state, setState] = useState({ data: [], loading: true, error: null });

  useEffect(() => {
    let isMounted = true; // guards against updating state after unmount

    // The arrow function inside the function to actually fetch the data 
    // Define it before calling it
    const fetchPredictions = () => {
      fetch('http://127.0.0.1:8000/predictions')
        // response.ok only returns turn for 2XX response codes; only return if it exists and in JSON form
        .then(response => {
          if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
          }
          return response.json();
        })
        // change the loading to false, since it the response has returned
        // if the data exits, it replaces the empty data array, and if not, error message!
        .then(data => {
          if (isMounted) {
            setState({ data, loading: false, error: null });
          }
        })
        .catch(error => {
          if (isMounted) {
            setState({ data: [], loading: false, error: error.message });
          }
        });
    };

    fetchPredictions(); // run once immediately

    // Set an interval for running this I presume? 
    const intervalId = setInterval(fetchPredictions, 60000); 

    return () => {
      isMounted = false;
      clearInterval(intervalId);
    };
  }, []);

  return state; // return the variable in form: { data, loading, error }
}

export default usePredictions;