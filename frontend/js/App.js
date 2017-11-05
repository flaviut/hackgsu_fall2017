import React from 'react';
import ToiletEntry from './ToiletEntry';

import '../sass/main.scss';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { toiletList: this.getToiletEntries() };
  }

  componentDidMount() {
    this.timer = setInterval(
      () => this.getToiletEntries(),
      1000,
    );
  }

  componentWillUnmount() {
    clearInterval(this.timer);
  }

  getToiletEntries() {
      fetch('/load').then((resp) => {
        this.setState({toiletList: resp.json().toilets});
      });
  }

  render() {
    return (<div>
      <h2 id="heading">Porta-Potty Statuses</h2>
      <tr>
        <th>Toilet #</th>
        <th>Status</th>
      </tr>
      {this.state.toiletList ? this.state.toiletList.map((id, status) => (
        <ToiletEntry toiletId={id} status={status} key={id} />
      )) : null}
    </div>);
  }
}

export default App;
