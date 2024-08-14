import React from 'react';
import Spinner from "./Spinner"
class MainContent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      contentUrl: null,
      eventType: null,
    };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.events === this.props.events || !this.props.events)
      return;

    for (let event of this.props.events)
      if (event.resource_tag === "meme" || event.resource_tag === "commercial" )
        this.setState({ contentUrl: event.payload, eventType: event.resource_tag })

  }

  render() {

    let content = Spinner()
    if (this.state.eventType === "meme")
      content = (<img src={this.state.contentUrl} alt={this.state.contentUrl} class="meme-image" />)
    else if (this.state.eventType === "commercial" ) {
      content = (<video src={this.state.contentUrl} alt={this.state.contentUrl} class="commercial-video" autoplay="autoplay" loop="true"/>)
    }

    return (
      <div className="MainContent">
        {content}
      </div>
    )
  }


}
export default MainContent;