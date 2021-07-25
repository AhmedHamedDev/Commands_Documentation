// import logo from './logo.svg';
// import './App.css';
import React from 'react';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

class connectionExample extends React.Component{
    componentDidMount(){
        const apiUrl = 'http://127.0.0.1:8000/api/';
        fetch(apiUrl)
            .then(response => response.json())
            .then(data => console.log(data))
    }

    render(){
        return <div> Connected </div>
    }
}

export default connectionExample;
