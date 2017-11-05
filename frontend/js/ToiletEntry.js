import React from 'react';
import PropTypes from 'prop-types';


const ToiletEntry = (props) => {
  return (
    <tr>
      <td>Toilet {props.toiletId}</td><td>{props.status == "clean" ? "Clean" : <b>Needs Attention</b>}</td>
    </tr>);
};

ToiletEntry.propTypes = {
  toiletId: PropTypes.number.isRequired,
  status: PropTypes.oneOf(['clean', 'dirty']).isRequired,
};

export default ToiletEntry;
