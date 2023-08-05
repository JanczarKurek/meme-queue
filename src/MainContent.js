import React from 'react';

class MainContent extends React.Component {

  constructor(props) {
      super(props);
      this.state = {
        imgUrl: "raccoon.jpg"
      };
  }

  componentDidUpdate(prevProps) {
    if (prevProps.event === this.props.event)
      return;

    if (this.props.event && this.props.event.type === "meme") {
      this.setState({imgUrl: this.props.event.url})
    }
  }

  render() {
    return (
      <div className="MainContent">
        <img src={this.state.imgUrl} className="App-logo" alt="logo" />
      </div>
    )
  }


}
export default MainContent;