import React from 'react';

import ToiletEntry from './ToiletEntry';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { toiletList: this.getToiletEntries() };
  }

  componentDidMount() {
    this.timer = setInterval(
      () => this.getToiletEntries(),
      1000
    );
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  getToiletEntries() {
    this.setState({
      toiletList: fetch('/load').then((resp) => {
        return resp.json();
      }).then((data) => {
        return data.toilets;
      })
    });
  }

  render() {
    return (<div>
      <h2 id="heading">Porta-Potty Statuses</h2>
      {this.state.toiletList.map((id, status) => (
        <ToiletEntry toiletId={id} status={status} key={id} />
      ))}
    </div>);
  }
}

export default App;