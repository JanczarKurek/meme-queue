import React from "react";


function StatusBarItem({text, grow, children}) {
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
      this.setState({time: new Date().toLocaleTimeString('pl-PL')})
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
          cheeseStatus: "",
          memeFileName: "raccoon.jpg"
        };
    }

  updateEvents(events) {
    this.setState({memeFileName: events[0].url})
  }
  
  componentDidUpdate(prevProps) {
    if (prevProps.event === this.props.event || !this.props.event)
      return;

    if (this.props.event.type === "meme") {
      this.setState({memeFileName: this.props.event.url})
    } else if (this.props.event.type === "cheeseStatus") {
      this.setState({cheeseStatus: this.props.event.status})
    }
  }

  render() {
      return (
        <div className="StatusBar">
            <StatusBarItem text="internet.www"/>
            <StatusBarItem text={this.state.cheeseStatus}/>
            <StatusBarItem text={this.state.memeFileName} grow={true}/>
            <StatusBarItem> <Clock/> </StatusBarItem>
            
        </div>
      )
  }
}

export default StatusBar;