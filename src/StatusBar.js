import React from "react";
import Spinner from "./Spinner";

function StatusBarItem({ text, grow, children }) {
  let style = {
    flexGrow: grow ? 1 : 0
  };
  return (
    <div className="StatusBarItem" style={style}>
      {text}
      {children}
    </div>
  )
}

class Clock extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      time: new Date().toLocaleTimeString('pl-PL')
    };
  }

  componentDidMount() {
    setInterval(() => this.updateTime(), 1000)
  }

  updateTime() {
    this.setState({ time: new Date().toLocaleTimeString('pl-PL') })
  }


  render() {
    return (
      <div className="Clock">
        {this.state.time}
      </div>
    )
  }

}




class StatusBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      events: [],
      cheeseStatus: null,
      memeFileName: null,
    };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.events === this.props.events || !this.props.events)
      return;

    for (let event of this.props.events)
      if (event.resource_tag === "meme")
        this.setState({ memeFileName: event.payload })
      else if (event.resource_tag === "status") {
        console.log(event.payload.cheese)
        this.setState({ cheeseStatus: "🧀: " + event.payload.ser })
      }
  }

  render() {
    return (
      <div className="StatusBar">
        <StatusBarItem text="internet.www" />
        <StatusBarItem text={this.state.cheeseStatus} />
        <StatusBarItem text={this.state.memeFileName} grow={true} />
        <StatusBarItem> <Clock /> </StatusBarItem>

      </div>
    )
  }
}

export default StatusBar;