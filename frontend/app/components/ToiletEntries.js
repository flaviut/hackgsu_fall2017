import React from 'react';
import PropTypes from 'prop-types';


const ToiletEntries = (props) => {
  return (
    <Table>
      <thead>
        <tr>
          <th>Toilet #</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {props.toiletEntries}
      </tbody>
    </Table>
  );
};

ToiletEntries.propTypes = {
    toiletEntries: PropTypes.arrayOf(PropTypes.node).isRequired,
};

export default ToiletEntries;
