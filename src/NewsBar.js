
import React from 'react';

class NewsBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      message: "Memiarka stała się tymczasowo szopiarką"
    };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.event === this.props.event)
      return;

    if (this.props.event && this.props.event.type === "news") {
      this.setState({message: this.props.event.message})
    }
  }

  render() {
    return (
      <div className="NewsBar">
        <marquee>{this.state.message}</marquee>
      </div>
    )
  }
}



export default NewsBar;