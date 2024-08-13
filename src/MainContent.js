import React from 'react';
import Spinner from "./Spinner"
class MainContent extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      imgUrl: null
    };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.events === this.props.events || !this.props.events)
      return;

    for (let event of this.props.events)
      if (event.resource_tag === "meme")
        this.setState({ imgUrl: event.payload })

  }

  render() {

    let content = Spinner()
    if (this.state.imgUrl !== null)
      content = (<img src={this.state.imgUrl} alt={this.state.imgUrl} />)

    return (
      <div className="MainContent">
        {content}
      </div>
    )
  }


}
export default MainContent;