import React from 'react';
import Spinner from "./Spinner"
import FoodStatus from "./FoodStatus"
import Queue from 'queue-fifo'

class MainContent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      contentUrl: null,
      eventType: null,
      showingFoodStatus: false,
      events: []
    };
    this.eventQueue = new Queue;
  }

  getNextEvent() {
    while (!this.eventQueue.isEmpty()) {
      const event = this.eventQueue.dequeue();
      if (event.decay_time === null) // Event is always fresh.
        return event;
      if (event.display_time + event.decay_time < Math.floor(Date.now() / 1000)) {
        return event;
      }
    }
    return null;
  }

  setNextState() {
    const event = this.getNextEvent();
    try {
      console.log("Pulled", event, "from queue");
      if (event === null) {
        setTimeout(() => this.setNextState(), 300);
        return;
      } else {
        if (event.resource_tag === "meme" || event.resource_tag === "commercial") {
          this.props.setCurrentMeme(event.payload);
        }
        this.setState({ ...this.state, contentUrl: event.payload, eventType: event.resource_tag, showingFoodStatus: event.resource_tag === "display_status" })
        setTimeout(() => this.setNextState(), event.minimal_display_time);
      }
    } catch (error) {
      console.log("During handling of an event", event, "something happened", error);
      setTimeout(() => this.setNextState(), 300);
    }
  }

  componentDidMount() {
    this.setNextState();
  }

  componentDidUpdate(prevProps) {
    if (prevProps.events === this.props.events || !this.props.events)
      return;
    for (let event of this.props.events)
      if (event.resource_tag === "meme" || event.resource_tag === "commercial" || event.resource_tag === "display_status") {
        console.log("Adding new event to the queue", event);
        this.eventQueue.enqueue(event);
      }
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