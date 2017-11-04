import React from 'react';
import PropTypes from 'prop-types';


const ToiletEntry = (props) => {
  return (
    <Table>
      <thead>
        <tr>
          <th>#</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {props.toiletEntries}
      </tbody>
    </Table>
  );
};

ToiletEntry.propTypes = {
    toiletEntries: PropTypes.arrayOf(PropTypes.node).isRequired,
};

export default ToiletEntry;
