import React from 'react';
import Spinner from "./Spinner"
import FoodStatus from "./FoodStatus"

class MainContent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      contentUrl: null,
      eventType: null,
      showingFoodStatus: false,
      events: []
    };
    this.foodStatus = (<FoodStatus events={this.state.events} visible={this.state.showingFoodStatus}></FoodStatus>);
  }

  componentDidUpdate(prevProps) {
    if (prevProps.events === this.props.events || !this.props.events)
      return;


    this.setState({ ...this.state, events: this.props.events })

    for (let event of this.props.events)
      if (event.resource_tag === "meme" || event.resource_tag === "commercial" || event.resource_tag === "display_status")
        this.setState({ ...this.state, contentUrl: event.payload, eventType: event.resource_tag, showingFoodStatus: event.resource_tag === "display_status" })

  }

  render() {

    let content = Spinner()
    if (this.state.eventType === "meme")
      content = (<img src={this.state.contentUrl} alt={this.state.contentUrl} class="meme-image" />)
    else if (this.state.eventType === "commercial") {
      content = (<video src={this.state.contentUrl} alt={this.state.contentUrl} class="meme-image" autoplay="autoplay" loop="true" />)
    }
    else if (this.state.eventType === "display_status") {
      content = (<div></div>)
    }

    return (
      <div className="MainContent">
        <FoodStatus events={this.state.events} visible={this.state.showingFoodStatus}></FoodStatus>
        {content}
      </div>
    )
  }


}
export default MainContent;