
import React from 'react';

class NewsBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      message: ""
    };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.events === this.props.events || !this.props.events)
      return;

    for (let event of this.props.events)
      if (event && event.type === "news")
        this.setState({message: event.message})

  }

  render() {
    if (this.state.message === "")
      return (<div></div>)
    else
      return (
        <div className="NewsBar">
          <marquee>{this.state.message}</marquee>
        </div>
      )
  }
}



export default NewsBar;