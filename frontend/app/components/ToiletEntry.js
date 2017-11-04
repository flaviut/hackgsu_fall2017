import React from 'react';
import PropTypes from 'prop-types';


const ToiletEntry = (props) => {
  return (
    <tr style={{ backgroundColor: props.status === 'clean' ? '#568203' : '#DC143C' }}>
      <tc>{props.toiletId}</tc><tc>{props.status}</tc>
    </tr>);
};

ToiletEntry.propTypes = {
  toiletId: PropTypes.number.isRequired,
  status: PropTypes.oneOf(['clean', 'dirty']).isRequired,
};

export default ToiletEntry;
