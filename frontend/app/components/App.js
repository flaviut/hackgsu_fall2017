import React from 'react';

import ToiletEntry from './ToiletEntry';

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {toiletList: getToiletEntries()};
  }

  render() {
    return (<div>
      <h2 id="heading">Porta-Potty Statuses</h2>
      {this.state.toiletList.map((id, status) => (
        <ToiletEntry toiletId={id} status={status} key={id} />
      ))}
    </div>);
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
      toiletList: fetch('/load').then(function(resp) {
        return resp.json()
      }).then(function(data) {
        return data.toilets;
      })
    });
  }
};
