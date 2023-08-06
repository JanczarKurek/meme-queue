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
        <NewsBar events = {this.state.events} />
        <MainContent events = {this.state.events} />
        <StatusBar events = {this.state.events} />
      </div>
    );
  }

  componentDidMount() {
      this.getCurrentEvents(this.host + "/queue/v1/currentEvents")
      setInterval(() => this.refreshEvents(), 10000)
  }

  getCurrentEvents(url) {
    fetch(url,
    {
      mode: 'cors',
      headers: {'Content-Type':'application/json'}
    })
    .then(async res => {
      const data = await res.json();
      this.setState({events : data})
    }).catch(err => console.log(err))
  }

  refreshEvents() {
    fetch(this.host + "/queue/v1/events",
    {
      mode: 'cors',
      headers: {'Content-Type':'application/json'}
    })
    .then(async res => {
      const data = await res.json();
      this.setState({events : [data[this.state.i % data.length]], i : this.state.i + 1})
    }).catch(err => console.log(err))
  }

}



export default App;
