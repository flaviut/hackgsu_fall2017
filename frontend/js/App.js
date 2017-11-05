import React from 'react';
import ToiletEntry from './ToiletEntry';
import ToiletEntries from './ToiletEntries';

import '../sass/main.scss';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { toiletList: null };
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
      fetch('http://54.211.92.19:5000/load').then((resp) => {
        return resp.json();
      }).then((json) => {
        let toiletList = [];
        Object.entries(json).forEach((entry) => {
          const k = entry[0];
          const v = entry[1];
          toiletList[k - 1] = v;
        });
        this.setState({toiletList: toiletList});
      });
  }

  toiletIsClean(toiletData) {
    let abortedShits = 0;
    let previousValue = null;

    toiletData.forEach((val) => {
      if(previousValue == null) {
        previousValue = val;
        return;
      }

      if(previousValue[3] === 'close' && val[3] === 'close') {
        // two closes in a row with no lock in the middle? there's an issue.
        abortedShits += 1;
      }
      previousValue = val;
    });

    return abortedShits > 3 ? 'dirty' : 'clean';
  }

  render() {
    let entries = null;
    if (this.state.toiletList != null) {
      entries = this.state.toiletList.map((value, id) => (
        <ToiletEntry toiletId={id+1}
                     status={this.toiletIsClean(value)}
                     key={id} />));
    }

    return (<div>
      <h2 id="heading">Porta-Potty Statuses</h2>
      <ToiletEntries>
        {entries}
      </ToiletEntries>
    </div>);
  }
}

export default App;
