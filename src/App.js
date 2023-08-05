import './App.css';
import React from 'react';

import NewsBar from './NewsBar';
import MainContent from './MainContent';
import StatusBar from './StatusBar';

class App extends React.Component {
  MAX_QUEUE_SIZE = 10;
  host = "http://localhost:5000";

  constructor(props) {
    super(props);
    this.state = {
      i : 0,
    }
  }

  render() {
    return (
      <div className="App">
        <NewsBar event = {this.state.event} />
        <MainContent event = {this.state.event} />
        <StatusBar event = {this.state.event} />
      </div>
    );
  }

  componentDidMount() {
      setInterval(() => this.refreshEvents(), 5000)
  }

  refreshEvents() {
    fetch(this.host + "/queue/v1/events",
    {
      mode: 'cors',
      headers: {'Content-Type':'application/json'}
    })
    .then(async res => {
      const data = await res.json();
      this.setState({event : data[this.state.i % data.length]})
    }).catch(err => console.log(err))
    this.setState({i : this.state.i + 1})
  }

}



export default App;
