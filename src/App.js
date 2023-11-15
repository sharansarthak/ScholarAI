import './App.css';

import React,{useState, useEffect} from 'react';

//useState is the state variable that is able to transfer data from backend to front end


function App() {

  const [data, setData] = useState([{}])
  useEffect(() => {
    fetch("/members").then( //fetch the data from that route
      res => res.json() 
    ).then(
      data => {
        setData(data)
        console.log(data)
      }
    )
  }, [])

  return (
    <div className="App">

    </div>
  );
}

export default App;
