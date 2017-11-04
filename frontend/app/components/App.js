import React from 'react';

import ToiletEntry from './ToiletEntry';

const App = () => {
  return (<div>
    <h2 id="heading">Hello ReactJS</h2>
    <ToiletEntry toiletId={1} status="clean" />
    <ToiletEntry toiletId={2} status="dirty" />
    <ToiletEntry toiletId={3} status="clean" />
    <ToiletEntry toiletId={4} status="clean" />
  </div>);
};

export default App;
