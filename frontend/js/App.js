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
        this.setState({toiletList: json.toilets});
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

      if(previousValue.action === 'close' && val.action === 'close') {
        // two closes in a row with no lock in the middle? there's an issue.
        abortedShits += 1;
      }
      previousValue = val;
    });

    return abortedShits > 3 ? 'dirty' : 'clean';
  }

  render() {
    return (<div>
      <h2 id="heading">Porta-Potty Statuses</h2>
      <ToiletEntries>
        {this.state.toiletList ?
          this.state.toiletList.map((value, id) => (
            <ToiletEntry toiletId={value.toiletId}
                         status={this.toiletIsClean(value)}
                         key={id} />)) :
          null}
      </ToiletEntries>
    </div>);
  }
}

export default App;
