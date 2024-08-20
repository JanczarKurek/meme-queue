import React from 'react';
import Spinner from "./Spinner"
import FoodStatus from "./FoodStatus"
import Queue from 'queue-fifo';

class MainContent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      contentUrl: null,
      eventType: null,
      showingFoodStatus: false,
      events: []
    };
    this.event_queue = new Queue;
    this.foodStatus = (<FoodStatus events={this.state.events} visible={this.state.showingFoodStatus}></FoodStatus>);
  }

  get_next_event() {
    while (!this.event_queue.isEmpty()) {
      const event = this.event_queue.dequeue();
      if (event.decay_time === null) // Event is always fresh
        return event;
      if (event.display_time + event.decay_time < Math.floor(Date.now() / 1000)) {
        return event;
      }
    }
    return null;
  }

  componentDidUpdate(prevProps) {
    if (prevProps.events === this.props.events || !this.props.events)
      return;


    this.setState({ ...this.state, events: this.props.events })

    for (let event of this.props.events)
      if (event.resource_tag === "meme" || event.resource_tag === "commercial" || event.resource_tag === "display_status")
        this.setState({ ...this.state, contentUrl: event.payload, eventType: event.resource_tag, showingFoodStatus: event.resource_tag === "display_status" })

  }

  // setNextEvent() {
  //   const event = this.get_next_event();
  //   if (event === null) {
  //     setTimeout(() => this.setNextEvent(), 1000);
  //     return
  //   }
  //   this.setState(...this.state, event.resource_tag = 
  // }

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
    setTimeout(() => this.setNextEvent(), 10000); // Put here time dependent on the resource...
    return (
      <div className="MainContent">
        <FoodStatus events={this.state.events} visible={this.state.showingFoodStatus}></FoodStatus>
        {content}
      </div>
    )
  }


}
export default MainContent;